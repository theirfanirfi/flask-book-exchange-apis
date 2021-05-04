from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.Factory.ModelFactory import MF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic
from application.API.utils import AuthorizeRequest, notLoggedIn
from flask import jsonify


class NotificationsBL(BusinessLogic):

    def get_notifications(self, user):

        query = "SELECT notifications.*,users.fullname, users.profile_image, " \
                "IF(exchange.to_exchange_with_user_id='"+user.user_id+"', true, false) as is_exchanged_with_me," \
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
                "WHERE to_be_notified_user_id ='" + str(user.user_id)+"'"

        return super().get_by_custom_query("notification", query, isMany=True, isDump=True)

    def create(self, request, involve_login_user=True):
        return super().create(request, "comment", involve_login_user, isBase64Decode=True,
                              post_insertion=[self.comment_notification])

    def delete_row(self, request, id):
        return super().delete_row(request, "comment", "comment_id", id, True)

    def exchange_confirmed_notifications(self, exchange):
        print('exchange confirmed '+exchange.exchange_id)

        model = MF.getModel("notification")
        notification = model[1].query.filter_by(exchange_id=exchange.exchange_id)
        if not notification.count() > 0:
            return False
        notification = notification.first()
        notification.is_exchange_confirmed = 1
        notification.is_exchange_declined = 0
        self.save_notification(notification)

        n = model[0]
        n.is_exchange_notification = 1
        n.is_exchange_confirmed = 1
        n.is_exchange_declined = 0
        n.exchange_id = notification.exchange_id
        n.to_exchange_with_user_id = notification.user_id
        return self.save_notification(n)

    def exchange_declined_notifications(self, exchange):
        print('exchange declined')
        model = MF.getModel("notification")
        notification = model[1].query.filter_by(exchange_id=exchange.exchange_id)
        if not notification.count() > 0:
            return False
        notification = notification.first()
        notification.is_exchange_confirmed = 0
        notification.is_exchange_declined = 1
        self.save_notification(notification)

        n = model[0]
        n.is_exchange_notification = 1
        n.is_exchange_confirmed = 0
        n.is_exchange_declined = 1
        n.exchange_id = notification.exchange_id
        n.to_exchange_with_user_id = notification.user_id
        return self.save_notification(n)

    def exchange_withdrawn_notifications(self, exchange):
        model = MF.getModel("notification")[1]
        notification = model.query.filter_by(exchange_id=exchange.exchange_id)
        if not notification.count() > 0:
            return False
        notification = notification.first()
        notification.is_exchange_confirmed = 0
        notification.is_exchange_declined = 0
        return self.save_notification(notification)

    def save_notification(self, notification):
        try:
            db.session.add(notification)
            db.session.commit()
            return True, "Notification confirmed"
        except Exception as e:
            print(e)
            return False, "Error occurred. Please try again"
