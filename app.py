import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from io import BytesIO
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
    st.set_page_config(page_title="Verge", layout="wide")

    # Custom CSS for styling
    st.markdown("""
        <style>
            body {
                background-color: #000;
                color: #fff;
                font-family: 'Arial', sans-serif;
            }
            .main {
                background-color: #000;
                color: #fff;
            }
            .stButton>button {
                background-color: #ff0000;
                color: #fff;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
            }
            .stButton>button:hover {
                background-color: #cc0000;
            }
            .hero {
                text-align: center;
                padding: 50px 0;
                background: linear-gradient(135deg, #ff0000, #000);
                border-radius: 15px;
                margin-bottom: 30px;
            }
            .hero h1 {
                font-size: 48px;
                margin-bottom: 20px;
            }
            .hero p {
                font-size: 18px;
                margin-bottom: 30px;
            }
            .cards {
                display: flex;
                justify-content: space-around;
                flex-wrap: wrap;
                margin-bottom: 30px;
            }
            .card {
                background: rgba(255, 0, 0, 0.1);
                border: 1px solid #ff0000;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                width: 300px;
                text-align: center;
            }
            .testimonial {
                background: rgba(255, 0, 0, 0.1);
                border: 1px solid #ff0000;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                width: 300px;
                text-align: center;
                animation: slide 10s infinite;
            }
            @keyframes slide {
                0% { transform: translateX(0); }
                50% { transform: translateX(-100%); }
                100% { transform: translateX(0); }
            }
            footer {
                text-align: center;
                padding: 20px 0;
                background: #000;
                color: #fff;
                border-top: 1px solid #ff0000;
            }
        </style>
    """, unsafe_allow_html=True)

    # Hero Section with Custom Upload Button
    st.markdown("""
        <div class="hero">
            <h1>Welcome to Verge</h1>
            <p>Optimize your dating profile with AI-powered reviews and personalized tips.</p>
            <div style="margin-top: 20px;">
                <input type="file" id="file-upload" accept="image/*" multiple style="display:none" onchange="document.getElementById('upload-text').innerHTML = 'Files selected: ' + this.files.length;">
                <label for="file-upload" class="stButton">
                    <button id="upload-button">Upload Images</button>
                </label>
                <p id="upload-text" style="color: white;"></p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # File uploader
    uploaded_files = st.file_uploader("", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="file-upload")

    if uploaded_files:
        images = [Image.open(file) for file in uploaded_files]
        st.image(images, caption="Uploaded Images", use_column_width=True)

        with st.spinner("Cooking, wait...takes 5-10 secs usually"):
            review = generate_review(images)

            if review:
                st.subheader("Profile Review")
                st.write(review)

    # Features Section
    st.markdown("""
        <div class="cards">
            <div class="card">
                <h3>AI-Powered Reviews</h3>
                <p>Get detailed reviews of your dating profile with specific improvement tips.</p>
            </div>
            <div class="card">
                <h3>Personalized Feedback</h3>
                <p>Receive personalized feedback tailored to your profile and interests.</p>
            </div>
            <div class="card">
                <h3>Easy to Use</h3>
                <p>Upload your images and get instant feedback with actionable tips.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Testimonials Section
    st.markdown("""
        <div class="cards">
            <div class="testimonial">
                <p>"Verge helped me improve my dating profile significantly. The tips were spot on!"</p>
                <p>- Alex</p>
            </div>
            <div class="testimonial">
                <p>"I love how easy it is to use Verge. The feedback was very specific and helpful."</p>
                <p>- Jamie</p>
            </div>
            <div class="testimonial">
                <p>"Thanks to Verge, my profile now stands out and I've received more matches!"</p>
                <p>- Taylor</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <footer>
            <p>&copy; 2024 Verge. All rights reserved.</p>
        </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
