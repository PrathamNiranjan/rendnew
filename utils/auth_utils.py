import bcrypt
import json
import os
from functools import wraps
from flask import session, redirect, url_for, flash

# In a real application, use a proper database
# This is simplified for demonstration purposes
USER_DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json')

def _load_users():
    if not os.path.exists(USER_DB_FILE):
        os.makedirs(os.path.dirname(USER_DB_FILE), exist_ok=True)
        return {}
    
    try:
        with open(USER_DB_FILE, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def _save_users(users):
    os.makedirs(os.path.dirname(USER_DB_FILE), exist_ok=True)
    with open(USER_DB_FILE, 'w') as file:
        json.dump(users, file)

def register_user(name, email, password):
    users = _load_users()
    
    # Check if user already exists
    if email in users:
        return False
    
    # Hash password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    # Add user
    users[email] = {
        'name': name,
        'password': hashed_password
    }
    
    _save_users(users)
    return True

def validate_login(email, password):
    users = _load_users()
    
    if email not in users:
        return False
    
    stored_password = users[email]['password']
    return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))

def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
