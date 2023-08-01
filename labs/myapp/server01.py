#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

#!/usr/bin/python3
"""RZFeeser || Alta3 Research
Tracking student inventory within a sqliteDB accessed
via Flask APIs"""

# standard library
import sqlite3 as sql

# python3 -m pip install flask
from flask import Flask
from flask import render_template
from flask import request, redirect

app = Flask(__name__)

# return home.html (landing page)
@app.route('/')
def home():
    return render_template('home.html')

# return student.html (a way to add a student to our sqliteDB)
@app.route('/enternew')
def new_student():
    return render_template('student.html')

# if someone uses student.html it will generate a POST
# this post will be sent to /addrec
# where the information will be added to the sqliteDB
@app.route('/addrec',methods = ['POST'])
def addrec():
    try:
        nm = request.form['nm']         # student name
        addr = request.form['addr']     # student street address
        city = request.form['city']     # student city
        pin = request.form['pin']       # "pin" assigned to student
                                        # ("pin" is just an example of meta data we want to track)

        # connect to sqliteDB
        with sql.connect("database.db") as con:
            cur = con.cursor()

            # place the info from our form into the sqliteDB
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            # commit the transaction to our sqliteDB
            con.commit()
        # if we have made it this far, the record was successfully added to the DB
        msg = "Record successfully added"
        
    except:
        con.rollback()  # this is the opposite of a commit()
        msg = "error in insert operation"    # we were NOT successful

    finally:
        con.close()     # successful or not, close the connection to sqliteDB
        return render_template("result.html",msg = msg)    #

# return all entries from our sqliteDB as HTML
@app.route('/list')
def list_students():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("SELECT * from students")           # pull all information from the table "students"
    
    rows = cur.fetchall()
    return render_template("list.html",rows = rows) # return all of the sqliteDB info as HTML

@app.route('/search')
def search():
    search = request.args.get('name', default='', type=str)
    with sql.connect('database.db') as con:
        con.row_factory = sql.Row

        query = f'SELECT * FROM students WHERE name LIKE \'%{search}%\''
        cur = con.cursor()
        cur.execute(query)
        return render_template('search.html', rows = cur.fetchall())

@app.route('/search/<name>')
def search_name(name):
    with sql.connect('database.db') as con:
        con.row_factory = sql.Row

        query = f'SELECT * FROM students WHERE name = \'{name}\''
        cur = con.cursor()
        cur.execute(query)
        return render_template('search_name.html', rows = cur.fetchall())

@app.route('/update', methods=['POST'])
def update():
    name = request.form.get('name', default='', type=str)
    address = request.form.get('address', default='', type=str)
    city = request.form.get('city', default='', type=str)
    pcode = request.form.get('pcode', default='', type=str)
    with sql.connect('database.db') as con:
        con.row_factory = sql.Row

        query = f"UPDATE students SET addr = '{address}', city = '{city}', pin = '{pcode}' WHERE name = '{name}'"
        cur = con.cursor()
        con.execute(query)
        con.commit()
        return redirect(f'{request.base_url.removesuffix("update")}search/{name}')

@app.route('/delete/<name>')
def delete_name(name):
    with sql.connect('database.db') as con:
        query = f"DELETE FROM students WHERE name = '{name}'"
        con.execute(query)
        con.commit()
        return redirect(f'{request.base_url.removesuffix(f"delete/{name}")}search')

if __name__ == '__main__':
    try:
        # ensure the sqliteDB is created
        con = sql.connect('database.db')
        print("Opened database successfully")
        # ensure that the table students is ready to be written to
        con.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
        print("Table created successfully")
        con.close()
        # begin Flask Application 
        app.run(host="0.0.0.0", port=2224, debug = True)
    except:
        print("App failed on boot")

