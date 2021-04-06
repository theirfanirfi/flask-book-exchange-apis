from application.Models.models import Book
from application.API.utils import uploadPostImage
from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic

class ExchangeBL(BusinessLogic):

    def getBooks(self, user, offset=0, isDump=False):
        books = Book.query.filter_by(is_available_for_exchange=1).all()
        return books if not isDump else SF.getSchema("book",isMany=True).dump(books)

    def add_list(self, title, isbn, desc, cover_image,author, source, user, isDump=False):
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
        book = self.get_by_column("book","book_id", book_id)
        if not book:
            return False

        try:
            db.session.delete(book)
            db.session.commit()
            return True, "Book deleted."
        except Exception as e:
            print(e)
            return False, "Error occurred in deleting the list. Please try again"