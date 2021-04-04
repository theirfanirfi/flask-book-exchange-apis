from application.Models.models import *
class SF:
    @staticmethod
    def getSchema(schemaName, isMany=True):
        schemaName = schemaName.lower()
        if schemaName == "post":
            return PostSchema(many=isMany)
        elif schemaName == "user":
            return UserSchema(many=isMany)
        elif schemaName == "list":
            return ListSchema(many=isMany)
        elif schemaName == "book":
            return BookSchema(many=isMany)
        elif schemaName == "stack":
            return StackSchema(many=isMany)
        elif schemaName == "like":
            return LikeSchema(many=isMany)
        elif schemaName == "comment":
            return CommentSchema(many=isMany)