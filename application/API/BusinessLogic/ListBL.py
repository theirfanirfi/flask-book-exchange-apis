from application.Models.models import List
from application.API.utils import uploadPostImage
from application import db
from application.API.Factory.SchemaFactory import SF


class ListBL:
    def getLists(self, user, isDump=False):
        user_lists = List.query.filter_by(user_id=user.user_id).all()
        return user_lists if not isDump else SF.getSchema("list", isMany=True).dump(user_lists)

    def getLists_by_user_id(self, user_id, isDump=False):
        user_lists = List.query.filter_by(user_id=user_id).all()
        return user_lists if not isDump else SF.getSchema("list", isMany=True).dump(user_lists)

    def add_list(self, title, user, isDump=False):
        newList = List()
        newList.list_title = title
        newList.user_id = user.user_id

        try:
            db.session.add(newList)
            db.session.commit()
            return True, newList if not isDump else SF.getSchema("list", False).dump(newList)
        except Exception as e:
            print(e)
            return False, None

    def get_list_by_id(self, list_id, isDump=False):
        listt = List.query.filter_by(list_id=list_id)
        if listt.count() > 0:
            listt = listt.first()
            return listt if not isDump else SF.getSchema("list", False).dump(listt)
        return False

    def get_list_by_id_user(self, list_id, user, isDump=False):
        listt = List.query.filter_by(list_id=list_id, user_id=user.user_id)
        if listt.count() > 0:
            listt = listt.first()
            return listt if not isDump else SF.getSchema("list", False).dump(listt)
        return False

    def delete_list(self, list_id):
        list_to_be_deleted = self.get_list_by_id(list_id, False)
        if not list:
            return False

        try:
            db.session.delete(list_to_be_deleted)
            db.session.commit()
            return True, "List deleted."
        except Exception as e:
            print(e)
            return False, "Error occurred in deleting the list. Please try again"
