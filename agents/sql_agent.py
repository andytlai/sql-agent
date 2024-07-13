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
import json
import toml

def execute_query(input):
    secrets = toml.load(".streamlit/secrets.toml")

    sqlite_path = "/kaggle/input/24169-pitchfork-reviews/data.sqlite3"
    sqlite_uri = f"sqlite:///{sqlite_path}"
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


def main():


    """
    This is the main function of the script.
    """
    answer = get_data()
    print(answer)
    data = json.loads(answer)
    print(data['ddl'])

    query_string = ''

   # Loop through each item in the array
    for item in data['ddl']:
   # Append each item followed by a newline character to the result string
      query_string += item + '\n'
      execute_query(item)

    for item in data['dml']:
   # Append each item followed by a newline character to the result string
      query_string += item + '\n'
      execute_query(item)

    print(query_string)

    #execute_query(query_string)

if __name__ == "__main__":
    main()