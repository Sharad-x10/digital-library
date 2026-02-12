// script.js - JavaScript for Digital Library System
// This file handles client-side form validation, animations, and interactivity

// Wait for DOM to be fully loaded before executing scripts
document.addEventListener('DOMContentLoaded', function() {
    
    // ==================== FORM VALIDATION ====================
    
    /**
     * Validate Registration Form
     * Checks username, email, password strength, and confirmation
     */
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // Get form values
            const username = document.getElementById('username').value.trim();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            
            let isValid = true;
            let errorMessage = '';
            
            // Validate username (3-20 characters, alphanumeric and underscore only)
            if (username.length < 3 || username.length > 20) {
                errorMessage += 'Username must be 3-20 characters long.\n';
                isValid = false;
            }
            
            if (!/^[a-zA-Z0-9_]+$/.test(username)) {
                errorMessage += 'Username can only contain letters, numbers, and underscores.\n';
                isValid = false;
            }
            
            // Validate email format
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                errorMessage += 'Please enter a valid email address.\n';
                isValid = false;
            }
            
            // Validate password strength (minimum 8 characters)
            if (password.length < 8) {
                errorMessage += 'Password must be at least 8 characters long.\n';
                isValid = false;
            }
            
            // Check for password complexity (at least one letter and one number)
            if (!/[a-zA-Z]/.test(password) || !/[0-9]/.test(password)) {
                errorMessage += 'Password must contain both letters and numbers.\n';
                isValid = false;
            }
            
            // Confirm passwords match
            if (password !== confirmPassword) {
                errorMessage += 'Passwords do not match.\n';
                isValid = false;
            }
            
            // If validation fails, show error
            if (!isValid) {
                alert(errorMessage);
                return false;
            }
            
            // If all validations pass, submit the form
            HTMLFormElement.prototype.submit.call(registerForm);
        });
        
        
        // Real-time password strength indicator
        const passwordInput = document.getElementById('password');
        if (passwordInput) {
            passwordInput.addEventListener('input', function() {
                const password = this.value;
                const strengthIndicator = document.getElementById('passwordStrength');
                
                if (strengthIndicator) {
                    let strength = 'Weak';
                    let color = '#E91E63'; // Pink for weak
                    
                    if (password.length >= 8) {
                        if (/[a-z]/.test(password) && /[A-Z]/.test(password) && 
                            /[0-9]/.test(password) && /[!@#$%^&*]/.test(password)) {
                            strength = 'Strong';
                            color = '#27AE60'; // Green for strong
                        } else if (/[a-zA-Z]/.test(password) && /[0-9]/.test(password)) {
                            strength = 'Medium';
                            color = '#F39C12'; // Orange for medium
                        }
                    }
                    
                    strengthIndicator.textContent = `Password Strength: ${strength}`;
                    strengthIndicator.style.color = color;
                    strengthIndicator.style.fontWeight = 'bold';
                }
            });
        }
    }
    
    /**
     * Validate Login Form
     * Checks for empty fields
     */
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;
            
            if (username === '' || password === '') {
                event.preventDefault();
                alert('Please fill in all fields.');
                return false;
            }
        });
    }
    
    /**
     * Validate Book Form
     * Checks ISBN format and other book details
     */
    const bookForm = document.getElementById('bookForm');
    if (bookForm) {
        bookForm.addEventListener('submit', function(event) {
            const title = document.getElementById('title').value.trim();
            const author = document.getElementById('author').value.trim();
            const isbn = document.getElementById('isbn').value.trim().replace(/-/g, '');
            const quantity = document.getElementById('quantity').value;
            
            let isValid = true;
            let errorMessage = '';
            
            // Validate title
            if (title.length < 1) {
                errorMessage += 'Book title is required.\n';
                isValid = false;
            }
            
            // Validate author
            if (author.length < 1) {
                errorMessage += 'Author name is required.\n';
                isValid = false;
            }
            
            // Validate ISBN (must be 10 or 13 digits)
            if (!/^\d{10}$|^\d{13}$/.test(isbn)) {
                errorMessage += 'ISBN must be 10 or 13 digits.\n';
                isValid = false;
            }
            
            // Validate quantity
            if (quantity < 1 || quantity > 1000) {
                errorMessage += 'Quantity must be between 1 and 1000.\n';
                isValid = false;
            }
            
            if (!isValid) {
                event.preventDefault();
                alert(errorMessage);
                return false;
            }
        });
    }
    
    // ==================== SEARCH FUNCTIONALITY ====================
    
    /**
     * Live search for books
     * Filters books as user types in search box
     */
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const bookCards = document.querySelectorAll('.book-card');
            
            bookCards.forEach(card => {
                const title = card.querySelector('.card-title').textContent.toLowerCase();
                const author = card.querySelector('.card-text').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || author.includes(searchTerm)) {
                    card.parentElement.style.display = 'block';
                } else {
                    card.parentElement.style.display = 'none';
                }
            });
        });
    }
    
    // ==================== CONFIRMATION DIALOGS ====================
    
    /**
     * Confirm before deleting a book
     */
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this book? This action cannot be undone.')) {
                event.preventDefault();
            }
        });
    });
    
    /**
     * Confirm before borrowing a book
     */
    const borrowButtons = document.querySelectorAll('.btn-borrow');
    borrowButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const bookTitle = this.getAttribute('data-book-title');
            if (!confirm(`Are you sure you want to borrow "${bookTitle}"? It will be due in 14 days.`)) {
                event.preventDefault();
            }
        });
    });
    
    /**
     * Confirm before returning a book
     */
    const returnButtons = document.querySelectorAll('.btn-return');
    returnButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const bookTitle = this.getAttribute('data-book-title');
            if (!confirm(`Confirm return of "${bookTitle}"?`)) {
                event.preventDefault();
            }
        });
    });
    
    // ==================== FLASH MESSAGE AUTO-HIDE ====================
    
    /**
     * Automatically hide flash messages after 5 seconds
     */
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
    
    // ==================== SMOOTH SCROLLING ====================
    
    /**
     * Smooth scroll to sections when clicking navigation links
     */
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                event.preventDefault();
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // ==================== TOOLTIPS INITIALIZATION ====================
    
    /**
     * Initialize Bootstrap tooltips
     */
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // ==================== IMAGE PREVIEW ====================
    
    /**
     * Preview image before uploading
     */
    const imageInput = document.getElementById('cover_image');
    if (imageInput) {
        imageInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                // Validate file type
                if (!file.type.startsWith('image/')) {
                    alert('Please select a valid image file.');
                    this.value = '';
                    return;
                }
                
                // Validate file size (max 5MB)
                if (file.size > 5 * 1024 * 1024) {
                    alert('Image size must be less than 5MB.');
                    this.value = '';
                    return;
                }
                
                // Show preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById('imagePreview');
                    if (preview) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    // ==================== DYNAMIC DATE CALCULATION ====================
    
    /**
     * Calculate and display due date for book borrowing
     */
    function calculateDueDate() {
        const today = new Date();
        const dueDate = new Date(today.setDate(today.getDate() + 14));
        const dueDateElement = document.getElementById('dueDate');
        
        if (dueDateElement) {
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            dueDateElement.textContent = dueDate.toLocaleDateString('en-US', options);
        }
    }
    
    calculateDueDate();
    
    // ==================== TABLE SORTING ====================
    
    /**
     * Sort table columns when clicking headers
     */
    const tableHeaders = document.querySelectorAll('th[data-sortable]');
    tableHeaders.forEach(header => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            const table = this.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const columnIndex = Array.from(this.parentElement.children).indexOf(this);
            const isAscending = this.classList.contains('sort-asc');
            
            rows.sort((a, b) => {
                const aValue = a.children[columnIndex].textContent.trim();
                const bValue = b.children[columnIndex].textContent.trim();
                
                if (isAscending) {
                    return aValue.localeCompare(bValue);
                } else {
                    return bValue.localeCompare(aValue);
                }
            });
            
            // Remove all rows
            rows.forEach(row => tbody.removeChild(row));
            
            // Add sorted rows
            rows.forEach(row => tbody.appendChild(row));
            
            // Toggle sort direction
            tableHeaders.forEach(h => h.classList.remove('sort-asc', 'sort-desc'));
            this.classList.toggle('sort-asc', !isAscending);
            this.classList.toggle('sort-desc', isAscending);
        });
    });
    
    // ==================== CATEGORY FILTER ====================
    
    /**
     * Filter books by category
     */
    const categoryFilter = document.getElementById('categoryFilter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function() {
            const selectedCategory = this.value.toLowerCase();
            const bookCards = document.querySelectorAll('.book-card');
            
            bookCards.forEach(card => {
                const category = card.querySelector('.badge-category').textContent.toLowerCase();
                
                if (selectedCategory === '' || category === selectedCategory) {
                    card.parentElement.style.display = 'block';
                } else {
                    card.parentElement.style.display = 'none';
                }
            });
        });
    }
    
    // ==================== LOADING ANIMATION ====================
    
    /**
     * Show loading spinner when submitting forms
     */
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
            }
        });
    });
    
    // ==================== CHARACTER COUNTER ====================
    
    /**
     * Show character count for textarea fields
     */
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        const counter = document.createElement('small');
        counter.className = 'text-muted';
        textarea.parentNode.appendChild(counter);
        
        const updateCounter = () => {
            const remaining = maxLength - textarea.value.length;
            counter.textContent = `${remaining} characters remaining`;
        };
        
        textarea.addEventListener('input', updateCounter);
        updateCounter();
    });
    
    // ==================== SCROLL TO TOP BUTTON ====================
    
    /**
     * Show scroll to top button when scrolling down
     */
    const scrollButton = document.getElementById('scrollTopBtn');
    if (scrollButton) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollButton.style.display = 'block';
            } else {
                scrollButton.style.display = 'none';
            }
        });
        
        scrollButton.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // ==================== NOTIFICATION BADGE ====================
    
    /**
     * Update notification badge count
     */
    function updateNotificationCount() {
        const overdueCount = document.querySelectorAll('.badge-overdue').length;
        const notificationBadge = document.getElementById('notificationBadge');
        
        if (notificationBadge && overdueCount > 0) {
            notificationBadge.textContent = overdueCount;
            notificationBadge.style.display = 'inline-block';
        }
    }
    
    updateNotificationCount();
    
    console.log('Digital Library System JavaScript loaded successfully!');
});

// ==================== UTILITY FUNCTIONS ====================

/**
 * Format date to readable string
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

/**
 * Show success toast notification
 */
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
    toast.style.zIndex = '9999';
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.5s ease';
        setTimeout(() => toast.remove(), 500);
    }, 3000);
}

/**
 * Validate ISBN checksum (for ISBN-13)
 */
function validateISBN13(isbn) {
    isbn = isbn.replace(/-/g, '');
    
    if (isbn.length !== 13) {
        return false;
    }
    
    let sum = 0;
    for (let i = 0; i < 12; i++) {
        let digit = parseInt(isbn[i]);
        sum += (i % 2 === 0) ? digit : digit * 3;
    }
    
    let checkDigit = (10 - (sum % 10)) % 10;
    return checkDigit === parseInt(isbn[12]);
}
