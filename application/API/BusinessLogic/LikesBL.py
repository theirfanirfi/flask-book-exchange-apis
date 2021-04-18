from application.Models.models import Stack
from application.API.utils import uploadPostImage
from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class LikesBL(BusinessLogic):

    def create(self, request, involve_login_user=True):
        return super().create(request, "like", involve_login_user, post_insertion=[self.like_notification])

    def delete_row(self, request, id):
        return super().delete_row(request, "like", "post_id", id, True)

    def like_notification(self, request, model, user):
        isFound, post = super().get_by_column("post", "post_id", model.post_id, isMany=False, isDump=False)
        if not isFound:
            return False

        if user.user_id == post.user_id:
            return True

        print(post)
        request.form = dict()
        request.form['post_id'] = model.post_id
        request.form['user_id'] = model.user_id
        request.form['to_be_notified_user_id'] = post.user_id
        request.form['is_like'] = 1
        isCreated, json_res = super().create(request, "notification", True)
        return isCreated

    def delete_like_notification(self, req, model_data):
        isDeleted, json_res = super().delete_row(request=req,
                                                 modelName="notification",
                                                 columnName="exchange_id",
                                                 columnValue=model_data.exchange_id,
                                                 verify_user=True)
        return isDeleted
