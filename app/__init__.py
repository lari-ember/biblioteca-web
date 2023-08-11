from datetime import date

from flask import Flask, flash, redirect, render_template, url_for, request
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user, UserMixin)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
#from utils.forms import BookForm, LoginForm, SearchForm
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///storage.db'
db = SQLAlchemy(app)

app.secret_key = 'secret'

lm = LoginManager(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    books = db.relationship('Book', backref='user', lazy=True)
    user_readings = db.relationship('UserReadings', backref='user', lazy=True)  # Adicione este atributo de relacionamento
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False


    def get_id(self):
        return str(self.id)

    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    
    def __init__(self, username, password, name):
        self.username = username
        self.password = password
        self.name = name
        
    def __repr__(self):
        return f'<User {self.username}>'
    
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # 'available', 'borrowed', or 'ex-libris'
    format = db.Column(db.String(50), nullable=False)  # 'physical', 'e-book', or 'pdf'
    read = db.Column(db.String(10), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    completion_date = db.Column(db.String(11), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_readings = db.relationship('UserReadings', backref='book', lazy=True)  # Adicione este atributo de relacionamento

    def __init__(self, user_id, code, title, author, publisher, year, pages, genre, status, format, read):
        self.user_id = user_id
        self.code = code
        self.title = title
        self.author = author
        self.publisher = publisher
        self.status = status
        self.format = format
        self.year = year
        self.pages = pages
        self.genre = genre
        self.read = read

    def __repr__(self):
        return f'<code={self.code}, book={self.title}, author={self.author}, year={self.year}, pages={self.pages}, genre={self.genre}, publisher={self.publisher}, format={self.format}, status={self.status}>'


class UserReadings(db.Model):
    __tablename__ = 'user_readings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    current_page = db.Column(db.Integer)
    reading_percentage = db.Column(db.Float)
    time_spent = db.Column(db.Integer)
    estimated_time = db.Column(db.Integer)

    def __init__(self, user_id, book_id, current_page, reading_percentage, time_spent, estimated_time):
        self.user_id = user_id
        self.book_id = book_id
        self.current_page = current_page
        self.reading_percentage = reading_percentage
        self.time_spent = time_spent
        self.estimated_time = estimated_time

    def __repr__(self):
        return f'<UserReading user_id={self.user_id}, book_id={self.book_id}, current_page={self.current_page}, reading_percentage={self.reading_percentage}, time_spent={self.time_spent}, estimated_time={self.estimated_time}>'

class UserRead(db.Model):
    __tablename__ = 'user_reads'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    user = db.relationship('User', backref='user_book_reads')
    book = db.relationship('Book', backref='user_read')

    def __init__(self, user_id, book_id, read_date):
        self.user_id = user_id
        self.book_id = book_id
        self.read_date = read_date

    def __repr__(self):
        return f'<UserBookRead user_id={self.user_id}, book_id={self.book_id}, read_date={self.read_date}>'


with app.app_context():
    db.create_all()


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app.controllers import defaut