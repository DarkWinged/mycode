#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

# app.py
import os
import json
from flask import Flask, render_template, request, redirect, url_for, session

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

if __name__ == '__main__':

    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Change this to a secure secret key

    data_base_path = os.path.expanduser('~/server_data')
    # Create data directory and logins.json file with default admin login if they don't exist
    if not os.path.exists(data_base_path):
        os.makedirs(f'{data_base_path}/logins.json')

    if not os.path.exists(data_base_path):
        default_admin_login = {
            "admin": "password"
        }
        with open(data_file_path, 'w') as f:
            json.dump(default_admin_login, f)

    data_controller = DataController(f'{data_base_path}/logins.json')


    @app.route('/', methods=['GET'])
    def index():
        if 'username' in session.keys():
            username = session['username']
            return render_template('index.html', title_text = 'Flask Game!', username=username)
        else:
            return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = {
            'title': 'Flask Game!',
            'fields': [
                {'label': 'Username:', 'name': 'username', 'type': 'text'},
                {'label': 'Password:', 'name': 'password', 'type': 'password'}
            ],
            'switch_text': 'Need an account? Signup here!',
            'switch_route': 'signup',
            'button_text': 'Login'
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
            'title': 'Flask Game!',
            'fields': [
                {'label': 'New Username:', 'name': 'new_username', 'type': 'text'},
                {'label': 'New Password:', 'name': 'new_password', 'type': 'password'},
                {'label': 'Confirm Password:', 'name': 'confirm_password', 'type': 'password'}
            ],
            'button_text': 'Sign Up',
            'switch_text': 'Already have an account?',
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


    app.run(host='0.0.0.0', port=2224, debug=True)

