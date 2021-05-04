from abc import ABC
from application.API.Factory.ModelFactory import MF
from application.API.Factory.SchemaFactory import SF
from application import db
from application.API.utils import AuthorizeRequest, notLoggedIn, invalidArgsResponse, b64_to_data
from flask import jsonify
from sqlalchemy import text
import types


class BusinessLogic(ABC):
    def create(self, request, modelName, involve_login_user=False, isDump=True, isBase64Decode=False,
               post_insertion=None, is_jsonify=True):
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

            if not post_insertion is None:
                for post_func in post_insertion:
                    # if isinstance(post_insertion, types.ClassMethodDescriptorType):
                    isNotified = post_func(request, model, user)
                    # else:
                    #     pass

            response.update({"isCreated": True,
                             modelName.lower(): SF.getSchema(modelName, isMany=False).dump(model) if isDump else model,
                             "message": modelName + " created"})
            return True, jsonify(response) if is_jsonify else response
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

    def delete_row(self, request, modelName, columnName, columnValue, verify_user=True, post_deletion=None):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return False, jsonify(notLoggedIn)

        model = MF.getModel(modelName)
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
            if not post_deletion is None:
                for post_func in post_deletion:
                    isD = post_func(request, data)

            response.update({"isDeleted": True, "message": modelName + " deleted"})
            return True, jsonify(response)
        except Exception as e:
            print(e)
            response.update(
                {"isDeleted": False,
                 "message": "Error occurred in deleting the " + modelName + ". Please try again"
                 })
            return True, jsonify(response)

    def search_model(self, modelName, searchColumn, searchValue, query=None):
        sql = "SELECT * FROM " + modelName + " WHERE " + searchColumn + " Like '%" + str(searchValue) + "%'"
        isFound, result = self.get_by_custom_query(schemaName=modelName, query=sql if query is None else query,
                                                   isMany=True, isDump=True)
        return result

    def update_model(self, request,
                     model_name,
                     column_name=None,
                     column_value=None,
                     model_filters=None,
                     form_filters=None,
                     is_dump=True,
                     is_many=False,
                     verify_user=True,
                     post_updation_filters=None,
                     ):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return False, jsonify(notLoggedIn)

        model = MF.getModel(model_name)
        model_queried = None
        model_obj = None
        form = request.form
        for field in form:
            if form[field] == "":
                return False, jsonify(invalidArgsResponse)

        if not form_filters is None:
            for f_filter in form_filters:
                form = f_filter(form)

        if not column_name is None and not column_value is None:
            if verify_user:
                model_queried = model[1].query.filter(getattr(model[1], column_name) == column_value, getattr(model[1], "user_id") == user.user_id)
            else:
                model_queried = model[1].query.filter(getattr(model[1], column_name) == column_value)
            if not model_queried.count() > 0:
                response.update({"isError": True, "message": "Not found"})
                return False, jsonify(response)

            model_queried = model_queried.first()

        if not model_filters is None:
            for m_filter in model_filters:
                model_queried = m_filter(model, model_queried, form)
        else:
            for field in form:
                if not hasattr(model_queried, field):
                    return False, jsonify(invalidArgsResponse)
                setattr(model_queried, field, form[field])


        try:
            db.session.add(model_queried)
            db.session.commit()
            if not post_updation_filters is None:
                for p_filter in post_updation_filters:
                    p_filter(request, model, user)

            response.update({"isUpdated": True,
                             model_name.lower(): SF.getSchema(model_name, isMany=False).dump(model) if is_dump else model,
                             "message": model_name + " updated"})
            return True, jsonify(response)
        except Exception as e:
            print(e)
            response.update({"isUpdated": False, model_name: False, "message": "Error occurred, please try again"})
            return False, jsonify(response)
