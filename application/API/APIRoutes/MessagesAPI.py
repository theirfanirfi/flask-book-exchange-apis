from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
from datetime import datetime

class MessagesAPI(FlaskView):

    def index(self):
        response = dict({"isLoggedIn": True})

        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        return 200, 'ok'
        # isFound, participants = BF.getBL("participants").get_my_chat_participants(user)
        # response.update({"isFound": isFound,"participants": participants})
        #
        # return jsonify(response)

    def get(self, id):
        print(id)
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        participants = BF.getBL("participants").get_participant_by_id(id, user.user_id)
        if not participants:
            return jsonify(invalidArgsResponse)

        isFound, messages = BF.getBL("message").get_chat_messages(participants, user)
        return jsonify({"isFound": isFound, "messages": messages})

    @route('/send/<string:participant_id>/', methods=["POST"])
    def send(self, participant_id):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        participants = BF.getBL("participants").get_participant_by_id(participant_id, user.user_id)
        if not participants:
            return jsonify(invalidArgsResponse)

        receiver_id = participants.user_two_id if not participants.user_two_id == user.user_id else participants.user_one_id

        form = dict()
        form['message_text'] = b64_to_data(request.form['text'])
        form['receiver_id'] = receiver_id
        form['sender_id'] = user.user_id
        form['is_message'] = 1
        form['p_id'] = participants.p_id
        form['created_at'] = str(datetime.now())[:19]
        form['updated_at'] = str(datetime.now())[:19]
        request.form = form

        isSent, json_res = BF.getBL("message").create(request, "messages", involve_login_user=False, isDump=True)
        return json_res