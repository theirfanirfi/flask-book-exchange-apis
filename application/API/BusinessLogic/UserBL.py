from application.Models.models import Stack
from application.API.utils import uploadPostImage
from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.Factory.ModelFactory import MF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class UserBL(BusinessLogic):
    def get_user(self, user_id):
        model = MF.getModel("user")[0]
        user = model.query.filter_by(user_id=user_id)
        if not user.count() > 0:
            return False
        return user.first()

    def get_profile(self, user):
        pass

    def check_have_i_followed(self, me, user):
        model = MF.getModel("follower")[0]
        follow = model.query.filter_by(followed_user_id=user.user_id, follower_user_id=me.user_id)
        if follow.count() > 0:
            return True
        return False

    def count_followers(self, user):
        model = MF.getModel("follower")[0]
        follow = model.query.filter_by(followed_user_id=user.user_id)
        return follow.count()

    def count_followed(self, user):
        model = MF.getModel("follower")[0]
        follow = model.query.filter_by(follower_user_id=user.user_id)
        return follow.count()