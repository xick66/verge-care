import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize API key and GenerativeModel
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("API key not found. Please make sure it is set in the .env file.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)
    model_text = genai.GenerativeModel("gemini-1.5-pro-latest")

def load_prompt(prompt_file_path):
    with open(prompt_file_path, "r") as file:
        return file.read()

def generate_review_and_rating(images):
    try:
        # Send all images together to the Gemini model for review and rating
        prompt = "Please review this dating profile and provide a rating and feedback."
        response = model_text.generate_content([prompt] + images)

        # Extract the rating and review from the response
        response_text = response.text.strip()
        rating = None
        review = None

        # Simple parsing logic to extract rating and review from the response
        if "Rating:" in response_text:
            parts = response_text.split("Rating:")
            rating_part = parts[1].split("\n")[0].strip()
            try:
                rating = int(rating_part)
            except ValueError:
                rating = "Invalid rating format"

            review = parts[1].split("\n", 1)[1].strip()

        return rating, review

    except Exception as e:
        st.error(f"An error occurred while generating the review and rating: {e}")
        return None, None

def main():
    st.set_page_config(page_title="ProfileMagic", 
                   page_icon="images/logo.png",
                   layout="wide",
                   initial_sidebar_state="expanded"
                   )
    st.title("👋Welcome to ProfileMagic!")

    st.markdown("Upload your dating app profile images, and get a detailed review and rating.")
    st.markdown("Let's optimize your dating profile and boost your success. **Get started now!**")
    st.markdown('___')

    uploaded_files = st.file_uploader("Upload your dating profile images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        images = [Image.open(file) for file in uploaded_files]

        rating, review = generate_review_and_rating(images)

        if images:
            # Display all uploaded images
            for img in images:
                st.image(img, caption="Uploaded Image")
            
            if rating is not None:
                st.write("____")
                st.write(f"⭐ {rating}/10")

            if review:
                st.subheader("Profile Review")
                st.write(review)

if __name__ == "__main__":
    main()
