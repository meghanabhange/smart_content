import json
import random
import string
import time
from pathlib import Path

import pandas as pd
import streamlit as st

import requests
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

df = pd.read_csv("map_concepts_activities_topics_Python_MasteryGrids_latest_course.csv")


def get_parsed_text(code):
    data = {"code": code, "mode": "simple"}
    response = requests.post("http://acos.cs.hut.fi/python-parser", data=data)
    return [v for k, v in response.json()["lines"].items()][0]


def get_smart_content(code_types, keywords):
    output = []
    for t in code_types:
        matched_content = df[df["component_name"] == t]
        for i, row in matched_content.iterrows():
            extacted = process.extractOne(row["topic_name"], keywords)
            if extacted and extacted[1]>70:
                output.append({"url": row["url"], "topic_name": row["topic_name"]})
    return {"Matched Smart Content": output[:10]}


def get_wikipedia(key):
    key = wikipedia.search(key)[0]
    summary = wikipedia.summary(key)
    url = wikipedia.page(key).url
    return summary, url


output_path = Path("output.json")

st.title("Python For Everybody ✨")
st.markdown("## Textbook Assistant 🎓")

st.markdown(
    """
The aim of this demo is to extract code samples from a given topic. 
For extracting the code and text from the book [Python For Everybody](https://github.com/csev/py4e/tree/master/book3/html)
There is also an Audio Assistant on the sidebar where you can ask your query and we will try our best to get matching answer from wikipedia for you

You can select the chapter and the topic and you will be able to see the extracted code. 
"""
)

content = json.load(output_path.open())
chapters = [ele for ele in content]
chapters.sort()
chapter = st.selectbox("Chapter", chapters)


chapter_content = content[chapter]["content"]
topics = [ele["Topic"] for ele in chapter_content]
topic = st.selectbox("Topic", topics)
concepts = content[chapter]["concepts"]

for ctx in chapter_content:
    if topic == ctx["Topic"]:
        col1, col2 = st.beta_columns(2)
        with col1:
            st.markdown("## Text")
            for text in ctx["text"]:
                st.write(text)
        with col2:
            st.markdown("## Code")
            for code in ctx["code"]:
                # st.code(code)
                codelines = code.split("\n")
                execcode = codelines
                outputcode = []
                if not(code.find(">>>")==-1):
                    execcode = [line[4:] for line in codelines if line[:3] == ">>>"]
                    outputcode = [line for line in codelines if line[:3] != ">>>"]
                execcode = "\n".join(execcode)
                outputcode = "\n".join(outputcode)
                st.code(execcode)
                st.text(outputcode)
                code_types = get_parsed_text(execcode)
                matched_urls = get_smart_content(code_types, concepts)
                st.markdown("### Matched Smart Content")
                st.write(matched_urls)
                # content = st_ace(execcode, key=code, language="python", theme="chaos", )

        st.write("Raw Json")
        st.write(ctx)