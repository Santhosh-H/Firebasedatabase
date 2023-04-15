from flask import Flask, request, render_template, redirect
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)

# Firebase Admin SDK initialization
cred = credentials.Certificate('static/key.json')
firebase_admin.initialize_app(cred)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            return redirect('/login')
        except:
            error = "Unable to create account. Please try again."
            return render_template('signup.html', error=error)
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.get_user_by_email(email)
            auth.sign_in_with_email_and_password(email, password)
            return redirect('/dashboard')
        except:
            error = "Invalid email or password. Please try again."
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
