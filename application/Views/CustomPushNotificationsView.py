from flask_classful import FlaskView, route
from flask import render_template, flash, redirect, url_for
from application.Forms.Forms import CustomPushNotificationForm
from flask_login import login_required, current_user
from application.Factories.BF import BF

class CustomPushNotificationsView(FlaskView):
	title = 'Custom Push Notifications'
	exclude_methods=['redirect_with_form']

	def redirect_with_form(self, form):
		user = current_user
		notifications = BF.getBL('push_notifications').get_notifications()
		return render_template("cpanel/custom_push_notification.html",title=self.title, form=form, notifications=notifications)

	@login_required
	def index(self):
		form = CustomPushNotificationForm()
		return self.redirect_with_form(form)

	def get(self, id):
		pass
	def put(self, id):
		pass

	@login_required
	def post(self):
		form = CustomPushNotificationForm()
		user = current_user
		if form.validate_on_submit():
			isSaved, message = BF.getBL('push_notifications').add_notification(form, user)
			if isSaved:
				flash(message, 'success')
			else:
				flash(message, 'error')
			return redirect(url_for("CustomPushNotificationsView:index"))
		else:
			return self.redirect_with_form(form)

	@route("/delete/<string:id>")
	@login_required
	def delete(self, id):
		isDeleted, message, message_type = BF.getBL('push_notifications').delete_notification(id)
		flash(message, message_type)
		return redirect(url_for("CustomPushNotificationsView:index"))
