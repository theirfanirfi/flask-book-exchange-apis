from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class BuyBookAPI(FlaskView, BusinessLogic):

    def post(self):
        isCreated, json_res = super().create(request=request, modelName="buy", involve_login_user=True,
                                             post_insertion=[self.buy_notification,
                                                             self.create_buy_request_in_chat])
        return json_res

    def delete(self, id):
        isDeleted, json_res = super().delete_row(request=request,
                                                 modelName="buy",
                                                 columnName="buy_id",
                                                 columnValue=id,
                                                 verify_user=True,
                                                 post_deletion=[self.delete_buy_request_notification,
                                                                self.delete_exchange_request_chat])
        return json_res

    def delete_buy_request_notification(self, req, model_data):
        isDeleted, json_res = super().delete_row(request=req,
                                                 modelName="notification",
                                                 columnName="buy_id",
                                                 columnValue=model_data.buy_id,
                                                 verify_user=True,
                                                 )
        return isDeleted
    #
    def delete_exchange_request_chat(self, req, model_data):
        isDeleted, json_res = super().delete_row(request=req,
                                                 modelName="message",
                                                 columnName="buy_id",
                                                 columnValue=model_data.buy_id,
                                                 verify_user=False,
                                                 )
        return isDeleted

    def buy_notification(self, request, model, user):
        # if user.user_id == model.user_id:
        #     return True
        print('buy id: ',model.buy_id)
        print(model)
        request.form = dict()
        request.form['buy_id'] = model.buy_id
        # @involve_login_user is set to True, so it will do the job.
        # request.form['user_id'] = model.to_exchange_with_user_id
        request.form['to_be_notified_user_id'] = model.book_holder_id
        request.form['is_for_sale'] = 1
        isCreated, json_res = super().create(request, modelName="notification", involve_login_user=True)
        return isCreated

    def create_buy_request_in_chat(self, request, model, user):
        return BF.getBL("participants").initiate_chat_for_buying_request(request, model.buy_id, user)

    @route("/approve_request/<string:buy_id>/")
    def approve_request(self, buy_id):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return False, jsonify(notLoggedIn)

        buy = BF.getBL("buy").verify_buy_request(buy_id, user)
        if not buy:
            return jsonify(invalidArgsResponse)

        buy.is_accepted = 1
        buy.is_rejected = 0
        ##from here to continue
        isConfirmed, message = BF.getBL("buy").save_buy_request(buy, isConfirmed=True)
        response.update({"isConfirmed": isConfirmed, "message": message})
        return jsonify(response)
    #
    # @route("/withdraw_exchange/<string:exchange_id>/")
    # def withdraw_approval(self, exchange_id):
    #     response = dict({"isLoggedIn": True})
    #     user = AuthorizeRequest(request.headers)
    #     if not user:
    #         return False, jsonify(notLoggedIn)
    #
    #     exchange = BF.getBL("exchange").verify_exchange_request(exchange_id, user)
    #     if not exchange:
    #         return jsonify(invalidArgsResponse)
    #
    #     exchange.is_exchange_confirmed = 0
    #     exchange.is_exchange_declined = 0
    #     isConfirmed, message = BF.getBL("exchange").save_exchange(exchange, isWithDrawn=True)
    #     response.update({"isConfirmed": isConfirmed, "message": message})
    #     return jsonify(response)
    #
    @route("/decline_request/<string:buy_id>/")
    def decline_exchange(self, buy_id):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return False, jsonify(notLoggedIn)

        buy = BF.getBL("buy").verify_buy_request(buy_id, user)
        if not buy:
            return jsonify(invalidArgsResponse)

        buy.is_accepted = 0
        buy.is_rejected = 1
        isDeclined, message = BF.getBL("buy").save_buy_request(buy, isConfirmed=True)
        response.update({"isDeclined": isDeclined, "message": message})
        return jsonify(response)
