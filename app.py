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

def generate_review(images):
    try:
        # Send all images together to the Gemini model for review
        prompt = """
        Assume the role of relationship coach and dating Expert. You are a 28yo dating expert, who has spent more than 8 years in online dating, you are known for giving very specific dating profile improvement tips unlike others who just give generic suggestions.
        1. Hi, {Name}!
        2. Overall view about their dating app profile.
        3. Rate their profile out of 10, be specific about the rating, don't give some random number, also include that many number of stars right next to the number.
        4. Body:
            - Pros of their profile and what stood out.
            - More Pros of their profile and what stood out.
            - Cons of their profile and what is not looking good.
            - More Cons about the profile i.e what they can improve.
        5. Suggestions: Include how they can improve their profile, give specific advice, not generic, give specific personalised tips
        6. In suggestions, be very specific, for example: change the cover photo, shuffle the images, change the prompt, change your bio, remove that photo, add some specific type of photo. Give these tips looking at their intersts and their entire profile.
        Ensure that the Review is overall understandable and easy to implementable. The tips and review should be on-point. No beating around the bush.
        """
        response = model_text.generate_content([prompt] + images)
        return response.text.strip()

    except Exception as e:
        st.error(f"An error occurred while generating the review: {e}")
        return 'No response'

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

        review = generate_review(images)

        if images:
            # Display all uploaded images
            for img in images:
                st.image(img, caption="Uploaded Image")

            if review:
                st.subheader("Profile Review")
                st.write(review)

if __name__ == "__main__":
    main()

