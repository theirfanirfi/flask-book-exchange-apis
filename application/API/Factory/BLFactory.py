from application.Models.models import *
from application.API.BusinessLogic.PostBL import PostBL
from application.API.BusinessLogic.ListBL import ListBL
from application.API.BusinessLogic.BooksBL import BooksBL
class BF:
    @staticmethod
    def getBL(blName):
        blName = blName.lower()
        if blName == "post":
            return PostBL()
        elif blName == "user":
            return User()
        elif blName == "list":
            return ListBL()
        elif blName == "book":
            return BooksBL()





