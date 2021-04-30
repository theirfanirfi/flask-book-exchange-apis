from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
import base64

class AuthAPI(FlaskView):

    def index(self):
        return 'index'
        # return jsonify(response)

    @route('/login', methods=['POST'])
    def login(self):
        response = dict({"isLoggedIn": True})
        form = request.form
        token = b64_to_data(form['token'])
        user_id = b64_to_data(form['user_id'])
        name = b64_to_data(form['fullname'])
        username = b64_to_data(form['username'])
        profile_image = None
        if 'profile_image' in form:
            profile_image = b64_to_data(form['profile_image'])

        if not (token or user_id or name or username):
            return jsonify(invalidArgsResponse)

        check_user = BF.getBL("user").check_user_for_sm_login(user_id, token)

        if check_user:
            response.update({"user": {"user_id": check_user.user_id,
                             "fullname": check_user.fullname,
                             "profile_image": check_user.profile_image,
                            "token": str(check_user.token)}
            })
            return jsonify(response)

        user = BF.getBL("user").create_sm_login(user_id,
                                                name,
                                                token,
                                                profile_image)
        if user:
            response.update({"user": {"user_id": user.user_id,
                             "fullname": user.fullname,
                             "profile_image": user.profile_image,
                             "token": str(user.token)}})
            return jsonify(response)


        return jsonify({"isLoggedIn": False,"message":"Invalid detaisl provided"})


