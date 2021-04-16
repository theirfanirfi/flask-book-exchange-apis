from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.Factory.ModelFactory import MF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic
from flask import jsonify
from sqlalchemy import and_, or_


class ChatMessagesBL(BusinessLogic):
    def create_exchange_message(self, request):
        checkExchangeMessage = MF.getModel("message")[1].query.filter_by(exchange_id=request.form['exchange_id'])
        if checkExchangeMessage.count() > 0:
            message = checkExchangeMessage.first()
            return True, jsonify({"isCreated": True, "messages": SF.getSchema("message", isMany=False).dump(message)})
        return super().create(request=request, modelName="message",involve_login_user=False,isDump=True)


