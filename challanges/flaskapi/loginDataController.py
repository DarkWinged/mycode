import os
import json
from peewee import *

db = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(primary_key=True)
    password = CharField()

class Permission(BaseModel):
    name = CharField(unique=True)

class UserPermission(BaseModel):
    user = ForeignKeyField(User, backref='user_permissions')
    permission = ForeignKeyField(Permission, backref='users')

class LoginDataController:
    def __init__(self, db_path: str):
        db.init(db_path)
        self._create_tables()
        self._initialize_permissions()
        self._initialize_admin_user()

    def _create_tables(self):
        with db:
            db.create_tables([User, Permission, UserPermission])

    def _initialize_permissions(self):
        predefined_permissions = ['user', 'moderator', 'admin']
        with db:
            for permission in predefined_permissions:
                Permission.get_or_create(name=permission)

    def _initialize_admin_user(self):
        admin_username = 'admin'
        admin_password = 'changeme'
        admin_permissions = ['admin']

        try:
            user = User.get(User.username == admin_username)
        except User.DoesNotExist:
            with db:
                user = User.create(username=admin_username, password=admin_password)
                for permission in admin_permissions:
                    permission_obj, _ = Permission.get_or_create(name=permission)
                    UserPermission.get_or_create(user=user, permission=permission_obj)

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
        try:
            user = User.get(User.username == username)
            return user.password == password
        except User.DoesNotExist:
            return False

    def add_new_account(self, new_username: str, new_password: str, confirm_password: str) -> tuple[bool, str]:
        try:
            User.get(User.username == new_username)
            return False, 'Username already in use!'
        except User.DoesNotExist:
            if new_password == confirm_password:
                with db:
                    user = User.create(username=new_username, password=new_password)
                    permission_obj, _ = Permission.get_or_create(name='user')
                    UserPermission.create(user=user, permission=permission_obj)
                return True, ''
            else:
                return False, 'Passwords do not match!'

    def change_password(self, username: str, new_password: str, confirm_password: str) -> tuple[bool, str]:
        if new_password == confirm_password:
            try:
                user = User.get(User.username == username)
                with db:
                    user.password = new_password
                    user.save()
                return True, 'Password changed successfully!'
            except User.DoesNotExist:
                return False, 'User not found!'
        else:
            return False, 'Passwords do not match!'

    def user_has_permission(self, username: str, permission: str) -> bool:
        try:
            user = User.get(User.username == username)
            permission_obj = Permission.get(Permission.name == permission)
            return UserPermission.select().where(UserPermission.user == user, UserPermission.permission == permission_obj).exists()
        except User.DoesNotExist:
            return False

    def get_usernames(self):
        with db:
            return [user.username for user in User.select()]

    def reset_user_password(self, admin_username: str, admin_password: str, new_password: str, confirm_password: str, username: str) -> bool:
        if self.validate_user_credentials(admin_username, admin_password):
            try:
                user = User.get(User.username == username)
                if new_password == confirm_password:
                    with db:
                        user.password = new_password
                        user.save()
                    return True
            except User.DoesNotExist:
                pass
        return False

    def _add_permission(self, username: str, permission: str) -> bool:
        try:
            user = User.get(User.username == username)
            permission_obj, _ = Permission.get_or_create(name=permission)
            with db:
                UserPermission.create(user=user, permission=permission_obj)
            return True
        except User.DoesNotExist:
            return False

    def _remove_permission(self, username: str, permission: str) -> bool:
        try:
            user = User.get(User.username == username)
            permission_obj = Permission.get(Permission.name == permission)
            with db:
                UserPermission.delete().where(UserPermission.user == user, UserPermission.permission == permission_obj).execute()
            return True
        except User.DoesNotExist:
            return False

    def set_user_permissions(self, admin_username: str, admin_password: str, action: str, permission: str, username: str) -> bool:
        if self.validate_user_credentials(admin_username, admin_password):
            if action == 'add':
                return self._add_permission(username, permission)
            elif action == 'remove':
                return self._remove_permission(username, permission)
        return False

