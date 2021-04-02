from application.Models.models import Post
from application.API.utils import uploadPostImage
from application import db
class PostBL:
    def add_post(self, title, description, image, user):
        post = Post()
        post.post_title = title
        post.post_description = description
        post.post_category = 0
        post.user_id = user.user_id
        post.is_admin_post = 1 if user.is_admin == 1 else 0

        if not image is None:
            isSaved, imageName = uploadPostImage(image, user)
            if isSaved:
                post.post_image = imageName

        try:
            db.session.add(post)
            db.session.commit()
            return True, post
        except Exception as e:
            return False, None