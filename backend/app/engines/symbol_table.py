class SymbolTable:
    def __init__(self):
        self.assignments = {}

    def set(self, var_name: str, value: str):
        self.assignments[var_name] = value

    def get(self, var_name: str):
        return self.assignments.get(var_name)