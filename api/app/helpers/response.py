from flask import jsonify

def response_json(body, status=200):
    return (jsonify(body), status)


def json_date(value):
    return value.strftime("%Y-%m-%d %H:%M:%S")
