#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

# app.py
import os
import json
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, request, make_response
import requests

class LoginDataController:
    def __init__(self, file_path: str):
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

    def validate_user_credentials(self, username: str, password: str) -> bool:
        return self._data.get(username)['password'] == password

    def add_new_account(self, new_username: str, new_password: str, confirm_password: str) -> tuple[bool, str]:
        if new_username in self._data:
            return False, 'Username already in use!'

        if new_password == confirm_password:
            self._data[new_username] = {
                    'password': new_password,
                    'permissions': []
                    }
            self._save_data()
            return True , ''

        return False, 'Passwords do not match!'

    def change_password(self, username: str, new_password: str, confirm_password: str) -> tuple[bool, str]:
        if new_password == confirm_password:
            if username in self._data:
                self._data[username]['password'] = new_password
                self._save_data()
                return True, 'Password changed successfully!'
            else:
                return False, 'User not found!'
        else:
            return False, 'Passwords do not match!'

    def user_has_permission(self, username: str, permission: str) -> bool:
        if username in self._data.keys():
            return permission in self._data[username]['permissions']
        else:
            return False


    def get_usernames(self):
        return list(self._data.keys())

if __name__ == '__main__':

    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Change this to a secure secret key
    app.permanent_session_lifetime = timedelta(minutes=15)

    data_base_path = os.path.expanduser('~/server_data')

    # Create data directory and logins.json file with default admin login if they don't exist
    if not os.path.exists(data_base_path):
        os.makedirs(f'{data_base_path}/logins.json')

    if not os.path.exists(f'{data_base_path}/logins.json'):
        default_admin_login = {
                "admin": {
                    "password": "changeme",
                    "permissions": ["admin"]
                }
        }
        with open(f'{data_base_path}/logins.json', 'w') as f:
            json.dump(default_admin_login, f)
    

    login_data_controller = LoginDataController(f'{data_base_path}/logins.json')
    
    @app.before_request
    def before_request():
        login_pages = ['login', 'signup']

        if 'username' in session:
            if request.endpoint in login_pages:
                return redirect('/')
            elif request.endpoint == 'admin':
                if not login_data_controller.user_has_permission(session['username'], 'admin'):
                    return redirect(url_for('index'))
        else:
            if request.endpoint not in login_pages:
                return redirect(url_for('login'))
   
    @app.route('/', methods=['GET'])
    def index():
        username = session['username']
        return render_template('index.html', title_text = 'Flask Game', username=username)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = {
            'title': 'Flask Game',
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

            if login_data_controller.validate_user_credentials(username, password):
                session['username'] = username  # Store username in session
                session['permissions'] = {}
                if login_data_controller.user_has_permission(username, 'admin'):
                    session['permissions']['admin'] = True
                return redirect(url_for('index'))
            else:
                return render_template('login_signup.html', form=form, message="Invalid credentials. Please try again.")

        return render_template('login_signup.html', form=form)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        form = {
            'title': 'Flask Game',
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

            attempt , message = login_data_controller.add_new_account(new_username, new_password, confirm_password)
            if attempt:
                return redirect(url_for('login'))
            else:
                return render_template('login_signup.html', form=form, message=f"{message} Please try again.")

        return render_template('login_signup.html', form=form)

    @app.route('/logout', methods=['POST'])
    def logout():
        session.clear()
        
        # Clear cookies used in /admin/users route
        response = redirect(url_for('login'))
        response.delete_cookie('search')
        response.delete_cookie('limit')
        response.delete_cookie('offset')

        return response
    

    @app.route('/account_settings', methods=['GET', 'POST'])
    def account_settings():
        if 'username' not in session:
            return redirect(url_for('login'))

        if request.method == 'POST':
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            username = session['username']
            if login_data_controller.validate_user_credentials(username, current_password):
                success, message = login_data_controller.change_password(username, new_password, confirm_password)
                if success:
                    return render_template('account_settings.html', message=message, username=username)
                else:
                    return render_template('account_settings.html', error=message, username=username)
            else:
                return render_template('account_settings.html', error='Invalid current password', username=username)

        username = session['username']
        return render_template('account_settings.html', username=username)

    @app.route('/users', methods=['GET'])
    def users(name='', limit=5, offset=0):
        limit = request.args.get('limit', default=5, type=int)
        offset = request.args.get('offset', default=0, type=int)
        name = request.args.get('name', default='', type=str)
        print(name)
        # Get the list of all usernames
        all_usernames = login_data_controller.get_usernames()

        # Filter usernames based on the name query (case-insensitive)
        filtered_usernames = [username for username in all_usernames if name.lower() in username.lower()]

        # Calculate the total number of users that passed the name filter
        total_filtered_users = len(filtered_usernames)

        # Apply the limit and offset to the filtered usernames
        filtered_usernames = filtered_usernames[offset:offset + limit]

        response_data = {
            'filtered_usernames': filtered_usernames,
            'total_filtered_users': total_filtered_users
        }

        return jsonify(response_data)

    @app.route('/admin', methods=['GET'])
    def admin():
        return render_template('admin.html')

    def get_filtered_users_data(current_search, limit, current_offset):
        # Get the filtered user data using the LoginDataController
        all_usernames = login_data_controller.get_usernames()
        filtered_usernames = [username for username in all_usernames if current_search.lower() in username.lower()]
        total_filtered_users = len(filtered_usernames)
        max_offset = max(0, total_filtered_users - limit)

        # Apply offset and limit to the filtered user data
        filtered_usernames = filtered_usernames[current_offset : current_offset + limit]

        return filtered_usernames, total_filtered_users, max_offset


    def render_admin_users_template(filtered_usernames, total_filtered_users, current_search, limit, current_offset, max_offset):
        # Render the template with the data
        response = make_response(render_template('admin_users.html',
                                                  filtered_usernames=filtered_usernames,
                                                  total_filtered_users=total_filtered_users,
                                                  current_search=current_search,
                                                  limit=limit,
                                                  current_offset=current_offset,
                                                  max_offset=max_offset))

        # Set cookies for the current search, limit, and offset values
        response.set_cookie('search', current_search)
        response.set_cookie('limit', str(limit))
        response.set_cookie('offset', str(current_offset))

        return response

    @app.route('/admin/users', methods=['GET', 'POST'])
    def admin_users():
        if request.method == 'POST':
            # Get the search query from the form submission
            current_search = request.form.get('search', '')

            # Get the limit value from the selected option in the dropdown
            limit = int(request.form.get('limit', 5))

            # Get the offset value from the selected option in the pagination
            current_offset = int(request.form.get('offset', 0))

            # Get the filtered users data using the helper function
            filtered_usernames, total_filtered_users, max_offset = get_filtered_users_data(current_search, limit, current_offset)

            # Render the template and set cookies using the helper function
            return render_admin_users_template(filtered_usernames, total_filtered_users, current_search, limit, current_offset, max_offset)

        elif request.method == 'GET':
            # Get the values from cookies or set default values
            current_search = request.cookies.get('search', '')
            limit = int(request.cookies.get('limit', 5))
            current_offset = int(request.cookies.get('offset', 0))

            # Get the filtered users data using the helper function
            filtered_usernames, total_filtered_users, max_offset = get_filtered_users_data(current_search, limit, current_offset)

            # Render the template and set cookies using the helper function
            return render_admin_users_template(filtered_usernames, total_filtered_users, current_search, limit, current_offset, max_offset)


    app.run(host='0.0.0.0', port=2224, debug=True)

