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
                position: relative;
            }
            .hero-text {
                flex: 1;
                padding: 20px;
                text-align: left;
            }
            .animation-container {
                display: block;
                position: relative;
                width: 800px;
                max-width: 100%;
                margin: 0 auto;
            }
            .lightning-container {
                position: absolute;
                top: 50%;
                left: 0;
                display: flex;
                transform: translateY(-50%);
            }
            .lightning {
                position: absolute;
                display: block;
                height: 12px;
                width: 12px;
                border-radius: 12px;
                transform-origin: 6px 6px;
                animation-name: woosh;
                animation-duration: 1.5s;
                animation-iteration-count: infinite;
                animation-timing-function: cubic-bezier(0.445, 0.050, 0.550, 0.950);
                animation-direction: alternate;
            }
            .lightning.white {
                background-color: white;
                box-shadow: 0px 50px 50px 0px rgba(255, 255, 255, 0.7);
            }
            .lightning.red {
                background-color: #fc7171;
                box-shadow: 0px 50px 50px 0px rgba(252, 113, 113, 0.7);
                animation-delay: 0.2s;
            }
            .boom-container {
                position: absolute;
                display: flex;
                width: 80px;
                height: 80px;
                text-align: center;
                align-items: center;
                transform: translateY(-50%);
                left: 200px;
                top: -145px;
            }
            .shape {
                display: inline-block;
                position: relative;
                opacity: 0;
                transform-origin: center center;
            }
            .triangle {
                width: 0;
                height: 0;
                border-style: solid;
                transform-origin: 50% 80%;
                animation-duration: 1s;
                animation-timing-function: ease-out;
                animation-iteration-count: infinite;
                margin-left: -15px;
                border-width: 0 2.5px 5px 2.5px;
                border-color: transparent transparent #42e599 transparent;
                animation-name: boom-triangle;
            }
            .triangle.big {
                margin-left: -25px;
                border-width: 0 5px 10px 5px;
                border-color: transparent transparent #fade28 transparent;
                animation-name: boom-triangle-big;
            }
            .disc {
                width: 8px;
                height: 8px;
                border-radius: 100%;
                background-color: #d15ff4;
                animation-name: boom-disc;
                animation-duration: 1s;
                animation-timing-function: ease-out;
                animation-iteration-count: infinite;
            }
            .circle {
                width: 20px;
                height: 20px;
                animation-name: boom-circle;
                animation-duration: 1s;
                animation-timing-function: ease-out;
                animation-iteration-count: infinite;
                border-radius: 100%;
                margin-left: -30px;
            }
            .circle.white {
                border: 1px solid white;
            }
            .circle.big {
                width: 40px;
                height: 40px;
                margin-left: 0px;
            }
            .circle.big.white {
                border: 2px solid white;
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
                display: inline-block;
                width: 190px;
                height: 254px;
                border-radius: 20px;
                padding: 5px;
                box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
                background-image: linear-gradient(144deg,#AF40FF, #5B42F3 50%,#00DDEB);
                margin: 10px;
                animation: slide 10s infinite;
            }
            .card__content {
                background: rgb(5, 6, 45);
                border-radius: 17px;
                width: 100%;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                color: #fff;
            }
            .faq {
                margin: 30px 0;
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
                margin-top: 10px;
            }
            .faq-answer {
                display: none;
                padding: 10px;
                background-color: #333;
                color: white;
                border-radius: 5px;
                margin-top: 10px;
            }
            footer {
                text-align: center;
                padding: 20px 0;
                background: #000;
                color: #fff;
                border-top: 1px solid #ff0000;
            }
            @keyframes woosh {
                0% { width: 12px; transform: translate(0px, 0px) rotate(-35deg); }
                15% { width: 50px; }
                30% { width: 12px; transform: translate(214px, -150px) rotate(-35deg); }
                30.1% { transform: translate(214px, -150px) rotate(46deg); }
                50% { width: 110px; }
                70% { width: 12px; transform: translate(500px, 150px) rotate(46deg); }
                70.1% { transform: translate(500px, 150px) rotate(-37deg); }
                85% { width: 50px; }
                100% { width: 12px; transform: translate(700px, 0) rotate(-37deg); }
            }
            @keyframes boom-circle {
                0% { opacity: 0; }
                5% { opacity: 1; }
                30% { opacity: 0; transform: scale(3); }
                100% {}
            }
            @keyframes boom-triangle-big {
                0% { opacity: 0; }
                5% { opacity: 1; }
                40% { opacity: 0; transform: scale(2.5) translate(50px, -50px) rotate(360deg); }
                100% {}
            }
            @keyframes boom-triangle {
                0% { opacity: 0; }
                5% { opacity: 1; }
                30% { opacity: 0; transform: scale(3) translate(20px, 40px) rotate(360deg); }
                100% {}
            }
            @keyframes boom-disc {
                0% { opacity: 0; }
                5% { opacity: 1; }
                40% { opacity: 0; transform: scale(2) translate(-70px, -30px); }
                100% {}
            }
            @keyframes slide {
                0% { transform: translateX(0); }
                50% { transform: translateX(-100%); }
                100% { transform: translateX(0); }
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
                <div class="card__content">
                    Verge User
                    <p>The AI insights were amazing. My profile looks much better now! By Chris 6 days ago</p>
                </div>
            </div>
            <div class="testimonial">
                <div class="card__content">
                    Verge User
                    <p>I got great tips that helped me get more matches. By Sam 2 days ago</p>
                </div>
            </div>
            <div class="testimonial">
                <div class="card__content">
                    Verge User
                    <p>Highly recommend Verge for anyone looking to improve their dating profile. By Pat 7 days ago</p>
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
