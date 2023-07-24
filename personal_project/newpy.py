#!/usr/bin/env python3

# Author: ChatGPT
# Created: July 2023
# Description: Python script generator with custom signature comments.

import os
import argparse

def load_signature_from_rc_file(user_override=None, contact_override=None):
    signature = ''
    rc_file_path = os.path.expanduser("~/.newpyrc")
    if not os.path.exists(rc_file_path):
        create_default_rc_file(rc_file_path)
    with open(rc_file_path, 'r') as rc_file:
        for line in rc_file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split(' ', 1)
            if key == "user":
                user_name = user_override if user_override else value.strip()
            elif key == "contact":
                contact_info = contact_override if contact_override else value.strip()
        signature = f"#{user_name}|{contact_info}"
    return signature

def create_default_rc_file(rc_file_path):
    default_content = '''# Configure user and contact for Python file signature
# Format:
# user {username}
# contact {contact}
#
# Example:
# user John Doe
# contact john.doe@example.com
#
# You can use this file to set the default signature for newly created Python files.
# To use the default, leave the fields blank when using the script.


'''

    with open(rc_file_path, 'w') as rc_file:
        rc_file.write(default_content)
    os.system(f'vim {rc_file_path}') 

def create_directory_if_not_exists(path):
    file_parent_dir = os.path.dirname(path)
    if not os.path.exists(file_parent_dir):
        os.system(f'mkdir -p {file_parent_dir}')

def create_python_file(path, user_override, contact_override):
    expanded_path = os.path.expanduser(os.path.normpath(path))
        
    if not expanded_path.endswith('.py'):
        expanded_path += '.py'
        
    signature = load_signature_from_rc_file(user_override, contact_override)

    file_content = f"""#! /usr/bin/env python3
{signature}

# Your Python code goes here

if __name__ == '__main__':
    # Your main code logic goes here
    pass

"""

    try:
        create_directory_if_not_exists(expanded_path)
        with open(expanded_path, 'w') as file:
            file.write(file_content)
        print(f"Python file created successfully at {expanded_path}")
        os.system(f'chmod u+x {expanded_path}')  # Set executable permissions
        os.system(f'vim {expanded_path}')       # Open the file with vim editor
    except IOError as e:
        print(f"An error occurred while creating the file: {e}")

def update_rc_file(user_override, contact_override):
    rc_file_path = os.path.expanduser("~/.newpyrc")

    with open(rc_file_path, 'r') as rc_file:
        lines = rc_file.readlines()

    with open(rc_file_path, 'w') as rc_file:
        for line in lines:
            if line != '' or line != '\n':
                if line.startswith('#'):
                    rc_file.write(line)
                    continue
                key, value = line.strip().split(' ', 1)
                if key == "user":
                    rc_file.write(f"user {user_override if user_override else value.strip()}\n")
                elif key == "contact":
                    rc_file.write(f"contact {contact_override if contact_override else value.strip()}\n")
                else:
                    rc_file.write(f'{key} {value}\n')

    print(f"Updated ~/.newpyrc with user: {user_override}, contact: {contact_override}")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Create a new Python file with custom signature comment.")
    parser.add_argument("path", nargs='?', type=str, help="Path where you want to create the Python file")
    parser.add_argument("-u", "--user", dest="user_override", type=str, help="Override the user name in the signature comment")
    parser.add_argument("-c", "--contact", dest="contact_override", type=str, help="Override the contact info in the signature comment")
    parser.add_argument("-o", "--update-rc", action="store_true", help="Update ~/.newpyrc with the signature overrides")
    args = parser.parse_args()

    if args.path:
        if args.update_rc:
            update_rc_file(args.user_override, args.contact_override)
        create_python_file(args.path, args.user_override, args.contact_override)
    else:
        if args.update_rc:
            update_rc_file(args.user_override, args.contact_override)
        else:
            print("Please provide a path to create the Python file or use the -h/--help option for more information.")

