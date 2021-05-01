class Config:
    SECRET_KEY = '123456789'
    SQL_USER = 'bfc6dfb2a1b3b2'
    SQL_PASS = '0f02b2e9'
    # Heroku = 'heroku_faf6be35db9c239'
    # SQL_URI = 'mysql+pymysql://root:root@localhost/bookexchanger'
    # SQL_URI = 'sqlite:///bookexchanger.db'
    SQL_URI = 'mysql+pymysql://icabbt58u2yfdjk1:df2kca2ubu664b5s@frwahxxknm9kwy6c.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/kgsigxkcxma0q6kt'
    SQLALCHEMY_DATABASE_URI = SQL_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = None