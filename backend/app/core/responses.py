from flask import jsonify


def success_response(data, status=200, message=None):
    body = {}
    if isinstance(data, list):
        body['data'] = data
    else:
        body['data'] = data
    if message:
        body['message'] = message
    return jsonify(body), status


def error_response(message, status=400):
    return jsonify({'error': message}), status
