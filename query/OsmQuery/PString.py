VARIABLE_SEQ_OPEN = "{{"
VARIABLE_SEQ_CLOSE = "}}"

class PString():
    def __init__(self, template):
        self._template = template
        self.variables = {}

        self._parse()

    def _parse(self):
        current_index = 0
        var_start = None
        try:
            while True:
                if var_start is None:
                    current_index = self._template.index(VARIABLE_SEQ_OPEN, current_index)
                    var_start = current_index + len(VARIABLE_SEQ_OPEN)
                else:
                    current_index = self._template.index(VARIABLE_SEQ_CLOSE, var_start)
                    var_name = self._template[var_start:current_index]
                    var_start = None
                    self.variables[var_name] = None

        except:
            pass

    def __setitem__(self, key, value):
        self.variables[key] = value

    def __getitem__(self, key):
        return self.variables[key]

    def __delitem__(self, key):
        raise NotImplementedError

    def __str__(self):
        s = self._template
        for var, value in self.variables.items():
            s = s.replace(f"{VARIABLE_SEQ_OPEN}{var}{VARIABLE_SEQ_CLOSE}", str(value))

        return s

