from application import db, bcrypt, login_manager, ma
from sqlalchemy.orm import class_mapper, ColumnProperty
from flask_login import UserMixin
from datetime import datetime
import uuid


@login_manager.user_loader
def load_user(user):
    return User.query.get(user)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    obj = uuid.uuid4
    user_id = db.Column(db.String(200), default=lambda: uuid.uuid4(), primary_key=True)
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    token = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Integer, default=0)
    profile_image = db.Column(db.Text, nullable=True)
    location_longitude = db.Column(db.String(50), nullable=True)
    location_latitude = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.String(50), default=str(datetime.now())[:19])
    updated_at = db.Column(db.String(50), default=str(datetime.now())[:19])

    def get_id(self):
        return (self.user_id)


class Categories(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_title = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.String(50), default=str(datetime.now())[:19])
    updated_at = db.Column(db.String(50), default=str(datetime.now())[:19])


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(200), nullable=False)
    post_description = db.Column(db.Text, nullable=True)
    post_image = db.Column(db.Text, nullable=True)
    post_category = db.Column(db.Integer, nullable=True)
    is_admin_post = db.Column(db.Integer, default=0)
    user_id = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.String(50), default=str(datetime.now())[:19])
    updated_at = db.Column(db.String(50), default=str(datetime.now())[:19])


class List(db.Model):
    list_id = db.Column(db.Integer, primary_key=True)
    list_title = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.String(50), default=str(datetime.now())[:19])
    updated_at = db.Column(db.String(50), default=str(datetime.now())[:19])


class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    book_isbn = db.Column(db.String(200), nullable=False)
    book_title = db.Column(db.String(200), nullable=False)
    book_description = db.Column(db.Text, nullable=True)
    book_author = db.Column(db.Text, nullable=True)
    book_cover_image = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.String(200), nullable=False)
    book_added_from = db.Column(db.String(200), nullable=False)
    is_available_for_exchange = db.Column(db.Integer, default=1)
    created_at = db.Column(db.String(50), default=str(datetime.now())[:19])
    updated_at = db.Column(db.String(50), default=str(datetime.now())[:19])


class Exchange(db.Model):
    obj = uuid.uuid4
    exchange_id = db.Column(db.String(200), default=lambda: uuid.uuid4(), primary_key=True)
    user_id = db.Column(db.String(200), nullable=False)
    to_exchange_with_user_id = db.Column(db.String(200), nullable=False)
    book_to_be_sent_id = db.Column(db.Integer, nullable=False)
    book_to_be_received_id = db.Column(db.Integer, nullable=False)
    is_exchange_confirmed = db.Column(db.Integer, default=0)
    created_at = db.Column(db.String(50), default=str(datetime.now())[:19])
    updated_at = db.Column(db.String(50), default=str(datetime.now())[:19])


class Stack(db.Model):
    __tablename__ = "stacks"
    obj = uuid.uuid4
    stack_id = db.Column(db.String(200), primary_key=True, default=lambda: uuid.uuid4())
    list_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.String(50), default=str(datetime.now()))
    updated_at = db.Column(db.String(50), default=str(datetime.now()))


class Like(db.Model):
    __tablename__ = "likes"
    obj = uuid.uuid4
    like_id = db.Column(db.String(200), default=lambda: uuid.uuid4(), primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.String(50), default=str(datetime.now())[:19])
    updated_at = db.Column(db.String(50), default=str(datetime.now())[:19])


class Comment(db.Model):
    __tablename__ = "comments"
    obj = uuid.uuid4
    comment_id = db.Column(db.String(200), default=lambda: uuid.uuid4(), primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(200), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.String(50), default=str(datetime.now())[:19])
    updated_at = db.Column(db.String(50), default=str(datetime.now())[:19])


class Notification(db.Model):
    __tablename__ = "notifications"
    obj = uuid.uuid4
    notification_id = db.Column(db.String(200), default=lambda: uuid.uuid4(), primary_key=True)
    post_id = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.String(200), nullable=False, default=0)
    to_be_notified_user_id = db.Column(db.String(200), nullable=False, default=0)
    exchange_id = db.Column(db.String(200), nullable=False, default=0)
    is_like = db.Column(db.Integer, nullable=False, default=0)
    is_comment = db.Column(db.Integer, nullable=False, default=0)
    is_follow = db.Column(db.Integer, nullable=False, default=0)
    is_exchange = db.Column(db.Integer, nullable=False, default=0)
    book_to_be_provided_id = db.Column(db.Integer, nullable=False, default=0)
    book_requested_id = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.String(50), default=str(datetime.now())[:19])
    updated_at = db.Column(db.String(50), default=str(datetime.now())[:19])


