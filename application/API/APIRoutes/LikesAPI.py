from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class LikesAPI(FlaskView):

    def index(self):
        response = dict({"isLoggedIn": True})
        return jsonify(response)
        # books = BF.getBL("book").get_by_column(
        #     modelName="book",
        #     columnName="is_available_for_exchange",
        #     columnValue=1,
        #     isMany=True,
        #     isDump=True)
        # return jsonify(books)

    def post(self):
        isCreated, json_res = BF.getBL("like").create(request, involve_login_user=True)
        return json_res

    def delete(self, id):
        print(id)
        isDeleted, json_res = BF.getBL("like").delete_row(request, id)
        print(json_res)
        return json_res

