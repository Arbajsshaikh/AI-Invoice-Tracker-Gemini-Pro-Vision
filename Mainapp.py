from dotenv import load_dotenv
load_dotenv()  ## load all the environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai  
import re

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')  ## Load Gemini pro vision model

# Function to extract the content from image using Gemini
def get_gemini_response(input, image, user_prompt):
    response = model.generate_content([input, image[0], user_prompt])
    return response.text

# Function to handle file upload and return image details
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()  # Read the file into bytes
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# Initialize our Streamlit app
st.set_page_config(page_title="AI-Invoice Extractor")

st.header("Invoice Extractor")
input = st.text_input("Input your query (e.g., 'total dues', 'invoice number', etc.):", key="input")

# Multi-file uploader to allow uploading multiple invoices
uploaded_files = st.file_uploader("Choose images of invoices...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Store extracted data for each uploaded invoice
invoices_data = []

submit_button = st.button("Submit Query")
if uploaded_files and submit_button:
    st.subheader("General Query Results:")
    input_prompt = """
        You are an expert in understanding invoices. We will upload images as invoices, 
        and you will have to answer any questions based on the uploaded invoice image.
        """
    # Process each uploaded file
    for i in uploaded_files:
        # Process the image data and get the response
        image_data = input_image_details(i)
        
    # Handling other custom queries
        answer = get_gemini_response(input=input_prompt, image=image_data, user_prompt=input)
        pattern = r'(\d{2}-\d{2}-\d{4}|\d+\.\d{2})'
        matches = re.findall(pattern, answer)
        for match in matches:
            styled = f"<span style='font-size:20px; font-weight:bold'>{match}</span>"
            answer = answer.replace(match, styled)
        st.markdown(f"Answer for {i.name} based on your input: {answer}",unsafe_allow_html=True)



