from application.Models.models import Stack
from application.API.utils import uploadPostImage
from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class StacksBL(BusinessLogic):

   def create(self, request, involve_login_user=True):
       return super().create(request, "stack", involve_login_user)

   def delete_row(self, request, id):
       return super().delete_row(request, "stack","stack_id", id, True)