#!/usr/bin/env python3

# Signature: 
# Author: ChatGPT
# Created: July 2023
# Description: Test script for main_script.py with various options.

"""
comment out line 61 of ../newpy.py before testing
"""

import os
import subprocess

def run_test(args):
    print(f"Running test: python3 ../newpy.py {' '.join(args)}")
    try:
        call = ["python3", "../newpy.py"]
        call.extend(args)
        output = subprocess.check_output(call, stderr=subprocess.STDOUT)
        print(output.decode("utf-8"))
    except subprocess.CalledProcessError as e:
        print(e.output.decode("utf-8"))

def run_tests():
    print('Test case 1: Create a Python file with default signature')
    run_test(["tests/test_file.py"])
    
    print('Test case 2: Create a Python file with custom signature')
    run_test(["tests/test_file_custom.py", "-u", "John Doe", "-c", "johndoe@example.com"])
    
    print('Test case 3: Update ~/.newpyrc with custom user and contact')
    run_test(["-o", "-u", "Jane Doe", "-c", "janedoe@example.com"])
    
    print('Test case 4: Update ~/.newpyrc with custom user only')
    run_test(["-o", "-u", "Alice Smith"])
    
    print('Test case 5: Update ~/.newpyrc with custom contact only')
    run_test(["-o", "-c", "asmith@example.com"])
    
    print('Test case 6: Update ~/.newpyrc with invalid option (should prompt to provide at least one override)')
    run_test(["-o"])
    
    print('Test case 7: Invalid option (should print usage message)')
    run_test(["-x"])
    
    print('Test case 8: Invalid file path (should handle invalid path gracefully)')
    run_test(["tests/invalid_folder/test_file.py"])
    
    print('Test case 9: Create a Python file with custom signature using short options')
    run_test(["tests/short_options_file.py", "-u", "John Smith", "-c", "jsmith@example.com"])
    
    print('Test case 10: Update ~/.newpyrc with custom user and contact using short options')
    run_test(["-o", "-u", "Jane Smith", "-c", "janesmith@example.com"])
    
    print('Test case 11: Update ~/.newpyrc with custom user only using short options')
    run_test(["-o", "-u", "Alice Johnson"])
    
    print('Test case 12: Update ~/.newpyrc with custom contact only using short options')
    run_test(["-o", "-c", "ajohnson@example.com"])
    
    print('Test case 13: Update ~/.newpyrc with invalid option using short options (should prompt to provide at least one override)')
    run_test(["-o"])
    
    print('Test case 14: Invalid option using short options (should print usage message)')
    run_test(["-x"])
    
    print('Test case 15: Invalid file path using short options (should handle invalid path gracefully)')
    run_test(["tests/invalid_folder/test_file.py"])

if __name__ == '__main__':
    run_tests()

