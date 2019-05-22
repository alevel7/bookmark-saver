from flask_wtf.form import FlaskForm
from flask_bootstrap import Bootstrap
from models import User
from wtforms import StringField, PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired, url,InputRequired,Email, Length, Regexp,EqualTo, ValidationError


class SignUpForm(FlaskForm):
    username=StringField('username', validators=[
        DataRequired(), Length(3, 80),
        Regexp('^[A-Za-z0-9_]{3,}$', message="Usernames consist of numbers,letters and underscores")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('password2',message='Passwords must match')
    ])
    password2 = PasswordField('Confirm password', validators=[
        DataRequired()
    ])
    email  = StringField('Email', validators=[
        DataRequired(), Length(1, 120), Email()
    ])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There already is a user with this email address.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken')


class BookmarkForm(FlaskForm):
    url = StringField('url',validators=[DataRequired(),url()])
    description = StringField('Add an optional description')

    def validate(self):
        if not self.url.data.startswith("http://") or self.url.data.startswith("https://"):
            self.url.data = "http://"+self.url.data
        if not FlaskForm.validate(self):
            return False
        if not self.description.data:
            self.description.data = self.url.data
        return True

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(),Length(min=4,max=15)])
    password = PasswordField('password',validators=[InputRequired(),Length(min=8,max=80)])
    remember = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


