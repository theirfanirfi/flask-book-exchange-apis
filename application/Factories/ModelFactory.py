from application.Models.models import Post, Categories

class ModeFactory:
    @staticmethod
    def getModel(model):
        if model == "post":
            return Post()
        elif model == "category":
            return Categories()