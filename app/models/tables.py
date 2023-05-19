from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    books = db.relationship('Book', backref='user', lazy=True)
    
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
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
        
    