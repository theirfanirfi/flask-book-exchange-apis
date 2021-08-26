from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class TeamForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired()])
    welcome_message = TextAreaField('Welcome Message', validators=[DataRequired()])
    submit = SubmitField()


class SendTeamMessageForm(FlaskForm):
    send_message = TextAreaField('Send Message to all', validators=[DataRequired()])
    submit = SubmitField()
