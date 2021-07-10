import streamlit as st
import json 
from pathlib import Path
import random
# from streamlit_ace import st_ace

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
        st.write("Raw Json")
        st.write(ctx)
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
                execcode = [line[4:] for line in codelines if line[:3]==">>>"]
                outputcode = [line for line in codelines if line[:3]!=">>>"]
                execcode = "\n".join(execcode)
                outputcode = "\n".join(outputcode)
                st.code(execcode)
                st.text(outputcode)
                # content = st_ace(execcode, key=code, language="python", theme="chaos", )

        
