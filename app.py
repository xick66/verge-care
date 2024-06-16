import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Initialize API key and GenerativeModel
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("API key not found. Please make sure it is set in the .env file.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)
    model_text = genai.GenerativeModel("gemini-1.5-pro-latest")

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
    st.set_page_config(page_title="Verge", 
                       page_icon="🖤",
                       layout="wide",
                       initial_sidebar_state="collapsed")
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        body {
            background-color: #0a0a0a;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .hero {
            background: linear-gradient(145deg, #ff004f, #200122);
            padding: 80px 0;
            text-align: center;
            border-radius: 15px;
        }
        .hero h1 {
            font-size: 3.5em;
            color: #ffffff;
        }
        .hero p {
            font-size: 1.5em;
            color: #ffdddd;
        }
        .hero .upload-button {
            background-color: #ff004f;
            border: none;
            color: white;
            padding: 15px 30px;
            font-size: 1.2em;
            cursor: pointer;
            border-radius: 10px;
            margin-top: 20px;
        }
        .section {
            margin: 50px 0;
            text-align: center;
        }
        .section h2 {
            font-size: 2.5em;
            color: #ff004f;
        }
        .section p {
            font-size: 1.2em;
            color: #dddddd;
        }
        .cards {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 20px;
        }
        .card {
            background: #151515;
            padding: 20px;
            border-radius: 10px;
            width: 300px;
            text-align: left;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .card h3 {
            font-size: 1.5em;
            color: #ff004f;
        }
        .card p {
            font-size: 1em;
            color: #cccccc;
        }
        .testimonial {
            background: linear-gradient(145deg, #200122, #ff004f);
            padding: 50px;
            border-radius: 15px;
            margin: 50px 0;
        }
        .testimonial h2 {
            color: #ffffff;
        }
        .testimonial p {
            font-size: 1.2em;
            color: #ffdddd;
        }
        .footer {
            background: #0a0a0a;
            padding: 20px;
            text-align: center;
            color: #ffdddd;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
        <div class="hero">
            <h1>Welcome to Verge</h1>
            <p>AI-Powered Dating Profile Reviews</p>
            <form action="#">
                <input type="file" id="fileInput" multiple class="upload-button" accept="image/*">
            </form>
        </div>
    """, unsafe_allow_html=True)

    # Features Section
    st.markdown("""
        <div class="section">
            <h2>How It Works</h2>
            <div class="cards">
                <div class="card">
                    <h3>Upload Images</h3>
                    <p>Upload your dating profile pictures directly on our platform.</p>
                </div>
                <div class="card">
                    <h3>AI Analysis</h3>
                    <p>Our AI analyzes your profile and gives detailed feedback.</p>
                </div>
                <div class="card">
                    <h3>Get Feedback</h3>
                    <p>Receive personalized tips to improve your dating profile.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Testimonial Section
    st.markdown("""
        <div class="testimonial">
            <h2>What Our Users Say</h2>
            <p>"Verge transformed my dating profile! The tips were specific and extremely helpful."</p>
            <p>"The AI feedback was spot on and helped me attract more matches."</p>
        </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div class="footer">
            <p>&copy; 2024 Verge. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)

    # Upload Images
    uploaded_files = st.file_uploader("Upload your dating profile images", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="fileInput", label_visibility="collapsed")

    if uploaded_files:
        with st.spinner("Cooking, wait...takes 5-10 secs usually"):
            images = [Image.open(file) for file in uploaded_files]
            time.sleep(5)  # Simulate loading time
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
