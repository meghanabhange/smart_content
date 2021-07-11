import json
import random
import string
import time
from pathlib import Path

import pandas as pd
import pke
import speech_recognition as sr
import streamlit as st
import wikipedia
from nltk.corpus import stopwords
from pydub import AudioSegment, silence
from pydub.playback import play

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
                execcode = [line[4:] for line in codelines if line[:3] == ">>>"]
                outputcode = [line for line in codelines if line[:3] != ">>>"]
                execcode = "\n".join(execcode)
                outputcode = "\n".join(outputcode)
                st.code(execcode)
                st.text(outputcode)
                # content = st_ace(execcode, key=code, language="python", theme="chaos", )
                
        st.write("Raw Json")
        st.write(ctx)

        r = sr.Recognizer()
        mic_list = sr.Microphone.list_microphone_names()
        mic_name = mic_list[0]
        st.sidebar.success(f"Using {mic_name}")
        st.sidebar.title("Wikipedia Query Answering System")
        st.sidebar.write("If you have any query about the content on this page, you can use the 'Ask Wikipedia' button to ask an audio query and we will find an answer for you from wikipedia.")

        sample_rate = 48000

        chunk_size = 2048

        with sr.Microphone(
            device_index=0, sample_rate=sample_rate, chunk_size=chunk_size
        ) as source:
            r.adjust_for_ambient_noise(source)

            if st.sidebar.button("Ask An Audio Query to Wikipedia"):
                audio = r.listen(source)

                try:
                    text = r.recognize_google(audio)
                    st.sidebar.success("you said: " + text)
                    if text : 
                        st.sidebar.success(
                            f"Hey, I found wikipedia information about {text}"
                        )
                        summary, url = get_wikipedia(text)
                        context = summary
                        st.sidebar.markdown("### Wikipedia Summary:")
                        st.sidebar.write(summary)
                        st.sidebar.write(f"Read more on wikipedia : {url}")

                except sr.UnknownValueError:
                    st.sidebar.write(
                        "Google Speech Recognition could not understand audio"
                    )

                except sr.RequestError as e:
                    st.sidebar.write(
                        "Could not request results from Google Speech Recognition service; {0}".format(
                            e
                        )
                    )
