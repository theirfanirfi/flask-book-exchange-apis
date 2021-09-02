from application.BusinessLogic.cpanel.PostBl import PostBL
from application.BusinessLogic.cpanel.CategoriesBL import CategoriesBL
from application.BusinessLogic.cpanel.CustomPushNotificationBl import CustomPushNotificationBL

class BF:
    @staticmethod
    def getBL(bl):
        if bl == "post":
            return PostBL()
        elif bl == "category":
            return CategoriesBL()
        elif bl == "push_notifications":
            return CustomPushNotificationBL()
