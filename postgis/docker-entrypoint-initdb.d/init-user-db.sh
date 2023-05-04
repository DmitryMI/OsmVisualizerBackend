#!/bin/bash
set -e

POSTGRES_USER=postgres
POSTGRES_DB=postgres

export PGPASSWORD='postgres'; psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER renderaccount WITH PASSWORD 'renderaccount';
	CREATE USER root WITH PASSWORD 'root';
	CREATE DATABASE gis;
	GRANT ALL PRIVILEGES ON DATABASE gis TO renderaccount;
EOSQL

export PGPASSWORD='postgres'; psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "gis" <<-EOSQL
    CREATE EXTENSION postgis;
	CREATE EXTENSION hstore;
	ALTER TABLE geometry_columns OWNER TO renderaccount;
	ALTER TABLE spatial_ref_sys OWNER TO renderaccount;
	ALTER SYSTEM SET jit=off;
	SELECT pg_reload_conf();
EOSQL
