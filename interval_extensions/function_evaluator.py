import sympy


class FunctionEvaluator:
    """Evaluates a function using sympy"""

    def __init__(self, expr: str, variable_names, operations: dict):
        """
        Init function evaluator

        Parameters
        ----------
        expr:
            A string with a math function
        variable_names:
            A list of variable names
        operations:
            A dictionary of operations that is passed to sympy.lambdify(modules=)
        """

        self.function = sympy.lambdify(list(variable_names), expr, modules=operations)

    def evaluate(self, variables: dict):
        return self.function(*list(variables.values()))
