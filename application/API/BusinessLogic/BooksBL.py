from application.Models.models import Book
from application.API.utils import uploadPostImage
from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class BooksBL(BusinessLogic):

    def getBooks(self, user, offset=0, isDump=False):
        books = Book.query.filter_by(is_available_for_exchange=1).all()
        return books if not isDump else SF.getSchema("book", isMany=True).dump(books)

    def get_book_by_isbn(self, isbn, isDump=False, user=None):
        checkExistence = None

        if user is None:
            checkExistence = Book.query.filter_by(book_isbn=isbn)
        else:
            checkExistence = Book.query.filter_by(book_isbn=isbn, user_id=user.user_id)

        if checkExistence.count() > 0:
            book = checkExistence.first()
            return True, book if not isDump else SF.getSchema("book", isMany=False).dump(book)
        return False, "Book not found"

    def make_book_by_isbn_for_sale(self, isbn, selling_price, isDump=False, user=None):
        if user is None:
            checkExistence = Book.query.filter_by(book_isbn=isbn)
        else:
            checkExistence = Book.query.filter_by(book_isbn=isbn, user_id=user.user_id)

        if checkExistence.count() > 0:
            book = checkExistence.first()
            book.selling_price = float(selling_price)
            book.is_for_sale = 1
            try:
                db.session.add(book)
                db.session.commit()
                return True, book if not isDump else SF.getSchema("book", isMany=False).dump(book)
            except Exception as e:
                return False, None
        return False, "Book not found"

    def make_book_by_isbn_for_exchange(self, isbn, isDump=False, user=None):
        if user is None:
            checkExistence = Book.query.filter_by(book_isbn=isbn)
        else:
            checkExistence = Book.query.filter_by(book_isbn=isbn, user_id=user.user_id)

        if checkExistence.count() > 0:
            book = checkExistence.first()
            book.is_available_for_exchange = 1
            try:
                db.session.add(book)
                db.session.commit()
                return True, book if not isDump else SF.getSchema("book", isMany=False).dump(book)
            except Exception as e:
                return False, None
        return False, "Book not found"

    def add_list(self, title, isbn, desc, cover_image, author, source, user, isDump=False):

        book = Book()
        book.book_isbn = isbn
        book.book_title = title
        book.book_description = desc
        book.book_author = author
        book.book_cover_image = cover_image
        book.book_added_from = source
        book.user_id = user.user_id

        try:
            db.session.add(book)
            db.session.commit()
            return True, book if not isDump else SF.getSchema("book", False).dump(book)
        except Exception as e:
            return False, None

    def delete_book(self, book_id):
        book = self.get_by_column("book", "book_id", book_id)
        if not book:
            return False

        try:
            db.session.delete(book)
            db.session.commit()
            return True, "Book deleted."
        except Exception as e:
            print(e)
            return False, "Error occurred in deleting the list. Please try again"

    def get_user_books(self, user_id, is_dump=True, is_many=True):
        books = Book.query.filter_by(user_id=user_id).all()
        return SF.getSchema("book", is_many).dump(books) if is_dump else books
