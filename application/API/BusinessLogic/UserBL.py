from application.API.Factory.ModelFactory import MF
from application.API.Factory.SchemaFactory import SF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic
from application import bcrypt, db
from sqlalchemy import text


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

    def search_users(self, search_term):
        model = MF.getModel("user")[0]
        sql = "SELECT user_id, fullname, profile_image FROM users WHERE fullname LIKE '%"+str(search_term)+"%'"
        users = db.engine.execute(text(sql))
        return SF.getSchema("user", isMany=True).dump(users)


    def count_followers(self, user):
        model = MF.getModel("follower")[0]
        follow = model.query.filter_by(followed_user_id=user.user_id)
        return follow.count()

    def count_followed(self, user):
        model = MF.getModel("follower")[0]
        follow = model.query.filter_by(follower_user_id=user.user_id)
        return follow.count()

    def check_user_for_sm_login(self, userId, token):
        model = MF.getModel("user")[0]
        user = model.query.filter_by(email=userId)
        if not user.count() > 0:
            return False
        user = user.first()
        if bcrypt.check_password_hash(user.password, token):
            return user
        return False

    def create_sm_login(self, userId, fullname, token, profile_image):
        model = MF.getModel("user")[0]
        model.fullname = fullname
        if not profile_image is None:
            model.profile_image = profile_image

        model.email = userId
        model.password = bcrypt.generate_password_hash(token)
        model.token = bcrypt.generate_password_hash(token)
        model.location_latitude = 0
        model.location_longitude = 0

        try:
            db.session.add(model)
            db.session.commit()
            return model
        except Exception as e:
            print(e)
            return False
