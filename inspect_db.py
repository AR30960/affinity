import sqlite3

conn = sqlite3.connect('affinity.db')
c = conn.cursor()
c.execute("SELECT sql FROM sqlite_master WHERE name='questions'")
print("TABLE questions DDL:")
print(c.fetchone()[0])

c.execute("SELECT count(*), classe, type FROM questions GROUP BY classe, type")
print("\nQuestions par classe et type:")
for row in c.fetchall():
    print(row)

conn.close()
