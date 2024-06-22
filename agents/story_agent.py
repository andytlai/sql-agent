from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import streamlit as st
import toml

def load_prompt():
    template =  """Generate a unique fantasy story with characters for a SQL game to teach users how to learn SQL in an interactive way. The story should generate at least 5 tables related to the story with at least 10 rows of data for each table related to the story that can be used to ask different levels of complex SQL questions about the data by joining data from multiple tables . Generate the DDL and DML statements for the data.

    Return the output into a json with a separate key for each type and an array for each line of the output which is a string for each type.  Make sure there is a semicolon to terminate each line of the SQL statements.
    story.txt contains the story text
    story.ddl contains the CREATE TABLE statements
    story.dml contains the INSERT statements
    
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


def main():


    """
    This is the main function of the script.
    """
    answer = get_data()
    print(answer)


if __name__ == "__main__":
    main()

