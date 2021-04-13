from flask import jsonify
from application.API.utils import invalidArgsResponse, b64_to_data


def validate_input_fields(form):
    for field in form:
        if form[field] == "":
            return False, jsonify(invalidArgsResponse)
    return form


def validate_attributes(required_attributes_list, form):
    for index in required_attributes_list:
        if not index in form:
            return False, jsonify(invalidArgsResponse)
    return form


def base64_decoder(form):
    for field in form:
        try:
            form[field] = b64_to_data(form[field])
        except Exception as e:
            print(e)
            return False, jsonify(invalidArgsResponse)

def authorize_request():
    pass
