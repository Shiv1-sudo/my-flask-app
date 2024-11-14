from flask import Flask, render_template, request, redirect, url_for,flash
import webbrowser
import threading
import os #using  environment variables for secert key & sensitive data
from werkzeug.security import generate_password_hash,check_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from wtforms import Form, StringField,PasswordField
from wtforms.validators import InputRequired


app = Flask(__name__)
app.secret_key=os.getenv('SECRET_KEY','default_secret_key')#Environment variables   
#app.secret_key= 'your_secret_key' # Required for flash messages

csrf = CSRFProtect(app)
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

# Secure user credentials with hashed passwords
users = {
    'user1': generate_password_hash('password1'),
    'user2': generate_password_hash('password2')
}

# Dummy user credentials 

users = { 'user1': 'password1', 'user2': 'password2' }

@app.route('/')
def home():
    return render_template('index.html')
#Access homepage use url ('http://127.0.0.1:5000/')
def open_browser():
    #webbrowser.open_new('http://127.0.0.1:5000/')
    webbrowser.open_new('http://127.0.0.1:5000/login')

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Rate limiting
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        if username in users and check_password_hash(users[username], password):
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

class LoginForm(Form):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

if __name__ == '__main__':
    threading.Timer(2, open_browser).start()
    app.run(debug=True)





    

"""@app.route('/login', methods=['GET', 'POST']) 
def login(): 
    if request.method == 'POST': 
        username = request.form['username'] 
        password = request.form['password'] 
        if username in users and users[username] == password: 
            return redirect(url_for('home')) 
        else: 
            flash('Invalid credentials. Please try again.') 
            return redirect(url_for('login')) 
    return render_template('login.html')

#Access the Login Page: Open your web browser and go to http://127.0.0.1:5000/login.

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/login')

if __name__ == '__main__':
    threading.Timer(2,open_browser).start()
    app.run(debug=True)"""
