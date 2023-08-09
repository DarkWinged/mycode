#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

import sqlite3

conn = sqlite3.connect('my_database3.db')

c = conn.cursor()

c.execute("""SELECT students.name FROM students""")

student_list = [student[0] for student in c.fetchall()]

while True:
    [print(student) for student in student_list]
    student_name = input('Enter the name of a student to see their courses:\n>>').capitalize()
    if student_name in student_list:
        break

c.execute('''
    SELECT courses.name
    FROM courses
    JOIN student_courses ON courses.id = student_courses.course_id
    JOIN students ON students.id = student_courses.student_id
    WHERE students.name = ?''', (student_name,))

courses = c.fetchall()
print(f"{student_name} is taking the following courses:")
for course in courses:
    print(course[0])

conn.close()

