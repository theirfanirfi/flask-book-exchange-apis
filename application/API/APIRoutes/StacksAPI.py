from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data, invalidArgsResponse
from application.API.Factory.BLFactory import BF
from application.API.Factory.ModelFactory import MF
from application.API.Factory.SchemaFactory import SF
from application import db

class StacksAPI(FlaskView):

    def index(self):
        response = dict({"isLoggedIn": True})
        return jsonify(response)
        # books = BF.getBL("book").get_by_column(
        #     modelName="book",
        #     columnName="is_available_for_exchange",
        #     columnValue=1,
        #     isMany=True,
        #     isDump=True)
        # return jsonify(books)

    def get(self, id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        isFound, books = BF.getBL("stack").get_list_books(id, user)
        return jsonify({"books": books})

    def post(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)


        form = request.form
        book_model = MF.getModel("book")
        fields_to_validate = ['book_title', 'book_author',
                              'book_cover_image', 'book_isbn',
                              'book_added_from', 'book_description', 'list_id']
        print(form)
        for field in fields_to_validate:
            if not field in form:
                return jsonify(invalidArgsResponse)
            if form[field] == "":
                return jsonify(invalidArgsResponse)

        model = book_model[0]
        model.is_available_for_exchange = 0
        model.book_title = form['book_title']
        model.user_id = user.user_id
        model.book_author = form['book_author']
        model.book_cover_image = form['book_cover_image']
        model.book_isbn = form['book_isbn']
        model.book_added_from = form['book_added_from']
        model.book_description = form['book_description']

        try:
            db.session.add(model)
            db.session.flush()
            stack = MF.getModel("stack")[0]
            stack.book_id = model.book_id
            stack.list_id = form['list_id']
            stack.user_id = user.user_id
            db.session.add(stack)
            db.session.commit()
            return jsonify(
                {"isCreated": True,
                 "isError": False,
                 "message": "Book added to list",
                 "stack": SF.getSchema("stack", isMany=False).dump(stack)
                 })
        except Exception as e:
            print(e)
            return jsonify({"isCreated": False, "isError":True, "message": "Error occurred. Please try again later."})

    def delete(self, id):
        print(id)
        isDeleted, json_res = BF.getBL("stack").delete_row(request, id)
        print(json_res)
        return json_res
