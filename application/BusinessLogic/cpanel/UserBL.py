from application import db, bcrypt
from application.Models.models import User

class UserBL:
    def add_user(self, fullname, form):
        user = User.query.filter_by(email=form.email.data)
        if user.count() > 0:
            return False, 'User already exists'
        user = User()
        user.fullname = fullname
        user.email = form.email.data
        user.password = bcrypt.generate_password_hash(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            return True, 'User added.'
        except Exception as e:
            return False, str(e)

    def get_users(self):
        users = User.query.all()
        return users

    def get_user_by_email(self,email):
        user = User.query.filter_by(email=email)
        if not user.count() > 0:
            return False, 'User not found', 'error'
        user = user.first()
        return True, user, 'success'

    def get_admin_by_email(self,email):
        user = User.query.filter_by(email=email,is_admin=1)
        if not user.count() > 0:
            return False, 'User not found', 'error'
        user = user.first()
        return True, user, 'success'

    def get_user_by_id(self,id):
        user = User.query.filter_by(user_id=id)
        if not user.count() > 0:
            return False, 'User not found', 'error'
        user = user.first()
        return True, user, 'success'

    def verify_user(self, form):
        email = form.email.data
        password = form.password.data
        isFound, user, msg_type = self.get_admin_by_email(email)
        if isFound:
            if(bcrypt.check_password_hash(user.password,password)):
                return True, user, 'success'
            return False, 'Invalid email or password','error'
        return False, 'Invalid email or password', 'error'

    def verify_password(self,user, password):
        if bcrypt.check_password_hash(user.password,password):
            return True
        return False

    def change_password(self, loggedInUser, password):
        isUserFound, user, msg_type = self.get_user_by_id(loggedInUser.user_id)
        if isUserFound:
            user.password = bcrypt.generate_password_hash(password)
            try:
                db.session.add(user)
                db.session.commit()
                return True, 'Password changed', 'success'
            except Exception as e:
                return False, str(e), 'error'
        return False, 'No such user found.', 'error'


    def updateUser(self, user_arg, form):
        isUserFound, userOrMessage, msg_type  = self.get_user_by_id(user_arg.user_id)
        if isUserFound:
            userOrMessage.fullname = form.fullname.data
            userOrMessage.email = form.email.data
            try:
                db.session.add(userOrMessage)
                db.session.commit()
                return True, 'Details updated', 'success'
            except Exception as e:
                return False, str(e), 'error'
        else:
            return False, 'no such user found', 'error'


    def delete_user(self, id):
        user = User.query.filter_by(user_id_id=id)
        if not user.count() > 0:
            return False, 'No such user found', 'error'

        user = user.first()
        try:
            db.session.delete(user)
            db.session.commit()
            return True, 'user deleted', 'success'
        except Exception as e:
            return False, str(e), 'error'