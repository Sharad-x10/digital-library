# 🚀 Digital Library System - Complete Setup Guide

This guide will walk you through setting up and running the Digital Library System from scratch.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your computer:

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, **CHECK** "Add Python to PATH"
   - Verify installation: Open Command Prompt/Terminal and run:
     ```bash
     python --version
     ```

2. **pip** (Python package manager)
   - Usually comes with Python
   - Verify: `pip --version`

3. **Text Editor** (Optional but recommended)
   - VS Code: https://code.visualstudio.com/
   - PyCharm: https://www.jetbrains.com/pycharm/
   - Or any text editor of your choice

---

## 📁 Step 1: Extract Project Files

1. Extract the `digital-library.zip` file to your desired location
2. You should see a folder structure like this:
   ```
   digital-library/
   ├── app.py
   ├── models.py
   ├── forms.py
   ├── requirements.txt
   ├── README.md
   ├── static/
   └── templates/
   ```

---

## 💻 Step 2: Open Terminal/Command Prompt

### On Windows:
1. Press `Win + R`
2. Type `cmd` and press Enter
3. Navigate to project folder:
   ```bash
   cd path\to\digital-library
   ```
   Example:
   ```bash
   cd C:\Users\YourName\Downloads\digital-library
   ```

### On macOS/Linux:
1. Open Terminal
2. Navigate to project folder:
   ```bash
   cd /path/to/digital-library
   ```

---

## 🔧 Step 3: Create Virtual Environment (Recommended)

A virtual environment keeps project dependencies isolated.

### Create Virtual Environment:
```bash
python -m venv venv
```

### Activate Virtual Environment:

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command prompt.

---

## 📦 Step 4: Install Dependencies

With virtual environment activated, install all required packages:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-SQLAlchemy (database)
- Flask-Login (authentication)
- Flask-WTF (forms)
- And other dependencies

**Wait for installation to complete** (may take 1-2 minutes).

---

## 🗄️ Step 5: Initialize Database

The database will be automatically created when you first run the application. Sample data (books, users) will be added automatically.

---

## ▶️ Step 6: Run the Application

Start the Flask development server:

```bash
python app.py
```

You should see output like:
```
Creating sample data...
Sample data created successfully!

Login Credentials:
Librarian - Username: admin, Password: admin123
Student - Username: john_doe, Password: student123

 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

---

## 🌐 Step 7: Open in Browser

1. Open your web browser (Chrome, Firefox, Edge, etc.)
2. Go to: **http://127.0.0.1:5000** or **http://localhost:5000**
3. You should see the colorful Digital Library homepage!

---

## 🎉 Step 8: Start Using the System

### Login as Student:
- **Username:** `john_doe`
- **Password:** `student123`
- Features: Browse books, borrow books, view borrowed books

### Login as Librarian:
- **Username:** `admin`
- **Password:** `admin123`
- Features: Add/edit/delete books, manage borrows, view statistics

### Or Register a New Account:
- Click "Register" in the navigation
- Fill in your details
- Choose role (Student or Librarian)

---

## 🛑 Stopping the Application

To stop the Flask server:
1. Go back to Terminal/Command Prompt
2. Press `CTRL + C`

---

## 🔄 Running Again

After the first setup, you only need to:

1. Navigate to project folder
   ```bash
   cd path/to/digital-library
   ```

2. Activate virtual environment
   ```bash
   # Windows:
   venv\Scripts\activate
   
   # macOS/Linux:
   source venv/bin/activate
   ```

3. Run the application
   ```bash
   python app.py
   ```

4. Open browser to http://127.0.0.1:5000

---

## 🐛 Troubleshooting

### Problem: "python is not recognized"
**Solution:** Python is not in PATH. Reinstall Python and check "Add Python to PATH"

### Problem: "No module named flask"
**Solution:** Virtual environment not activated or dependencies not installed.
```bash
# Activate venv first, then:
pip install -r requirements.txt
```

### Problem: "Port 5000 is already in use"
**Solution:** Another program is using port 5000. Either:
- Stop that program, OR
- Edit `app.py`, change the last line to:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)
  ```
  Then access at http://127.0.0.1:5001

### Problem: Database errors
**Solution:** Delete the `library.db` file and run the app again. It will recreate the database.

### Problem: "ModuleNotFoundError: No module named '_sqlite3'"
**Solution:** SQLite3 not installed with Python. Reinstall Python or install python-sqlite separately.

---

## 📸 Taking Screenshots for Documentation

For your assignment submission, take screenshots of:
1. Homepage
2. Registration page
3. Login page
4. Student dashboard
5. Browse books page
6. Book details page
7. My books page (with borrowed books)
8. Librarian dashboard
9. Add book page
10. Manage books page
11. All borrows page
12. Mobile responsive views (resize browser window)

---

## 🎓 For Assignment Submission

### What to Submit:

1. **Code Files** (Entire project folder as ZIP)
   - Include all `.py`, `.html`, `.css`, `.js` files
   - Include `requirements.txt`, `README.md`
   - Do NOT include `venv/` folder
   - Do NOT include `library.db` file
   - Do NOT include `__pycache__/` folders

2. **Documentation** (PDF)
   - Cover page with your details
   - README content
   - Screenshots of all pages
   - Database schema diagram
   - Installation guide

3. **GitHub Repository** (MANDATORY)
   - Create public repository
   - Push all project files
   - Include GitHub URL in documentation

---

## 📚 Additional Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **Bootstrap 5 Docs:** https://getbootstrap.com/docs/5.3/
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org/
- **Flask-Login Guide:** https://flask-login.readthedocs.io/

---

## 💡 Tips for Success

1. **Read the Code Comments:** The code is heavily commented to explain each section
2. **Understand the Flow:** Follow how a request goes from route → template → user
3. **Modify Gradually:** Make small changes and test frequently
4. **Use Browser DevTools:** F12 in browser to debug CSS and JavaScript
5. **Check Terminal Output:** Flask shows errors in the terminal window

---

## ✅ Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Project files extracted
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Application running (`python app.py`)
- [ ] Browser opened to http://127.0.0.1:5000
- [ ] Logged in successfully (admin/admin123 or john_doe/student123)
- [ ] All features working correctly

---

## 🎓 Project Developed For

**Course:** Web Technology (BIT233)  
**Institution:** Texas College of Management & IT  
**Assignment:** Full-Stack Website Development Project

---

**Good Luck with Your Project! 🚀**

If you encounter any issues not covered in this guide, refer to the README.md file or consult your course instructor.
