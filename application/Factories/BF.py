from application.BusinessLogic.cpanel.PostBl import PostBL
from application.BusinessLogic.cpanel.CategoriesBL import CategoriesBL

class BF:
    @staticmethod
    def getBL(bl):
        if bl == "post":
            return PostBL()
        elif bl == "category":
            return CategoriesBL()