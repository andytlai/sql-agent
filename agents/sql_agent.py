from langchain.agents.agent_toolkits import SQLDatabaseToolkit, create_sql_agent 
from langchain.sql_database import SQLDatabase 
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from story_agent import *
from question_agent import *
import json
import toml
import sqlite3
import sys

class SQLHandler(BaseCallbackHandler):
    def __init__(self):
        print("ESTOOO")
        self.sql_result = None

    def on_agent_action(self, action, **kwargs):
        """Run on agent action. if the tool being used is sql_db_query,
         it means we're submitting the sql and we can 
         record it as the final sql"""

        if action.tool == "sql_db_query":
            self.sql_result = action.tool_input

def execute_query_via_agent(input):
    secrets = toml.load(".streamlit/secrets.toml")
    db = SQLDatabase.from_uri("sqlite:///Chinook.db")
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key= secrets["OPENAI_API_KEY"])
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

    handler = SQLHandler()
    result = agent_executor.invoke({"input": input}, {"callbacks": [handler]})['output']

    print('query run: ')
    print(handler.sql_result)

    # Return the twitter content of each of these n rows
    return result

def execute_ddl_dml(ddl, dml):
    connection = sqlite3.connect("Chinook.db")

    cursor = connection.cursor()

    for item in ddl:
      cursor.execute(item)

    for item in dml:
      cursor.execute(item)
      connection.commit()   

def execute_query(query):
    connection = sqlite3.connect("Chinook.db")
    cursor = connection.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
def main():
    print ('argument list', sys.argv)
    use_existing_schema = bool(sys.argv[1])

    if use_existing_schema:
       question = "List the total sales per country. Which country's customers spent the most?" 
       print(question)
       print(execute_query_via_agent(question))
       return

    """
    This is the main function of the script.
    """
    answer = get_simulated_data()
    print(answer)
    story, ddl, dml = get_story_ddl_dml(answer)

    execute_ddl_dml(ddl, dml)

    easy_question = ask_question(ddl, story, "Give me an easy level SQL question")
    "List the total sales per country. Which country's customers spent the most?" 
    print(easy_question)
    question, difficulty, sql = get_query_difficulty(easy_question)

    print(execute_query_via_agent(question))
    print(execute_query(sql))

if __name__ == "__main__":
    main()