from application import db
from application.Models.models import Post, Categories
from application.utils import save_file, delete_image
class PostBL:
    def add_post(self, form, user):
        post = Post()
        post.post_title = form.post_title.data
        post.post_description = form.post_description.data
        post.post_category = form.post_category.data
        post.user_id = user.user_id
        post.is_admin_post = 1 if user.is_admin == 1 else 0
        isSaved, file_name = save_file(form.post_image.data, 'posts')
        post.post_image = file_name
        try:
            db.session.add(post)
            db.session.commit()
            return True, 'Post added.'
        except Exception as e:
            return False, str(e)

    def get_posts(self):
        posts = Post.query.all()
        return posts

    def get_admin_posts(self, user):
        posts = Post.query.filter_by(user_id=user.user_id,is_admin_post=1).all()
        return posts

    def get_categories(self):
        cats = Categories.query.all()
        cats = [(str(c.cat_id), str(c.cat_title)) for c in cats]
        return cats


    def delete_post(self, id):
        post = Post.query.filter_by(post_id=id)
        if not post.count() > 0:
            return False, 'No such post found', 'error'

        post = Post.first()
        delete_image(post.post_image, 'posts')
        try:
            db.session.delete(post)
            db.session.commit()
            return True, 'Post deleted', 'success'
        except Exception as e:
            return False, str(e), 'error'