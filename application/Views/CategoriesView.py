from flask_classful import FlaskView, route
from flask import render_template, flash, redirect, url_for
from application.Forms.Forms import CategoriesForm
from application.BusinessLogic.cpanel.CategoriesBL import CategoriesBL
from flask_login import login_required

class CategoriesView(FlaskView):
	title = 'Categories'
	exclude_methods=['redirect_with_form']
	cbl = CategoriesBL()

	def redirect_with_form(self, form):
		cats = self.cbl.get_categories()
		return render_template("cpanel/add_category.html",title=self.title, form=form, categories=cats)

	@login_required
	def index(self):
		form = CategoriesForm()
		return self.redirect_with_form(form)
		# return 'wrking'

	def get(self, id):
		pass

	def put(self, id):
		pass

	@login_required
	def post(self):
		form = CategoriesForm()
		if form.validate_on_submit():
			isSaved, message = self.cbl.add_category(form)
			if isSaved:
				flash(message, 'success')
			else:
				flash(message, 'error')

			return redirect(url_for("CategoriesView:index"))
		else:
			return self.redirect_with_form(form)

	@route("/delete/<int:id>")
	@login_required
	def delete(self, id):
		isDeleted, message, message_type = self.cbl.delete_category(id)
		flash(message, message_type)
		return redirect(url_for("CategoriesView:index"))
		