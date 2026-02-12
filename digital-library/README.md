# 📚 Digital Library System

A complete, colorful, and feature-rich web application for managing a digital library system built with Flask, Bootstrap 5, and SQLAlchemy.

**Course:** Web Technology (BIT233)  
**Institution:** Texas College of Management & IT  
**Project Type:** Full-Stack Website Development

---

## 🎯 Project Overview

The Digital Library System is a comprehensive web application that allows students to browse and borrow books, while librarians can manage the entire catalog and track borrowing activities. The system features a modern, colorful UI with smooth animations and responsive design.

---

## ✨ Features

### 🔐 Authentication System
- User registration with email validation
- Secure login with password hashing (Werkzeug)
- Role-based access control (Student/Librarian)
- Session management with Flask-Login
- Logout functionality

### 📖 Student Features
- **Browse Books**: Search by title, author, or ISBN
- **Filter by Category**: Fiction, Science, Technology, History, etc.
- **Book Details**: View comprehensive book information
- **Borrow Books**: Borrow available books with automatic due date calculation (14 days)
- **My Books Dashboard**: View active borrows and borrowing history
- **Return Books**: Return borrowed books
- **Overdue Tracking**: Automatic overdue book detection and notifications

### 👨‍💼 Librarian Features
- **Dashboard**: View statistics and recent activities
- **Add Books**: Add new books to the catalog
- **Edit Books**: Update book information
- **Delete Books**: Remove books from catalog
- **Manage Borrows**: View all borrow records
- **Mark Returns**: Process book returns
- **Statistics**: Track total books, users, borrows, and overdue items

### 🎨 Design Features
- **Colorful UI**: Vibrant gradients and modern color schemes
- **Responsive Design**: Mobile, tablet, and desktop optimized
- **Animations**: Smooth transitions and hover effects
- **Interactive Elements**: Card-based layouts with shadows
- **Font Awesome Icons**: Professional iconography throughout
- **Bootstrap 5**: Modern, responsive components

---

## 🛠️ Technology Stack

### Backend
- **Python** 3.8+
- **Flask** 2.3.0 - Web framework
- **Flask-SQLAlchemy** 3.0.3 - ORM for database operations
- **Flask-Login** 0.6.2 - User session management
- **Flask-WTF** 1.1.1 - Form handling and validation
- **Werkzeug** 2.3.0 - Password hashing and security
- **SQLite** - Database

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom styling with gradients and animations
- **Bootstrap 5** - Responsive framework
- **JavaScript** - Client-side validation and interactivity
- **Font Awesome** 6.4.0 - Icons

---

## 📁 Project Structure

```
digital-library/
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── forms.py                    # WTForms for validation
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
│
├── static/
│   ├── css/
│   │   └── style.css          # Custom colorful styles
│   ├── js/
│   │   └── script.js          # JavaScript for interactivity
│   └── images/
│       └── book_covers/       # Book cover images
│
└── templates/
    ├── base.html              # Base template with navigation
    ├── index.html             # Landing page
    ├── register.html          # Registration page
    ├── login.html             # Login page
    ├── student_dashboard.html # Student dashboard
    ├── librarian_dashboard.html # Librarian dashboard
    ├── browse_books.html      # Book catalog
    ├── book_details.html      # Book details page
    ├── my_books.html          # User's borrowed books
    ├── add_book.html          # Add book form (librarian)
    ├── edit_book.html         # Edit book form (librarian)
    ├── manage_books.html      # Manage all books (librarian)
    └── all_borrows.html       # All borrow records (librarian)
```

---

## 🗄️ Database Schema

### Users Table
```sql
- id (Integer, Primary Key)
- username (String, Unique, Not Null)
- email (String, Unique, Not Null)
- password (String, Not Null) [Hashed]
- role (String, Not Null) [student/librarian]
- registration_date (DateTime, Default: Now)
```

### Books Table
```sql
- id (Integer, Primary Key)
- title (String, Not Null)
- author (String, Not Null)
- isbn (String, Unique, Not Null)
- category (String, Not Null)
- description (Text)
- cover_image (String)
- quantity (Integer, Not Null)
- available_quantity (Integer, Not Null)
- publication_year (Integer)
```

### BorrowRecords Table
```sql
- id (Integer, Primary Key)
- user_id (Integer, Foreign Key -> Users)
- book_id (Integer, Foreign Key -> Books)
- borrow_date (DateTime, Not Null)
- return_date (DateTime, Nullable)
- due_date (DateTime, Not Null)
- status (String, Not Null) [borrowed/returned/overdue]
```

### Relationships
- **One-to-Many**: User → BorrowRecords
- **One-to-Many**: Book → BorrowRecords

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for version control)

### Step 1: Clone or Download Project
```bash
# If using Git
git clone <repository-url>
cd digital-library

# Or download and extract ZIP file
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
The database will be automatically created when you first run the application. Sample data is included.

### Step 5: Run the Application
```bash
python app.py
```

The application will start on `http://127.0.0.1:5000/`

---

## 👤 Demo Credentials

### Librarian Account
- **Username:** admin
- **Password:** admin123
- **Email:** admin@library.com

### Student Accounts
1. **Username:** john_doe  
   **Password:** student123  
   **Email:** john@student.com

2. **Username:** jane_smith  
   **Password:** student123  
   **Email:** jane@student.com

