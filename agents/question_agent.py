from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import streamlit as st
from langchain.schema.runnable import RunnableMap
import toml
import json
import uuid


def load_question_prompt(ddl,story):
    # print("DEBUG")
    template =  f"""You are a SQL tutor, given the ddl : {ddl} and story : {story} generate a question about the given story and specified
difficulty level (easy, medium, or hard) for the student to write a SQL query for the given ddl for the question you provide.  

Return the output json format with the key as 'question' and the value is the actual question generated, and another key is the 'difficulty' level with value as 'easy', 'medium', or 'hard' based on the difficulty level of the question.
Difficulty Levels:

easy: Simple SELECT statements with basic conditions. These should involve one or two tables with straightforward WHERE clauses.
medium: More complex queries that may involve joins between multiple tables, aggregate functions, and GROUP BY clauses.
hard: Advanced queries requiring multiple joins, subqueries, nested queries, and complex conditions.
    
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

def ask_question(ddl,story,question):
    # Generate the answer by calling OpenAI's Chat Model
    chat_model = load_chat_model()
    prompt = load_question_prompt(ddl,story)
    inputs = RunnableMap({
        'question': lambda x: x['question']
    })
    chain = inputs | prompt | chat_model
    response = chain.invoke({'question': question})
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
    
    print("")
    print("easy question")
    easy_question = ask_question(ddl,story,"Give me an easy level SQL question")

    print(easy_question)

    print("")
    print("medium question")
    hard_question = ask_question(ddl,story,"Give me a medium level SQL question")
    print(hard_question)


    print("")
    print("hard question")
    hard_question = ask_question(ddl,story,"Give me a really hard level SQL question")
    print(hard_question)

if __name__ == "__main__":
    main()

