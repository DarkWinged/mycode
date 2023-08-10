#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

from flask import Flask, render_template, url_for
import csv
import os

if __name__ == '__main__':
 
    csv_file_path = os.path.join(os.path.dirname(__file__), 'static', 'emails.csv')

    email_data = []

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            email_data.append(row)

    app = Flask(__name__)
    app.secret_key = 'Foobar Borsef'

    @app.route('/email')
    def index():
        return render_template('index.html', emails=email_data)

    app.run(host='0.0.0.0', port=9002, debug=True)

