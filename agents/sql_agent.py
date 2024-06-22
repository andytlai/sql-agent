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

def execute_query(input):
    sqlite_path = "/kaggle/input/24169-pitchfork-reviews/data.sqlite3"
    sqlite_uri = f"sqlite:///{sqlite_path}"
    db = SQLDatabase.from_uri("sqlite:///Chinook.db")

    toolkit = SQLDatabaseToolkit(db=db, llm=ChatOpenAI(temperature=0))
    context = toolkit.get_context()
    tools = toolkit.get_tools()

    messages = [
       HumanMessagePromptTemplate.from_template("{input}"),
       AIMessage(content=SQL_FUNCTIONS_SUFFIX),
       MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]

    prompt = ChatPromptTemplate.from_messages(messages)
    prompt = prompt.partial(**context)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    agent = create_openai_tools_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
       agent=agent,
       tools=toolkit.get_tools(),
       verbose=True,
    )

    result = agent_executor.invoke({"input": input})

    # Return the twitter content of each of these n rows
    return result