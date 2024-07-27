from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableSequence
import streamlit as st
import toml
import json
from story_agent import *

def load_question_prompt(ddl, story, dml, question):
    template = f"""
    You are a SQL tutor. Given the DDL: {ddl}, story: {story}, and data: {dml}, generate a question about the given story with a specified difficulty level (easy, medium, or hard) for the student to write a SQL query for the given DDL.

    Return the output in JSON format with the key 'question' containing the actual question generated, the key 'difficulty' with the value 'easy', 'medium', or 'hard' based on the difficulty level of the question, and the key 'sql' containing the expected SQL SELECT statement for the 'question'.

    Difficulty Levels:
    - easy: Simple SELECT statements with basic conditions. These should involve one or two tables with straightforward WHERE clauses.
    - medium: More complex queries that may involve joins between multiple tables, aggregate functions, and GROUP BY clauses.
    - hard: Advanced queries requiring multiple joins, subqueries, nested queries, and complex conditions.
    """

    return ChatPromptTemplate.from_messages([("system", template), ("user", question)])

# Cache OpenAI Chat Model for future runs
def load_chat_model():
    secrets = toml.load(".streamlit/secrets.toml")
    return ChatOpenAI(
        temperature=0.01,
        model='gpt-3.5-turbo',
        streaming=True,
        verbose=True,
        openai_api_key=secrets["OPENAI_API_KEY"]
    )

def ask_question(ddl, story, dml, question):
    # Generate the answer by calling OpenAI's Chat Model
    chat_model = load_chat_model()
    prompt = load_question_prompt(ddl, story, dml, question)
  
    sequence = RunnableSequence(
        prompt | chat_model
    )

    response = sequence.invoke({})
    return response.content

def get_query_difficulty(answer):
    data = json.loads(answer)
    question = data.get("question", "")
    difficulty = data.get("difficulty", "")
    sql = data.get("sql", "")
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
    print("Easy question")
    easy_question = ask_question(ddl, story, dml, "Give me an easy level SQL question")
    print(easy_question)

    print("")
    print("Medium question")
    medium_question = ask_question(ddl, story, dml, "Give me a medium level SQL question")
    print(medium_question)

    print("")
    print("Hard question")
    hard_question = ask_question(ddl, story, dml, "Give me a really hard level SQL question")
    print(hard_question)

if __name__ == "__main__":
    main()
