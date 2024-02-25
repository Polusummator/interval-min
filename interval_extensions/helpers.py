def calculate_centred_form(variables: dict, centre: dict, gradient: dict, extension):
    result = extension.evaluate(centre)
    for variable, interval in variables.items():
        result += gradient[variable] * (variables[variable] - centre[variable])
    return result
