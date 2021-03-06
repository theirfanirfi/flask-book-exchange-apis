from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data
from application.API.Factory.BLFactory import BF
from application.API.Factory.ModelFactory import MF
from application import db
class APIListView(FlaskView):

    def index(self):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        lists = BF.getBL("list").getLists(user, True)
        response.update({"lists": lists})
        return jsonify(response)

    @route('/create/', methods=['POST'])
    def create(self):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        form = request.form
        title = form['list_title']
        isListCreated, newList = BF.getBL("list").add_list(title, user, isDump=True)
        response.update({"isListCreated": isListCreated, "list": newList})
        return jsonify(response)

    def get(self, id):
        pass

    def user(self, id):
        user_id = id
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        if str(id) == "me":
            user_id = user.user_id

        lists = BF.getBL("list").getLists_by_user_id(user_id, True)
        response.update({"lists": lists})
        return jsonify(response)

    def delete(self, id):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        listt = BF.getBL("list").get_list_by_id_user(id, user, isDump=False)
        if not listt:
            response.update({"isListDeleted": False, "message": "No such list found to delete"})
            return jsonify(response)

        books_in_the_list_stack = MF.getModel("stack")[1].query.filter_by(list_id=id, user_id=user.user_id).all()
        session = db.session
        toDelete = False
        for stack in books_in_the_list_stack:
            lists_book = MF.getModel("book")[1].query.filter_by(book_id=stack.book_id, user_id=user.user_id)
            if lists_book.count() > 0:
                toDelete=True
                session.delete(lists_book.first())
        if toDelete:
            session.commit()

        isListDeleted, message = BF.getBL("list").delete_list(listt.list_id)
        response.update({"isListDeleted": isListDeleted, "message": message})
        return jsonify(response)



