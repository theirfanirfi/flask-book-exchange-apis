from application.Models.models import *
from application.API.BusinessLogic.PostBL import PostBL
from application.API.BusinessLogic.ListBL import ListBL
from application.API.BusinessLogic.BooksBL import BooksBL
from application.API.BusinessLogic.LikesBL import LikesBL
from application.API.BusinessLogic.CommentBL import CommentBL
from application.API.BusinessLogic.ExchangeBL import ExchangeBL
from application.API.BusinessLogic.StacksBL import StacksBL
from application.API.BusinessLogic.NotificationsBL import NotificationsBL
from application.API.BusinessLogic.ParticipantBL import ParticipantBL
from application.API.BusinessLogic.ChatMessagesBL import ChatMessagesBL
from application.API.BusinessLogic.LocationBL import LocationBL
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
        elif blName == "participants" or blName == "participant":
            return ParticipantBL()
        elif blName == "message" or blName == "messages":
            return ChatMessagesBL()
        elif blName == "location":
            return LocationBL()





