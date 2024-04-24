import sympy


class FunctionEvaluator:
    def __init__(self, expr: str, variable_names, operations: dict):
        self.variable_names = list(variable_names)  # saved to preserve order of values
        self.function = sympy.lambdify(self.variable_names, expr, modules=operations)

    def evaluate(self, variables: dict):
        """
        Get result of function evaluation.

        Order of variables in the dict is ignored.
        """

        return self.function(*[variables[variable_name] for variable_name in self.variable_names])
