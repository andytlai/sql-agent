from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import streamlit as st
from langchain.schema.runnable import RunnableMap
import toml
import json
import uuid
from story_agent import *

def load_question_prompt(ddl,story):
    # print("DEBUG")
    template =  f"""You are a SQL tutor, given the ddl : {ddl} and story : {story} generate a question about the given story and specified
difficulty level (easy, medium, or hard) for the student to write a SQL query for the given ddl for the question you provide.  

Return the output json format with the key as 'question' and the value is the actual question generated, and another key is the 'difficulty' level with value as 'easy', 'medium', or 'hard' based on the difficulty level of the question. 
The final key should be 'sql' containing the expected SQL SELECT statement for the 'question'.
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

def get_query_difficulty(answer):
    data = json.loads(answer)
    question = data.get("question", [])
    difficulty = data.get("difficulty", [])
    sql = data.get("sql", [])
    return question, difficulty, sql

def main():

    answer = get_simulated_data()
    print(answer)
    story, ddl, dml = get_story_ddl_dml(answer)

    # Print the story and DDL
    print("Story:")
    for paragraph in story:
        print(paragraph)
        print()
    
    print("")
    print("easy question")
    easy_question = ask_question(ddl, story, "Give me an easy level SQL question")

    print(easy_question)

    print("")
    print("medium question")
    hard_question = ask_question(ddl, story, "Give me a medium level SQL question")
    print(hard_question)


    print("")
    print("hard question")
    hard_question = ask_question(ddl, story, "Give me a really hard level SQL question")
    print(hard_question)

if __name__ == "__main__":
    main()

