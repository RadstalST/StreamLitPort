import requests
import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
load_dotenv()

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

# DALL-E API endpoint
API_ENDPOINT = "https://api.openai.com/v1/engines/davinci-codex/completions"

# Set your OpenAI API key
API_KEY = "YOUR_API_KEY"

# Helper function to generate DALL-E image
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
text_input = st.text_input("Enter your text prompt")
generate_button = st.button("Generate Image")

if generate_button:
    if text_input:
        try:
            url = generate_dalle_image(text_input)
            st.image(url, caption="Generated Image", use_column_width=True)
            st.success("Image generated successfully!")
            st.info(f"Image generated using DALL-E API {url}")
        except Exception as e:
            st.error(f"Error generating image: {e}")
    else:
        st.warning("Please enter a text prompt")
