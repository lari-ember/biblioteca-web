from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, SubmitField

class BookForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    pages = IntegerField('Pages', validators=[DataRequired()])
    status = SelectField('Status', choices=[('available', 'Available'), ('borrowed', 'Borrowed'), ('ex-libris', 'Ex-Libris')], validators=[DataRequired()])
    format = SelectField('Format', choices=[('physical', 'Physical'), ('e-book', 'E-book'), ('pdf', 'PDF')], validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])

class SearchForm(FlaskForm):
    code = StringField('Code')
    title = StringField('Title')
    author = StringField('Author')
    publisher = StringField('Publisher')
    status = SelectField('Status', choices=[('all', 'All'), ('available', 'Available'), ('borrowed', 'Borrowed'), ('ex-libris', 'Ex-Libris')])
    format = SelectField('Format', choices=[('all', 'All'), ('physical', 'Physical'), ('e-book', 'E-book'), ('pdf', 'PDF')])
    genre = StringField('Genre')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')