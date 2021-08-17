from application.Models.models import *


class MF:
    @staticmethod
    def getModel(modelName):
        modelName = modelName.lower()
        if modelName == "post":
            return Post(), Post
        elif modelName == "user" or modelName == "users":
            return User(), User
        elif modelName == "list":
            return List()
        elif modelName == "book":
            return Book(), Book
        elif modelName == "stack":
            return Stack(), Stack
        elif modelName == "like":
            return Like(), Like
        elif modelName == "comment":
            return Comment(), Comment
        elif modelName == "exchange":
            return Exchange(), Exchange
        elif modelName == "notification":
            return Notification(), Notification
        elif modelName == "participants" or modelName == "participant":
            return ChatParticipant(), ChatParticipant
        elif modelName == "message" or modelName == "messages":
            return ChatMessage(), ChatMessage
        elif modelName == "follower" or modelName == "followers":
            return Follower(), Follower
        elif modelName == "buy":
            return buy_book(), buy_book
