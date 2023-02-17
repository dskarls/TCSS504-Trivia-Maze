import csv


"""
Take a csv file of question and answer data and write the data to a .txt file
"""
# Open the input file
with open('Lone Rangers QA DB.csv', 'r') as input_file:
    reader = csv.reader(input_file)

    # Open the output file
    with open('LoneRangersQA_DB.txt', 'w') as output_file:
        # Loop through each row in the input file
        for row in reader:
            # Join the columns in the row with a comma separator
            line = ','.join(row)
            # Write the line to the output file
            output_file.write(line + '\n')



import csv
import sqlite3

"""
Take a csv file of question and answer data and import it to a SQLite database
"""

# Open a connection to the database file
connection = sqlite3.connect('Question_and_Answer_DB.db')

# Create a new table to hold the data
connection.execute('''CREATE TABLE IF NOT EXISTS questions
                (category TEXT, type TEXT, difficulty TEXT, question TEXT, 
                 option_1 TEXT, option_2 TEXT, option_3 TEXT, option_4 TEXT,
                 answer TEXT, hint TEXT)''')

# Open the CSV file
with open('Lone Rangers QA DB.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    # Skip the header row
    next(reader)
    # Insert each row into the database
    for row in reader:
        query = "INSERT INTO questions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        connection.execute(query, row)

# Commit the changes to the database and close the connection
connection.commit()
connection.close()

