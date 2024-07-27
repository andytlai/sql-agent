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
#     story.dml contains the INSERT statements for each table
    
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
    "Once upon a time in the enchanted land of SQLara, there was a grand kingdom known as DataRealm.",
    "The kingdom was divided into several regions, each governed by wise leaders.",
    "The regions included the Forest of Queries, the Mountains of Joins, the Plains of Conditions, the Lakes of Aggregations, and the Deserts of Nulls.",
    "The kingdom was home to various inhabitants, including humans, elves, dwarves, and magical creatures.",
    "The wise leaders often held councils to maintain peace and prosperity in the kingdom.",
    "Each leader kept detailed records of their region’s population, resources, and alliances to ensure the kingdom's growth and stability.",
    "The residents of SQLara had to learn the ancient art of SQL magic to interact with these records.",
    "They practiced their skills by solving problems and completing quests that required them to query and manipulate the data stored in the kingdom’s enchanted database."
  ],
  "story.ddl": [
    "CREATE TABLE Regions (region_id INT PRIMARY KEY, region_name VARCHAR(50), description TEXT);",
    "CREATE TABLE Leaders (leader_id INT PRIMARY KEY, name VARCHAR(50), region_id INT, FOREIGN KEY (region_id) REFERENCES Regions(region_id));",
    "CREATE TABLE Inhabitants (inhabitant_id INT PRIMARY KEY, name VARCHAR(50), species VARCHAR(50), region_id INT, FOREIGN KEY (region_id) REFERENCES Regions(region_id));",
    "CREATE TABLE Resources (resource_id INT PRIMARY KEY, resource_name VARCHAR(50), quantity INT, region_id INT, FOREIGN KEY (region_id) REFERENCES Regions(region_id));",
    "CREATE TABLE Alliances (alliance_id INT PRIMARY KEY, region_one_id INT, region_two_id INT, FOREIGN KEY (region_one_id) REFERENCES Regions(region_id), FOREIGN KEY (region_two_id) REFERENCES Regions(region_id));"
  ],
  "story.dml": [
    "INSERT INTO Regions (region_id, region_name, description) VALUES (1, 'Forest of Queries', 'A mystical forest filled with questions and secrets.');",
    "INSERT INTO Regions (region_id, region_name, description) VALUES (2, 'Mountains of Joins', 'Towering peaks where data connections are made.');",
    "INSERT INTO Regions (region_id, region_name, description) VALUES (3, 'Plains of Conditions', 'Vast plains where conditions are evaluated.');",
    "INSERT INTO Regions (region_id, region_name, description) VALUES (4, 'Lakes of Aggregations', 'Serene lakes where data is summarized.');",
    "INSERT INTO Regions (region_id, region_name, description) VALUES (5, 'Deserts of Nulls', 'A barren desert where missing data resides.');",

    "INSERT INTO Leaders (leader_id, name, region_id) VALUES (1, 'Aria the Wise', 1);",
    "INSERT INTO Leaders (leader_id, name, region_id) VALUES (2, 'Gorin the Strong', 2);",
    "INSERT INTO Leaders (leader_id, name, region_id) VALUES (3, 'Lyra the Clever', 3);",
    "INSERT INTO Leaders (leader_id, name, region_id) VALUES (4, 'Nero the Calm', 4);",
    "INSERT INTO Leaders (leader_id, name, region_id) VALUES (5, 'Selene the Silent', 5);",

    "INSERT INTO Inhabitants (inhabitant_id, name, species, region_id) VALUES (1, 'Elara', 'Elf', 1);",
    "INSERT INTO Inhabitants (inhabitant_id, name, species, region_id) VALUES (2, 'Thorin', 'Dwarf', 2);",
    "INSERT INTO Inhabitants (inhabitant_id, name, species, region_id) VALUES (3, 'Mira', 'Human', 3);",
    "INSERT INTO Inhabitants (inhabitant_id, name, species, region_id) VALUES (4, 'Faye', 'Fairy', 4);",
    "INSERT INTO Inhabitants (inhabitant_id, name, species, region_id) VALUES (5, 'Valkor', 'Orc', 5);",
    "INSERT INTO Inhabitants (inhabitant_id, name, species, region_id) VALUES (6, 'Nera', 'Nymph', 4);",
    "INSERT INTO Inhabitants (inhabitant_id, name, species, region_id) VALUES (7, 'Kira', 'Human', 1);",
    "INSERT INTO Inhabitants (inhabitant_id, name, species, region_id) VALUES (8, 'Dorin', 'Dwarf', 2);",
    "INSERT INTO Inhabitants (inhabitant_id, name, species, region_id) VALUES (9, 'Luna', 'Elf', 3);",
    "INSERT INTO Inhabitants (inhabitant_id, name, species, region_id) VALUES (10, 'Zara', 'Fairy', 4);",

    "INSERT INTO Resources (resource_id, resource_name, quantity, region_id) VALUES (1, 'Mana Crystals', 100, 1);",
    "INSERT INTO Resources (resource_id, resource_name, quantity, region_id) VALUES (2, 'Iron Ore', 200, 2);",
    "INSERT INTO Resources (resource_id, resource_name, quantity, region_id) VALUES (3, 'Wheat', 300, 3);",
    "INSERT INTO Resources (resource_id, resource_name, quantity, region_id) VALUES (4, 'Water', 400, 4);",
    "INSERT INTO Resources (resource_id, resource_name, quantity, region_id) VALUES (5, 'Sand', 500, 5);",
    "INSERT INTO Resources (resource_id, resource_name, quantity, region_id) VALUES (6, 'Herbs', 150, 1);",
    "INSERT INTO Resources (resource_id, resource_name, quantity, region_id) VALUES (7, 'Gold', 50, 2);",
    "INSERT INTO Resources (resource_id, resource_name, quantity, region_id) VALUES (8, 'Corn', 250, 3);",
    "INSERT INTO Resources (resource_id, resource_name, quantity, region_id) VALUES (9, 'Fish', 350, 4);",
    "INSERT INTO Resources (resource_id, resource_name, quantity, region_id) VALUES (10, 'Cactus', 450, 5);",

    "INSERT INTO Alliances (alliance_id, region_one_id, region_two_id) VALUES (1, 1, 2);",
    "INSERT INTO Alliances (alliance_id, region_one_id, region_two_id) VALUES (2, 2, 3);",
    "INSERT INTO Alliances (alliance_id, region_one_id, region_two_id) VALUES (3, 3, 4);",
    "INSERT INTO Alliances (alliance_id, region_one_id, region_two_id) VALUES (4, 4, 5);",
    "INSERT INTO Alliances (alliance_id, region_one_id, region_two_id) VALUES (5, 5, 1);"
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