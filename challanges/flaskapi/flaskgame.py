#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

# app.py
import os
import json
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

data_dir = os.path.expanduser('~/server_data')
data_file_path = os.path.join(data_dir, 'logins.json')

# Create data directory and logins.json file with default admin login if they don't exist
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if not os.path.exists(data_file_path):
    default_admin_login = {
        "admin": "password"
    }
    with open(data_file_path, 'w') as f:
        json.dump(default_admin_login, f)

class DataController:
    def __init__(self, file_path):
        self._file_path = file_path
        self._data = self._load_data()

    def _load_data(self):
        if os.path.exists(self._file_path):
            with open(self._file_path, 'r') as f:
                return json.load(f)
        else:
            return {}

    def _save_data(self):
        with open(self._file_path, 'w') as f:
            json.dump(self._data, f)

    def validate_user_credentials(self, username, password):
        return self._data.get(username) == password

    def add_new_account(self, new_username, new_password, confirm_password):
        if new_username in self._data:
            return False

        if new_password == confirm_password:
            self._data[new_username] = new_password
            self._save_data()
            return True

        return False

data_controller = DataController(data_file_path)

def is_user_logged_in():
    return 'username' in session

@app.route('/', methods=['GET'])
def index():
    if is_user_logged_in():
        username = session['username']
        return render_template('index.html', username=username)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = {
        'title': 'Login',
        'fields': [
            {'label': 'Username:', 'name': 'username', 'type': 'text', 'required': True},
            {'label': 'Password:', 'name': 'password', 'type': 'password', 'required': True}
        ],
        'button_text': 'Login',
        'switch_text': 'Sign Up',
        'switch_route': 'signup'
    }

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if data_controller.validate_user_credentials(username, password):
            session['username'] = username  # Store username in session
            return redirect(url_for('index'))
        else:
            return render_template('login_signup.html', form=form, message="Invalid credentials. Please try again.")

    return render_template('login_signup.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = {
        'title': 'Sign Up',
        'fields': [
            {'label': 'New Username:', 'name': 'new_username', 'type': 'text', 'required': True},
            {'label': 'New Password:', 'name': 'new_password', 'type': 'password', 'required': True},
            {'label': 'Confirm Password:', 'name': 'confirm_password', 'type': 'password', 'required': True}
        ],
        'button_text': 'Sign Up',
        'switch_text': 'Login',
        'switch_route': 'login'
    }

    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if data_controller.add_new_account(new_username, new_password, confirm_password):
            return redirect(url_for('login'))
        else:
            return render_template('login_signup.html', form=form, message="Failed to create an account. Please try again.")

    return render_template('login_signup.html', form=form)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2224, debug=True)


