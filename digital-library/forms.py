# forms.py - Form classes for user input validation
# Uses Flask-WTF for form handling and validation

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from models import User, Book
import re


# Registration Form - For new user signup
class RegistrationForm(FlaskForm):
    """
    Form for user registration with validation
    
    Fields:
        username: Unique username (3-20 characters)
        email: Valid email address
        password: Strong password (minimum 8 characters)
        confirm_password: Must match password
        role: Select student or librarian
    """
    username = StringField('Username', 
                          validators=[
                              DataRequired(message='Username is required'),
                              Length(min=3, max=20, message='Username must be 3-20 characters')
                          ])
    
    email = StringField('Email', 
                       validators=[
                           DataRequired(message='Email is required'),
                           Email(message='Please enter a valid email address')
                       ])
    
    password = PasswordField('Password', 
                            validators=[
                                DataRequired(message='Password is required'),
                                Length(min=8, message='Password must be at least 8 characters long')
                            ])
    
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[
                                        DataRequired(message='Please confirm your password'),
                                        EqualTo('password', message='Passwords must match')
                                    ])
    
    role = SelectField('Role', 
                      choices=[('student', 'Student'), ('librarian', 'Librarian')],
                      validators=[DataRequired()])
    
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """
        Custom validator to check if username already exists
        Raises ValidationError if username is taken
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        """
        Custom validator to check if email already exists
        Raises ValidationError if email is already registered
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')


# Login Form - For user authentication
class LoginForm(FlaskForm):
    """
    Form for user login
    
    Fields:
        username: User's username or email
        password: User's password
    """
    username = StringField('Username or Email', 
                          validators=[DataRequired(message='Username/Email is required')])
    
    password = PasswordField('Password', 
                            validators=[DataRequired(message='Password is required')])
    
    submit = SubmitField('Login')


# Book Form - For adding/editing books (Librarian only)
class BookForm(FlaskForm):
    """
    Form for adding or editing books
    Used by librarians to manage book catalog
    
    Fields:
        title: Book title
        author: Author name
        isbn: ISBN number (13 digits)
        category: Book category/genre
        description: Book description
        quantity: Total copies
        publication_year: Year published
    """
    title = StringField('Book Title', 
                       validators=[
                           DataRequired(message='Book title is required'),
                           Length(max=200)
                       ])
    
    author = StringField('Author', 
                        validators=[
                            DataRequired(message='Author name is required'),
                            Length(max=100)
                        ])
    
    isbn = StringField('ISBN', 
                      validators=[
                          DataRequired(message='ISBN is required'),
                          Length(min=10, max=13, message='ISBN must be 10-13 characters')
                      ])
    
    category = SelectField('Category', 
                          choices=[
                              ('Fiction', 'Fiction'),
                              ('Non-Fiction', 'Non-Fiction'),
                              ('Science', 'Science'),
                              ('Technology', 'Technology'),
                              ('History', 'History'),
                              ('Biography', 'Biography'),
                              ('Mystery', 'Mystery'),
                              ('Romance', 'Romance'),
                              ('Fantasy', 'Fantasy'),
                              ('Self-Help', 'Self-Help'),
                              ('Business', 'Business'),
                              ('Literature', 'Literature')
                          ],
                          validators=[DataRequired()])
    
    description = TextAreaField('Description', 
                               validators=[Length(max=1000)])
    
    quantity = IntegerField('Total Quantity', 
                           validators=[
                               DataRequired(message='Quantity is required'),
                               NumberRange(min=1, max=1000, message='Quantity must be between 1-1000')
                           ])
    
    publication_year = IntegerField('Publication Year', 
                                   validators=[
                                       NumberRange(min=1000, max=2025, message='Enter a valid year')
                                   ])
    
    submit = SubmitField('Save Book')
    
    def validate_isbn(self, isbn):
        """
        Custom validator to check ISBN format and uniqueness
        ISBN should contain only digits and hyphens
        """
        # Remove hyphens for validation
        isbn_clean = isbn.data.replace('-', '').replace(' ', '')
        
        # Check if ISBN contains only digits
        if not isbn_clean.isdigit():
            raise ValidationError('ISBN should contain only numbers')
        
        # Check if ISBN length is valid (10 or 13 digits)
        if len(isbn_clean) not in [10, 13]:
            raise ValidationError('ISBN must be 10 or 13 digits')


# Search Form - For searching books
class SearchForm(FlaskForm):
    """
    Form for searching books in the catalog
    
    Fields:
        search_query: Search term (title, author, or ISBN)
        category: Filter by category
    """
    search_query = StringField('Search Books', 
                              validators=[Length(max=100)])
    
    category = SelectField('Category', 
                          choices=[
                              ('', 'All Categories'),
                              ('Fiction', 'Fiction'),
                              ('Non-Fiction', 'Non-Fiction'),
                              ('Science', 'Science'),
                              ('Technology', 'Technology'),
                              ('History', 'History'),
                              ('Biography', 'Biography'),
                              ('Mystery', 'Mystery'),
                              ('Romance', 'Romance'),
                              ('Fantasy', 'Fantasy'),
                              ('Self-Help', 'Self-Help'),
                              ('Business', 'Business'),
                              ('Literature', 'Literature')
                          ])
    
    submit = SubmitField('Search')
