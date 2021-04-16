from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class ParticipantsAPI(FlaskView):

    def index(self):
        response = dict({"isLoggedIn": True})
        return jsonify(response)
        # books = BF.getBL("book").get_by_column(
        #     modelName="book",
        #     columnName="is_available_for_exchange",
        #     columnValue=1,
        #     isMany=True,
        #     isDump=True)
        # return jsonify(books)

    def get(self, id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        isFound, books = BF.getBL("stack").get_list_books(id, user)
        return jsonify({"books": books})

    def post(self):
        isCreated, json_res = BF.getBL("stack").create(request, involve_login_user=True)
        return json_res

    @route('/initiate_chat/<string:exchange_id>/', methods=["POST"])
    def initiate_chat(self, exchange_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        exchange = BF.getBL("exchange").get_exchange(exchange_id, False)

        if not exchange:
            return jsonify(invalidArgsResponse)

        # the participants of the chat are received.
        participants = BF.getBL("participants").get_participant(exchange.user_id, user.user_id)
        # now, the exchange request message will be created in the chat

        return 'working'


    def delete(self, id):
        print(id)
        isDeleted, json_res = BF.getBL("stack").delete_row(request, id)
        print(json_res)
        return json_res
