from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class ProfileAPI(FlaskView):

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
        user_id = id
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        bl = BF.getBL("user")

        # if type(id) == int:
        if str(id) == "me":
            user_id = user.user_id

        print('user_id: '+str(user_id))

        profile = bl.get_user(user_id)
        if not profile:
            return jsonify({"isLoggedIn": True,"isFound": False, "message": "invalid profile"})

        if profile.user_id == user.user_id:
            return jsonify({"isLoggedIn": True,"isFound": True, "isFollowed": False,"profile": {
                "fullname": profile.fullname,
                "profile_image": profile.profile_image,
                "user_id": profile.user_id,
                "followers": bl.count_followers(user),
                "followed": bl.count_followed(user),
            }})
        return jsonify(
            {
                "isLoggedIn": True,
                "isFound": True,
                "isFollowed": BF.getBL("user").check_have_i_followed(user, profile),
                "profile": {
                    "fullname": profile.fullname,
                    "profile_image": profile.profile_image,
                    "user_id": profile.user_id,
                    "followers": bl.count_followers(profile),
                    "followed": bl.count_followed(profile),
                }})


    def post(self):
        isCreated, json_res = BF.getBL("stack").create(request, involve_login_user=True)
        return json_res

    def delete(self, id):
        print(id)
        isDeleted, json_res = BF.getBL("stack").delete_row(request, id)
        print(json_res)
        return json_res
