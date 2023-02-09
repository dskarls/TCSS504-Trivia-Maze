import sqlite3

connection_string = sqlite3.connect(qa_true_false.db, qa_multiple_choice.db, qa_short_answer.db)
cursor = connection_string.cursor()

cursor.execute("create table qa_true_false (question_id text, difficulty text, category text, question text, answer text, hint text")
true_and_false = [
    ("1001", "easy", "general cs", "Computer science is not the study of the theory and application of computers.", "false", "Hint 1"),
    ("1002", "easy", "general cs", "The first electronic computer was created in the 17th century.", "false", "Hint 2"),
    ("1003", "medium", "general cs", "A Turing machine is a theoretical model of a general-purpose computer that can perform any calculation that is algorithmically solvable.", "true", "Hint 1003"),
    ("1004", "medium", "general cs", "Von Neumann architecture is a design model for computers that separates the memory and processing units.", "true", "Hint 1004"),
    ("1005", "hard", "general cs", "The P vs NP problem is a computational problem that asks whether every problem whose solution can be verified in polynomial time, can also be solved in polynomial time.", "true", "Hint 1005"),
    ("1006", "hard", "general cs", "The Halting problem is a problem that asks whether, given a description of an arbitrary computer program, it is possible to decide whether the program finishes running or continues running forever.", "true", "Hint 1006"),
]

cursor.execute("create table qa_multiple_choice (question_id text, difficulty text, category text, question text, answer text, hint text")
multiple_choice = [
    ("2001", "easy", "general cs", "Which of the following is not a type of computer memory? a) RAM b) ROM c) CPU d) HDD", "c", "Hint 2001"),
    ("2002", "easy", "general cs", "Which of the following is not a type of computer network? a) LAN b) WAN c) PAN d) SAN", "d", "Hint 2002"),
    ("2003", "medium", "general cs", "Which of the following is not a type of software? a) System software b) Application software c) Hardware software d) Firmware", "c", "Hint 2003"),
    ("2004", "medium", "general cs", "Which of the following is not a type of computer language? a) Assembly b) High-level c) Low-level d) Database", "d", "Hint 2004"),
    ("2005", "hard", "general cs", "Which of the following is not a type of computer architecture? a) Von Neumann b) Harvard c) Neural d) Quantum", "c", "Hint 2005"),
    ("2006", "hard", "general cs", "Which of the following is not a type of computer security? a) Network security b) Application security c) Hardware security d) Time security", "d", "Hint 2006"),
]

cursor.execute("create table qa_short_answer (question_id text, difficulty text, category text, question text, answer, text, hint text")
short_answer = [
    ("3001", "easy", "general cs", "A _____ specific set of instructions that a computer can perform.", "computer program", "Hint 3001"),
    ("3002", "easy", "general cs", "A _____ is a set of rules and conventions for organizing and formatting data.", "code", "Hint 3002"),
    ("3003", "medium", "general cs", "An _____ is a list set of instructions used to solve problems or perform tasks, based on the understanding of available alternatives.", "algorithm", "Hint 3003"),
    ("3004", "medium", "general cs", "A _____ is a sequence of instructions that are executed in a specific order.", "program", "Hint 3004"),
    ("3005", "hard", "general cs", "A _____ is a program or device that can gain unauthorized access to a computer system.", "malware", "Hint 3005"),
    ("3006", "hard", "general cs", "A _____ is a process of ensuring that data is kept private and secure. ", "encryption", "Hint 3006"),
]

cursor.executemany("insert into qa_true_false values (question_id, difficulty, category, question, answer, hint), true_and_false")
cursor.executemany("insert into qa_multiple_choice values(question_id, difficulty, category, question, answer, hint), multiple_choice")
cursor.executemany("insert into qa_short_answer values(question_id, difficulty, category, question, answer, hint), short_answer")

connection_string.close()
