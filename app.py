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
        6. In suggestions, be very specific, for example: change the cover photo, shuffle the images, change the prompt, change your bio, remove that photo, add some specific type of photo. Give these tips looking at their interests and their entire profile.
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
            .testimonial-section {
                position: relative;
                overflow: hidden;
                padding: 50px 0;
                margin-top: 50px;
                background-color: #000;
            }
            .testimonial-section::before,
            .testimonial-section::after {
                content: '';
                position: absolute;
                top: 0;
                bottom: 0;
                width: 50px;
                background: linear-gradient(to right, rgba(0, 0, 0, 1), rgba(0, 0, 0, 0));
                z-index: 1;
            }
            .testimonial-section::after {
                right: 0;
                left: auto;
                background: linear-gradient(to left, rgba(0, 0, 0, 1), rgba(0, 0, 0, 0));
            }
            .testimonial-row {
                display: flex;
                white-space: nowrap;
                animation: slide 20s linear infinite;
                gap: 30px;
                padding: 20px 0;
            }
            .testimonial-row:nth-child(2) {
                animation: slide-reverse 20s linear infinite;
            }
            .testimonial {
                display: inline-block;
                width: 300px;
                height: 150px;
                border-radius: 20px;
                padding: 10px;
                box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
                background-image: linear-gradient(144deg, #AF40FF, #5B42F3 50%, #00DDEB);
                color: white;
                font-size: 16px;
                text-align: center;
            }
            .faq {
                margin: 50px 0;
                padding: 0 20px;
            }
            .faq h2 {
                text-align: center;
                margin-bottom: 30px;
            }
            .faq button {
                width: 100%;
                padding: 10px;
                margin: 5px 0;
                background-color: #ff0000;
                color: #fff;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-align: left;
            }
            .faq .faq-answer {
                display: none;
                background-color: #333;
                color: #fff;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            .faq .faq-answer.show {
                display: block;
            }
            footer {
                text-align: center;
                padding: 20px 0;
                background: #000;
                color: #fff;
                border-top: 1px solid #ff0000;
            }
            @keyframes slide {
                from {
                    transform: translateX(100%);
                }
                to {
                    transform: translateX(-100%);
                }
            }
            @keyframes slide-reverse {
                from {
                    transform: translateX(-100%);
                }
                to {
                    transform: translateX(100%);
                }
            }
            @keyframes woosh {
                0% {
                    width: 12px;
                    transform: translate(0px, 0px) rotate(-35deg);
                }
                15% {
                    width: 50px;
                }
                30% {
                    width: 12px;
                    transform: translate(214px, -150px) rotate(-35deg);
                }
                30.1% {
                    transform: translate(214px, -150px) rotate(46deg);
                }
                50% {
                    width: 110px;
                }
                70% {
                    width: 12px;
                    transform: translate(500px, 150px) rotate(46deg);
                }
                70.1% {
                    transform: translate(500px, 150px) rotate(-37deg);
                }
                85% {
                    width: 50px;
                }
                100% {
                    width: 12px;
                    transform: translate(700px, 0) rotate(-37deg);
                }
            }
            @keyframes boom-circle {
                0% {
                    opacity: 0;
                }
                5% {
                    opacity: 1;
                }
                30% {
                    opacity: 0;
                    transform: scale(3);
                }
                100% {
                }
            }
            @keyframes boom-triangle-big {
                0% {
                    opacity: 0;
                }
                5% {
                    opacity: 1;
                }
                40% {
                    opacity: 0;
                    transform: scale(2.5) translate(50px, -50px) rotate(360deg);
                }
                100% {
                }
            }
            @keyframes boom-triangle {
                0% {
                    opacity: 0;
                }
                5% {
                    opacity: 1;
                }
                30% {
                    opacity: 0;
                    transform: scale(3) translate(20px, 40px) rotate(360deg);
                }
                100% {
                }
            }
            @keyframes boom-disc {
                0% {
                    opacity: 0;
                }
                5% {
                    opacity: 1;
                }
                40% {
                    opacity: 0;
                    transform: scale(2) translate(-70px, -30px);
                }
                100% {
                }
            }
        </style>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
        <div class="hero">
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
            <h1>Welcome to Verge</h1>
            <p>Optimize your dating profile with AI-powered reviews and personalized tips.</p>
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
            <div class="testimonial-row">
                <div class="testimonial">verge user<br>can't believe how easy it was to improve my profile. - sam 4 days ago</div>
                <div class="testimonial">verge user<br>thanks verge, more matches than ever! - taylor 3 days ago</div>
                <div class="testimonial">verge user<br>ai insights were amazing. profile looks better now! - chris 6 days ago</div>
                <div class="testimonial">verge user<br>verge's tips transformed my profile, now it's lit! - pat 2 days ago</div>
                <div class="testimonial">verge user<br>can't believe how easy it was to improve my profile. - sam 4 days ago</div>
                <div class="testimonial">verge user<br>thanks verge, more matches than ever! - taylor 3 days ago</div>
            </div>
            <div class="testimonial-row">
                <div class="testimonial">verge user<br>ai insights were amazing. profile looks better now! - chris 6 days ago</div>
                <div class="testimonial">verge user<br>verge's tips transformed my profile, now it's lit! - pat 2 days ago</div>
                <div class="testimonial">verge user<br>can't believe how easy it was to improve my profile. - sam 4 days ago</div>
                <div class="testimonial">verge user<br>thanks verge, more matches than ever! - taylor 3 days ago</div>
                <div class="testimonial">verge user<br>ai insights were amazing. profile looks better now! - chris 6 days ago</div>
                <div class="testimonial">verge user<br>verge's tips transformed my profile, now it's lit! - pat 2 days ago</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # FAQ Section
    st.markdown("""
        <div class="faq">
            <h2>Frequently Asked Questions</h2>
            <button class="accordion">What is Verge?</button>
            <div class="panel">
                <p>Verge uses AI to analyze your dating profile and provide personalized improvement tips.</p>
            </div>
            <button class="accordion">What kind of tips does Verge provide?</button>
            <div class="panel">
                <p>Verge provides tips on photos, bio, and overall profile presentation to help you attract more matches.</p>
            </div>
            <button class="accordion">Is Verge free to use?</button>
            <div class="panel">
                <p>Yes, Verge offers a free version with basic features. Premium features are available with a subscription.</p>
            </div>
        </div>
        <script>
            var acc = document.getElementsByClassName("accordion");
            var i;

            for (i = 0; i < acc.length; i++) {
                acc[i].addEventListener("click", function() {
                    this.classList.toggle("active");
                    var panel = this.nextElementSibling;
                    if (panel.style.display === "block") {
                        panel.style.display = "none";
                    } else {
                        panel.style.display = "block";
                    }
                });
            }
        </script>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <footer>
            <p>&copy; 2024 Verge. All rights reserved.</p>
        </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
