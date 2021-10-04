from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.Factory.ModelFactory import MF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic
from application.API.utils import AuthorizeRequest, notLoggedIn
from flask import jsonify

from application.Models import models
from application import socketio

class NotificationsBL(BusinessLogic):

    def get_notifications(self, user):

        query = "SELECT notifications.*,users.fullname, users.profile_image, " \
                "IF(exchange.to_exchange_with_user_id='"+user.user_id+"', true, false) as is_exchanged_with_me, " \
                "IF(buy_book.book_holder_id='"+user.user_id+"', true, false) as am_i_book_holder, " \
                "JSON_OBJECT('book_cover_image', book_to_be_received.book_cover_image," \
                " 'book_title', book_to_be_received.book_title) as book_to_received, " \
                " JSON_OBJECT('book_cover_image', book_to_be_sent.book_cover_image, " \
                "'book_title', book_to_be_sent.book_title) as book_to_send, " \
                "JSON_OBJECT('book_cover_image', bbook.book_cover_image, " \
                "'book_title', bbook.book_title) as buybook " \
                "FROM notifications LEFT JOIN users on users.user_id = notifications.user_id " \
                "LEFT JOIN exchange on exchange.exchange_id = notifications.exchange_id " \
                "LEFT JOIN book as book_to_be_received on " \
                "book_to_be_received.book_id = exchange.`book_to_be_received_id` " \
                "LEFT JOIN book as book_to_be_sent on " \
                "book_to_be_sent.book_id = exchange.`book_to_be_sent_id` " \
                "LEFT JOIN buy_book on buy_book.buy_id = notifications.buy_id " \
                "LEFT JOIN book as bbook on bbook.book_id = buy_book.book_id " \
                "WHERE to_be_notified_user_id ='" + str(user.user_id)+"'"

        return super().get_by_custom_query("notification", query, isMany=True, isDump=True)


    def get_push_notifications(self, user):

        query = "SELECT notifications.*,users.fullname, users.profile_image, " \
                "IF(exchange.to_exchange_with_user_id='"+user.user_id+"', true, false) as is_exchanged_with_me, " \
                "IF(buy_book.book_holder_id='"+user.user_id+"', true, false) as am_i_book_holder, " \
                "JSON_OBJECT('book_cover_image', book_to_be_received.book_cover_image," \
                " 'book_title', book_to_be_received.book_title) as book_to_received, " \
                " JSON_OBJECT('book_cover_image', book_to_be_sent.book_cover_image, " \
                "'book_title', book_to_be_sent.book_title) as book_to_send, " \
                "JSON_OBJECT('book_cover_image', bbook.book_cover_image, " \
                "'book_title', bbook.book_title) as buybook " \
                "FROM notifications LEFT JOIN users on users.user_id = notifications.user_id " \
                "LEFT JOIN exchange on exchange.exchange_id = notifications.exchange_id " \
                "LEFT JOIN book as book_to_be_received on " \
                "book_to_be_received.book_id = exchange.`book_to_be_received_id` " \
                "LEFT JOIN book as book_to_be_sent on " \
                "book_to_be_sent.book_id = exchange.`book_to_be_sent_id` " \
                "LEFT JOIN buy_book on buy_book.buy_id = notifications.buy_id " \
                "LEFT JOIN book as bbook on bbook.book_id = buy_book.book_id " \
                "WHERE to_be_notified_user_id ='" + str(user.user_id)+"' AND is_notification_read = 0"

        update_query = "UPDATE notifications SET notifications.is_notification_read = 1 WHERE to_be_notified_user_id ='" + str(user.user_id)+"'"
        try:
            db.engine.execute(update_query)
            print('updated')
        except Exception as e:
            print(e)

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
        n.user_id = notification.to_be_notified_user_id
        n.to_be_notified_user_id = notification.user_id
        isSaved = self.save_notification(n)
        if isSaved[0]:
            push_notification = dict({
                "is_custom_push_notification": False,
                "notification": SF.getSchema("notification", isMany=False).dump(n),
                "to_be_notified_user_id": notification.to_be_notified_user_id,
            })
            socketio.emit("notification", push_notification)

        return isSaved

    def buy_confirmed_notifications(self, buy):
        print('buy confirmed '+buy.buy_id)

        model = MF.getModel("notification")
        notification = model[1].query.filter_by(buy_id=buy.buy_id)
        if not notification.count() > 0:
            return False
        notification = notification.first()
        notification.is_buy_confirmed = 1
        notification.is_buy_declined = 0
        self.save_notification(notification)

        n = model[0]
        n.is_for_sale = 1
        n.is_buy_confirmed = 1
        n.is_buy_declined = 0
        n.buy_id = notification.buy_id
        n.user_id = notification.to_be_notified_user_id
        n.to_be_notified_user_id = notification.user_id

        isSaved =  self.save_notification(n)
        if isSaved[0]:
            push_notification = dict({
                "is_custom_push_notification": False,
                "notification": SF.getSchema("notification", isMany=False).dump(n),
                "to_be_notified_user_id": notification.to_be_notified_user_id,
            })
            socketio.emit("notification", push_notification)

        return isSaved
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
        n.user_id = notification.to_be_notified_user_id
        n.to_be_notified_user_id = notification.user_id

        isSaved = self.save_notification(n)
        if isSaved[0]:
            push_notification = dict({
                "is_custom_push_notification": False,
                "notification": SF.getSchema("notification", isMany=False).dump(n),
                "to_be_notified_user_id": notification.to_be_notified_user_id,
            })
            socketio.emit("notification", push_notification)

        return isSaved

    def buy_declined_notifications(self, buy):
        model = MF.getModel("notification")
        notification = model[1].query.filter_by(buy=buy.buy_id)
        if not notification.count() > 0:
            return False
        notification = notification.first()
        notification.is_buy_confirmed = 0
        notification.is_buy_declined = 1
        self.save_notification(notification)

        n = model[0]
        n.is_for_sale = 1
        n.is_buy_confirmed = 0
        n.is_buy_declined = 1
        n.buy_id = notification.buy_id
        n.user_id = notification.to_be_notified_user_id
        n.to_be_notified_user_id = notification.user_id

        isSaved = self.save_notification(n)
        if isSaved[0]:
            push_notification = dict({
                "is_custom_push_notification": False,
                "notification": SF.getSchema("notification", isMany=False).dump(n),
                "to_be_notified_user_id": notification.to_be_notified_user_id,
            })
            socketio.emit("notification", push_notification)

        return isSaved

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


    ##read notifications

    def is_notification_read(self, notification_id, user_id):
        model = MF.getModel("read")[1]
        notification = model.query.filter_by(notification_id=notification_id, user_id=user_id)
        if not notification.count() > 0:
            return self.make_custom_notification_read(notification_id, user_id)
        else:
            return False

    def make_custom_notification_read(self,notification_id, user_id):
        model = MF.getModel("read")[0]
        model.notification_id = notification_id
        model.user_id = user_id
        try:
            db.session.add(model)
            db.session.commit()
            return model
        except Exception as e:
            print(e)
            return False
