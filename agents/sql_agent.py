from langchain.agents.agent_toolkits import SQLDatabaseToolkit 
from langchain.sql_database import SQLDatabase 
from langchain.agents import AgentExecutor 
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_openai_tools_agent
from langchain_community.agent_toolkits.sql.prompt import SQL_FUNCTIONS_SUFFIX
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from story_agent import *
from question_agent import *
import json
import toml
import sqlite3

def execute_query_via_agent(input):
    secrets = toml.load(".streamlit/secrets.toml")
    db = SQLDatabase.from_uri("sqlite:///Chinook.db")

    toolkit = SQLDatabaseToolkit(db=db, llm=ChatOpenAI(temperature=0, openai_api_key= secrets["OPENAI_API_KEY"]))
    context = toolkit.get_context()
    tools = toolkit.get_tools()

    messages = [
       HumanMessagePromptTemplate.from_template("{input}"),
       AIMessage(content=SQL_FUNCTIONS_SUFFIX),
       MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]

    prompt = ChatPromptTemplate.from_messages(messages)
    prompt = prompt.partial(**context)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key= secrets["OPENAI_API_KEY"])

    agent = create_openai_tools_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
       agent=agent,
       tools=toolkit.get_tools(),
       verbose=True,
    )

    result = agent_executor.invoke({"input": input})

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

    """
    This is the main function of the script.
    """
    answer = get_simulated_data()
    print(answer)
    story, ddl, dml = get_story_ddl_dml(answer)

    execute_ddl_dml(ddl, dml)

    easy_question = ask_question(ddl, story, "Give me an easy level SQL question")
    print(easy_question)
    question, difficulty, sql = get_query_difficulty(easy_question)

    print(execute_query_via_agent(question))
    print(execute_query(sql))

if __name__ == "__main__":
    main()