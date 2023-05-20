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
    genre = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, user_id, code, title, author, publisher, year, pages, genre):
        self.user_id = user_id
        self.code = code
        self.title = title
        self.author = author
        self.publisher = publisher
        self.year = year
        self.pages = pages
        self.genre = genre

    def __repr__(self):
        return f'<code={self.code}, book={self.title}, author={self.author}, year={self.year}, pages={self.pages}, genre={self.genre}, publisher={self.publisher}, format={self.format}, status={self.status}>'

with app.app_context():
    db.create_all()


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app.controllers import defaut

'''


@app.route('/books', methods=['GET', 'POST'])
@login_required
def books():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            code=form.code.data,
            title=form.title.data,
            author=form.author.data,
            publisher=form.publisher.data,
            year=form.year.data,
            pages=form.pages.data,
            status=form.status.data,
            format=form.format.data,
            genre=form.genre.data,
            user_id=current_user.id
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added')
        
@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            code=form.code.data,
            title=form.title.data,
            author=form.author.data,
            publisher=form.publisher.data,
            year=form.year.data,
            pages=form.pages.data,
            status=form.status.data,
            format=form.format.data,
            genre=form.genre.data,
            user_id=current_user.id
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_book.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    books = []
    if form.validate_on_submit():
        search_string = form.search.data
        if search_string:
            search = "%{}%".format(search_string)
            books = Book.query.filter(
                or_(Book.code.like(search),
                    Book.title.like(search),
                    Book.author.like(search),
                    Book.publisher.like(search),
                    Book.year.like(search),
                    Book.pages.like(search),
                    Book.status.like(search),
                    Book.format.like(search),
                    Book.genre.like(search),
                    )
            ).all()
            if not books:
                flash('No results found.', 'warning')
    return render_template('search.html', form=form, books=books)

app.route('/login')
def login():
    return render_template('login.html')

@app.route('/search')
def search():
    return render_template('search.html')
'''