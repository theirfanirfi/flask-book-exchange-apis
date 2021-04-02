from application.Models.models import *

class MF:
    @staticmethod
    def getModel(modelName):
        if modelName == "post":
            return Post()
        elif modelName == "user":
            return User()
        elif modelName == "list":
            return List()