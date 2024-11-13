from flask import Flask, render_template, request, redirect, url_for,flash
import webbrowser
import threading

app = Flask(__name__)
app.secret_key= 'your_secret_key' # Required for flash messages

# Dummy user credentials 

users = { 'user1': 'password1', 'user2': 'password2' }

@app.route('/')
def home():
    return render_template('index.html')
#Access homepage use url ('http://127.0.0.1:5000/')
def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

@app.route('/login', methods=['GET', 'POST']) 
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
    app.run(debug=True)
