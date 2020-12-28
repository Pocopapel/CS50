import sys
import copy
import csv
from sys import argv, exit

# check for correct usage
if (len(argv) != 3):
    print("usage: python database dnafile")
    exit(1)

# read the dna file into dnaseq
with open(argv[2]) as f:
    dnaseq = f.read()

# read the database into dnadata
dnadata = csv.DictReader(open(sys.argv[1]))

# create dna dict with the count of seqs
dna = {}
headers = dnadata.fieldnames
keycount = 0
for key in headers:
    if key != 'name':
        dna.update({key: 0})
        keycount += 1

# for each seperate STR reset the ounts
for str in dna:
    seqsize = len(str)
    highcount = 0
    tmpcount = 0
    for i in range(len(dnaseq)):
        # check if a sequence is the same as the str
        if dnaseq[i: i + seqsize] == str:
            # reset the counter to 1 (for the first hit)
            tmpcount = 1
            # while each sequence is equal to the previous and doesnt go out of bounds of the sequence
            while dnaseq[i - seqsize: i] == dnaseq[i: i + seqsize] and i < len(dnaseq):
                tmpcount += 1
                i += seqsize
            # adapt counter if tmp counter is higher
            if tmpcount > highcount:
                highcount = tmpcount

    # update the dict with the highcount
    dna[str] = highcount

# get a counter for the strs found and a bool to make sure if at the end its still not found it prints no match
check = False
found = 0
for row in dnadata:
    for str in dna:
        if dna[str] == int(row[str]):
            found += 1
        else:
            found = 0
            continue

    # if all  strs are found, print the match
    if found == keycount:
        print(row['name'])
        exit(0)

# if program hasnt exitted, no match was found
print("no match")