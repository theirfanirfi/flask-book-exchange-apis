from application.Models.models import *
from application.API.BusinessLogic.PostBL import PostBL
from application.API.BusinessLogic.ListBL import ListBL
from application.API.BusinessLogic.BooksBL import BooksBL
from application.API.BusinessLogic.LikesBL import LikesBL
from application.API.BusinessLogic.CommentBL import CommentBL
from application.API.BusinessLogic.ExchangeBL import ExchangeBL
from application.API.BusinessLogic.StacksBL import StacksBL
from application.API.BusinessLogic.NotificationsBL import NotificationsBL
class BF:
    @staticmethod
    def getBL(blName):
        blName = blName.lower()
        if blName == "post":
            return PostBL()
        elif blName == "user" or blName == "users":
            return User()
        elif blName == "list":
            return ListBL()
        elif blName == "book":
            return BooksBL()
        elif blName == "like":
            return LikesBL()
        elif blName == "comment":
            return CommentBL()
        elif blName == "exchange":
            return ExchangeBL()
        elif blName == "stack":
            return StacksBL()
        elif blName == "notification" or blName == "notifications":
            return NotificationsBL()





