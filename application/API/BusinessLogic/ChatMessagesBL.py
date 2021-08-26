from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.Factory.ModelFactory import MF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic
from flask import jsonify
from sqlalchemy import and_, or_


class ChatMessagesBL(BusinessLogic):

    def get_unread_messages_count_for_participant(self, participant_id):
        message_model = MF.getModel("message")[1]
        return message_model.query.filter_by(p_id=participant_id, is_read=0).count()

    def get_unread_messages_count_for_user(self, user_id):
        message_model = MF.getModel("message")[1]
        return message_model.query.filter_by(receiver_id=user_id, is_read=0).count()

    def make_messages_read_for_user(self, user_id):
        message_model = MF.getModel("message")[1]
        messages = message_model.query.filter_by(receiver_id=user_id, is_read=0).update({"is_read": 1})
        try:
            # db.session.add(messages)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def create_chat_message(self, sender_id, receiver_id, message, participant_id):
        message_model = MF.getModel("message")[0]
        message_model.sender_id = sender_id
        message_model.receiver_id = receiver_id
        message_model.message_text = message
        message_model.p_id = participant_id
        try:
            db.session.add(message_model)
            db.session.commit()
            return message_model
        except Exception as e:
            print(e)
            return False

    def create_exchange_message(self, request):
        checkExchangeMessage = MF.getModel("message")[1].query.filter_by(exchange_id=request.form['exchange_id'])
        if checkExchangeMessage.count() > 0:
            message = checkExchangeMessage.first()
            return True, jsonify({"isCreated": True, "messages": SF.getSchema("message", isMany=False).dump(message)})
        return super().create(request=request, modelName="message",involve_login_user=False,isDump=True)

    def create_buy_message(self, request):
        checkBuyMessage = MF.getModel("message")[1].query.filter_by(buy_id=request.form['buy_id'])
        if checkBuyMessage.count() > 0:
            message = checkBuyMessage.first()
            return True, jsonify({"isCreated": True, "messages": SF.getSchema("message", isMany=False).dump(message)})
        return super().create(request=request, modelName="message",involve_login_user=False,isDump=True)

    def get_chat_messages(self, participants, user):

        query = "SELECT buy_book.buy_id,buy_book.is_rejected, buy_book.is_accepted, " \
                "chat_messages.*,exchange.exchange_message, " \
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
                "JSON_OBJECT('book_id', bbook.book_id, 'book_title', " \
                "bbook.book_title, 'book_author', bbook.book_author, " \
                "'book_cover_image', bbook.book_cover_image, 'selling_price', bbook.selling_price) as bbook_buy, " \
                "IF(sender.user_id = '"+str(user.user_id)+"', true, false) as amISender " \
                "FROM chat_messages " \
                "LEFT JOIN users as sender on sender.user_id = chat_messages.sender_id " \
                "LEFT JOIN users as receiver on receiver.user_id = chat_messages.receiver_id " \
                "LEFT JOIN exchange on exchange.exchange_id = chat_messages.exchange_id " \
                "LEFT JOIN book as book_to_be_sent on book_to_be_sent.book_id = exchange.book_to_be_sent_id " \
                "LEFT JOIN book as book_to_be_received on book_to_be_received.book_id = exchange.book_to_be_received_id " \
                "LEFT JOIN buy_book on buy_book.buy_id = chat_messages.buy_id " \
                "LEFT JOIN book as bbook on bbook.book_id = buy_book.book_id " \
                "WHERE p_id = '"+str(participants.p_id)+"' ORDER BY chat_messages.message_id DESC"

        return super().get_by_custom_query(schemaName="message", query=query, isMany=True, isDump=True)

    def get_chat_messages_for_team(self, participants, user, isDump=False):

        query = "SELECT *, " \
                "IF(users.user_id = '"+str(user.user_id)+"', 1, 0) as amISender " \
                "FROM chat_messages " \
                "LEFT JOIN users on users.user_id = chat_messages.sender_id " \
                "WHERE p_id = '"+str(participants.p_id)+"' ORDER BY chat_messages.message_id ASC"

        return super().get_by_custom_query(schemaName="message", query=query, isMany=True, isDump=isDump)


