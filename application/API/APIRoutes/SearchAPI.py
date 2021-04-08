from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class SearchAPI(FlaskView, BusinessLogic):

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

    def get(self, type, search):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        if type == "posts":
            posts = BF.getBL("post").search_posts(user, search)
            response.update({"posts": posts})
            return jsonify(response)
        elif type == "users":
            users = super().search_model(modelName="users", searchColumn="fullname", searchValue=search)
            response.update({"users": users})
            return jsonify(response)
        elif type == "books":
            #query = "SELECT * FROM book WHERE ((book_title Like '%"+search+"%' OR book_author LIKE '%"+search+"%') OR book_isbn = '"+str(search)+"') AND is_available_for_exchange = 1"

            query = "SELECT book.*, " \
                    " 111.111 * DEGREES(ACOS(LEAST(1.0, COS(RADIANS(" + user.location_latitude + ")) * COS(RADIANS(users.location_latitude))" \
                                                                                                 " * COS(RADIANS(" + user.location_longitude + " - users.location_longitude)) + SIN(RADIANS(" + user.location_latitude + ")) * SIN(RADIANS(users.location_latitude))))) AS distance_in_km, " \
                                                                                                                                                                                                                         "users.fullname, users.profile_image, users.location_longitude, users.location_latitude" \
                                                                                                                                                                                                                         " FROM book LEFT JOIN users on users.user_id = book.user_id WHERE ((book_title Like '%"+search+"%' OR book_author LIKE '%"+search+"%') OR book_isbn = '"+str(search)+"') AND is_available_for_exchange = 1"
            books = super().search_model(modelName="book",query=query, searchColumn="book_title", searchValue=search)
            response.update({"books": books})
            return jsonify(response)
        else:
            return jsonify(invalidArgsResponse)
    #
    # def post(self):
    #     isCreated, json_res = BF.getBL("stack").create(request, involve_login_user=True)
    #     return json_res

    # def delete(self, id):
    #     print(id)
    #     isDeleted, json_res = BF.getBL("stack").delete_row(request, id)
    #     print(json_res)
    #     return json_res
