from application.Models.models import *
from application.API.BusinessLogic.PostBL import PostBL
from application.API.BusinessLogic.ListBL import ListBL
class BF:
    @staticmethod
    def getBL(blName):
        if blName == "post":
            return PostBL()
        elif blName == "user":
            return User()
        elif blName == "list":
            return ListBL()





