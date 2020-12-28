from cs50 import SQL
import sys
from sys import argv, exit
import csv
db = SQL("sqlite:///students.db")

#check for correct usage
if len(argv) != 2:
    print('usage: python import.py csvfile')
    exit(1)

database = csv.DictReader(open(sys.argv[1]))

for row in database:
    #divide full name into names
    splitname = row['name'].split()
    #check for middle name
    if len(splitname) == 3:
        firstname = splitname[0]
        middlename = splitname[1]
        lastname = splitname[2]
    else:
        firstname = splitname[0]
        middlename = None
        lastname = splitname[1]
    house = row['house']
    birth = row['birth']
    db.execute('INSERT INTO students (first, middle, last, house, birth) VALUES (?,?,?,?,?)',
    firstname, middlename, lastname, house, birth)
