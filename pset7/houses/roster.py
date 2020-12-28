from cs50 import SQL
import sys
from sys import argv, exit
import csv
db = SQL("sqlite:///students.db")

if len(argv) !=2:
    print('usage: python roster.py "house"')
    exit(1)

choicehouse = argv[1]
selection = db.execute('SELECT first, middle, birth, last FROM students WHERE house = ? ORDER BY last, first', choicehouse);

for person in selection:
    if person['middle'] == None:
        print(f"{person['first']} {person['last']}, born {person['birth']}")
    else:
        print(f'{person["first"]} {person["middle"]} {person["last"]}, born {person["birth"]}')


