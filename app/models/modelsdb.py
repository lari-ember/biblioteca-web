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
    password_hash = db.Column(db.String(), nullable=False)
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
    isbn = db.Column(db.String(17), nullable=True, unique=False)  # ISBN-13 format
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
        if not isbn:
            return None

        # 1. Limpeza básica
        s = isbn.replace('-', '').replace(' ', '').upper()

        # 2. ISBN-10?
        if len(s) == 10:
            if not all(c.isdigit() or (i == 9 and c == 'X') for i, c in enumerate(s)):
                raise ValueError("ISBN-10 deve ter 9 dígitos e um dígito verificador (0–9 ou X).")
            # checksum ISBN-10
            total = sum((10 - i) * (10 if c == 'X' else int(c)) for i, c in enumerate(s))
            if total % 11 != 0:
                raise ValueError("Checksum inválido para ISBN-10.")
            # converte para ISBN-13 (prefixo 978)
            core = '978' + s[:-1]
            # calcula novo dígito verificador ISBN-13
            check = 0
            for i, ch in enumerate(core):
                n = int(ch)
                check += n if i % 2 == 0 else 3 * n
            cd = (10 - (check % 10)) % 10
            return core + str(cd)

        # 3. ISBN-13?
        if len(s) == 13 and s.isdigit():
            # checksum ISBN-13
            total = sum((1 if i % 2 == 0 else 3) * int(ch) for i, ch in enumerate(s[:-1]))
            cd = (10 - (total % 10)) % 10
            if cd != int(s[-1]):
                raise ValueError("Checksum inválido para ISBN-13.")
            return s

        # 4. Qualquer outro formato
        raise ValueError("ISBN deve ser ISBN-10 (10 chars, último pode ser X) ou ISBN-13 (13 dígitos).")



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