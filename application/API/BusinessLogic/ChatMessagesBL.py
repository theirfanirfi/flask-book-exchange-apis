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

    def get_chat_messages(self, participants, user):

        query = "SELECT chat_messages.*,exchange.exchange_message, " \
                "exchange.is_exchange_declined, exchange.is_exchange_confirmed, " \
                "exchange.to_exchange_with_user_id, " \
                "chat_messages.message_id as _id, chat_messages.message_text as text, " \
                "chat_messages.created_at as createdAt, " \
                "JSON_OBJECT('_id', sender.user_id, 'name', sender.fullname, " \
                "'avatar', sender.profile_image ) as user, " \
                "JSON_OBJECT('book_id', book_to_be_sent.book_id, 'book_title'," \
                " book_to_be_sent.book_title, 'book_author', book_to_be_sent.book_author, " \
                "'book_cover_image', book_to_be_sent.book_cover_image) as book_to_be_sent, " \
                "JSON_OBJECT('book_id', book_to_be_received.book_id, 'book_title', " \
                "book_to_be_received.book_title, 'book_author', book_to_be_received.book_author, " \
                "'book_cover_image', book_to_be_received.book_cover_image) as book_to_be_received, " \
                "JSON_OBJECT('_id', sender.user_id, 'name', sender.fullname, 'avatar', " \
                "sender.profile_image ) as sender, " \
                "JSON_OBJECT('_id', receiver.user_id, 'name', receiver.fullname, 'avatar', " \
                "receiver.profile_image ) as receiver, " \
                "IF(sender.user_id = '"+str(user.user_id)+"', true, false) as amISender " \
                "FROM chat_messages " \
                "LEFT JOIN users as sender on sender.user_id = chat_messages.sender_id " \
                "LEFT JOIN users as receiver on receiver.user_id = chat_messages.receiver_id " \
                "LEFT JOIN exchange on exchange.exchange_id = chat_messages.exchange_id " \
                "LEFT JOIN book as book_to_be_sent on book_to_be_sent.book_id = exchange.book_to_be_sent_id " \
                "LEFT JOIN book as book_to_be_received on book_to_be_received.book_id = exchange.book_to_be_received_id " \
                "WHERE p_id = '"+str(participants.p_id)+"' ORDER BY chat_messages.message_id DESC"

        return super().get_by_custom_query(schemaName="message", query=query, isMany=True, isDump=True)


