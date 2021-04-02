from application import db
from application.Models.models import Categories
class CategoriesBL:
	def add_category(self, form):
		cat = Categories.query.filter_by(cat_title=form.cat_title.data)
		if cat.count() > 0:
			return False, 'Category already exists'

		cat = Categories()
		cat.cat_title = form.cat_title.data
		try:
			db.session.add(cat)
			db.session.commit()
			return True, 'Category added.'
		except Exception as e:
			return False, str(e)

	def get_categories(self):
		return Categories.query.all()

	def delete_category(self, id):
		cat = Categories.query.filter_by(cat_id=id)
		if not cat.count() > 0:
			return False, 'No such category found', 'error'
		
		cat = cat.first()
		try:
			db.session.delete(cat)
			db.session.commit()
			return True, 'Category deleted', 'success'
		except Exception as e:
			return False, str(e), 'error'
