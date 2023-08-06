from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Email, InputRequired


class LoginForm(FlaskForm):
    email = StringField('Enter email to save results.', validators=[Email(), InputRequired()])
    submit = SubmitField("Send Magic Link")