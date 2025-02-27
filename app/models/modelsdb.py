# models.py
from datetime import datetime

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    sum_pages = db.Column(db.Integer, default=0)

    # Relationships
    user_books = db.relationship('UserBooks', back_populates='user', cascade='all, delete-orphan')
    readings = db.relationship('UserReadings', back_populates='user', cascade='all, delete-orphan')
    loans = db.relationship('Loan', foreign_keys='Loan.borrower_id', back_populates='borrower')

    # Flask-Login required methods
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

    # Password handling
    def set_password(self, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        self.password_hash = generate_password_hash(
            password,
            method='scrypt',
            salt_length=16
        )

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @validates('username')
    def validate_username(self, key, username):
        if not 4 <= len(username) <= 50:
            raise ValueError("Username must be between 4-50 characters")
        return username.lower()


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(13), unique=True, nullable=False) # código de localização na prateleira fisica
    isbn = db.Column(db.String(17), nullable=False, unique=True)  # ISBN-13 format
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    cover_url = db.Column(db.String(200))
    format = db.Column(db.String(20), nullable=False)  # physical, ebook, pdf
    genre = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user_books = db.relationship('UserBooks', back_populates='book', cascade='all, delete-orphan')
    readings = db.relationship('UserReadings', back_populates='book', cascade='all, delete-orphan')

    # Validations
    __table_args__ = (
        CheckConstraint('publication_year BETWEEN 1800 AND EXTRACT(YEAR FROM NOW())',
                        name='valid_publication_year'),
    )

    @validates('isbn')
    def validate_isbn(self, key, isbn):
        # Basic ISBN-13 validation
        isbn = isbn.replace('-', '')
        if len(isbn) != 13 or not isbn.isdigit():
            raise ValueError("Invalid ISBN-13 format")
        return isbn


class UserBooks(db.Model):
    __tablename__ = 'user_books'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='available')  # available/borrowed
    acquisition_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='user_books')
    book = db.relationship('Book', back_populates='user_books')
    loans = db.relationship('Loan', back_populates='user_book', cascade='all, delete-orphan')


class UserReadings(db.Model):
    __tablename__ = 'readings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    current_page = db.Column(db.Integer, default=0)

    # Relationships
    user = db.relationship('User', back_populates='readings')
    book = db.relationship('Book', back_populates='readings')

    # Calculated property
    @property
    def progress(self):
        if self.book.pages > 0:
            return round((self.current_page / self.book.pages) * 100, 2)
        return 0.0


class UserRead(db.Model):
    __tablename__ = 'user_reads'
    id = db.Column(db.Integer, primary_key=True)
    user_book_id = db.Column(db.Integer, db.ForeignKey('user_books.id'), nullable=False)
    completion_date = db.Column(db.Date, nullable=False)  # Data de conclusão da leitura

    def __init__(self, user_book_id, completion_date):
        self.user_book_id = user_book_id
        self.completion_date = completion_date

    def __repr__(self):
        return f'<UserBookRead user_id={self.user_id}, book_id={self.book_id}, read_date={self.read_date}>'


class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    user_book_id = db.Column(db.Integer, db.ForeignKey('user_books.id'), nullable=False)
    borrower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    loan_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime)

    # Relationships
    user_book = db.relationship('UserBooks', back_populates='loans')
    borrower = db.relationship('User', foreign_keys=[borrower_id], back_populates='loans')

    __table_args__ = (
        db.UniqueConstraint('user_book_id', 'due_date', name='unique_loan'),
    )

    # Validations
    @validates('user_book_id')
    def validate_user_book(self, key, user_book_id):
        existing_loan = Loan.query.filter(
            Loan.user_book_id == user_book_id,
            Loan.return_date is None
        ).first()
        if existing_loan:
            raise ValueError("This book is already on loan")
        return user_book_id