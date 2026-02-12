# models.py - Database Models for Digital Library System
# This file defines the structure of our database tables and their relationships

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy (will be configured in app.py)
db = SQLAlchemy()


# User Model - Stores information about students and librarians
class User(UserMixin, db.Model):
    """
    User table stores all registered users (students and librarians)
    
    Attributes:
        id: Unique identifier for each user (Primary Key)
        username: Unique username for login
        email: User's email address (must be unique)
        password: Hashed password for security
        role: Either 'student' or 'librarian' for access control
        registration_date: When the user registered
    
    Relationships:
        borrow_records: One-to-Many relationship with BorrowRecord
                       (One user can have many borrow records)
    """
    __tablename__ = 'users'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # User credentials and information
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)  # Will store hashed password
    
    # User role: 'student' or 'librarian'
    role = db.Column(db.String(20), nullable=False, default='student')
    
    # Timestamp for when user registered
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationship: One user can have many borrow records
    # backref creates a reverse relationship (borrow_record.user)
    # lazy='dynamic' means the relationship will return a query object
    borrow_records = db.relationship('BorrowRecord', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """
        Hash the password before storing it in database
        This ensures passwords are never stored in plain text
        """
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verify if provided password matches the hashed password
        Returns True if password is correct, False otherwise
        """
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        """String representation of User object for debugging"""
        return f'<User {self.username}>'


# Book Model - Stores information about all books in the library
class Book(db.Model):
    """
    Book table stores all books available in the library
    
    Attributes:
        id: Unique identifier for each book (Primary Key)
        title: Book title
        author: Book author name
        isbn: International Standard Book Number (unique)
        category: Book category/genre (Fiction, Science, History, etc.)
        description: Brief description of the book
        cover_image: Filename of book cover image
        quantity: Total number of copies available
        available_quantity: Number of copies currently available for borrowing
        publication_year: Year the book was published
    
    Relationships:
        borrow_records: One-to-Many relationship with BorrowRecord
                       (One book can have many borrow records)
    """
    __tablename__ = 'books'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Book information
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(100), nullable=False, index=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.String(200), nullable=True, default='default_book.jpg')
    
    # Quantity tracking
    quantity = db.Column(db.Integer, nullable=False, default=1)
    available_quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # Publication information
    publication_year = db.Column(db.Integer, nullable=True)
    
    # Relationship: One book can have many borrow records
    borrow_records = db.relationship('BorrowRecord', backref='book', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def is_available(self):
        """Check if book is available for borrowing"""
        return self.available_quantity > 0
    
    def __repr__(self):
        """String representation of Book object for debugging"""
        return f'<Book {self.title}>'


# BorrowRecord Model - Tracks book borrowing transactions
class BorrowRecord(db.Model):
    """
    BorrowRecord table tracks all book borrowing transactions
    
    Attributes:
        id: Unique identifier for each borrow record (Primary Key)
        user_id: Foreign Key referencing User table
        book_id: Foreign Key referencing Book table
        borrow_date: When the book was borrowed
        return_date: When the book was actually returned (NULL if not returned)
        due_date: When the book should be returned (14 days from borrow_date)
        status: 'borrowed', 'returned', or 'overdue'
    
    Relationships:
        user: Many-to-One relationship with User (many records can belong to one user)
        book: Many-to-One relationship with Book (many records can belong to one book)
    """
    __tablename__ = 'borrow_records'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys establishing relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False, index=True)
    
    # Date tracking
    borrow_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)  # NULL if book not returned yet
    due_date = db.Column(db.DateTime, nullable=False)  # Calculated as borrow_date + 14 days
    
    # Status tracking: 'borrowed', 'returned', 'overdue'
    status = db.Column(db.String(20), nullable=False, default='borrowed', index=True)
    
    @property
    def is_overdue(self):
        """
        Check if book is overdue
        Returns True if current date is past due_date and book not returned
        """
        if self.status == 'returned':
            return False
        return datetime.utcnow() > self.due_date
    
    @property
    def days_until_due(self):
        """Calculate days until due date (negative if overdue)"""
        delta = self.due_date - datetime.utcnow()
        return delta.days
    
    def __repr__(self):
        """String representation of BorrowRecord object for debugging"""
        return f'<BorrowRecord User:{self.user_id} Book:{self.book_id} Status:{self.status}>'
