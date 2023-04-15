import os
import uuid

from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize Firebase
cred = credentials.Certificate('static/key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# User roles
ADMIN = 'admin'
USER = 'user'

# Login required decorator
def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper

# Admin required decorator
def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        user = db.collection('users').document(session['user']['uid']).get().to_dict()
        if not user['isAdmin']:
            return redirect(url_for('dashboard'))
        return func(*args, **kwargs)
    return wrapper

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            # Create Firebase user
            user = auth.create_user(email=email, password=password)
            # Add user to Firestore
            db.collection('users').document(user.uid).set({
                'email': email,
                'role': USER
            })
            return redirect(url_for('login'))
        except auth.EmailAlreadyExistsError:
            return 'Email already exists'
    return render_template('signup.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            # Sign in user with Firebase
            user = auth.sign_in_with_email_and_password(email, password)
            # Get user from Firestore
            user_data = db.collection('users').document(user.uid).get().to_dict()
            # Store user data in session
            session['user'] = {
                'uid': user.uid,
                'email': user_data['email'],
                'role': user_data['role']
            }
            # Redirect to admin panel if user is admin
            if user_data['role'] == ADMIN:
                return redirect(url_for('admin'))
            # Otherwise redirect to user dashboard
            return redirect(url_for('dashboard'))
        except auth.InvalidEmailError:
            return 'Invalid email'
        except auth.WrongPasswordError:
            return 'Wrong password'
        except auth.UserNotFoundError:
            return 'User not found'
    return render_template('login.html')

# Admin panel
@app.route('/admin')
@admin_required
def admin():
    # Get all users from Firestore
    users_ref = db.collection('users')
    users = [doc.to_dict() for doc in users_ref.stream()]
    return render_template('admin.html', users=users)

# Add user
@app.route('/admin/add_user', methods=['POST'])
@admin_required
def add_user():
    email = request.form['email']
    password = uuid.uuid4().hex
    # Create Firebase user
    user = auth.create_user(email=email, password=password)
    # Add user to Firestore
    db.collection('users').document(user.uid).set({
        'email': email,
        'role': USER
    })
    return redirect(url_for('admin'))


#Delete user
@app.route('/admin/delete_user/<uid>', methods=['POST'])
@admin_required
def delete_user(uid):
    # Delete user from Firebase and Firestore
    auth.delete_user(uid)
    db.collection('users').document(uid).delete()
    return redirect(url_for('admin'))

#User dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return 'User dashboard'

#Logout
@app.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if name == 'main':
    app.run(debug=True)