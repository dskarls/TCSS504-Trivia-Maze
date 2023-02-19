import csv
import sqlite3

"""
Take a csv file of question and answer data and import it to a SQLite database
"""

# Open a connection to the database file
connection = sqlite3.connect('Question_and_Answer_DB.sqlite')

# Create a new table to hold the data
connection.execute('''CREATE TABLE IF NOT EXISTS questions
                (question_id INTEGER , category TEXT, qa_type TEXT, difficulty TEXT, question TEXT, 
                 option_1 TEXT, option_2 TEXT, option_3 TEXT, option_4 TEXT,
                 answer TEXT, hint TEXT)''')

# Open the CSV file
with open('Lone_Rangers_QA_DB.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    # Skip the header row
    next(reader)
    # Insert each row into the database
    for row in reader:
        query = 'INSERT INTO questions VALUES (?,?,?,?,?,?,?,?,?,?,?)'
        connection.execute(query, row)

# Commit the changes to the database and close the connection
connection.commit()
connection.close()


