from application.Models.models import Post, Categories, CustomPushNotification

class ModeFactory:
    @staticmethod
    def getModel(model):
        if model == "post":
            return Post()
        elif model == "category":
            return Categories()
        elif model == "push_notifications":
            return CustomPushNotification()
