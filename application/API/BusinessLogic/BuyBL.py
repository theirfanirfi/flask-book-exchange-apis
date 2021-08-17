from application.Models.models import buy_book
from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.Factory.ModelFactory import MF
from application.API.BusinessLogic.NotificationsBL import NotificationsBL
from application.API.BusinessLogic.BusinessLogic import BusinessLogic

class BuyBL(BusinessLogic):

    # def getBooks(self, user, offset=0, isDump=False):
    #     books = Book.query.filter_by(is_available_for_exchange=1).all()
    #     return books if not isDump else SF.getSchema("book",isMany=True).dump(books)

    def get_buy_request(self, id, isDump=False):
        buy = MF.getModel("buy")[1].query.filter_by(buy_id=id)
        if not buy.count() > 0:
            return False

        buy = buy.first()
        return buy if not isDump else SF.getSchema("buy",isMany=False).dump(buy)

    # def add_list(self, title, isbn, desc, cover_image,author, source, user, isDump=False):
    #     book = Book()
    #     book.book_isbn = isbn
    #     book.book_title = title
    #     book.book_description = desc
    #     book.book_author = author
    #     book.book_cover_image = cover_image
    #     book.book_added_from = source
    #     book.user_id = user.user_id
    #
    #     try:
    #         db.session.add(book)
    #         db.session.commit()
    #         return True, book if not isDump else SF.getSchema("book", False).dump(book)
    #     except Exception as e:
    #         return False, None
    #
    #
    # def delete_book(self, book_id):
    #     book = self.get_by_column("book","book_id", book_id)
    #     if not book:
    #         return False
    #
    #     try:
    #         db.session.delete(book)
    #         db.session.commit()
    #         return True, "Book deleted."
    #     except Exception as e:
    #         print(e)
    #         return False, "Error occurred in deleting the list. Please try again"
    #
    def verify_buy_request(self, buy_id, user):
        model = MF.getModel("buy")[1]
        is_there_any_such_request = model.query.filter_by(buy_id=buy_id)
        if not is_there_any_such_request.count() > 0:
            return False

        buy = is_there_any_such_request.first()
        return buy
    #
    def save_buy_request(self, buy, isConfirmed=False, isWithDrawn=False):
        try:
            db.session.add(buy)
            db.session.commit()
            bl = NotificationsBL()
            if not isWithDrawn:
                print('withdrawn is '+str(isWithDrawn)+ ' isconfirmed is: '+str(isConfirmed))
                if isConfirmed:
                    bl.buy_confirmed_notifications(buy)
                    book = self.get_by_column("book", "book_id", buy.book_id)
                    if book[1]:
                        book[1].is_available_for_exchange = 0
                        book[1].is_for_sale = 0
                        try:
                            db.session.add(book[1])
                            db.session.commit()
                        except Exception as e:
                            print(e)

                else:
                    bl.buy_declined_notifications(buy)
            else:
                pass
                # bl.exchange_withdrawn_notifications(exchange)

            return True, "Buy confirmed"
        except Exception as e:
            print(e)
            return False, "Error occurred. Please try again"
