# DEPENDENCIES 
from dotenv import load_dotenv
load_dotenv()  # load all env variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image



genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # getting the api key

# MAKING RESPONSE USING GEMINI
def get_gemini_response(input, image, prompt): 
    model = genai.GenerativeModel("gemini-pro-vision") # load the model
    response = model.generate_content([input, image[0], prompt])
    return response.text


# SETUP THE IMAGE FOR THE INPUTTING THE MODEL
def input_image_setup(uploaded_file): 
    if uploaded_file is not None: # if file is uploaded
        # read the file into bytes, images into numbers
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
                }
            ]
        return image_parts
    else:
        raise FileNotFoundError("File not Found")

    

# INITIALISE THE APP
st.set_page_config(page_title="Master-Chef Ai")
st.header(':blue[Be a Cookiee]')
input = st.text_input("Input Prompt :  Optional", key="input")
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None: #if image uploaded
    image = Image.open(uploaded_file)
    st.image(image, caption="Image Uploaded", width=500 ) # to show the image
    
    
submit = st.button("CHECK") # submit button
 
 # prompt to Gemini Ai for showing the result
input_prompt = """
Make response only when it is food items.
What is in the picture.
You are a cooking specialist. Describe me how to make the dish
"""

if submit: # if clicked submit
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input) # make response
    st.subheader("The Response is...")
    st.write(response)  # to show response in the window