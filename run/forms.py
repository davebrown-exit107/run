'''Forms'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from run.models import User

class SignupForm(FlaskForm):
    """User Signup Form."""
    username = StringField('Username',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[Length(min=6),
                                    Email(message='Enter a valid email.'),
                                    DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password',
                            validators=[DataRequired(),
                                        EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

#    def _validate_username(self, username):
#        user = User.query.filter_by(username=username.data).first()
#        if user is not None:
#            raise ValidationError('Please use a different username.')
#
#    def _validate_email(self, email):
#        user = User.query.filter_by(email=email.data).first()
#        if user is not None:
#            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    """User Login Form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class ProfileForm(FlaskForm):
    """Form to modify user profile."""
    username = StringField('Username',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[Length(min=6),
                                    Email(message='Enter a valid email.'),
                                    DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password',
                            validators=[DataRequired(),
                                        EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Update')

