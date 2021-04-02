from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, FileField, FloatField, \
    BooleanField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired


class UserForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField()

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField()

class CategoriesForm(FlaskForm):
    cat_title = StringField('Category Title', validators=[DataRequired()])
    submit = SubmitField()


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()


class PostForm(FlaskForm):
    post_title = StringField('Post Title', validators=[DataRequired()])
    post_description = TextAreaField('Post Description', validators=[DataRequired()], render_kw={'class':'ckeditor'})
    post_category = SelectField('Select Post Category', choices=[], coerce=str)
    post_image = FileField('Post Image', validators=[
        FileAllowed(['png', 'jpg', 'jpeg'], "JPG, PNG, JPEG files are only allowed.")])
    submit = SubmitField()




