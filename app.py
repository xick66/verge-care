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

def generate_review(images):
    try:
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
            .hero .card {
                position: absolute;
                right: 50px;
                top: 50%;
                transform: translateY(-50%);
                width: 190px;
                height: 254px;
                background-color: #000;
                display: flex;
                flex-direction: column;
                justify-content: end;
                padding: 12px;
                gap: 12px;
                border-radius: 8px;
                cursor: pointer;
            }
            .hero .card::before {
                content: '';
                position: absolute;
                inset: 0;
                left: -5px;
                margin: auto;
                width: 200px;
                height: 264px;
                border-radius: 10px;
                background: linear-gradient(-45deg, #e81cff 0%, #40c9ff 100%);
                z-index: -10;
                pointer-events: none;
                transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }
            .hero .card::after {
                content: "";
                z-index: -1;
                position: absolute;
                inset: 0;
                background: linear-gradient(-45deg, #fc00ff 0%, #00dbde 100%);
                transform: translate3d(0, 0, 0) scale(0.95);
                filter: blur(20px);
            }
            .hero .heading {
                font-size: 20px;
                text-transform: capitalize;
                font-weight: 700;
            }
            .hero .card p:not(.heading) {
                font-size: 14px;
            }
            .hero .card p:last-child {
                color: #e81cff;
                font-weight: 600;
            }
            .hero .card:hover::after {
                filter: blur(30px);
            }
            .hero .card:hover::before {
                transform: rotate(-90deg) scaleX(1.34) scaleY(0.77);
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
            .boom-container.second {
                left: 485px;
                top: 155px;
            }
            .shape {
                display: inline-block;
                position: relative;
                opacity: 0;
                transform-origin: center center;
            }
            .shape.triangle {
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
            .shape.triangle.big {
                margin-left: -25px;
                border-width: 0 5px 10px 5px;
                border-color: transparent transparent #fade28 transparent;
                animation-name: boom-triangle-big;
            }
            .shape.disc {
                width: 8px;
                height: 8px;
                border-radius: 100%;
                background-color: #d15ff4;
                animation-name: boom-disc;
                animation-duration: 1s;
                animation-timing-function: ease-out;
                animation-iteration-count: infinite;
            }
            .shape.circle {
                width: 20px;
                height: 20px;
                animation-name: boom-circle;
                animation-duration: 1s;
                animation-timing-function: ease-out;
                animation-iteration-count: infinite;
                border-radius: 100%;
                margin-left: -30px;
            }
            .shape.circle.white {
                border: 1px solid white;
            }
            .shape.circle.big {
                width: 40px;
                height: 40px;
                margin-left: 0px;
            }
            .shape.circle.big.white {
                border: 2px solid white;
            }
            .shape:after {
                background-color: rgba(178, 215, 232, 0.2);
            }
            .testimonial-section {
                position: relative;
                overflow: hidden;
                padding: 50px 0;
                margin-top: 50px;
                background-color: #000;
            }
            .testimonial-row {
                display: flex;
                gap: 30px;
                animation: move-horizontal 20s linear infinite;
            }
            .testimonial-row:nth-child(2) {
                animation-direction: reverse;
            }
            .testimonial {
                width: 300px;
                height: 200px;
                border-radius: 20px;
                padding: 20px;
                box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
                background-image: linear-gradient(144deg, #AF40FF, #5B42F3 50%, #00DDEB);
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                color: white;
                font-size: 16px;
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
            @keyframes move-horizontal {
                0% {
                    transform: translateX(100%);
                }
                100% {
                    transform: translateX(-100%);
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
            <h1>Welcome to Verge</h1>
            <p>Optimize your dating profile with AI-powered reviews and personalized tips.</p>
            <div class="card">
                <p class="heading">Popular This Month</p>
                <p>Powered By</p>
                <p>Uiverse</p>
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
    uploaded_files = st.file_uploader("", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="file-upload")

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

    # Testimonial Section
    st.markdown("""
        <div class="testimonial-section">
            <div class="testimonial-row">
                <div class="testimonial">Verge User<br>ai insights were amazing. profile looks better now! - chris 6 days ago</div>
                <div class="testimonial">Verge User<br>thanks verge, more matches than ever! - taylor 3 days ago</div>
                <div class="testimonial">Verge User<br>verge's tips transformed my profile, now it's lit! - pat 2 days ago</div>
                <div class="testimonial">Verge User<br>can't believe how easy it was to improve my profile. - sam 4 days ago</div>
                <div class="testimonial">Verge User<br>ai insights were amazing. profile looks better now! - chris 6 days ago</div>
                <div class="testimonial">Verge User<br>thanks verge, more matches than ever! - taylor 3 days ago</div>
                <div class="testimonial">Verge User<br>verge's tips transformed my profile, now it's lit! - pat 2 days ago</div>
                <div class="testimonial">Verge User<br>can't believe how easy it was to improve my profile. - sam 4 days ago</div>
            </div>
            <div class="testimonial-row">
                <div class="testimonial">Verge User<br>verge's tips transformed my profile, now it's lit! - pat 2 days ago</div>
                <div class="testimonial">Verge User<br>can't believe how easy it was to improve my profile. - sam 4 days ago</div>
                <div class="testimonial">Verge User<br>thanks verge, more matches than ever! - taylor 3 days ago</div>
                <div class="testimonial">Verge User<br>ai insights were amazing. profile looks better now! - chris 6 days ago</div>
                <div class="testimonial">Verge User<br>verge's tips transformed my profile, now it's lit! - pat 2 days ago</div>
                <div class="testimonial">Verge User<br>can't believe how easy it was to improve my profile. - sam 4 days ago</div>
                <div class="testimonial">Verge User<br>thanks verge, more matches than ever! - taylor 3 days ago</div>
                <div class="testimonial">Verge User<br>ai insights were amazing. profile looks better now! - chris 6 days ago</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # FAQ Section
    st.markdown("""
        <div class="faq">
            <h2>Frequently Asked Questions</h2>
            <button onclick="toggleAnswer('answer1')">What is Verge?</button>
            <div id="answer1" class="faq-answer">Verge is an AI-powered dating profile review service that provides personalized feedback and tips to improve your dating profile.</div>
            <button onclick="toggleAnswer('answer2')">How does Verge work?</button>
            <div id="answer2" class="faq-answer">Upload your dating profile images, and our AI will analyze them to provide you with detailed reviews and personalized improvement tips.</div>
            <button onclick="toggleAnswer('answer3')">Is Verge free to use?</button>
            <div id="answer3" class="faq-answer">Yes, Verge offers a free version with basic features. Premium features are available with a subscription.</div>
        </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <footer>
            <p>&copy; 2024 Verge. All rights reserved.</p>
        </footer>
        <script>
            function toggleAnswer(id) {
                var answer = document.getElementById(id);
                if (answer.classList.contains('show')) {
                    answer.classList.remove('show');
                } else {
                    answer.classList.add('show');
                }
            }
        </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
