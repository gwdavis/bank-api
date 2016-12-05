from flask import jsonify


def get_data(request):
    """Get data from request either from form-data or json body"""

    # NOTE:  Not sure this works for a form as request is not a FLASK
    # function

    data = request.form
    if not data:
        data = request.get_json()
    return data


def error(message, status=200):
    """Wrap an error message in a response JSON"""
    data = {"status": "error", "reason": message}
    return jsonify(data), status


def check_required_params(params, data):
    """Check if `data` contains list of mandatory parameters `params`"""
    for param in params:
        result = check_required_param(param, data)
        if result:
            return result


def check_required_param(param, data):
    """Check if `data` contains mandatory parameter `param`"""
    if not data:
        return error("Missing mandatory parameter {}".format(param))
    try:
        data[param]
    except KeyError:
        return error("Missing mandatory parameter {}".format(param))
    return None


def numeric_amount(param, data):
    """Validate that param in data is a representation of a positive
    decimal number"""
    try:
        numeric_amount = float(data[param])
    except ValueError:
        return (None, error("Invalid {} specified: {}. Must be a decimal number\
                            , e.g. 123.45.".format(param, data[param]), 400))
    if numeric_amount < 0:
        return (None, error("{} must be a positive decimal \
                            number.".format(param, data[param]), 400))
    return (numeric_amount, None)



