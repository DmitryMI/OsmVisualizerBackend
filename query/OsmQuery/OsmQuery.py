#!/usr/bin/python3

import argparse
from email.policy import default
import requests
import os.path
from PString import PString

CSV_SEPARATOR = ","

def get_configs(config_dir):
    configs = []
    for (dirpath, dirnames, filenames) in os.walk(config_dir):
        for filename in filenames:
            if ".query" not in filename:
                continue
            config_name = os.path.splitext(os.path.basename(filename))[0]
            configs.append(config_name)
        break

    return configs

def get_tags_all(config_dir):
    tags = {}
    for (dirpath, dirnames, filenames) in os.walk(config_dir):
        for filename in filenames:
            if ".csv" not in filename:
                continue
            
            fpath = os.path.join(config_dir, filename)

            load_tags_from_file(fpath, tags)

    return tags

def get_tags_by_config(config_dir, config_name):
    tags = {}
    for (dirpath, dirnames, filenames) in os.walk(config_dir):
        for filename in filenames:
            if ".csv" not in filename:
                continue
            if not filename.startswith(config_name):
                continue
            
            fpath = os.path.join(config_dir, filename)

            load_tags_from_file(fpath, tags)

    return tags

def load_tags_from_file(fpath, tags: dict):
    with open(fpath, "r") as f:
        tags_csv = f.readlines()

    header = None
    for i, config_line in enumerate(tags_csv):
        words = config_line.split(CSV_SEPARATOR)
        if i == 0:
            header = words
            continue

        tag_value = words[0]
        condition_values = {}

        for i, word in enumerate(words):
            if i == 0:
                continue
            condition_name = header[i].rstrip()
            condition_value = word.rstrip()
            condition_values[condition_name] = condition_value
    
        if header[0] not in tags:
            tags[header[0]] = {tag_value : condition_values}
        else:
            tags[header[0]][tag_value] = condition_values


def get_queries(config_dir, config_name, zoom, out_format, timeout):
    config_path = os.path.join(config_dir, config_name + ".txt")
    with open(config_path, "r") as f:
        query_template = f.read()

    queries = []

    config_types_path = os.path.join(config_dir, config_name + "_types.csv")
    if os.path.exists(config_types_path):
        with open(config_types_path, "r") as f:
            config_types_csv = f.readlines()

        key = None
        for i, config_line in enumerate(config_types_csv):
            words = config_line.split(CSV_SEPARATOR)
            if i == 0:
                key = words[0]
                continue
            
            value = words[0]
            value_zoom = int(words[1])

            if value_zoom > zoom:
                continue

            query = query_template.format(timeout=timeout, out_format=out_format, **{key: value})
            query_name = f"{config_name}.{key}={value}"
            queries.append((query_name, query))
    else:
        query = query_template.format(timeout=timeout, out_format=out_format)
        queries.append((config_name, query))

    return queries

def get_all_combinations(key_values_in):
    if len(key_values_in.keys()) == 0:
        return []

    key_values = {}
    for key, values in key_values_in.items():
        if values:
            key_values[key] = values

    combinations = []
    combinations_num = 1
    index_counters = []
    for key, values in key_values.items():
        combinations_num *= len(values)
        index_counters.append(0)

    for combination_index in range(combinations_num):
        combination = {}
        for i, (key, values) in enumerate(key_values.items()):
            value_index = index_counters[i]
            combination[key] = values[value_index]
        combinations.append(combination)

        index_counters[0] += 1
        for i in range(len(index_counters)):
            if index_counters[i] >= len(list(key_values.items())[i][1]):
                index_counters[i] = 0
                if i == len(index_counters) - 1:
                    break
                index_counters[i + 1] += 1

    return combinations
    

