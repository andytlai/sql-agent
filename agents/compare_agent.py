from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import streamlit as st
from langchain.schema.runnable import RunnableMap
import toml
import json
import uuid
from story_agent import *
from question_agent import *


def load_question_prompt(ddl,expected_answer,student_answer):
    # print("DEBUG")
    template =  f"""You are an SQL teaching assistant. Your task is to compare a student's SQL query with the expected correct SQL query and determine if they are equivalent. If the queries are not equivalent, provide hints to guide the student toward the correct answer. Use the following format:

    The table schema(s) are provided in {ddl} the students SQL query is given as {student_answer} and the expected SQL query is {expected_answer}

    Return output in json format with 
    1. key 'equivalent' to indicate if the the queries are euivalent or not via 'true' or 'false'.   The student answer doesn't need to be optimal SQL to be equivalent.   As long as the query would result in the same output we should consider it equivalent.
    2. key 'hint' with 
        a. 'list_of_potential_issues' : listing potential issues or differences between the student answer and expected
        b. 'suggested_specific_changes' : which suggest a list of specific changes or areas of the query the student should focus on.
        c. 'explanation' : provides a brief explanation of why the expected query is correct and how the student's query can be improved.

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

def compare_answers(ddl,expected_answer,student_answer):
    # Generate the answer by calling OpenAI's Chat Model
    chat_model = load_chat_model()
    prompt = load_question_prompt(ddl,expected_answer,student_answer)
    inputs = RunnableMap({
    })
    chain = inputs | prompt | chat_model
    response = chain.invoke({})
    return response.content

def get_story_and_ddl(data):
    #print("debug1")
    story = data.get("story.txt", [])
   # print("debug2")
    ddl = data.get("story.ddl", [])
   # print("debug3")
    return story, ddl

def main():

    answer = get_simulated_data()
    print(answer)
    story, ddl, dml = get_story_ddl_dml(answer)

    # Print the story and DDL
    print("Story:")
    for paragraph in story:
        print(paragraph)
        print()
    
    expected_answer = """SELECT hq.name AS house_query_name, hj.name AS house_join_name, hq.specialty
FROM house_query hq
JOIN house_join hj ON hq.id = hj.id
WHERE hq.specialty = 'Cardiology'
ORDER BY hq.name;"""

    student_answer = """SELECT hq.name AS house_query_name, hj.name AS house_join_name, hq.specialty
FROM house_query hq, (SELECT * FROM house_join) hj
WHERE hq.id = hj.id
AND hq.specialty = 'Cardiology'
ORDER BY hq.name;
"""

    bad_answer = """SELECT hq.name AS house_query_name, hj.name AS house_join_name, hq.specialty
FROM house_query hq, (SELECT * FROM house_join) hj
WHERE hq.specialty = 'Cardiology'
ORDER BY hq.name;"""

    res1 = compare_answers(ddl,expected_answer,student_answer)
    print(res1)

    res2 = compare_answers(ddl,expected_answer,bad_answer)
    print(res2)
   
if __name__ == "__main__":
    main()

