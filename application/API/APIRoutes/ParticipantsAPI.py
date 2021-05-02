from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic
from application.API.Factory.SchemaFactory import SF


class ParticipantsAPI(FlaskView):

    def index(self):
        response = dict({"isLoggedIn": True})

        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        isFound, participants = BF.getBL("participants").get_my_chat_participants(user)
        response.update({"isFound": isFound,"participants": participants})

        return jsonify(response)


    @route('/initiate_chat/<string:exchange_id>/', methods=["POST"])
    def initiate_chat(self, exchange_id):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        exchange = BF.getBL("exchange").get_exchange(exchange_id, False)

        if not exchange:
            return jsonify(invalidArgsResponse)

        # the participants of the chat are received.
        participants = BF.getBL("participants").get_participant(exchange.to_exchange_with_user_id, user.user_id)
        # now, the exchange request message will be created in the chat
        print('user user_id: '+user.user_id)
        print('exchange user_id: '+exchange.to_exchange_with_user_id)

        form = dict()
        form['exchange_id'] = exchange.exchange_id
        form['is_exchange'] = 1
        form['receiver_id'] = exchange.to_exchange_with_user_id
        form['sender_id'] = user.user_id
        form['p_id'] = participants.p_id
        request.form = form
        isCreated, json_res = BF.getBL("messages").create_exchange_message(request)
        if isCreated:
            response.update(
                {"isCreated": True,
                 "participants": SF.getSchema("participants",isMany=False).dump(participants)
                 })
            return jsonify(response)
        return jsonify({"isCreated": False, "message": "Error occurred, please try again "})

    def chat(self, id):
        ##id = user_id come from profile page
        response = dict({"isLoggedIn": True})

        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        participants = BF.getBL("participants").get_participant(id, user.user_id)
        response.update({"participant": SF.getSchema("participants",isMany=False).dump(participants),
                         "isFound": True})
        return jsonify(response)

    # def delete(self, id):
    #     print(id)
    #     isDeleted, json_res = BF.getBL("stack").delete_row(request, id)
    #     print(json_res)
    #     return json_res
