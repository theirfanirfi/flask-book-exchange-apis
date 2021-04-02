from flask_classful import FlaskView, route
from flask import render_template, flash, redirect, url_for, request
from application.Forms.Forms import UserForm, LoginForm, ChangePasswordForm
from application.BusinessLogic.cpanel.UserBL import UserBL
from flask_login import login_user, logout_user, login_required, current_user


class UserView(FlaskView):
	title = 'Login'
	exclude_methods=['redirect_with_form']
	ubl = UserBL()

	def redirect_with_form(self, form):
		return render_template("login.html",title=self.title, form=form)

	def index(self):
		form = LoginForm()
		return self.redirect_with_form(form)

	def get(self, id):
		#currently, not implemented
		pass

	@route("/update", methods=['GET', 'POST'])
	@login_required
	def update(self):
		user = current_user
		self.title = user.fullname
		form = UserForm()
		formpass = ChangePasswordForm()
		if request.method == "GET":
			form.fullname.data = user.fullname
			form.email.data = user.email
			return render_template("cpanel/user_update.html",title=self.title,form=form, formpass=formpass)
		elif request.method == "POST":
			if form.validate_on_submit():
				isUpdated, message, msg_type = self.ubl.updateUser(user, form)
				flash(message, msg_type)
				return redirect(url_for("UserView:update"))
			elif formpass.validate_on_submit():
				isOldPasswordCorrect = self.ubl.verify_password(user, formpass.old_password.data)
				if isOldPasswordCorrect:
					isPasswordChanged, message, message_type = self.ubl.change_password(user, formpass.new_password.data)
					flash(message, message_type)
					return redirect(url_for("UserView:update"))
				flash('Invalid current password entered', 'error')
				return redirect(url_for("UserView:update"))
			return render_template("cpanel/user_update.html", title=self.title, form=form, formpass=formpass)
		else:
			return 'invalid request'

	def post(self):
		form = LoginForm()
		if form.validate_on_submit():
			isVerified, userOrException, message_type = self.ubl.verify_user(form)
			if isVerified:
				login_user(userOrException)
				return redirect(url_for("PostsView:index"))
			else:
				flash(userOrException, 'error')
			return redirect(url_for("UserView:index"))
		else:
			return self.redirect_with_form(form)

	@route("/delete/<int:id>")
	def delete(self, id):
		#currently, not implemented.
		pass

	@route("/logout")
	def logout(self):
		logout_user()
		return redirect(url_for("UserView:index"))
		