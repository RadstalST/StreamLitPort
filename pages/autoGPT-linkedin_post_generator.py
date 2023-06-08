import os

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

from langchain.experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
# import dotenv
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

from dotenv import load_dotenv
load_dotenv()

def generate_dalle_image(PROMPT):
    
    response = openai.Image.create(
        prompt=PROMPT,
        n=1,
        size="256x256",
    )

    url = response["data"][0]["url"]
    return url
# prompt template
linkedin_post_template = PromptTemplate(
    input_variables=["topic","context","target_audience","wiki_knowledge"],
    template = '''
    Write a linked in video post title about {topic} based on th following context: 
    {context}
    and based on the knowledge from wikipedia:
    {wiki_knowledge}
    , write a linkedin post in markdown format
    for {target_audience}.
    ''',
)

dalle_prompt_template = PromptTemplate(
    input_variables=["post"],
    template = '''
    generate DALLE image generation prompt based on:
    {post}

    that would be suitable for background image and is realisitc
    ''',
)
title_prompt_template = PromptTemplate(
    input_variables=["post"],
    template = '''
    Generate a very short title for the post {post}
    that would be suitable image caption
    ''',
)
subtitle_prompt_template = PromptTemplate(
    input_variables=["post"],
    template = '''
    Generate a very short subtitle for the post {post}
    that would be suitable image caption
    ''',
)
caption_prompt_template = PromptTemplate(
    input_variables=["post"],
    template = '''
    Generate  a very short caption for the post {post}
    that would be suitable image caption
    ''',
)

# linkedin_template = PromptTemplate(
#     input_variables=["topic"],
#     template = 'Write a youtube video title about {topic}.',
# )

#memory
linkedin_post_memory = ConversationBufferMemory(
    input_key="topic",
    memory_key="chat_memory",
)
linkedin_post_memory2 = ConversationBufferMemory(
    input_key="post",
    memory_key="chat_memory",
)

st.title("Linkedin Post Generator")
'''This Streamlit page features a LinkedIn post generator. The page allows you to generate LinkedIn post titles based on a given topic, context, target audience, and knowledge from Wikipedia.

The page begins by prompting you to provide your OpenAI API key, either by entering it directly or by providing it in a .env file. Once the API key is provided, you can proceed with generating the LinkedIn post.

You will be prompted to enter the topic, context, and target audience for the LinkedIn post. The context should include information about the problem, its importance, and the proposed solution. Additionally, the generator utilizes knowledge from Wikipedia to enhance the post.

After filling in the required inputs, the page generates a markdown-formatted LinkedIn post based on the provided information. The generated post will be displayed, and you can copy and use it for your LinkedIn profile.'''

if os.getenv("OPENAI_API_KEY"):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
else:
    st.write("Provided an OPENAI_API_KEY in .env file")
    OPENAI_API_KEY = st.text_input("OPENAI API_KEY",type="password")

if OPENAI_API_KEY:
    #model and chains 
    llm = OpenAI(temperature=0.9)
    post_chain = LLMChain(llm=llm, prompt=linkedin_post_template,verbose=True,output_key="title",memory=linkedin_post_memory)
    dalle_chain = LLMChain(llm=llm, prompt=dalle_prompt_template,verbose=True,output_key="prompt")
    title_chain = LLMChain(llm=llm, prompt=title_prompt_template,verbose=True,output_key="title",memory=linkedin_post_memory2)
    subtitle_chain = LLMChain(llm=llm, prompt=subtitle_prompt_template,verbose=True,output_key="subtitle",memory=linkedin_post_memory2)
    caption_chain = LLMChain(llm=llm, prompt=caption_prompt_template,verbose=True,output_key="caption",memory=linkedin_post_memory2)


    wiki = WikipediaAPIWrapper()
    

topic = st.text_input("Topic",value="Climate Change",placeholder="e.g. climate change")
context = st.text_area("context",value="Caged animal or Free Range",placeholder="1. What is the problem?\n2. Why is it important?\n3. What is the solution?")
target_audience = st.text_input("Target Audience",value="general public",placeholder="e.g. policymakers, scientists, general public")


st.divider()

dalle_image_url = {i:"https://pbs.twimg.com/media/E1c0iM9WUAMN7pF.jpg" for i in range(3)}

@st.cache_data
def open_ai_generation(topic,context,target_audience):
    images =  dalle_image_url
    markdown_response = post_chain.run(
            topic=topic,
            context=context,
            target_audience=target_audience,
            wiki_knowledge=wiki.run(topic)
            )
        
    for i in range(3):
        dalle_prompt = dalle_chain.run(post=markdown_response)
        url = generate_dalle_image(dalle_prompt)
        images[i] = url
    titles = [ title_chain.run(post=markdown_response) for i in range(3)]
    sub_titles = [ subtitle_chain.run(post=markdown_response) for i in range(3)]
    captions = [ caption_chain.run(post=markdown_response) for i in range(3)]

    return markdown_response,images,titles,sub_titles,captions


with st.container():
    if OPENAI_API_KEY and topic and context and target_audience:
        markdown_response,dalle_image_url,titles,sub_titles,captions= open_ai_generation(topic,context,target_audience)
        st.markdown(markdown_response)
    else: 
        titles = ["","",""]
        sub_titles = ["","",""]
        captions = ["","",""]
        st.write("Please provide a topic, context and target audience")
        #template markdown
       
cols = st.columns(3)
for i,col in enumerate(cols):
    with col:
        st.image(
            dalle_image_url[i], 
            caption=f'index {i}'
            )
                
st.divider()
st.title("Post Images Customization")

image_index = st.radio("image index", [0,1,2], index=0)
setting_cols = st.columns(2)


with setting_cols[0]:
    main_title = st.selectbox("Main Title", titles, index=0, label_visibility="visible")
    sub_title = st.selectbox("Subtitle", sub_titles, index=0, label_visibility="visible")
    caption = st.selectbox("Caption", captions, index=0, label_visibility="visible")

with setting_cols[1]:
    gradient_col = st.columns(2)
    with gradient_col[0]:
        first_color = st.color_picker("gradient1", value="#F00", key=None, help=None, on_change=None,
                                    args=None, kwargs=None, disabled=False, label_visibility="visible")
    with gradient_col[1]:
        second_color = st.color_picker("gradient2", value="#00F", key=None, help=None, on_change=None,
                                    args=None, kwargs=None, disabled=False, label_visibility="visible")
    angle = st.slider("angle", value=45, min_value=0, max_value=360, disabled=False, label_visibility="visible")
    opacity = st.slider("opacity", value=0.5, min_value=0.0, max_value=1.0, step=0.05, disabled=False,
                        label_visibility="visible")

html_code = f'''
    <style>
        .container {{
            position: relative;
            width: 100%;
            padding-top: 100%; /* Maintain a 1:1 aspect ratio */
            background: url('{dalle_image_url[image_index]}') no-repeat center/cover;
        }}

        .overlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient({angle}deg,{first_color}, {second_color});
            opacity: {opacity};
        }}

        .content {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: white;
            font-family: sans-serif;
            font-size: 0.5rem;
        }}
    </style>

    <div class="container">
        <div class="overlay"></div>
        <div class="content">
            <h1>{main_title.replace('"',"")}</h1>
            
        </div>
    </div>
'''

st.components.v1.html(html_code, width=400, height=400, scrolling=False)
