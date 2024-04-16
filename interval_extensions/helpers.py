from mp_exp import Interval


def calculate_centred_form(variables: dict, centre: dict, gradient: dict, extension) -> Interval:
    result = extension.evaluate(centre)
    for variable, interval in variables.items():
        result += gradient[variable] * (variables[variable] - centre[variable])
    return result


def get_centre(variables: dict) -> dict:
    """Get centre of a box"""

    return {variable: interval.mid_interval for variable, interval in variables.items()}
