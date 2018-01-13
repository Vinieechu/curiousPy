import re
import sqlite3

conn = sqlite3.connect('emaildbass.sqlite') #this one makes a file
cur = conn.cursor() #is very similar conceptually to calling open() when dealing with text ﬁles.

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox-short.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]
    parts = email.split('@')
    org = parts[1]
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,)) # We specify the values as question marks (?, ?) to indicate that the actual values are passed in as a tuple
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))
    conn.commit()
sqlstr = 'SELECT * FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
