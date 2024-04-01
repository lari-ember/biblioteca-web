from datetime import date

from flask import Flask, flash, redirect, render_template, url_for, request
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user, UserMixin)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
#from utils.forms import BookForm, LoginForm, SearchForm
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from sqlalchemy import func

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
    user_books = db.relationship('UserBooks', backref='user', lazy=True)
    user_readings = db.relationship('UserReadings', backref='user', lazy=True)  # atributo de relacionamento
    sum_pages = db.Column(db.Integer)
    
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
        return f'{self.name}'
    
    def update_sum_pages(self):
        total_pages_completed = db.session.query(func.sum(Book.pages)).filter(Book.read == 'read').scalar() or 0
        total_pages_in_progress = db.session.query(func.sum(UserReadings.current_page)).filter(
            UserReadings.user_id == self.id).scalar() or 0
        self.sum_pages = total_pages_in_progress + total_pages_completed
        db.session.commit()
    
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
    user_books = db.relationship('UserBooks', backref='book', lazy=True)
    user_readings = db.relationship('UserReadings', backref='book', lazy=True)  # Adicione este atributo de relacionamento
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=True)  # Chave estrangeira para a tabela Loan
    loan = db.relationship('Loan', backref='book', uselist=False,foreign_keys="[Loan.book_id]")

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

class UserBooks(db.Model):
    __tablename__ = 'user_books'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    # Se necessário, você pode adicionar mais informações específicas para a relação entre usuário e livro aqui

    def __init__(self, user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id

    def __repr__(self):
        return f'<UserBooks user_id={self.user_id}, book_id={self.book_id}>'

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

class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_borrowed = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    date_returned = db.Column(db.Date, nullable=True)
    borrower = db.relationship('User', foreign_keys=[borrower_id])
    lender = db.relationship('User', foreign_keys=[lender_id])

    def __init__(self, book_id, borrower_id, lender_id, date_borrowed, due_date):
        self.book_id = book_id
        self.borrower_id = borrower_id
        self.lender_id = lender_id
        self.date_borrowed = date_borrowed
        self.due_date = due_date

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