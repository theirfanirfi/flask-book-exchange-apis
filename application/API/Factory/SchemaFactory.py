from application.Models.models import *
class SF:
    @staticmethod
    def getSchema(schemaName, isMany=True):
        if schemaName == "post":
            return PostSchema()
        elif schemaName == "user":
            return UserSchema(many=isMany)
        elif schemaName == "list":
            return ListSchema(many=isMany)