from application.Models.models import Stack
from application.API.utils import uploadPostImage
from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic
from application.API.utils import AuthorizeRequest, notLoggedIn
from flask import jsonify


class CommentBL(BusinessLogic):

    def get_comments(self,user, id):
        query = "SELECT comments.*, users.fullname, users.profile_image FROM comments LEFT JOIN users on users.user_id = comments.user_id WHERE comments.post_id = "+str(id)
        return super().get_by_custom_query("comment", query, isMany=True, isDump=True)

    def create(self, request, involve_login_user=True):
        return super().create(request, "comment", involve_login_user, isBase64Decode=True)

    def delete_row(self, request, id):
        return super().delete_row(request, "comment", "comment_id", id, True)
