from application.Models.models import Book
from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.Factory.ModelFactory import MF
from application.API.Factory.BLFactory import BF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic

class ExchangeBL(BusinessLogic):

    def getBooks(self, user, offset=0, isDump=False):
        books = Book.query.filter_by(is_available_for_exchange=1).all()
        return books if not isDump else SF.getSchema("book",isMany=True).dump(books)

    def get_exchange(self, id, isDump=False):
        exchange = MF.getModel("exchange")[1].query.filter_by(exchange_id=id)
        if not exchange.count() > 0:
            return False

        exchange = exchange.first()
        return exchange if not isDump else SF.getSchema("exchange",isMany=False).dump(exchange)

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

    def verify_exchange_request(self, exchange_id, user):
        model = MF.getModel("exchange")[1]
        is_there_any_such_exchange = model.query.filter_by(exchange=exchange_id,
                                                           to_exchange_with_user_id=user.user_id)
        if not is_there_any_such_exchange.count() > 0:
            return False

        exchange = is_there_any_such_exchange.first()
        return exchange

    def save_exchange(self, exchange, isConfirmed=False):
        try:
            db.session.add(exchange)
            db.session.commit()
            if isConfirmed:
                BF.getBL("notification").exchange_confirmed_notifications(exchange)
            BF.getBL("notification").exchange_declined_notifications(exchange)
            return True, "Exchange confirmed"
        except Exception as e:
            print(e)
            return False, "Error occurred. Please try again"
