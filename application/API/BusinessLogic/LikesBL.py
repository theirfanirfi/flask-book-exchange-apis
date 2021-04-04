from application.Models.models import Stack
from application.API.utils import uploadPostImage
from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class LikesBL(BusinessLogic):

   def create(self, request, involve_login_user=True):
       return super().create(request, "like", involve_login_user)

   def delete_row(self, request, id):
       return super().delete_row(request, "like","post_id", id, True)