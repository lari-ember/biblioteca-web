from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Optional, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')  # adiciona o campo que o template espera
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Register')


class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[Optional(), Length(max=17)])
    pages = IntegerField('Pages', validators=[DataRequired()])
    country_of_origin = StringField('Country of Origin', validators=[Optional(), Length(max=80)])
    original_language = StringField('Original Language', validators=[Optional(), Length(max=40)])
    read = SelectField('Reading Status', choices=[
        ('want_to_read', 'Want to read — Added to wishlist'),
        ('unread', 'Unread — Not started yet'),
        ('reading', 'Reading — Currently in progress'),
        ('read', 'Read — Finished reading'),
    ], default='unread', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    status = SelectField('Availability', choices=[
        ('available', 'Available — In your shelf'),
        ('borrowed', 'Borrowed — Lent to someone'),
        ('wishlist', 'Wishlist — Want to acquire'),
        ('ex-libris', 'Ex-Libris — No longer owned'),
    ], default='available', validators=[DataRequired()])
    format = SelectField('Format', choices=[
        ('physical', 'Physical — Printed book'),
        ('hardcover', 'Hardcover — Rigid cover edition'),
        ('paperback', 'Paperback — Soft cover edition'),
        ('ebook', 'E-book — Digital reader'),
        ('pdf', 'PDF — Digital document'),
        ('audiobook', 'Audiobook — Audio format'),
        ('comic', 'Comic/Graphic Novel'),
    ], default='physical', validators=[DataRequired()])
    cover_url = HiddenField()
    openlibrary_key = HiddenField()


class SearchForm(FlaskForm):
    search_field = SelectField('Search Field', choices=[
        ('', 'Select Field'),
        ('code', 'Code'),
        ('title', 'Title'),
        ('author', 'Author'),
        ('pages', 'Pages'),
        ('year', 'Year'),
        ('genre', 'Genre'),
        ('read', 'Read'),
        ('status', 'Status'),
        ('format', 'Format'),
        ('publisher', 'Publisher')
    ], validators=[DataRequired()])
    search_term = StringField('Search Term', validators=[DataRequired()])


class EditReadingForm(FlaskForm):
    current_page = IntegerField('Current Page', validators=[DataRequired()])
    # Adicione outros campos de edição conforme necessário
    submit = SubmitField('Update')


class LogReadingForm(FlaskForm):
    pages_read = IntegerField('Pages Read', validators=[DataRequired()])
    time_spent = IntegerField('Time Spent', validators=[DataRequired()])
    submit = SubmitField('Log Reading')
