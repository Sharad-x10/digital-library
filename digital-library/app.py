# app.py - Main Flask Application for Digital Library System
# This is the core file that handles all routing, authentication, and business logic

from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from models import db, User, Book, BorrowRecord
from forms import RegistrationForm, LoginForm, BookForm, SearchForm
from functools import wraps
import os

# Initialize Flask application
app = Flask(__name__)

# Configuration settings
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'  # Used for session encryption
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources
app.config['UPLOAD_FOLDER'] = 'static/images/book_covers'  # Folder for book cover images
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size: 16MB

# Initialize database with app
db.init_app(app)

# Initialize Flask-Login for user session management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if user not authenticated
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """
    Load user from database by ID
    Required by Flask-Login to manage user sessions
    """
    return User.query.get(int(user_id))


# Custom decorator to restrict access to librarians only
def librarian_required(f):
    """
    Decorator to restrict route access to librarians only
    Returns 403 error if non-librarian tries to access
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'librarian':
            flash('Access denied. Librarian privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== HOME & AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    """
    Home page / Landing page
    Shows library features and recent books
    """
    # Get 6 most recently added books for display
    recent_books = Book.query.order_by(Book.id.desc()).limit(6).all()
    
    # Get total statistics for homepage
    total_books = Book.query.count()
    total_users = User.query.filter_by(role='student').count()
    total_borrowed = BorrowRecord.query.filter_by(status='borrowed').count()
    
    return render_template('index.html', 
                         recent_books=recent_books,
                         total_books=total_books,
                         total_users=total_users,
                         total_borrowed=total_borrowed)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    User registration page
    Handles both displaying form and processing registration
    """
    # If user already logged in, redirect to appropriate dashboard
    if current_user.is_authenticated:
        if current_user.role == 'librarian':
            return redirect(url_for('librarian_dashboard'))
        return redirect(url_for('student_dashboard'))
    
    form = RegistrationForm()
    
    # When form is submitted and valid
    if form.validate_on_submit():
        # Create new user instance
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)  # Hash password before saving
        
        # Add to database
        db.session.add(user)
        db.session.commit()
        
        flash(f'Registration successful! Welcome {user.username}. Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login page
    Authenticates users and redirects to appropriate dashboard
    """
    # If user already logged in, redirect to dashboard
    if current_user.is_authenticated:
        if current_user.role == 'librarian':
            return redirect(url_for('librarian_dashboard'))
        return redirect(url_for('student_dashboard'))
    
    form = LoginForm()
    
    # When form is submitted and valid
    if form.validate_on_submit():
        # Check if login is with email or username
        user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.username.data)
        ).first()
        
        # Verify user exists and password is correct
        if user and user.check_password(form.password.data):
            login_user(user)  # Create user session
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect to appropriate dashboard based on role
            if user.role == 'librarian':
                return redirect(url_for('librarian_dashboard'))
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid username/email or password. Please try again.', 'danger')
    
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """
    Logout current user and destroy session
    """
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


# ==================== STUDENT ROUTES ====================

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    """
    Student dashboard
    Shows borrowed books, available books, and borrowing history
    """
    if current_user.role != 'student':
        return redirect(url_for('librarian_dashboard'))
    
    # Get student's active borrows
    active_borrows = BorrowRecord.query.filter_by(
        user_id=current_user.id, 
        status='borrowed'
    ).all()
    
    # Update overdue status for active borrows
    for borrow in active_borrows:
        if borrow.is_overdue:
            borrow.status = 'overdue'
    db.session.commit()
    
    # Get featured/available books (limit to 6)
    available_books = Book.query.filter(Book.available_quantity > 0).limit(6).all()
    
    # Count overdue books
    overdue_count = BorrowRecord.query.filter_by(
        user_id=current_user.id, 
        status='overdue'
    ).count()
    
    return render_template('student_dashboard.html',
                         active_borrows=active_borrows,
                         available_books=available_books,
                         overdue_count=overdue_count)


@app.route('/browse')
@login_required
def browse_books():
    """
    Browse all books with search and filter functionality
    """
    form = SearchForm(request.args, meta={'csrf': False})
    
    # Start with all books
    query = Book.query
    
    # Apply search filter if provided
    search_query = request.args.get('search_query', '').strip()
    if search_query:
        search_filter = f'%{search_query}%'
        query = query.filter(
            (Book.title.like(search_filter)) |
            (Book.author.like(search_filter)) |
            (Book.isbn.like(search_filter))
        )
    
    # Apply category filter if provided
    category = request.args.get('category', '').strip()
    if category:
        query = query.filter_by(category=category)
    
    # Get filtered books
    books = query.all()
    
    return render_template('browse_books.html', books=books, form=form)


@app.route('/book/<int:book_id>')
@login_required
def book_details(book_id):
    """
    Show detailed information about a specific book
    """
    book = Book.query.get_or_404(book_id)
    
    # Check if current user has already borrowed this book
    user_has_borrowed = False
    if current_user.is_authenticated and current_user.role == 'student':
        user_has_borrowed = BorrowRecord.query.filter_by(
            user_id=current_user.id,
            book_id=book_id,
            status='borrowed'
        ).first() is not None
    
    return render_template('book_details.html', book=book, user_has_borrowed=user_has_borrowed)


@app.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    """
    Borrow a book (Student only)
    Creates a new borrow record and updates book availability
    """
    if current_user.role != 'student':
        flash('Only students can borrow books.', 'danger')
        return redirect(url_for('browse_books'))
    
    book = Book.query.get_or_404(book_id)
    
    # Check if book is available
    if book.available_quantity < 1:
        flash('Sorry, this book is currently not available.', 'warning')
        return redirect(url_for('book_details', book_id=book_id))
    
    # Check if user already has this book borrowed
    existing_borrow = BorrowRecord.query.filter_by(
        user_id=current_user.id,
        book_id=book_id,
        status='borrowed'
    ).first()
    
    if existing_borrow:
        flash('You have already borrowed this book.', 'warning')
        return redirect(url_for('book_details', book_id=book_id))
    
    # Create new borrow record
    borrow_record = BorrowRecord(
        user_id=current_user.id,
        book_id=book_id,
        borrow_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=14),  # 14 days borrowing period
        status='borrowed'
    )
    
    # Update book availability
    book.available_quantity -= 1
    
    # Save to database
    db.session.add(borrow_record)
    db.session.commit()
    
    flash(f'Successfully borrowed "{book.title}". Due date: {borrow_record.due_date.strftime("%B %d, %Y")}', 'success')
    return redirect(url_for('my_books'))


@app.route('/my-books')
@login_required
def my_books():
    """
    Show all books borrowed by current student
    Includes active borrows and borrowing history
    """
    if current_user.role != 'student':
        return redirect(url_for('librarian_dashboard'))
    
    # Get all borrow records for current user
    active_borrows = BorrowRecord.query.filter_by(
        user_id=current_user.id,
        status='borrowed'
    ).order_by(BorrowRecord.borrow_date.desc()).all()
    
    overdue_borrows = BorrowRecord.query.filter_by(
        user_id=current_user.id,
        status='overdue'
    ).order_by(BorrowRecord.due_date.asc()).all()
    
    history = BorrowRecord.query.filter_by(
        user_id=current_user.id,
        status='returned'
    ).order_by(BorrowRecord.return_date.desc()).all()
    
    return render_template('my_books.html',
                         active_borrows=active_borrows,
                         overdue_borrows=overdue_borrows,
                         history=history)


@app.route('/return/<int:record_id>', methods=['POST'])
@login_required
def return_book(record_id):
    """
    Return a borrowed book
    Updates borrow record and restores book availability
    """
    borrow_record = BorrowRecord.query.get_or_404(record_id)
    
    # Verify user owns this borrow record
    if borrow_record.user_id != current_user.id and current_user.role != 'librarian':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    
    # Check if already returned
    if borrow_record.status == 'returned':
        flash('This book has already been returned.', 'info')
        return redirect(url_for('my_books'))
    
    # Update borrow record
    borrow_record.return_date = datetime.utcnow()
    borrow_record.status = 'returned'
    
    # Restore book availability
    book = Book.query.get(borrow_record.book_id)
    book.available_quantity += 1
    
    db.session.commit()
    
    flash(f'Successfully returned "{book.title}". Thank you!', 'success')
    
    if current_user.role == 'librarian':
        return redirect(url_for('librarian_dashboard'))
    return redirect(url_for('my_books'))


# ==================== LIBRARIAN ROUTES ====================

@app.route('/librarian/dashboard')
@login_required
@librarian_required
def librarian_dashboard():
    """
    Librarian dashboard
    Shows statistics, recent borrows, and overdue books
    """
    # Get statistics
    total_books = Book.query.count()
    total_users = User.query.filter_by(role='student').count()
    borrowed_books = BorrowRecord.query.filter_by(status='borrowed').count()
    overdue_books = BorrowRecord.query.filter_by(status='overdue').count()
    
    # Get recent borrow records (last 10)
    recent_borrows = BorrowRecord.query.order_by(
        BorrowRecord.borrow_date.desc()
    ).limit(10).all()
    
    # Get overdue records
    overdue_records = BorrowRecord.query.filter_by(status='overdue').all()
    
    # Update overdue status
    all_borrowed = BorrowRecord.query.filter_by(status='borrowed').all()
    for record in all_borrowed:
        if record.is_overdue:
            record.status = 'overdue'
    db.session.commit()
    
    return render_template('librarian_dashboard.html',
                         total_books=total_books,
                         total_users=total_users,
                         borrowed_books=borrowed_books,
                         overdue_books=overdue_books,
                         recent_borrows=recent_borrows,
                         overdue_records=overdue_records)


@app.route('/librarian/books')
@login_required
@librarian_required
def manage_books():
    """
    View all books in library (Librarian)
    """
    books = Book.query.all()
    return render_template('manage_books.html', books=books)


@app.route('/librarian/book/add', methods=['GET', 'POST'])
@login_required
@librarian_required
def add_book():
    """
    Add new book to library (Librarian only)
    """
    form = BookForm()
    
    if form.validate_on_submit():
        # Check if ISBN already exists
        existing_book = Book.query.filter_by(isbn=form.isbn.data).first()
        if existing_book:
            flash('A book with this ISBN already exists.', 'danger')
            return render_template('add_book.html', form=form)
        
        # Create new book
        book = Book(
            title=form.title.data,
            author=form.author.data,
            isbn=form.isbn.data,
            category=form.category.data,
            description=form.description.data,
            quantity=form.quantity.data,
            available_quantity=form.quantity.data,  # Initially all copies available
            publication_year=form.publication_year.data
        )
        
        db.session.add(book)
        db.session.commit()
        
        flash(f'Book "{book.title}" added successfully!', 'success')
        return redirect(url_for('manage_books'))
    
    return render_template('add_book.html', form=form)


@app.route('/librarian/book/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
@librarian_required
def edit_book(book_id):
    """
    Edit existing book (Librarian only)
    """
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    
    if form.validate_on_submit():
        # Update book details
        book.title = form.title.data
        book.author = form.author.data
        book.isbn = form.isbn.data
        book.category = form.category.data
        book.description = form.description.data
        
        # Update quantity (maintain borrowed books)
        borrowed_count = book.quantity - book.available_quantity
        book.quantity = form.quantity.data
        book.available_quantity = form.quantity.data - borrowed_count
        
        book.publication_year = form.publication_year.data
        
        db.session.commit()
        
        flash(f'Book "{book.title}" updated successfully!', 'success')
        return redirect(url_for('manage_books'))
    
    return render_template('edit_book.html', form=form, book=book)


@app.route('/librarian/book/delete/<int:book_id>', methods=['POST'])
@login_required
@librarian_required
def delete_book(book_id):
    """
    Delete book from library (Librarian only)
    Only possible if no active borrows exist
    """
    book = Book.query.get_or_404(book_id)
    
    # Check if book has active borrows
    active_borrows = BorrowRecord.query.filter_by(
        book_id=book_id,
        status='borrowed'
    ).count()
    
    if active_borrows > 0:
        flash('Cannot delete book with active borrows. Please wait for returns.', 'danger')
        return redirect(url_for('manage_books'))
    
    db.session.delete(book)
    db.session.commit()
    
    flash(f'Book "{book.title}" deleted successfully.', 'success')
    return redirect(url_for('manage_books'))


@app.route('/librarian/borrows')
@login_required
@librarian_required
def all_borrows():
    """
    View all borrow records (Librarian)
    """
    # Get filter parameters
    status_filter = request.args.get('status', 'all')
    
    query = BorrowRecord.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    borrows = query.order_by(BorrowRecord.borrow_date.desc()).all()
    
    return render_template('all_borrows.html', borrows=borrows, status_filter=status_filter)


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500


# ==================== DATABASE INITIALIZATION ====================

def init_db():
    """
    Initialize database and create sample data
    Run this function once to set up the database
    """
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if data already exists
        if User.query.first() is None:
            print("Creating sample data...")
            
            # Create librarian account
            librarian = User(
                username='admin',
                email='admin@library.com',
                role='librarian'
            )
            librarian.set_password('admin123')
            db.session.add(librarian)
            
            # Create sample students
            students = [
                {'username': 'john_doe', 'email': 'john@student.com', 'password': 'student123'},
                {'username': 'jane_smith', 'email': 'jane@student.com', 'password': 'student123'},
                {'username': 'bob_wilson', 'email': 'bob@student.com', 'password': 'student123'}
            ]
            
            for student_data in students:
                student = User(
                    username=student_data['username'],
                    email=student_data['email'],
                    role='student'
                )
                student.set_password(student_data['password'])
                db.session.add(student)
            
            # Create sample books
            books = [
                {
                    'title': 'Python Programming',
                    'author': 'John Smith',
                    'isbn': '9781234567897',
                    'category': 'Technology',
                    'description': 'A comprehensive guide to Python programming for beginners and experts.',
                    'quantity': 5,
                    'publication_year': 2023
                },
                {
                    'title': 'Web Development Fundamentals',
                    'author': 'Sarah Johnson',
                    'isbn': '9781234567898',
                    'category': 'Technology',
                    'description': 'Learn HTML, CSS, JavaScript, and modern web development practices.',
                    'quantity': 4,
                    'publication_year': 2022
                },
                {
                    'title': 'Data Science Essentials',
                    'author': 'Michael Brown',
                    'isbn': '9781234567899',
                    'category': 'Science',
                    'description': 'Master data analysis, visualization, and machine learning basics.',
                    'quantity': 3,
                    'publication_year': 2023
                },
                {
                    'title': 'The Great Gatsby',
                    'author': 'F. Scott Fitzgerald',
                    'isbn': '9780743273565',
                    'category': 'Fiction',
                    'description': 'A classic American novel set in the Jazz Age.',
                    'quantity': 6,
                    'publication_year': 1925
                },
                {
                    'title': '1984',
                    'author': 'George Orwell',
                    'isbn': '9780451524935',
                    'category': 'Fiction',
                    'description': 'A dystopian social science fiction novel.',
                    'quantity': 5,
                    'publication_year': 1949
                },
                {
                    'title': 'Sapiens',
                    'author': 'Yuval Noah Harari',
                    'isbn': '9780062316097',
                    'category': 'History',
                    'description': 'A brief history of humankind from the Stone Age to modern times.',
                    'quantity': 4,
                    'publication_year': 2011
                },
                {
                    'title': 'Atomic Habits',
                    'author': 'James Clear',
                    'isbn': '9780735211292',
                    'category': 'Self-Help',
                    'description': 'An easy and proven way to build good habits and break bad ones.',
                    'quantity': 7,
                    'publication_year': 2018
                },
                {
                    'title': 'The Lean Startup',
                    'author': 'Eric Ries',
                    'isbn': '9780307887894',
                    'category': 'Business',
                    'description': 'How constant innovation creates radically successful businesses.',
                    'quantity': 3,
                    'publication_year': 2011
                }
            ]
            
            for book_data in books:
                book = Book(
                    title=book_data['title'],
                    author=book_data['author'],
                    isbn=book_data['isbn'],
                    category=book_data['category'],
                    description=book_data['description'],
                    quantity=book_data['quantity'],
                    available_quantity=book_data['quantity'],
                    publication_year=book_data['publication_year']
                )
                db.session.add(book)
            
            db.session.commit()
            print("Sample data created successfully!")
            print("\nLogin Credentials:")
            print("Librarian - Username: admin, Password: admin123")
            print("Student - Username: john_doe, Password: student123")


# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    # Initialize database on first run
    init_db()
    
    # Run Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)
