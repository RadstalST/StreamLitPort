import os
import streamlit as st
from PIL import Image
import openai
from dotenv import load_dotenv

load_dotenv()

# Set OpenAI API key

# Function to generate DALL-E image URL
def generate_dalle_image(PROMPT):
    response = openai.Image.create(
        prompt=PROMPT,
        n=1,
        size="256x256",
    )
    url = response["data"][0]["url"]
    return url

# Streamlit app
st.title("DALL-E Image Generator")

# Check if API key is provided
if os.getenv("OPENAI_API_KEY"):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
else:
    st.write("Please provide OPENAI_API_KEY in .env file")
    OPENAI_API_KEY = st.text_input("OPENAI API_KEY", type="password")

# Check if all required inputs are provided
if OPENAI_API_KEY:
    topic = st.text_input("Topic", placeholder="e.g. climate change")
    context = st.text_area("Context", placeholder="1. What is the problem?\n2. Why is it important?\n3. What is the solution?")
    target_audience = st.text_input("Target Audience", placeholder="e.g. policymakers, scientists, general public")
    openai.api_key = OPENAI_API_KEY

    st.divider()

    # Initialize DALL-E image URL with default values
    dalle_image_urls = ["https://pbs.twimg.com/media/E1c0iM9WUAMN7pF.jpg"] * 3

    with st.container():
        if topic and context and target_audience:
            markdown_response = f"# Title\n\nLorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum."

            st.markdown(markdown_response, unsafe_allow_html=False, help=None)

            for i in range(3):
                dalle_prompt = f"generate a prompt to be used with DALLE image generation based on the following post:\n\n{markdown_response}"
                url = generate_dalle_image(dalle_prompt)
                dalle_image_urls[i] = url

            cols = st.columns(3)

            for i, col in enumerate(cols):
                with col:
                    st.image(dalle_image_urls[i], caption=f'Index {i}')

        else:
            st.warning("Please provide a topic, context, and target audience")
