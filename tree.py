from functools import reduce


class VariableNode:
    def __init__(self, variable_name):
        self.variable_name = variable_name

    def calculate(self, variables: dict):
        return variables[self.variable_name]


class ConstNode:
    def __init__(self, constant):
        self.constant = constant

    def calculate(self, variables: dict):
        return self.constant


class UnaryNode:
    def __init__(self, func, argument):
        self.func = func
        self.argument = argument

    def calculate(self, variables: dict):
        return self.func(self.argument.calculate(variables))


class BinaryNode:
    def __init__(self, func, arguments):
        self.func = func
        self.arguments = arguments

    def calculate(self, variables: dict):
        arguments = [argument.calculate(variables) for argument in self.arguments]
        return reduce(self.func, arguments)
