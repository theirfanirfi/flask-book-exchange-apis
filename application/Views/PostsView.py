from flask_classful import FlaskView, route
from flask import render_template, flash, redirect, url_for
from application.Forms.Forms import PostForm
from flask_login import login_required, current_user
from application.Factories.BF import BF

class PostsView(FlaskView):
	title = 'Posts'
	exclude_methods=['redirect_with_form']

	def redirect_with_form(self, form):
		user = current_user
		posts = BF.getBL('post').get_admin_posts(user)
		form.post_category.choices = BF.getBL('post').get_categories()
		return render_template("cpanel/post.html",title=self.title, form=form, posts=posts)

	@login_required
	def index(self):
		form = PostForm()
		return self.redirect_with_form(form)

	def get(self, id):
		pass
	def put(self, id):
		pass

	@login_required
	def post(self):
		form = PostForm()
		form.post_category.choices = BF.getBL('post').get_categories()
		user = current_user
		if form.validate_on_submit():
			isSaved, message = BF.getBL('post').add_post(form, user)
			if isSaved:
				flash(message, 'success')
			else:
				flash(message, 'error')
			return redirect(url_for("PostsView:index"))
		else:
			return 'not validated'
			return self.redirect_with_form(form)

	@route("/delete/<int:id>")
	@login_required
	def delete(self, id):
		isDeleted, message, message_type = self.pbl.delete_product(id)
		flash(message, message_type)
		return redirect(url_for("PostsView:index"))
		