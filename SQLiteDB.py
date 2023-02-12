import sqlite3


def create_sqlite_database(qa_true_false, qa_multiple_choice, qa_short_answer):
    """
    This function creates an SQLite database and inserts data into three tables: qa_true_false, qa_multiple_choice,
    and qa_short_answer.

    Returns:
        None
    """
    connection = sqlite3.connect("questions_answers.db")

    cursor = connection.cursor()

    cursor.execute("CREATE TABLE qa_true_false (question_id INTEGER, difficulty TEXT, category TEXT, question TEXT, answer TEXT, hint TEXT)")

    true_false = [
        (1001, "easy", "general cs", "Computer science is not the study of the theory and application of computers.",
         "false", "Not not false"),
        (1002, "easy", "general cs", "The first electronic computer was created in the 17th century.", "false",
         "Not not false"),
        (1003, "medium", "general cs", "A Turing machine is a theoretical model of a general-purpose computer that "
                                       "can perform any calculation that is algorithmically solvable.",
         "true", "Not not not false"),
        (1004, "medium", "general cs", "Von Neumann architecture is a design model for computers that separates the "
                                       "memory and processing units.", "true", "Not not not false"),
        (1005, "hard", "general cs", "The P vs NP problem is a computational problem that asks whether every "
                                     "problem whose solution can be verified in polynomial time, can also be solved "
                                     "in polynomial time.", "true", "Not not not false"),
        (1006, "hard", "general cs", "The Halting problem is a problem that asks whether, given a description of an "
                                     "arbitrary computer program, it is possible to decide whether the program "
                                     "finishes running or continues running forever.", "true", "Not not not false"),
    ]
    cursor.executemany("INSERT INTO qa_true_false VALUES(?,?,?,?,?,?)", true_false)

    cursor.execute("CREATE TABLE qa_multiple_choice (question_id INTEGER, difficulty TEXT, category TEXT, question TEXT, answer TEXT, hint TEXT)")

    multiple_choice = [
        (2001, "easy", "general cs", "Which of the following is not a type of computer memory? a) RAM b) ROM c) CPU "
                                     "d) HDD", "c", "Not a) or d)"),
        (2002, "easy", "general cs", "Which of the following is not a type of computer network? a) LAN b) WAN c) "
                                     "PAN d) SAN", "d", "Not b) or c)"),
        (2003, "medium", "general cs", "Which of the following is not a type of software? a) System software b) "
                                       "Application software c) Hardware software d) Firmware", "c", "Not a) or d)"),
        (2004, "medium", "general cs", "Which of the following is not a type of computer language? a) Assembly b) "
                                       "High-level c) Low-level d) Database", "d", "Not b) or c)"),
        (2005, "hard", "general cs", "Which of the following is not a type of computer architecture? a) Von Neumann "
                                     "b) Harvard c) Neural d) Quantum", "c", "Not a) or d)"),
        (2006, "hard", "general cs", "Which of the following is not a type of computer security? a) Network "
                                     "security b) Application security c) Hardware security d) Time security", "d",
         "Not b) or c)"),
    ]

    cursor.executemany("INSERT INTO qa_multiple_choice VALUES(?,?,?,?,?,?)", multiple_choice)

    cursor.execute("CREATE TABLE qa_short_answer(question_id INTEGER, difficulty TEXT, category TEXT, question TEXT, answer TEXT, hint TEXT)")

    short_answer = [
        (3001, "easy", "general cs", "A _____ specific set of instructions that a computer can perform.",
         "computer program", "c______r p_____m"),
        (3002, "easy", "general cs", "A _____ is a set of rules and conventions for organizing and formatting data.",
         "code", "c__e"),
        (3003, "medium", "general cs", "An _____ is a list set of instructions used to solve problems or perform "
                                       "tasks, based on the understanding of available alternatives.", "algorithm",
         "a_______m"),
        (3004, "medium", "general cs", "A _____ is a sequence of instructions that are executed in a specific order.",
         "program", "p_____m"),
        (3005, "hard", "general cs", "A _____ is a program or device that can gain unauthorized access to a "
                                     "computer system.", "malware", "m_____e"),
        (3006, "hard", "general cs", "A _____ is a process of ensuring that data is kept private and secure. ",
         "encryption", "e________n"),
    ]

    cursor.executemany("INSERT INTO qa_short_answer VALUES(?,?,?,?,?,?)", short_answer)

    connection.commit()
    connection.close()

