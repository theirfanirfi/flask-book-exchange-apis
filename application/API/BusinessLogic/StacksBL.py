from application.Models.models import Stack
from application.API.utils import uploadPostImage
from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class StacksBL(BusinessLogic):

    def create(self, request, involve_login_user=True):
        return super().create(request, "stack", involve_login_user)

    def delete_row(self, request, id):
        return super().delete_row(request, "stack", "stack_id", id, True)

    def get_list_books(self, list_id, user):
        sql = "SELECT *, 111.111 * DEGREES(ACOS(LEAST(1.0, COS(RADIANS(" + user.location_latitude + ")) * COS(RADIANS(users.location_latitude))" \
                                                                                             " * COS(RADIANS(" + user.location_longitude + " - users.location_longitude)) + SIN(RADIANS(" + user.location_latitude + ")) * SIN(RADIANS(users.location_latitude))))) AS distance_in_km, " \
                                                                                                                                                                                                                     "IF(stacks.user_id='" + str(user.user_id) + "',true,false) as isMine FROM stacks " \
                                                                    "LEFT JOIN users on users.user_id = book.user_id " \
                                                                    "LEFT JOIN book on book.book_id = stacks.book_id WHERE list_id = " + str(
            list_id)
        return super().get_by_custom_query(schemaName="stack", query=sql, isMany=True, isDump=True)
