#!/usr/bin/env python3

import random
from time import ctime

def init():
    wordbank= ["indentation", "spaces"]
    tlgstudents= ['Alex', 'Benji', 'Cayla', 'Demetra', 'Derek', 'Deshawn', 'James', 'Maria', 'Marylyn', 'Nor', 'Sal', 'Sammy']
    wordbank.append(4)
    return wordbank, tlgstudents

def get_input():
    num = input('Which studen are we talking about?\n>')
    num_strs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    is_int = False

    for num_str in num_strs:
        if num_str in num:
            num = int(num)
            is_int = True
            break
    
    return num, is_int

def find_student(students: list[str], id_val: any, id_type: bool) -> str:
    if id_type:
        if id_val > len(students) -1 or id_val < -1 * len(students):
            raise ValueError(f'{id_val} is out side of range ({-1 * len(students)}, {len(students) -1})')
        return students[id_val]
    if id_val in students:
        return students[students.index(id_val)]
    return id_val

def print_student(student: str, wordbank: list[any]):
    print(f'{student} always uses {wordbank[2]} {wordbank[1]} to indent.')

def rand_student(students: list[str]) -> str:
    random.seed(ctime())
    num = int((random.random()*100) % len(students))
    return students[num]

if __name__ == '__main__':
    wordbank, tlgstudents = init()
    num, is_int = get_input()
    student = find_student(tlgstudents, num, is_int)
    print_student(student, wordbank)
    student = rand_student(tlgstudents)
    print_student(student, wordbank)