def get_queries_from_tags(config_dir, config_name, const_params: dict, tags, conditional_params, do_write_const_param_names):
    query_path = os.path.join(config_dir, config_name + ".query")

    with open(query_path, "r") as fin:
        query_template = fin.read()

    pstr = PString(query_template)
    variables = list(pstr.variables.keys())
    possible_values = {}
    for var in variables:
        possible_values[var] = []

    for key, value in const_params.items():
        possible_values[key] = [value]

    for tag, tag_values in tags.items():
        if tag not in possible_values.keys():
            continue

        for tag_value, tag_value_conditions in tag_values.items():
            conditions_met = True
            for condition_name, condition_value in tag_value_conditions.items():
                if condition_name not in conditional_params.keys():
                    continue
                condition_evaluator = conditional_params[condition_name]
                if not condition_evaluator(condition_value):
                    conditions_met = False
                    break
            if conditions_met:
                possible_values[tag].append(tag_value)

    # combs = itertools.combinations()
    queries = []
    var_combinations = get_all_combinations(possible_values)
    for var_combination in var_combinations:
        pstr.variables = var_combination
        query_name = f"{config_name}-"
        name_parts = []
        for var, value in var_combination.items():
            if var in const_params and not do_write_const_param_names:
                continue
            name_parts.append(f"{var}={value}")
        query_name += ",".join(name_parts)

        queries.append((query_name, str(pstr)))

    return queries


def execute_query(endpoint, query, output_dir, output_ext):
    query_name = query[0]
    print(f"Executing {query_name}...")

    fname = os.path.join(output_dir, f"{query_name}.{output_ext}")
    if os.path.exists(fname):
        print(f"\tFile {fname} already exists, skipping.")
        return True

    query_text = query[1]
    resp = requests.post(endpoint, query_text)
    if resp.status_code != 200:
        error_msg = resp.content
        print(f"\tRequest failed for query {query_name}: {error_msg}")
        return False

    print(f"\tReturned code: {resp.status_code}")
    fname = os.path.join(output_dir, f"{query_name}.{output_ext}")
    with open(fname, "wb") as fout:
        fout.write(resp.content)
    print(f"\tResult of {query_name} saved to {fname}")
    return True
         

def execute_queries(endpoint, queries, output_dir, output_ext, stop_on_error):
    if not queries:
        return
    for q in queries:
        ok = execute_query(endpoint, q, output_dir, output_ext)
        if not ok and stop_on_error:
            print("Stop on error enabled. Stopping.")
            return

def main():
    parser = argparse.ArgumentParser(
        prog="OsmQuery",
        description="Queries OSM globally restricted by zoom level",
        epilog="By Dmitriy",
    )

    parser.add_argument("config_dir")
    parser.add_argument("-o", "--output_dir", required=False, default="./")
    parser.add_argument("-z", "--zoom", required=False, default=5)
    parser.add_argument("--endpoint", required=False, default="https://lz4.overpass-api.de/api/interpreter")
    parser.add_argument("--timeout", required=False, default=3600, type=int)
    parser.add_argument("--maxsize", required=False, default=2000000000, type=int)
    parser.add_argument("--format", required=False, default="json")
    parser.add_argument("--write_const_param_names", required=False, default=False)
    parser.add_argument("-e", "--stop_on_error", required=False, default=False)

    args = parser.parse_args()
    config_dir = args.config_dir
    output_dir = args.output_dir
    zoom = args.zoom
    endpoint = args.endpoint
    timeout = args.timeout
    out_format = args.format
    maxsize = args.maxsize
    stop_on_error = args.stop_on_error
    do_write_const_param_names = args.write_const_param_names

    os.makedirs(output_dir, exist_ok=True)

    config_names = get_configs(config_dir)

    const_params = {"out_format": out_format, "timeout": timeout, "maxsize": maxsize}

    for config_name in config_names:
        tags = get_tags_by_config(config_dir, config_name)
        query_texts = get_queries_from_tags(config_dir, config_name, const_params, tags, {"zoom" : lambda x: int(x) <= zoom}, do_write_const_param_names)
        execute_queries(endpoint, query_texts, output_dir, out_format, stop_on_error)
    
    print("Finished")
    
if __name__ == "__main__":
    code = main()
    exit(code)