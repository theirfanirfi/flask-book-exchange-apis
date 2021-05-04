from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class CommentsAPI(FlaskView):

    def index(self):
        response = dict({"isLoggedIn": True})
        comments = BF.getBL("comment").get_by_column(
            modelName="comment",columnName="comment_id",
            columnValue=id,isMany=True, isDump=True)
        # books = BF.getBL("book").get_by_column(
        #     modelName="book",
        #     columnName="is_available_for_exchange",
        #     columnValue=1,
        #     isMany=True,
        #     isDump=True)
        # return jsonify(books)

    def get(self, id):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return False, jsonify(notLoggedIn)

        isFetched, comments = BF.getBL("comment").get_comments(user,id)
        print(comments)
        response.update({"isFetched": isFetched, "comments": comments})
        return jsonify(response)

    def post(self):
        isCreated, json_res = BF.getBL("comment").create(request, involve_login_user=True)
        print('comment id: '+json_res.comment_id)
        print('user id: '+json_res.user_id)
        return json_res

    def delete(self, id):
        print(id)
        isDeleted, json_res = BF.getBL("comment").delete_row(request, id)
        print(json_res)
        return json_res
