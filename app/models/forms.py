from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Register')


class BookForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    pages = IntegerField('Pages', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    status = SelectField('Status', choices=[('available', 'Available'), ('borrowed', 'Borrowed'), ('ex-libris', 'Ex-Libris')], validators=[DataRequired()])
    book_format = SelectField('Format', choices=[('physical', 'Physical'), ('e-book', 'E-book'), ('pdf', 'PDF')], validators=[DataRequired()])