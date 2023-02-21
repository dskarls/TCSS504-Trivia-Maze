import csv
import sqlite3


def db_loader(filename, questions=None):
    print("Loading data into database...") # Added for testing
    # Open a connection to the database file
    conn = sqlite3.connect('Question_and_Answer_DB.sqlite')

    # Create a new table to hold the data
    # Commented out for testing
    conn.execute('''CREATE TABLE questions
                        (category TEXT, qa_type TEXT, difficulty TEXT, question TEXT, 
                         option_1 TEXT, option_2 TEXT, option_3 TEXT, option_4 TEXT,
                         correct_answer TEXT)''')
    # Mock list for testing
    """questions = [('General CS', 'Multiple Choice', 'Easy', 'What does the R RAM stand for?', 'Random', 'Rascal', 'Ruby',
                  'Robot', 'Random'),
                 ('General CS', 'True/False', 'Medium', 'Computers use electricity.', 'True', 'False', '', '', 'True'), (
                     'General CS', 'Short Answer', 'Hard',
                     'Elon Musks home planet is named __________.',
                     'Tralfamadore', '', '', '', 'Tralfamadoe')]              
    print(questions) # Added for testing"""
    for row in questions:
        query = 'INSERT INTO questions VALUES (?,?,?,?,?,?,?,?,?)'
        conn.execute(query, row)

    # Open the CSV file
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Skip the header row
        next(reader)
        # Insert each row into the database
        for row in reader:
            query = 'INSERT INTO questions VALUES (?,?,?,?,?,?,?,?,?)'
            conn.execute(query, row)

    # Commit the changes to the database and close the connection
    conn.commit()
    # conn.close() # Hashed out for testing

    # Verify that the questions table exists in the database
    try:
        conn.execute('SELECT * FROM questions')
        print("Table 'questions' exists")
    except sqlite3.Error as e:
        print(e)


db_loader('Lone_Rangers_QA_DB.csv')
