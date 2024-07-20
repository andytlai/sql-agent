from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import streamlit as st
from langchain.schema.runnable import RunnableMap
import toml
import json
import uuid


def load_question_prompt(ddl,expected_answer,student_answer):
    # print("DEBUG")
    template =  f"""You are an SQL teaching assistant. Your task is to compare a student's SQL query with the expected correct SQL query and determine if they are equivalent. If the queries are not equivalent, provide hints to guide the student toward the correct answer. Use the following format:

    The table schema(s) are provided in {ddl} the students SQL query is given as {student_answer} and the expected SQL query is {expected_answer}

    Return output in json format with 
    1. key 'equivalent' to indicate if the the queries are euivalent or not via 'true' or 'false'.   The student answer doesn't need to be optimal SQL to be equivalent.   As long as the query would result in the same output we should consider it equivalent.
    2. key 'hint' with 
        a. 'list_of_potential_issues' : listing potential issues or differences between the student answer and expected
        b. 'suggested_specific_changes' : which suggest a list of specific changes or areas of the query the student should focus on.
        c. 'explanation' : provides a brief explanation of why the expected query is correct and how the student's query can be improved.

"""
    return ChatPromptTemplate.from_messages([("system", template)])
   

# Cache OpenAI Chat Model for future runs
def load_chat_model():
    secrets = toml.load(".streamlit/secrets.toml")
    return ChatOpenAI(
        temperature=0.01,
        model='gpt-3.5-turbo',
        streaming=True,
        verbose=True,
        openai_api_key= secrets["OPENAI_API_KEY"]
    )

def ask_question(ddl,expected_answer,student_answer):
    # Generate the answer by calling OpenAI's Chat Model
    chat_model = load_chat_model()
    prompt = load_question_prompt(ddl,expected_answer,student_answer)
    inputs = RunnableMap({
    })
    chain = inputs | prompt | chat_model
    response = chain.invoke({})
    return response.content

def get_story_and_ddl(data):
    #print("debug1")
    story = data.get("story.txt", [])
   # print("debug2")
    ddl = data.get("story.ddl", [])
   # print("debug3")
    return story, ddl

def main():

    answer = """{
 "story.txt": [
    "In the land of SQLoria, there are five powerful houses that govern the realm, each specializing in a different aspect of data manipulation.",
    "1. House Query: Known for their expertise in writing complex SQL queries and unraveling data mysteries.",
    "2. House Join: Masters of joining tables together to combine information and uncover hidden connections.",
    "3. House Index: Keepers of the indexes, they ensure quick data retrieval and efficient query performance.",
    "4. House Transaction: Guardians of data integrity, they oversee all transactions and maintain the database's consistency.",
    "5. House Backup: Protectors of data security, they store backups and ensure the realm's information is safe from harm."
  ],
  "story.ddl": [
    "CREATE TABLE house_query (id INT PRIMARY KEY, name VARCHAR(50), specialty VARCHAR(100));",
    "CREATE TABLE house_join (id INT PRIMARY KEY, name VARCHAR(50), specialty VARCHAR(100));",
    "CREATE TABLE house_index (id INT PRIMARY KEY, name VARCHAR(50), specialty VARCHAR(100));",
    "CREATE TABLE house_transaction (id INT PRIMARY KEY, name VARCHAR(50), specialty VARCHAR(100));",
    "CREATE TABLE house_backup (id INT PRIMARY KEY, name VARCHAR(50), specialty VARCHAR(100));"
  ],
  "story.dml": [
    "INSERT INTO house_query (id, name, specialty) VALUES (1, 'House Query', 'Writing complex SQL queries');",
    "INSERT INTO house_query (id, name, specialty) VALUES (2, 'House Query', 'Analyzing data patterns');",
    "INSERT INTO house_query (id, name, specialty) VALUES (3, 'House Query', 'Optimizing query performance');",
    "INSERT INTO house_join (id, name, specialty) VALUES (1, 'House Join', 'Mastering table joins');",
    "INSERT INTO house_join (id, name, specialty) VALUES (2, 'House Join', 'Combining data from multiple sources');",
    "INSERT INTO house_join (id, name, specialty) VALUES (3, 'House Join', 'Identifying relationships between tables');",
    "INSERT INTO house_index (id, name, specialty) VALUES (1, 'House Index', 'Creating efficient indexes');",
    "INSERT INTO house_index (id, name, specialty) VALUES (2, 'House Index', 'Optimizing data retrieval');",
    "INSERT INTO house_index (id, name, specialty) VALUES (3, 'House Index', 'Maintaining index integrity');",
    "INSERT INTO house_transaction (id, name, specialty) VALUES (1, 'House Transaction', 'Ensuring data consistency');",
    "INSERT INTO house_transaction (id, name, specialty) VALUES (2, 'House Transaction', 'Managing database locks');",
    "INSERT INTO house_transaction (id, name, specialty) VALUES (3, 'House Transaction', 'Rolling back failed transactions');",
    "INSERT INTO house_backup (id, name, specialty) VALUES (1, 'House Backup', 'Storing secure backups');",
    "INSERT INTO house_backup (id, name, specialty) VALUES (2, 'House Backup', 'Implementing disaster recovery plans');",
    "INSERT INTO house_backup (id, name, specialty) VALUES (3, 'House Backup', 'Encrypting sensitive data during backups');"
  ]
}"""

    data = json.loads(answer)
    story, ddl = get_story_and_ddl(data)

    # Print the story and DDL
    print("Story:")
    for paragraph in story:
        print(paragraph)
        print()
    
    expected_answer = """SELECT hq.name AS house_query_name, hj.name AS house_join_name, hq.specialty
FROM house_query hq
JOIN house_join hj ON hq.id = hj.id
WHERE hq.specialty = 'Cardiology'
ORDER BY hq.name;"""

    student_answer = """SELECT hq.name AS house_query_name, hj.name AS house_join_name, hq.specialty
FROM house_query hq, (SELECT * FROM house_join) hj
WHERE hq.id = hj.id
AND hq.specialty = 'Cardiology'
ORDER BY hq.name;
"""

    bad_answer = """SELECT hq.name AS house_query_name, hj.name AS house_join_name, hq.specialty
FROM house_query hq, (SELECT * FROM house_join) hj
WHERE hq.specialty = 'Cardiology'
ORDER BY hq.name;"""

    res1 = ask_question(ddl,expected_answer,student_answer)
    print(res1)

    res2 = ask_question(ddl,expected_answer,bad_answer)
    print(res2)
   
if __name__ == "__main__":
    main()

