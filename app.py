import streamlit as st
import fitz
from PIL import Image
import io
import json
import google.generativeai as genai
import os
import pyperclip
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize API key and GenerativeModel
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("API key not found. Please make sure it is set in the .env file.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)
    model_vision = genai.GenerativeModel('gemini-pro-vision')
    model_text = genai.GenerativeModel("gemini-1.5-pro-latest")

# Paths
INTERMEDIATE_JSON_PATH = "temp.json"

def load_prompt(prompt_file_path):
    with open(prompt_file_path, "r") as file:
        return file.read()

# Function to process PDF and extract content
def process_pdf_and_save_profile_desc(uploaded_file):
    if not uploaded_file:
        return None, "No file provided"

    try:
        # Read the PDF content
        pdf_content = uploaded_file.read()

        # Convert PDF to image
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        page = doc.load_page(0)
        pix = page.get_pixmap()
        img_bytes = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_bytes))
        doc.close()

        # Further processing with the image
        prompt = load_prompt("prompts/profile_parsing_prompt.txt")
        response = model_vision.generate_content([prompt, image])
        
        json_data = response.text

        # Save the JSON data for other tabs to access
        with open(INTERMEDIATE_JSON_PATH, "w") as json_file:
            json.dump(json_data, json_file)

        return image, json_data

    except Exception as e:
        st.error(f"An error occurred while processing the PDF: {e}")
        return None, str(e)

def generate_rating(profile_data):
    try:
        prompt = load_prompt("prompts/ratings_prompt.txt").replace("profile_data", profile_data)
        responses = model_text.generate_content(prompt)
        return int(responses.text)
    except Exception as e:
        st.error(f"An error occurred while generating the rating: {e}")
        return 'No response'

def generate_profile_review(profile_description, profile_data):
    try:
        prompt = load_prompt("prompts/profile-reviewer.txt").replace(
            "{profile_description}", profile_description).replace("{json_data}", profile_data)
        response = model_text.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred while generating the profile review: {e}")
        return 'No response'

def main():
    st.set_page_config(page_title="ProfileMagic", 
                   page_icon="images/logo.png",
                   layout="wide",
                   initial_sidebar_state="expanded"
                   )
    st.title("👋Welcome to ProfileMagic!")

    st.markdown("Upload your dating app profile (PDF), and get a detailed review and rating.")
    st.markdown("Let's optimize your dating profile and boost your success. **Get started now!**")
    st.markdown('___')

    uploaded_file = st.file_uploader("Upload your dating profile (PDF)", type=["pdf"])

    if uploaded_file:
        image, json_data = process_pdf_and_save_profile_desc(uploaded_file)

        if json_data:
            st.image(image, caption="Processed PDF")
            st.subheader("Extracted JSON Content:")
            st.write(json_data)

            rating = generate_rating(json_data)
            st.write("____")
            st.write(f"⭐ {rating}/10")

            profile_description = st.text_area("Enter profile description", "This is a sample profile description.")
            if profile_description:
                review = generate_profile_review(profile_description, json_data)
                st.subheader("Profile Review")
                st.write(review)

if __name__ == "__main__":
    main()
