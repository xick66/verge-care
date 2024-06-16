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
                padding: 100px 0;
                background: linear-gradient(135deg, #ff0000, #000);
                border-radius: 15px;
                margin-bottom: 30px;
                position: relative;
            }
            .hero h1 {
                font-size: 48px;
                margin-bottom: 20px;
            }
            .hero p {
                font-size: 18px;
                margin-bottom: 30px;
            }
            .animation-container {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 100%;
                height: 100%;
                z-index: -1;
            }
            .testimonial-section {
                position: relative;
                padding: 50px 0;
            }
            .testimonial-row {
                display: flex;
                overflow: hidden;
                white-space: nowrap;
                margin: 0 auto;
                padding: 20px 0;
                width: 100%;
                position: relative;
            }
            .testimonial-row::before, .testimonial-row::after {
                content: '';
                position: absolute;
                top: 0;
                bottom: 0;
                width: 100px;
                background: linear-gradient(to left, transparent, #000);
                z-index: 1;
            }
            .testimonial-row::after {
                right: 0;
                transform: rotate(180deg);
            }
            .testimonial {
                width: 300px;
                height: 200px;
                background: linear-gradient(144deg, #AF40FF, #5B42F3 50%, #00DDEB);
                border-radius: 20px;
                padding: 5px;
                margin-right: 20px;
                box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #fff;
                font-size: 14px;
                white-space: normal;
            }
            @keyframes slide {
                0% { transform: translateX(100%); }
                100% { transform: translateX(-100%); }
            }
            @keyframes slide-reverse {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }
            .faq {
                padding: 20px;
                background: #111;
                border-radius: 10px;
                margin: 20px 0;
            }
            .faq h2 {
                margin-bottom: 10px;
            }
            .faq button {
                width: 100%;
                background: #222;
                color: #fff;
                border: none;
                padding: 10px;
                margin-bottom: 5px;
                text-align: left;
                cursor: pointer;
                font-size: 16px;
                border-radius: 5px;
            }
            .faq button:hover {
                background: #333;
            }
            .faq-answer {
                background: #333;
                padding: 10px;
                border-radius: 5px;
                display: none;
                margin-bottom: 10px;
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
            <div class="animation-container">
                <div class="lightning-container">
                    <div class="lightning white"></div>
                    <div class="lightning red"></div>
                </div>
                <div class="boom-container">
                    <div class="shape circle big white"></div>
                    <div class="shape circle white"></div>
                    <div class="shape triangle big yellow"></div>
                    <div class="shape disc white"></div>
                    <div class="shape triangle blue"></div>
                </div>
                <div class="boom-container second">
                    <div class="shape circle big white"></div>
                    <div class="shape circle white"></div>
                    <div class="shape disc white"></div>
                    <div class="shape triangle blue"></div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # File uploader
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

    # Testimonials Section
    st.markdown("""
        <div class="testimonial-section">
            <div class="testimonial-row" style="animation: slide 15s linear infinite;">
                <div class="testimonial">
                    <div class="card__content">
                        Verge User
                        <p>verge's tips transformed my profile, now it's lit! - pat 2 days ago</p>
                    </div>
                </div>
                <div class="testimonial">
                    <div class="card__content">
                        Verge User
                        <p>can't believe how easy it was to improve my profile. - sam 4 days ago</p>
                    </div>
                </div>
                <div class="testimonial">
                    <div class="card__content">
                        Verge User
                        <p>thanks verge, more matches than ever! - taylor 3 days ago</p>
                    </div>
                </div>
                <div class="testimonial">
                    <div class="card__content">
                        Verge User
                        <p>ai insights were amazing. profile looks better now! - chris 6 days ago</p>
                    </div>
                </div>
            </div>
            <div class="testimonial-row" style="animation: slide-reverse 15s linear infinite;">
                <div class="testimonial">
                    <div class="card__content">
                        Verge User
                        <p>verge's tips transformed my profile, now it's lit! - pat 2 days ago</p>
                    </div>
                </div>
                <div class="testimonial">
                    <div class="card__content">
                        Verge User
                        <p>can't believe how easy it was to improve my profile. - sam 4 days ago</p>
                    </div>
                </div>
                <div class="testimonial">
                    <div class="card__content">
                        Verge User
                        <p>thanks verge, more matches than ever! - taylor 3 days ago</p>
                    </div>
                </div>
                <div class="testimonial">
                    <div class="card__content">
                        Verge User
                        <p>ai insights were amazing. profile looks better now! - chris 6 days ago</p>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # FAQ Section
    st.markdown("""
        <div class="faq">
            <h2>Frequently Asked Questions</h2>
            <button onclick="toggleAnswer('faq1')">What is Verge?</button>
            <div class="faq-answer" id="faq1">
                Verge is an AI-powered platform that helps you optimize your dating profile by providing detailed reviews and personalized tips.
            </div>
            <button onclick="toggleAnswer('faq2')">How does Verge work?</button>
            <div class="faq-answer" id="faq2">
                Upload your dating profile images, and our AI will analyze them to provide you with specific improvement tips to enhance your profile.
            </div>
            <button onclick="toggleAnswer('faq3')">Is Verge free to use?</button>
            <div class="faq-answer" id="faq3">
                Verge offers both free and premium plans. The free plan includes basic features, while the premium plan provides more advanced insights and tips.
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
