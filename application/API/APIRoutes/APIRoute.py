from flask_classful import FlaskView
from abc import ABC
from flask import jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn
from application.API.BusinessLogic.BusinessLogic import BusinessLogic
class APIRoute(FlaskView, BusinessLogic):

    def delete_data(self, id, request, model, columnName, verify_user=True):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return False, jsonify(notLoggedIn)

        isDeleted, message = super().delete_row(
            modelName=model,
            columnName=columnName,
            columnValue=id,
            user=user,
            verify_user=verify_user)
        response.update({"isDeleted":isDeleted, "message": message})
        return True, jsonify(response)