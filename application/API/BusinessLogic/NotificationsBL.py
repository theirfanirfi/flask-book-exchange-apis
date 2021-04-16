from application.Models.models import Stack
from application.API.utils import uploadPostImage
from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic
from application.API.utils import AuthorizeRequest, notLoggedIn
from flask import jsonify


class NotificationsBL(BusinessLogic):

    def get_notifications(self, user):

        query = "SELECT notifications.*,users.fullname, users.profile_image, " \
                "JSON_OBJECT('book_cover_image', book_to_be_received.book_cover_image," \
                " 'book_title', book_to_be_received.book_title) as book_to_received, " \
                " JSON_OBJECT('book_cover_image', book_to_be_sent.book_cover_image, " \
                "'book_title', book_to_be_sent.book_title) as book_to_send " \
                "FROM notifications LEFT JOIN users on users.user_id = notifications.user_id " \
                "LEFT JOIN exchange on exchange.exchange_id = notifications.exchange_id " \
                "LEFT JOIN book as book_to_be_received on " \
                "book_to_be_received.book_id = exchange.`book_to_be_received_id` " \
                "LEFT JOIN book as book_to_be_sent on " \
                "book_to_be_sent.book_id = exchange.`book_to_be_sent_id`" \
                "WHERE to_be_notified_user_id =" + str(user.user_id)

        return super().get_by_custom_query("notification", query, isMany=True, isDump=True)

    def create(self, request, involve_login_user=True):
        return super().create(request, "comment", involve_login_user, isBase64Decode=True,
                              post_insertion=self.comment_notification)

    def delete_row(self, request, id):
        return super().delete_row(request, "comment", "comment_id", id, True)