from langchain.agents import create_sql_agent 
from langchain.agents.agent_toolkits import SQLDatabaseToolkit 
from langchain.sql_database import SQLDatabase 
from langchain.llms.openai import OpenAI 
from langchain.agents import AgentExecutor 
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI

def execute_query(query):
    sqlite_path = "/kaggle/input/24169-pitchfork-reviews/data.sqlite3"
    sqlite_uri = f"sqlite:///{sqlite_path}"
    db = SQLDatabase.from_uri("sqlite:///Chinook.db")

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

    result = agent_executor.invoke("Execute the given query {}", query)

    # Return the twitter content of each of these n rows
    return result