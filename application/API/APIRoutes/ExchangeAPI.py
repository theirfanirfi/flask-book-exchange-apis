from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class ExchangeAPI(FlaskView, BusinessLogic):

    def index(self):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return False, jsonify(notLoggedIn)

        query = "SELECT book.*, " \
                " 111.111 * DEGREES(ACOS(LEAST(1.0, COS(RADIANS("+user.location_latitude+")) * COS(RADIANS(users.location_latitude))"\
         " * COS(RADIANS("+user.location_longitude+" - users.location_longitude)) + SIN(RADIANS("+user.location_latitude+")) * SIN(RADIANS(users.location_latitude))))) AS distance_in_km, " \
                "users.fullname, users.profile_image, users.location_longitude, users.location_latitude" \
                " FROM book LEFT JOIN users on users.user_id = book.user_id WHERE book.is_available_for_exchange = 1"
                #"AND book.user_id != "+str(user.user_id)
        isFetched, books = super().get_by_custom_query("book", query, isMany=True,isDump=True)
        response.update({"isFetched": isFetched, "books":books})
        return jsonify(response)

    def post(self):
        isCreated, json_res = super().create(request=request, modelName="exchange", involve_login_user=True)
        return json_res

    def delete(self, id):
        print(id)
        isDeleted, json_res = super().delete_row(request=request,
                                                 modelName="exchange",
                                                 columnName="exchange_id",
                                                 columnValue=id,
                                                 verify_user=True)
        print(json_res)
        return json_res
