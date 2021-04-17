from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class ExchangeAPI(FlaskView, BusinessLogic):

    def index(self):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return False, jsonify(notLoggedIn)

        query = "SELECT book.*, " \
                " 111.111 * DEGREES(ACOS(LEAST(1.0, COS(RADIANS(" + user.location_latitude + ")) * COS(RADIANS(users.location_latitude))" \
                                                                                             " * COS(RADIANS(" + user.location_longitude + " - users.location_longitude)) + SIN(RADIANS(" + user.location_latitude + ")) * SIN(RADIANS(users.location_latitude))))) AS distance_in_km, " \
                                                                                                                                                                                                                     "users.fullname, users.profile_image, users.location_longitude, users.location_latitude" \
                                                                                                                                                                                                                     " FROM book LEFT JOIN users on users.user_id = book.user_id WHERE book.is_available_for_exchange = 1"
        # "AND book.user_id != "+str(user.user_id)
        isFetched, books = super().get_by_custom_query("book", query, isMany=True, isDump=True)
        response.update({"isFetched": isFetched, "books": books})
        return jsonify(response)

    def post(self):
        isCreated, json_res = super().create(request=request, modelName="exchange", involve_login_user=True,
                                             post_insertion=self.exchange_notification)
        return json_res

    def delete(self, id):
        isDeleted, json_res = super().delete_row(request=request,
                                                 modelName="exchange",
                                                 columnName="exchange_id",
                                                 columnValue=id,
                                                 verify_user=True,
                                                 post_deletion=self.delete_exchange_notification)
        return json_res

    def delete_exchange_notification(self, req, model_data):
        isDeleted, json_res = super().delete_row(request=req,
                                                 modelName="notification",
                                                 columnName="exchange_id",
                                                 columnValue=model_data.exchange_id,
                                                 verify_user=True)
        return isDeleted

    def exchange_notification(self, request, model, user):
        # if user.user_id == model.user_id:
        #     return True

        request.form = dict()
        request.form['exchange_id'] = model.exchange_id
        request.form['book_to_be_provided_id'] = model.book_to_be_sent_id
        request.form['book_requested_id'] = model.book_to_be_received_id
        # @involve_login_user is set to True, so it will do the job.
        # request.form['user_id'] = model.to_exchange_with_user_id
        request.form['to_be_notified_user_id'] = model.to_exchange_with_user_id
        request.form['is_exchange'] = 1
        isCreated, json_res = super().create(request, modelName="notification", involve_login_user=True)
        return isCreated

    @route("/approve_exchange/<string:exchange_id>/")
    def approve_exchange(self, exchange_id):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return False, jsonify(notLoggedIn)

        exchange = BF.getBL("exchange").verify_exchange_request(exchange_id, user)
        if not exchange:
            return jsonify(invalidArgsResponse)

        exchange.is_exchange_confirmed = 1
        exchange.is_exchange_declined = 0
        isConfirmed, message = BF.getBL("exchange").save_exchange(exchange, isConfirmed=True)
        response.update({"isConfirmed": isConfirmed, "message": message})
        return jsonify(response)

    @route("/withdraw_exchange/<string:exchange_id>/")
    def withdraw_approval(self, exchange_id):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return False, jsonify(notLoggedIn)

        exchange = BF.getBL("exchange").verify_exchange_request(exchange_id, user)
        if not exchange:
            return jsonify(invalidArgsResponse)

        exchange.is_exchange_confirmed = 0
        exchange.is_exchange_declined = 0
        isConfirmed, message = BF.getBL("exchange").save_exchange(exchange, isWithDrawn=True)
        response.update({"isConfirmed": isConfirmed, "message": message})
        return jsonify(response)

    @route("/decline_exchange/<string:exchange_id>/")
    def decline_exchange(self, exchange_id):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return False, jsonify(notLoggedIn)

        exchange = BF.getBL("exchange").verify_exchange_request(exchange_id, user)
        if not exchange:
            return jsonify(invalidArgsResponse)

        exchange.is_exchange_confirmed = 0
        exchange.is_exchange_declined = 1
        isDeclined, message = BF.getBL("exchange").save_exchange(exchange)
        response.update({"isDeclined": isDeclined, "message": message})
        return jsonify(response)
