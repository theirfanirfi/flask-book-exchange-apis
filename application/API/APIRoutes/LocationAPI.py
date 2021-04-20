from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF


class LocationAPI(FlaskView):

    def index(self):
        response = dict({"isLoggedIn": True})
        return jsonify(response)

    def put(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        isUpdated, json_res = BF.getBL("location").update(request, columnName="user_id",
                                                          columnValue=user.user_id)
        print(isUpdated)
        print(json_res)
        return json_res


