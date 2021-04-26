from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
from application.Models.models import Follower
from application import db
from sqlalchemy import or_, and_

class FollowAPI(FlaskView):

    def index(self):
        response = dict({"isLoggedIn": True})
        return jsonify(response)

    #follow user
    def get(self, id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        follower = Follower.query.filter(or_(and_(Follower.follower_user_id==id, Follower.followed_user_id==user.user_id),
                                                and_(Follower.followed_user_id==id, Follower.follower_user_id==user.user_id)))
        if follower.count() > 0:
            return jsonify({"isLoggedIn": True, "isFollowed": False, "message": "You have already followed the user"})

        follower = Follower()
        follower.follower_user_id = user.user_id
        follower.followed_user_id = id
        try:
            db.session.add(follower)
            db.session.commit()
            return jsonify({"isLoggedIn": True, "isFollowed": True, "message": "Followed"})
        except Exception as e:
            print(e)
            return jsonify({"isLoggedIn": True, "isFollowed": False, "message": "Error occurred, please try again"})

    def unfollow(self, id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        follower = Follower.query.filter(or_(and_(Follower.follower_user_id==id, Follower.followed_user_id==user.user_id),
                                                and_(Follower.followed_user_id==id, Follower.follower_user_id==user.user_id)))
        if not follower.count() > 0:
            return jsonify({"isLoggedIn": True, "isUnFollowed": False, "message": "You have not followed each other"})

        follower = follower.first()
        try:
            db.session.delete(follower)
            db.session.commit()
            return jsonify({"isLoggedIn": True, "isUnFollowed": True, "message": "Unfollowed"})
        except Exception as e:
            print(e)
            return jsonify({"isLoggedIn": True, "isUnFollowed": False, "message": "Error occurred, please try again"})


    def post(self):
        pass

    def delete(self, id):
        print(id)
        isDeleted, json_res = BF.getBL("stack").delete_row(request, id)
        print(json_res)
        return json_res
