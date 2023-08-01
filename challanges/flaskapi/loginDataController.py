#James L. Rogers|github.com/DarkWinged

import json
import os

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
        if username in self._data.keys():
            return self._data.get(username)['password'] == password
        else:
            return False

    def add_new_account(self, new_username: str, new_password: str, confirm_password: str) -> tuple[bool, str]:
        if new_username in self._data.keys():
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

    def reset_user_password(self, admin_username: str, admin_password: str, new_password: str, confirm_password: str, username: str) -> bool:
        # Check if the admin password is valid
        if not self.validate_user_credentials(admin_username, admin_password):
            return False

        # Check if new password and confirm password are the same
        if new_password != confirm_password:
            return False

        # Here, you can perform any additional checks or validations as needed before changing the password

        # Update the user's password to the new one
        if self._data.get(username):
            self._data[username]['password'] = new_password
            self._save_data()
            return True

        return False
    
    def _add_permission(self, username: str, permission: str) -> bool:
        if permission in self._data[username]['permissions']:
            return True
        else:
            self._data[username]['permissions'].append(permission)
            self._save_data()
            return True
        return False
   
    def _remove_permission(self, username: str, permission: str) -> bool:
        if permission not in self._data[username]['permissions']:
            return True
        else:
            self._data[username]['permissions'].pop(self._data[username]['permissions'].index(permission))
            self._save_data()
            return True
        return False

    def set_user_permissions(self, admin_username: str, admin_password: str, action: str, permission: str, username: str) -> bool:
        # Check if the admin password is valid
        if not self.validate_user_credentials(admin_username, admin_password):
            return False
        
        if action == 'add':
            return self._add_permission(username, permission)
        
        if action == 'remove':
            return self._remove_permission(username, permission)