3. **Username:** bob_wilson  
   **Password:** student123  
   **Email:** bob@student.com

---

## 📖 User Guide

### For Students

1. **Registration**
   - Click "Register" in navigation
   - Fill in username, email, password, and select "Student" role
   - Click "Register" to create account

2. **Login**
   - Enter username/email and password
   - Click "Login"

3. **Browse Books**
   - Navigate to "Browse Books"
   - Use search bar to find books by title, author, or ISBN
   - Filter by category using dropdown
   - Click "Details" to view full book information

4. **Borrow Books**
   - Go to book details page
   - Click "Borrow This Book" if available
   - Book will be added to your borrowings with 14-day due date

5. **Manage Borrowed Books**
   - Go to "My Books" to see active borrows
   - View due dates and overdue status
   - Click "Return" to return a book

### For Librarians

1. **Dashboard**
   - View statistics: total books, users, borrows, overdue
   - See recent borrowing activities
   - Quick access to management functions

2. **Add Books**
   - Click "Add New Book"
   - Fill in book details (title, author, ISBN, etc.)
   - Click "Save Book"

3. **Manage Books**
   - View all books in catalog
   - Click "Edit" to update book information
   - Click "Delete" to remove book (only if not borrowed)

4. **Manage Borrows**
   - View all borrow records
   - Filter by status (borrowed, returned, overdue)
   - Mark books as returned

---

## 🎨 Color Scheme

- **Primary Blue:** #4A90E2
- **Primary Purple:** #9B59B6
- **Secondary Orange:** #F39C12
- **Secondary Teal:** #1ABC9C
- **Accent Pink:** #E91E63
- **Accent Green:** #27AE60
- **Text Dark:** #2C3E50
- **Background:** Light gradients

---

## ✅ Form Validation

### Client-Side (JavaScript)
- Real-time password strength indicator
- Email format validation
- Username character validation
- Password confirmation matching
- ISBN format validation
- Required field validation

### Server-Side (Flask-WTF)
- Email validator
- Password length (minimum 8 characters)
- Username length (3-20 characters)
- ISBN format (10 or 13 digits)
- Quantity range validation
- Unique username and email checks

---

## 🔒 Security Features

- Password hashing with Werkzeug
- Session-based authentication
- CSRF protection with Flask-WTF
- Role-based access control
- SQL injection prevention (SQLAlchemy ORM)
- Secure form handling

---

## 📱 Responsive Design

The application is fully responsive and works on:
- **Desktop** (1200px and above)
- **Tablet** (768px - 1199px)
- **Mobile** (below 768px)

---

## 🧪 Testing

### Manual Testing Checklist

**Authentication**
- [ ] User can register with valid credentials
- [ ] User cannot register with existing username/email
- [ ] User can login with correct credentials
- [ ] User cannot login with incorrect credentials
- [ ] User can logout successfully

**Student Features**
- [ ] Student can browse all books
- [ ] Student can search books by title/author/ISBN
- [ ] Student can filter books by category
- [ ] Student can view book details
- [ ] Student can borrow available books
- [ ] Student can view borrowed books
- [ ] Student can return books
- [ ] Overdue books are marked correctly

**Librarian Features**
- [ ] Librarian can view dashboard statistics
- [ ] Librarian can add new books
- [ ] Librarian can edit existing books
- [ ] Librarian can delete books (if not borrowed)
- [ ] Librarian can view all borrow records
- [ ] Librarian can mark books as returned

---

## 🐛 Known Issues & Limitations

- Book cover image upload not yet implemented (placeholder icons used)
- No email notifications for due dates
- No pagination for large book catalogs
- No advanced search filters (price, rating, etc.)

---

## 🚀 Future Enhancements

- [ ] Book cover image upload functionality
- [ ] Email notifications for due dates and overdue books
- [ ] Advanced search with multiple filters
- [ ] Book ratings and reviews
- [ ] Reading history and recommendations
- [ ] Export reports (PDF, CSV)
- [ ] Book reservation system
- [ ] Multi-language support
- [ ] Admin panel with user management
- [ ] API for mobile application

---

## 📝 Assignment Compliance

This project fulfills all requirements for the Web Technology (BIT233) assignment:

✅ **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5  
✅ **Backend:** Flask framework, Python  
✅ **Database:** SQLAlchemy with 3 related tables  
✅ **Features:** Authentication, CRUD operations, search, validation  
✅ **Pages:** 5+ interconnected pages  
✅ **Design:** Colorful, responsive, modern UI  
✅ **Documentation:** Comprehensive README, code comments  
✅ **Version Control:** Git-ready with .gitignore

---

## 👨‍💻 Developer

**Name:** [Your Name]  
**LCID:** [Your LCID]  
**Course:** Web Technology (BIT233)  
**Institution:** Texas College of Management & IT

---

## 📄 License

This project is created for educational purposes as part of the BIT233 Web Technology course assignment.

---

## 🙏 Acknowledgments

- Texas College of Management & IT
- Mr. Ashish Gautam (Course Instructor)
- Flask Documentation
- Bootstrap 5 Documentation
- Font Awesome
- Stack Overflow Community

---

## 📞 Support

For questions or issues:
- Email: [your-email@example.com]
- GitHub Issues: [repository-url]/issues

---

**Made with ❤️ for BIT233 Web Technology Assignment**
