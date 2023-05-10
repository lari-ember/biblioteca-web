from datetime import date

from flask import Flask, flash, redirect, render_template, url_for
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from utils.forms import BookForm, LoginForm, SearchForm
from werkzeug.security import check_password_hash, generate_password_hash



app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

'''db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.route('/')
def index():
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # 'available', 'borrowed', or 'ex-libris'
    format = db.Column(db.String(50), nullable=False)  # 'physical', 'e-book', or 'pdf'
    genre = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

@app.cli.command('create_tables')
#@login_required
def create_tables():
    db.create_all()
    return 'Tabelas criadas!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

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

if __name__ == '__main__':
    app.run()
'''