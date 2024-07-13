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
difficulty level (easy, medium, and hard) for the student to write a SQL query for the given ddl for the question you provide.   Also give the recommended SELECT 
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

  #  print("OLD")
    """
    This is the main function of the script.
    """
    answer = get_data()
    answer2 = """{
  "story": [
    "In the realm of SQLandia, there existed a powerful wizard named Querymaster. Querymaster was known far and wide for his ability to harness the magic of SQL to solve any problem that came his way.",
    "One day, a group of adventurers arrived at Querymaster's tower seeking his help. They had heard of his legendary SQL skills and hoped he could assist them in their quest to retrieve a rare artifact known as the Crystal of Aggregation.",
    "The adventurers explained that the Crystal of Aggregation was said to hold immense power, but it had been lost for centuries in the depths of the Dark Database. They needed Querymaster's expertise to navigate the treacherous data structures and retrieve the crystal.",
    "Querymaster agreed to help the adventurers, knowing that the journey ahead would not be easy. He gathered his trusty companions - a brave knight named Joiner, a cunning rogue named Filterella, and a wise cleric named Indexia.",
    "Together, the party set out on their quest, facing challenges such as nested queries, complex joins, and tricky subqueries. But with Querymaster leading the way, they were able to overcome each obstacle with the power of SQL.",
    "After many trials and tribulations, the party finally reached the heart of the Dark Database where the Crystal of Aggregation lay hidden. Using a combination of SELECT statements and WHERE clauses, they were able to locate the crystal and retrieve it safely.",
    "As they emerged from the depths of the database, the adventurers thanked Querymaster for his invaluable assistance. The wizard smiled, knowing that he had once again used the magic of SQL to help others in need.",
    "And so, the party returned to the realm of SQLandia as heroes, their names forever etched in the annals of database history."
  ],
  "ddl": [
    "CREATE TABLE adventurers (id INT, name VARCHAR(50), class VARCHAR(50));",
    "CREATE TABLE challenges (id INT, description VARCHAR(100), difficulty VARCHAR(50));",
    "CREATE TABLE party (id INT, member_id INT, role VARCHAR(50));",
    "CREATE TABLE artifacts (id INT, name VARCHAR(50), power VARCHAR(50));",
    "CREATE TABLE locations (id INT, name VARCHAR(50), type VARCHAR(50));"
  ],
  "dml": [
    "INSERT INTO adventurers (id, name, class) VALUES (1, 'Querymaster', 'Wizard');",
    "INSERT INTO adventurers (id, name, class) VALUES (2, 'Joiner', 'Knight');",
    "INSERT INTO adventurers (id, name, class) VALUES (3, 'Filterella', 'Rogue');",
    "INSERT INTO adventurers (id, name, class) VALUES (4, 'Indexia', 'Cleric');",
    "INSERT INTO challenges (id, description, difficulty) VALUES (1, 'Nested queries', 'Hard');",
    "INSERT INTO challenges (id, description, difficulty) VALUES (2, 'Complex joins', 'Medium');",
    "INSERT INTO challenges (id, description, difficulty) VALUES (3, 'Subqueries', 'Difficult');",
    "INSERT INTO party (id, member_id, role) VALUES (1, 1, 'Leader');",
    "INSERT INTO party (id, member_id, role) VALUES (2, 2, 'Fighter');",
    "INSERT INTO party (id, member_id, role) VALUES (3, 3, 'Scout');",
    "INSERT INTO party (id, member_id, role) VALUES (4, 4, 'Healer');",
    "INSERT INTO artifacts (id, name, power) VALUES (1, 'Crystal of Aggregation', 'Aggregation');",
    "INSERT INTO locations (id, name, type) VALUES (1, 'Dark Database', 'Dungeon');",
    "INSERT INTO locations (id, name, type) VALUES (2, 'SQLandia', 'Realm')"
  ]
}"""
    print(answer)
    data = json.loads(answer)
    story, ddl = get_story_and_ddl(data)

    # Print the story and DDL
    print("Story:")
    for paragraph in story:
        print(paragraph)
        print()
    
    print("")
    print("easy question")
    easy_question = ask_question(ddl,story,"give me an easy question")

    print(easy_question)

    print("")
    print("medium question")
    hard_question = ask_question(ddl,story,"give me a really medium level question")
    print(hard_question)


    print("")
    print("hard question")
    hard_question = ask_question(ddl,story,"give me a really hard question")
    print(hard_question)

if __name__ == "__main__":
    main()

