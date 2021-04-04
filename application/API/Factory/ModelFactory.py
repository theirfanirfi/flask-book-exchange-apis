from application.Models.models import *

class MF:
    @staticmethod
    def getModel(modelName):
        modelName = modelName.lower()
        if modelName == "post":
            return Post()
        elif modelName == "user":
            return User()
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