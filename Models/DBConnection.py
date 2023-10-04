import sqlite3
from typing import Tuple

with sqlite3.connect("guaguaPR.db") as connection:
    db = connection.cursor()