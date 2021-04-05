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
    user_id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    token = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Integer, default=0)
    profile_image = db.Column(db.Text, nullable=True)
    location_longitude = db.Column(db.String(50), nullable=True)
    location_latitude = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.String(50), default=str(datetime.now()))
    updated_at = db.Column(db.String(50), default=str(datetime.now()))


    def get_id(self):
        return (self.user_id)


class Categories(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_title = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.String(50), default=str(datetime.now()))
    updated_at = db.Column(db.String(50), default=str(datetime.now()))


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(200), nullable=False)
    post_description = db.Column(db.Text, nullable=True)
    post_image = db.Column(db.Text, nullable=True)
    post_category = db.Column(db.Integer, nullable=True)
    is_admin_post = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.String(50), default=str(datetime.now()))
    updated_at = db.Column(db.String(50), default=str(datetime.now()))


class List(db.Model):
    list_id = db.Column(db.Integer, primary_key=True)
    list_title = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.String(50), default=str(datetime.now()))
    updated_at = db.Column(db.String(50), default=str(datetime.now()))


class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    book_isbn = db.Column(db.String(200), nullable=False)
    book_title = db.Column(db.String(200), nullable=False)
    book_description = db.Column(db.Text, nullable=True)
    book_author = db.Column(db.Text, nullable=True)
    book_cover_image = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_added_from = db.Column(db.String(200), nullable=False)
    is_available_for_exchange = db.Column(db.Integer, default=1)
    created_at = db.Column(db.String(50), default=str(datetime.now()))
    updated_at = db.Column(db.String(50), default=str(datetime.now()))


class Exchange(db.Model):
    exchange_id = db.Column(db.Integer, primary_key=True)
    exchanger_user_id = db.Column(db.Integer, nullable=False)
    to_exchange_with_user_id = db.Column(db.Integer, nullable=False)
    book_to_be_sent_id = db.Column(db.Integer, nullable=False)
    book_to_be_received_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.String(50), default=str(datetime.now()))
    updated_at = db.Column(db.String(50), default=str(datetime.now()))


class Stack(db.Model):
    __tablename__ = "stacks"
    obj = uuid.uuid4()
    stack_id = db.Column(db.String(200), primary_key=True, default=str(obj.hex))
    list_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.String(50), default=str(datetime.now()))
    updated_at = db.Column(db.String(50), default=str(datetime.now()))


class Like(db.Model):
    __tablename__ = "likes"
    obj = uuid.uuid4()
    like_id = db.Column(db.String(200), primary_key=True, default=str(obj.hex))
    post_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.String(50), default=str(datetime.now()))
    updated_at = db.Column(db.String(50), default=str(datetime.now()))


class Comment(db.Model):
    __tablename__ = "comments"
    obj = uuid.uuid4
    comment_id = db.Column(db.String(200), default=lambda: uuid.uuid4(),primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.String(50), default=str(datetime.now()))
    updated_at = db.Column(db.String(50), default=str(datetime.now()))


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

class StackSchema(ma.Schema):
    class Meta:
        fields = [
            prop.key
            for prop in class_mapper(Stack).iterate_properties
            if isinstance(prop, ColumnProperty)
        ]

class LikeSchema(ma.Schema):
    class Meta:
        fields = [
            prop.key
            for prop in class_mapper(Like).iterate_properties
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


