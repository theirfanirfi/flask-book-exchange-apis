from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class BooksAPI(FlaskView, BusinessLogic):

    def index(self):
        response = dict({"isLoggedIn": True})
        books = BF.getBL("book").get_by_column(
            modelName="book",
            columnName="is_available_for_exchange",
            columnValue=1,
            isMany=True,
            isDump=True)
        return jsonify(books)

    def post(self):
        isCreated, json_res = super().create(request=request, modelName="book", involve_login_user=True)
        return json_res

    def delete(self, id):
        print(id)
        isDeleted, json_res = super().delete_row(request=request,
                                                 modelName="book",
                                                 columnName="book_id",
                                                 columnValue=id,
                                                 verify_user=False)
        print(json_res)
        return json_res
