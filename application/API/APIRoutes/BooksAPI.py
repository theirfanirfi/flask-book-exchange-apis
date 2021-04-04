from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class BooksAPI(FlaskView, BusinessLogic):

    def index(self):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return False, jsonify(notLoggedIn)

        query = "SELECT * FROM book WHERE book.is_available_for_exchange = 1 AND book.user_id != "+str(user.user_id)
        isFetched, books = super().get_by_custom_query("book", query, isMany=True,isDump=True)
        response.update({"isFetched": isFetched, "books":books})
        return jsonify(response)

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
