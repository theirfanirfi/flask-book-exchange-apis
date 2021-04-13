from application.Models.models import Stack
from application.API.utils import uploadPostImage
from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic
from application.API.utils import AuthorizeRequest, notLoggedIn
from flask import jsonify


class CommentBL(BusinessLogic):

    def get_comments(self, user, id):
        query = "SELECT comments.*, users.fullname, users.profile_image FROM comments LEFT JOIN users on users.user_id = comments.user_id WHERE comments.post_id = " + str(
            id)
        return super().get_by_custom_query("comment", query, isMany=True, isDump=True)

    def create(self, request, involve_login_user=True):
        return super().create(request, "comment", involve_login_user, isBase64Decode=True,
                              post_insertion=self.comment_notification)

    def delete_row(self, request, id):
        return super().delete_row(request, "comment", "comment_id", id, True)

    def comment_notification(self, request, model, user):
        isFound, post = super().get_by_column("post", "post_id", model.post_id, isMany=False, isDump=False)
        if not isFound:
            return False

        if user.user_id == post.user_id:
            return True

        request.form = dict()
        request.form['post_id'] = model.post_id
        request.form['user_id'] = model.user_id
        request.form['to_be_notified_user_id'] = post.user_id
        request.form['is_comment'] = 1
        isCreated, json_res = super().create(request, "notification", True)
        return isCreated
