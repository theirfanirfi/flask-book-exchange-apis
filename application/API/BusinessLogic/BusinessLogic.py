from abc import ABC
from application.API.Factory.ModelFactory import MF
from application.API.Factory.SchemaFactory import SF
from application import db
from application.API.utils import AuthorizeRequest, notLoggedIn, invalidArgsResponse, b64_to_data
from flask import jsonify
from sqlalchemy import text


class BusinessLogic(ABC):
    def create(self, request, modelName, involve_login_user=False, isDump=True, isBase64Decode=False):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return False, jsonify(notLoggedIn)

        model = MF.getModel(modelName)
        model = model[0]
        form = request.form
        for field in form:
            if form[field] == "":
                return False, jsonify(invalidArgsResponse)
            else:
                if not hasattr(model, field):
                    return False, jsonify(invalidArgsResponse)

                setattr(model, field, b64_to_data(form[field]) if isBase64Decode else form[field])

        if involve_login_user:
            model.user_id = user.user_id

        try:
            db.session.add(model)
            db.session.commit()
            response.update({"isCreated": True,
                             modelName.lower(): SF.getSchema(modelName, isMany=False).dump(model) if isDump else model,
                             "message": modelName + " created"})
            return True, jsonify(response)
        except Exception as e:
            print(e)
            response.update({"isCreated": False, modelName: False, "message": "Error occurred, please try again"})
            return False, jsonify(response)

    def get_by_column(self, modelName, columnName, columnValue, isMany=False, isDump=False):
        model = MF.getModel(modelName)
        model = model[1]
        data = model.query.filter(getattr(model, columnName) == columnValue)
        if not data.count() > 0:
            return False, 0

        data = data.all() if isMany else data.first()
        return True, SF.getSchema(modelName, isMany).dump(data) if isDump else data

    def get_by_custom_query(self, schemaName, query, isMany=False, isDump=False):
        try:
            sql = text(query)
            result = db.engine.execute(sql)
            return True, SF.getSchema(schemaName, isMany).dump(result) if isDump else result
        except Exception as e:
            print(e)
            return False, 0

    def delete_row(self, request, modelName, columnName, columnValue, verify_user=True):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return False, jsonify(notLoggedIn)

        model = MF.getModel(modelName)
        print('columnName='+str(columnName))
        attribute = getattr(model[1], columnName)
        print(attribute)
        data = None

        if verify_user:
            data = model[1].query.filter(getattr(model[1], columnName) == columnValue, model[1].user_id == user.user_id)
        else:
            data = model[1].query.filter(getattr(model[1], columnName) == columnValue)

        if not data.count() > 0:
            return False, modelName + " not found to delete"

        data = data.first()
        try:
            db.session.delete(data)
            db.session.commit()
            response.update({"isDeleted": True, "message": modelName + " deleted"})
            return True, jsonify(response)
        except Exception as e:
            response.update(
                {"isDeleted": False,
                 "message": "Error occurred in deleting the " + modelName + ". Please try again"
                 })
            return True, jsonify(response)
