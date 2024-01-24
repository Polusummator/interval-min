from functools import reduce


class VariableNode:
    def __init__(self, variable_name):
        self.variable_name = variable_name

    def evaluate(self, variables: dict):
        return variables[self.variable_name]


class ConstNode:
    def __init__(self, constant):
        self.constant = constant

    def evaluate(self, variables: dict):
        return self.constant


class UnaryNode:
    def __init__(self, func, argument):
        self.func = func
        self.argument = argument

    def evaluate(self, variables: dict):
        return self.func(self.argument.evaluate(variables))


class BinaryNode:
    def __init__(self, func, arguments):
        self.func = func
        self.arguments = arguments

    def evaluate(self, variables: dict):
        arguments = [argument.evaluate(variables) for argument in self.arguments]
        return reduce(self.func, arguments)
