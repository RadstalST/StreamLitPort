import os

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

#plan and execute agent
from langchain.experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner

# import dotenv
from dotenv import load_dotenv
load_dotenv()

# prompt template
title_template = PromptTemplate(
    input_variables=["topic"],
    template = 'Write a youtube video title about {topic}.',
)

script_template = PromptTemplate(
    input_variables=["title","wikipedia_research"],
    template = 'Write a youtube video script based on {title} based on the following research: {wikipedia_research}.',
)

# memory
title_memory = ConversationBufferMemory(
    input_key="topic",
    memory_key="chat_memory",
)
script_memory = ConversationBufferMemory(
    input_key="title",
    memory_key="chat_memory",
)

llm = OpenAI(temperature=0.9)
title_chain = LLMChain(llm=llm, prompt=title_template,verbose=True,output_key="title",memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_template,verbose=True,output_key="script",memory=script_memory)

wiki = WikipediaAPIWrapper()


st.title("LangChain")
st.subheader("A tool for generating text using GPT-3")

prompt = st.text_input("Topic that you want to write about:")
if prompt:

    title = title_chain.run(prompt)
    wikiknowledge = wiki.run(prompt)
    script = script_chain.run(title=title,wikipedia_research=wikiknowledge)

    st.title("title")
    st.write(title)

    st.title("script")
    st.write(script)

    # expander
    with st.expander("title history"):
        st.info(script_memory.buffer)
    with st.expander("script history"):
        st.info(script_memory.buffer)
    with st.expander("wiki history"):
        st.info(wikiknowledge)
