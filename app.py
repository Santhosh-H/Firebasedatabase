from flask import Flask, request, render_template, redirect
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)

# Firebase Admin SDK initialization
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
  "apiKey": "AIzaSyAtmsy6n_5JfOj1VgdasvGNnE1L6T5hE2Q",
  "authDomain": "test-653fc.firebaseapp.com",
  "projectId": "test-653fc",
  "storageBucket": "test-653fc.appspot.com",
  "messagingSenderId": "703564637211",
  "appId": "1:703564637211:web:258c0ca9bb8a247c9784be",
  "measurementId": "G-WTRTPXHP85"
})

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
        except Exception as e:
            print(e)
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
