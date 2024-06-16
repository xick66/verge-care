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
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .hero-text {
                flex: 1;
                padding: 20px;
            }
            .cards {
                display: flex;
                justify-content: space-around;
                flex-wrap: wrap;
                margin-bottom: 30px;
            }
            .feature-card {
                background: rgba(255, 0, 0, 0.1);
                border: 1px solid #ff0000;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                width: 300px;
                text-align: center;
            }
            .testimonial {
                background: rgba(0, 0, 0, 0.5);
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                width: 300px;
                text-align: center;
                animation: slide 10s infinite;
                color: #fff;
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
            .faq button {
                background-color: #ff0000;
                color: white;
                border: none;
                padding: 10px;
                text-align: left;
                width: 100%;
                cursor: pointer;
                font-size: 16px;
            }
            .faq-answer {
                display: none;
                padding: 10px;
                background-color: #333;
                color: white;
                border-radius: 5px;
            }
            .faq button.active + .faq-answer {
                display: block;
            }
        </style>
        <script>
            function toggleAnswer(id) {
                var answer = document.getElementById(id);
                if (answer.style.display === "block") {
                    answer.style.display = "none";
                } else {
                    answer.style.display = "block";
                }
            }
        </script>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
        <div class="hero">
            <div class="hero-text">
                <h1>Welcome to Verge</h1>
                <p>Optimize your dating profile with AI-powered reviews and personalized tips.</p>
            </div>
            <div class="card">
                <p class="heading">Popular this month</p>
                <p>Powered By</p>
                <p>Uiverse</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # File uploader
    uploaded_files = st.file_uploader("Upload your dating profile images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

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
            <div class="feature-card">
                <h3>AI-Powered Reviews</h3>
                <p>Get detailed reviews of your dating profile with specific improvement tips.</p>
            </div>
            <div class="feature-card">
                <h3>Personalized Feedback</h3>
                <p>Receive personalized feedback tailored to your profile and interests.</p>
            </div>
            <div class="feature-card">
                <h3>Easy to Use</h3>
                <p>Upload your images and get instant feedback with actionable tips.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Testimonials Section
    st.markdown("""
        <div class="cards">
            <div class="testimonial">
                <div class="card">
                    <p class="heading">Verge User</p>
                    <p>The AI insights were amazing. My profile looks much better now!</p>
                    <p>By Chris 6 days ago</p>
                </div>
            </div>
            <div class="testimonial">
                <div class="card">
                    <p class="heading">Verge User</p>
                    <p>I got great tips that helped me get more matches.</p>
                    <p>By Sam 2 days ago</p>
                </div>
            </div>
            <div class="testimonial">
                <div class="card">
                    <p class="heading">Verge User</p>
                    <p>Highly recommend Verge for anyone looking to improve their dating profile.</p>
                    <p>By Pat 7 days ago</p>
                </div>
            </div>
        </div>
        <div class="cards">
            <div class="testimonial">
                <div class="card">
                    <p class="heading">Verge User</p>
                    <p>Verge transformed my dating profile! The tips were specific and extremely helpful.</p>
                    <p>By Alex 4 days ago</p>
                </div>
            </div>
            <div class="testimonial">
                <div class="card">
                    <p class="heading">Verge User</p>
                    <p>The AI feedback was spot on and helped me attract more matches.</p>
                    <p>By Jamie 3 days ago</p>
                </div>
            </div>
            <div class="testimonial">
                <div class="card">
                    <p class="heading">Verge User</p>
                    <p>Thanks to Verge, my profile now stands out and I've received more matches!</p>
                    <p>By Taylor 5 days ago</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # FAQ Section
    st.markdown("""
        <div class="faq">
            <h2>Frequently Asked Questions</h2>
            <button onclick="toggleAnswer('answer1')">What is Verge?</button>
            <div id="answer1" class="faq-answer">
                Verge is an AI-powered platform that provides detailed reviews and personalized tips to optimize your dating profile.
            </div>
            <button onclick="toggleAnswer('answer2')">How does it work?</button>
            <div id="answer2" class="faq-answer">
                Simply upload your dating profile images, and our AI will analyze them to provide specific improvement tips.
            </div>
            <button onclick="toggleAnswer('answer3')">Is Verge free to use?</button>
            <div id="answer3" class="faq-answer">
                Yes, Verge offers a free plan with basic features. Premium plans are also available for more advanced features.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <footer>
            <p>&copy; 2023 Verge. All rights reserved.</p>
        </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
