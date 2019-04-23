from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from app.models import User


class RegisterForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(),
                                Length(min=6, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password', validators=[DataRequired(),
                                Length(min=6, max=20)])
    confirm = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username already taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email already taken')


class LoginForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(),
                                Length(min=6, max=20)])
    password = PasswordField(
        'Password', validators=[DataRequired(),
                                Length(min=6, max=20)])
    remember = BooleanField("Remeber Me")
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('user does not exist')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'New Password', validators=[DataRequired(),
                                    Length(min=6, max=20)])
    confirm = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Reset Password')


class PostForm(FlaskForm):
    text = TextAreaField(
        'Add somthing to your todo list',
        validators=[DataRequired(), Length(min=1, max=70)])
    submit = SubmitField('Submit')