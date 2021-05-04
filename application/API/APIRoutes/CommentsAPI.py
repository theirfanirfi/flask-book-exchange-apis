from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
from application.API.Factory.SchemaFactory import SF
from sqlalchemy import text
from application import db

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
        if isCreated:
            sql = text("SELECT comments.*,users.fullname, users.profile_image FROM comments "
                       "LEFT JOIN users on users.user_id = comments.user_id "
                       "WHERE comment_id = '"+str(json_res['comment'].comment_id)+"'")
            comment = db.engine.execute(sql)
            if comment.rowcount > 0:
                print('found ')
                return jsonify({"isLoggedIn": True, "isCreated": True,
                                "comment": SF.getSchema("comment", isMany=True).dump(comment)})
            else:
                return jsonify({"isLoggedIn": True, "isCreated": False, "comment": comment})
        else:
            return json_res

    def delete(self, id):
        print(id)
        isDeleted, json_res = BF.getBL("comment").delete_row(request, id)
        print(json_res)
        return json_res
