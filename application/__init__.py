from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from application.config import Config
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO



db = SQLAlchemy()

bcrypt = Bcrypt()


app = Flask(__name__)
app.config.from_object(Config)
ma = Marshmallow(app)

app.jinja_env.filters['str'] = str()
db.app = app
db.init_app(app)
bcrypt.init_app(app)



migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'UserView:index'
login_manager.login_message_category = 'info'
socketio = SocketIO(app, async_mode='threading')

num = 0


@socketio.on('my_event')
def handle_my_custom_event(j):
    print('received args: ', str(j))

@socketio.on('my')
def event():
    print('event rec')
    socketio.emit('update', {'data': "test"});

@socketio.on('connect')
def test_connect():
    print('connected')
    global num
    num = num + 1
    print('num: ',num)
    socketio.emit('message', {'data': "test"})
    # socketio.emit('update', {'data': "test"})

from application.Models import *
# from application.cpanel.routes import cpanel

# # # app.register_blueprint(main)
# # app.register_blueprint(cpanel, url_prefix="/cpanel")

from application.Views.CategoriesView import CategoriesView
from application.Views.PostsView import PostsView
from application.Views.UserView import UserView
from application.Views.CustomPushNotificationsView import CustomPushNotificationsView


from application.API.APIRoutes.PostView import APIPostView
from application.API.APIRoutes.ListView import APIListView
from application.API.APIRoutes.BooksAPI import BooksAPI
from application.API.APIRoutes.StacksAPI import StacksAPI
from application.API.APIRoutes.LikesAPI import LikesAPI
from application.API.APIRoutes.CommentsAPI import CommentsAPI
from application.API.APIRoutes.ExchangeAPI import ExchangeAPI
from application.API.APIRoutes.SearchAPI import SearchAPI
from application.API.APIRoutes.NotificationsAPI import NotificationsAPI
from application.API.APIRoutes.ParticipantsAPI import ParticipantsAPI
from application.API.APIRoutes.MessagesAPI import MessagesAPI
from application.API.APIRoutes.LocationAPI import LocationAPI
from application.API.APIRoutes.ProfileAPI import ProfileAPI
from application.API.APIRoutes.FollowAPI import FollowAPI
from application.API.APIRoutes.AuthAPI import AuthAPI
from application.API.APIRoutes.BuyBookAPI import BuyBookAPI
from application.Team.TeamView import TeamView
#
#
# ProductsView.register(app, route_base='cpanel/products/')
UserView.register(app, route_base='/cpanel/login/')
PostsView.register(app, route_base='/cpanel/posts/')
CategoriesView.register(app, route_base='/cpanel/categories/')
TeamView.register(app, route_base='/cpanel/team/')
CustomPushNotificationsView.register(app, route_base='/cpanel/push_notifications/')

APIPostView.register(app, route_base='/api/post/')
APIListView.register(app, route_base='/api/list/')
BooksAPI.register(app, route_base='/api/book/')
StacksAPI.register(app, route_base='/api/stack/')
LikesAPI.register(app, route_base='/api/like/')
CommentsAPI.register(app, route_base='/api/comment/')
ExchangeAPI.register(app, route_base='/api/exchange/')
SearchAPI.register(app, route_base='/api/search/')
NotificationsAPI.register(app, route_base='/api/notification/')
ParticipantsAPI.register(app, route_base='/api/participant/')
LocationAPI.register(app, route_base='/api/location/')
ProfileAPI.register(app, route_base='/api/profile/')
MessagesAPI.register(app, route_base='/api/messages/')
FollowAPI.register(app, route_base='/api/follow/')
AuthAPI.register(app, route_base='/api/auth/')
BuyBookAPI.register(app, route_base='/api/buy/')


