from application import db
from application.Models.models import CustomPushNotification
from application.utils import save_file, delete_image
class CustomPushNotificationBL:
    def add_notification(self, form, user):
        notification = CustomPushNotification()
        notification.notification_message = form.notification_message.data
        try:
            db.session.add(notification)
            db.session.commit()
            return True, 'Notification Sent.'
        except Exception as e:
            return False, str(e)

    def get_notifications(self):
        notifications = CustomPushNotification.query.all()
        return notifications

    def get_pushh_notifications(self):
        notifications = CustomPushNotification.query.all()
        return notifications

    def get_notification(self, notification_id):
        notification = CustomPushNotification.query.filter_by(notification_id=notification_id)
        if notification.count() > 0:
            return notification.first()
        return False


    def delete_notification(self, id):
        notification = CustomPushNotification.query.filter_by(notification_id=id)
        if not notification.count() > 0:
            return False, 'No such notification found', 'error'

        notification = notification.first()
        try:
            db.session.delete(notification)
            db.session.commit()
            return True, 'Notification deleted', 'success'
        except Exception as e:
            return False, str(e), 'error'
