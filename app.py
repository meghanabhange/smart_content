import streamlit as st
import json 
from pathlib import Path

output_path = Path("output.json")

st.title("Code Extraction Demo")

st.markdown("""
The aim of this demo is to extract code samples from a given topic. 
For extracting the code and text from the book [Python For Everybody](https://github.com/csev/py4e/tree/master/book3/html)

You can select the chapter and the topic and you will be able to see the extracted code. 
""")

content = json.load(output_path.open())
chapters = [ele for ele in content]
chapters.sort()
chapter = st.selectbox("Chapter", chapters)


chapter_content = content[chapter]["content"]
topics = [ele["Topic"] for ele in chapter_content]
topic = st.selectbox("Topic", topics)

for ctx in chapter_content:
    if topic == ctx["Topic"]:
        st.markdown("## Text")
        for text in ctx["text"]:
            st.write(text)
        if ctx["code"]:
            st.markdown("## Code")
            for code in ctx["code"]:
                st.text(code)
