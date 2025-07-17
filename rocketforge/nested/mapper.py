import json
from rocketforge.utils.logger import logger

VARIABLES_PATH = "rocketforge/nested/variables.json"
with open(VARIABLES_PATH, "r") as f:
    variables = json.load(f)
    
class VarMapper:
    def __init__(self, name_to_symbol):
        self._name_to_symbol = name_to_symbol
        self._symbol_to_name = {}
        # Reverse mapping
        for type, pair in self._name_to_symbol.items():
            for name, symbol in pair.items():
                self._symbol_to_name[symbol] = name
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
    
    def get_all_names(self, type):
        return list(self._name_to_symbol.get(type, {}).keys())            

mapper = VarMapper(variables)