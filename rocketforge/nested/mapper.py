import json
from rocketforge.utils.logger import logger

VARIABLES_PATH = "rocketforge/nested/variables.json"
with open(VARIABLES_PATH, "r") as f:
    var_dict = json.load(f)

class VarMapper:
    def __init__(self, var_dict):
        self._name_to_symbol = {}
        self._symbol_to_name = {}
        self._symbol_to_unit = {}

        for var_type, variables in var_dict.items():
            self._name_to_symbol[var_type] = {}
            for name, info in variables.items():
                sym = info["symbol"]
                uom = info["unit"]

                self._name_to_symbol[var_type][name] = sym
                self._symbol_to_name[sym] = name
                self._symbol_to_unit[sym] = uom

    def get_symbol(self, name):
        for pair in self._name_to_symbol.values():
            if name in pair:
                return pair[name]
        logger.warning(f"Name '{name}' not found in mapping.")
        return None

    def get_name(self, symbol):
        if symbol in self._symbol_to_name:
            return self._symbol_to_name[symbol]
        logger.warning(f"Symbol '{symbol}' not found in mapping.")
        return None

    def get_uom(self, symbol):
        if symbol in self._symbol_to_unit:
            return self._symbol_to_unit[symbol]
        logger.warning(f"Symbol '{symbol}' not found in mapping.")
        return None

    def get_all_names(self, type):
        return list(self._name_to_symbol.get(type, {}).keys())

mapper = VarMapper(var_dict)