import psycopg2
import os
import json
import random
from dotenv import load_dotenv
dir_path = os.path.dirname(os.path.realpath(__file__))

#Load variables from the .env file into connect
load_dotenv()

# 1 #establish a connection
conn = psycopg2.connect(
    dbname=os.getenv('db_name'),
    user=os.getenv('db_user'),
    password=os.getenv('db_password'),
    host=os.getenv('db_host'),
    port=os.getenv('db_port')
)

# Create a cursor object to interact with the database
cur = conn.cursor()

# Execute SQL Queries:
# cur.execute('''CREATE TABLE quizz(
# 	id serial PRIMARY KEY,
# 	username VARCHAR ( 50 )  NOT NULL,
# 	question VARCHAR (500) NOT NULL,
# 	answer INT NOT NULL,
# 	correct_answer VARCHAR (500) NOT NULL)
# ''')

conn.commit()

# Execute a simple SQL query
cur.execute("SELECT * FROM quizz;")
conn.commit()

# Fetch all results
result = cur.fetchall()
print(result)

# Execute a Query with Parameters:

# Use parameterized query to avoid SQL injection
query = "SELECT * FROM quizz;"
parameter = ("some_value",)
cur.execute(query, parameter)

# Commit and Close:

# Commit changes (if any)
conn.commit()

# Close the cursor and connection


total=5
quizz=''
def fetch_question():

    user_name=input('Enter your name: ')

with open(dir_path + '\quizz.json', mode='r') as json_file:
    data=json.load(json_file)

    questions=data['questions']

def quizz_question(question_called):
    score=0
    user_name=input('Enter your name: ')

    for question in question_called:
        # question, correct_answer=fetch_question(cur)

        print("\nQuestion:", question['question'])

        for i,option in enumerate(question['options']):
            print(i+1, option)

        user_answer = int(input("Your answer: "))


        if question['options'][user_answer-1] == question['correct_answer']:
            print('Correct')
            score+=1
        else:
            print(f'Incorrect. The correct answer is', question['correct_answer'])

    return user_name, question['question'], question['correct_answer'], user_answer, score

user_name, question, user_answer, correct_answer, score = quizz_question(questions)

query = 'INSERT INTO quizz (username, question, answer, correct_answer, score) VALUES (%s, %s, %s, %s, %s)'
data = (user_name, question, correct_answer, user_answer, score)

cur.execute(query, data)
conn.commit()

# Commit and Close:
# Commit changes (if any)

print(f'Your score is: {score}')

cur.close()
conn.close()

# Error Handling:

# try:
#     # your code here
# Except psycopg2.Error as e:
#     print("Error:", e)
#     # Handle the error as needed
# finally:
#     # Ensure to close the connection in case of an error
#     if conn is not None:
#     conn.close()