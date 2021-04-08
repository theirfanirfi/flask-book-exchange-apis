from application.Models.models import Post
from application.API.utils import uploadPostImage
from application import db
from sqlalchemy import text
from application.API.Factory.SchemaFactory import SF
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
            print(e)
            return False, None

    def get_posts(self, user):
        sql = text("SELECT post.*, users.fullname, "
                   " (SELECT COUNT(*) FROM likes WHERE likes.post_id = post.post_id AND likes.user_id = "+str(user.user_id)+") as isLiked, "
                   +" (SELECT COUNT(*) FROM likes WHERE likes.post_id = post.post_id) as likes_count, "
                   "(SELECT COUNT(*) FROM comments WHERE comments.post_id = post.post_id) as comments_count "
                   "FROM post LEFT JOIN users on users.user_id = post.user_id ORDER BY post.post_id DESC")
        posts = db.engine.execute(sql)
        return SF.getSchema("post", isMany=True).dump(posts)

    def search_posts(self, user, search):
        sql = text("SELECT post.*, users.fullname, "
                   " (SELECT COUNT(*) FROM likes WHERE likes.post_id = post.post_id AND likes.user_id = "+str(user.user_id)+") as isLiked, "
                   +" (SELECT COUNT(*) FROM likes WHERE likes.post_id = post.post_id) as likes_count, "
                   "(SELECT COUNT(*) FROM comments WHERE comments.post_id = post.post_id) as comments_count "
                   "FROM post LEFT JOIN users on users.user_id = post.user_id WHERE post_title Like '%"+str(search)+"%'")
        posts = db.engine.execute(sql)
        return SF.getSchema("post", isMany=True).dump(posts)