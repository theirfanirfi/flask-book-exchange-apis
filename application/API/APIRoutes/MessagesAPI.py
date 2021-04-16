from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic
from application.API.Factory.SchemaFactory import SF


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
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        participants = BF.getBL("participants").get_participant_by_id(id, user.user_id)
        if not participants:
            return jsonify(invalidArgsResponse)

        isFound, messages = BF.getBL("message").get_chat_messages(participants, user)
        return jsonify({"isFound": isFound, "messages": messages})


    # def delete(self, id):
    #     print(id)
    #     isDeleted, json_res = BF.getBL("stack").delete_row(request, id)
    #     print(json_res)
    #     return json_res
