from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import streamlit as st
from langchain.schema.runnable import RunnableMap
import toml
import json
import uuid

def load_prompt():
#     template =  """Generate a unique fantasy story with characters for a SQL game to teach users how to learn SQL in an interactive way. The story should generate at least 5 tables related to the story with at least 10 rows of data for each table related to the story that can be used to ask different levels of complex SQL questions about the data by joining data from multiple tables . Generate the DDL and DML statements for the data.

#     Return the output into a json with a separate key for each type and an array for each line of the output which is a string for each type.  Make sure there is a semicolon to terminate each line of the SQL statements.
#     story.txt contains the story text
#     story.ddl contains the CREATE TABLE statements
#     story.dml contains the INSERT statements
    
# """
    template = """Generate a unique fantasy story that incorporates characters and elements suitable for teaching users how to learn SQL in an interactive way. The story should include at least five distinct houses or factions, each with their own unique characteristics and responsibilities.

Requirements:

Story Text (story.txt):

Provide a brief narrative of the fantasy world and introduce the five houses or factions.
Describe the unique characteristics and responsibilities of each house.
Database Schema (story.ddl):

Create at least five tables relevant to the story, each representing a different aspect of the fantasy world (e.g., houses, members, artifacts, resources, quests).
Ensure each table has an appropriate primary key and relevant columns.
Define necessary foreign key relationships between tables.
Data Population (story.dml):

Populate each table with at least ten rows of data.
Ensure the data is relevant to the story and can be used to formulate various SQL queries.
Output Format:

Return the output in JSON format with separate keys for each type (story.txt, story.ddl, story.dml).
Each key should contain an array of strings, with each string representing a line of the output.
Ensure each SQL statement is terminated with a semicolon.
"""
    return ChatPromptTemplate.from_messages([("system", template)])


def load_question_prompt(ddl,story):
    # print("DEBUG")
    template =  f"""You are a SQL tutor, given the ddl : {ddl} and story : {story} generate a question about the given story and specified
difficulty level (easy, medium, or hard) for the student to write a SQL query for the given ddl for the question you provide.   Also give the recommended SELECT 
statement for the generated question for validation.

Difficulty Levels:

Easy: Simple SELECT statements with basic conditions. These should involve one or two tables with straightforward WHERE clauses.
Medium: More complex queries that may involve joins between multiple tables, aggregate functions, and GROUP BY clauses.
Hard: Advanced queries requiring multiple joins, subqueries, nested queries, and complex conditions.
    
"""
    return ChatPromptTemplate.from_messages([("system", template)])
   

# Cache OpenAI Chat Model for future runs
def load_chat_model():
    secrets = toml.load(".streamlit/secrets.toml")
    return ChatOpenAI(
        temperature=0.3,
        model='gpt-3.5-turbo',
        streaming=True,
        verbose=True,
        openai_api_key= secrets["OPENAI_API_KEY"]
    )

def get_data():
    # Generate the answer by calling OpenAI's Chat Model
    chat_model = load_chat_model()
    prompt = load_prompt()

    chain = prompt | chat_model
    response = chain.invoke({})
    return response.content

def get_simulated_data():
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
    return answer


def get_story_ddl_dml(answer):
    data = json.loads(answer)
    story = data.get("story.txt", [])
    ddl = data.get("story.ddl", [])
    dml = data.get("story.dml", [])
    return story, ddl, dml

def main():

  #  print("OLD")
    """
    This is the main function of the script.
    """
    answer = get_data()
 
    print(answer)

    story, ddl, dml = get_story_ddl_dml(answer)

    # Print the story and DDL
    print("Story:")
    for paragraph in story:
        print(paragraph)
        print()

if __name__ == "__main__":
    main()