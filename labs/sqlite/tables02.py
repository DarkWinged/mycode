#!/usr/bin/env python3
"""J. Hutcheson | creating tables in SQLite"""

import sqlite3

# Create a connection to a new SQLite database
conn = sqlite3.connect('my_database.db')

# Create a cursor object to execute SQL commands
c = conn.cursor()

# Create the companies table with columns for Company ID and Company Name
c.execute('''CREATE TABLE IF NOT EXISTS companies
             (id INTEGER PRIMARY KEY,
              name TEXT)''')

# Create the companies table with columns for Company ID and Company Name
c.execute('''CREATE TABLE IF NOT EXISTS products
             (id INTEGER PRIMARY KEY,
              name TEXT,
              company_id INTEGER REFERENCES companies(id))''')

# Insert some example data into the companies table
c.execute("INSERT INTO companies (id, name) VALUES (1, 'Acme Inc.')")
c.execute("INSERT INTO companies (id, name) VALUES (2, 'XYZ Corp')")
#c.execute("INSERT INTO companies (id, name) VALUES (3, 'Apple Inc.')")
#c.execute("INSERT INTO companies (id, name) VALUES (4, 'Samsung Electronics')")
#c.execute("INSERT INTO companies (id, name) VALUES (5, 'Toyota Motor Corporation')")
#c.execute("INSERT INTO companies (id, name) VALUES (6, 'Google LLC')")

c.execute("INSERT INTO products (id, name, company_id) VALUES (1, 'Widget', 1)")
c.execute("INSERT INTO products (id, name, company_id) VALUES (2, 'Gizmo', 2)")
c.execute("INSERT INTO products (id, name, company_id) VALUES (3, 'Thingamajig', 1)")
c.execute("INSERT INTO products (id, name, company_id) VALUES (4, 'Doohickey', 2)")
c.execute("INSERT INTO products (id, name, company_id) VALUES (5, 'Whatchamacallit', 1)")
c.execute("INSERT INTO products (id, name, company_id) VALUES (6, 'gadget', 2)")
c.execute("INSERT INTO products (id, name, company_id) VALUES (7, 'gizmometer', 2)")
c.execute("INSERT INTO products (id, name, company_id) VALUES (8, 'doohicky 2', 1)")
c.execute("INSERT INTO products (id, name, company_id) VALUES (9, 'thingamajig 2', 1)")
c.execute("INSERT INTO products (id, name, company_id) VALUES (10, 'widget pro', 1)")

# Commit changes and close the connection
conn.commit()
conn.close()

