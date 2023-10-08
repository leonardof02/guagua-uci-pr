import sqlite3

with sqlite3.connect("guaguaPR.db") as connection:
    db = connection.cursor()