class ChatParticipant(db.Model):
    __tablename__ = "chat_participants"
    obj = uuid.uuid4
    p_id = db.Column(db.String(200), default=lambda: uuid.uuid4(), primary_key=True)
    user_one_id = db.Column(db.String(200), nullable=False)
    user_two_id = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.String(50), default=str(datetime.now())[:19])
    updated_at = db.Column(db.String(50), default=str(datetime.now())[:19])


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"
    obj = uuid.uuid4
    message_id = db.Column(db.String(200), default=lambda: uuid.uuid4(), primary_key=True)
    sender_id = db.Column(db.String(200), nullable=False)
    receiver_id = db.Column(db.String(200), nullable=False)
    is_message = db.Column(db.Integer, default=0)
    is_exchange = db.Column(db.Integer, default=0)
    exchange_id = db.Column(db.String(200), default=0)
    created_at = db.Column(db.String(50), default=str(datetime.now())[:19])
    updated_at = db.Column(db.String(50), default=str(datetime.now())[:19])


######## schemas

class UserSchema(ma.Schema):
    class Meta:
        fields = [
            prop.key
            for prop in class_mapper(User).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]
        # fields = fields + ["followers"]


class PostSchema(ma.Schema):
    class Meta:
        fields = [
            prop.key
            for prop in class_mapper(Post).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]
        fields = fields + [
            prop.key
            for prop in class_mapper(User).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]
        fields = fields + ['likes_count', 'comments_count', 'isLiked']


class ListSchema(ma.Schema):
    class Meta:
        fields = [
            prop.key
            for prop in class_mapper(List).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]


class BookSchema(ma.Schema):
    class Meta:
        fields = [
            prop.key
            for prop in class_mapper(Book).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]
        fields = fields + [
            prop.key
            for prop in class_mapper(User).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]
        fields = fields + ['distance_in_km']


class StackSchema(ma.Schema):
    class Meta:
        fields = [
            prop.key
            for prop in class_mapper(Stack).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]
        fields = fields + [
            prop.key
            for prop in class_mapper(Book).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]
        fields += ['isMine']


# class StackSchema(ma.Schema):
#     class Meta:
#         fields = [
#             prop.key
#             for prop in class_mapper(Stack).iterate_properties
#             if isinstance(prop, ColumnProperty)
#         ]


class LikeSchema(ma.Schema):
    class Meta:
        fields = [
            prop.key
            for prop in class_mapper(Like).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]


class ExchangeSchema(ma.Schema):
    class Meta:
        fields = [
            prop.key
            for prop in class_mapper(Exchange).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]
        fields += [
            prop.key
            for prop in class_mapper(User).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]
        fields += [
            prop.key
            for prop in class_mapper(Book).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]


class CommentSchema(ma.Schema):
    class Meta:
        fields = [
            prop.key
            for prop in class_mapper(Comment).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]

        fields += [
            prop.key
            for prop in class_mapper(User).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]
        fields += ['isMine']


class NotificationSchema(ma.Schema):
    class Meta:
        fields = [
            prop.key
            for prop in class_mapper(Notification).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]

        fields += [
            prop.key
            for prop in class_mapper(User).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]
        fields += [
            prop.key
            for prop in class_mapper(Book).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]
        fields += ['isMine', 'book_to_received', 'book_to_send']


class MessageSchema(ma.Schema):
    class Meta:
        fields = [
            prop.key
            for prop in class_mapper(ChatMessage).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]

        fields += [
            prop.key
            for prop in class_mapper(User).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]
        fields += ['isMine', 'book_to_received', 'book_to_send']

class ParticipantSchema(ma.Schema):
    class Meta:
        fields = [
            prop.key
            for prop in class_mapper(ChatParticipant).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]

        fields += [
            prop.key
            for prop in class_mapper(User).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]
        fields += ['isMine', 'book_to_received', 'book_to_send']
