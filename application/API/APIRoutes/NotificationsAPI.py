from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class NotificationsAPI(FlaskView):
    def index(self):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        is_found, notifications = BF.getBL("notification").get_notifications(user)
        push_notifications = BF.getBL("push_notifications").get_notifications()
        user_push_notifications = list()

        response.update({"notifications": notifications})

        if len(push_notifications) > 0:
            for push_notification in push_notifications:
                p_notification = BF.getBL("notification").is_notification_read(push_notification.notification_id, user.user_id)
                if p_notification:
                    user_push_notifications.append(push_notification)
            response.update({"isPushNotificationsFound": True if len(user_push_notifications) > 0 else False, "push_notifications": user_push_notifications})
        else:
            response.update({"isPushNotificationsFound": False,
                             "push_notifications": user_push_notifications})

        return jsonify(response)

    @route('/get_notifications/')
    def get_push_notifications(self):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        is_found, notifications = BF.getBL("notification").get_push_notifications(user)
        user_push_notifications = list()

        response.update({"isFound": is_found, "notifications": notifications,"isPushNotificationsFound": False,
                             "push_notifications": user_push_notifications})

        push_notifications = BF.getBL("push_notifications").get_pushh_notifications()

        if len(push_notifications) > 0:
            for push_notification in push_notifications:
                p_notification = BF.getBL("notification").is_notification_read(push_notification.notification_id,
                                                                               user.user_id)
                if p_notification:
                    user_push_notifications.append(push_notification)
            response.update({"isPushNotificationsFound": True if len(user_push_notifications) > 0 else False,
                             "push_notifications": user_push_notifications})
        else:
            response.update({"isPushNotificationsFound": False,
                             "push_notifications": user_push_notifications})

        return jsonify(response)
