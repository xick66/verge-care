import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv
from google.generativeai.types import HarmCategory, HarmBlockThreshold

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
        3. Rate their profile out of 10, be specific about the rating, give everyone a minimum of 6, don't give some random number, also include that many number of stars right next to the number.
        4. Body:
            - Pros of their profile and what stood out.
            - More Pros of their profile and what stood out.
            - Cons of their profile and what is not looking good.
            - More Cons about the profile i.e what they can improve.
        5. Suggestions: Include how they can improve their profile, give specific advice, not generic, give specific personalised tips
        6. In suggestions, be very specific, for example: change the cover photo, shuffle the images, change the prompt, change your bio, remove that photo, add some specific type of photo. Give these tips looking at their interests and their entire profile.
        Ensure that the Review is overall understandable and easy to implementable. The tips and review should be on-point. No beating around the bush.

1. Profile Analysis
○ Photo Review: Assess the quality, variety, and appropriateness of profile pictures.
○ Bio Analysis: Evaluate the bio for readability, engagement, and personality reflection.
○ Interest and Activity Suggestions: Recommend interests and activities to add for a well-rounded profile.
2. Profile Improvement Suggestions
○ Photo Suggestions: Provide tips on photo selection, including background, and attire.
○ Bio Enhancement: Offer specific suggestions to improve the bio, making it more appealing and authentic.
○ Interest Expansion: Suggest additional interests or activities that align with the user's profile.

If you don't think its a dating profile and its something else, just say "doesn't seem like a dating app profile"
        """
        response = model_text.generate_content(
            [prompt] + images,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        if not response.parts:
            st.error("The response was blocked by safety filters. Please try again with different images.")
            return 'No response'
        return response.text.strip()
    except Exception as e:
        st.error(f"An error occurred while generating the review: {e}")
        return 'No response'

def main():
    st.set_page_config(
        page_title="Outlier",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={}
    )

    # Hide the sidebar and toggle button
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            section[data-testid="stSidebar"][aria-expanded="true"]{
                display: none;
            }
            div[data-testid="collapsedControl"] {
                visibility: hidden;
            }
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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
            .animation-container {
                display: block;
                position: absolute;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                z-index: 0;
                pointer-events: none;
            }

            .hero {
                position: relative;
                text-align: center;
                padding: 150px 0;
                background: linear-gradient(135deg, #ff0000, #000);
                border-radius: 15px;
                margin-bottom: 0px;
                overflow: hidden;
            }

            .hero h1, .hero p {
                position: relative;
                z-index: 1;
            }

            .testimonial-section {
                position: relative;
                overflow: hidden;
                padding: 50px 0;
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
                flex-wrap: nowrap;
                white-space: nowrap;
                gap: 30px;
                padding: 20px 0;
                position: relative;
                animation: slide 20s linear infinite;
            }

            .testimonial-row:nth-child(2) {
                animation: slide-reverse 20s linear infinite;
            }

            .testimonial {
                display: inline-block;
                width: 300px; /* Ensure consistent card size */
                height: 150px; /* Ensure consistent card size */
                border-radius: 20px;
                padding: 10px;
                box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
                background-image: linear-gradient(144deg, #660000, #330000 50%, #000000);
                color: white;
                font-size: 16px;
                text-align: center;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: normal;
                word-wrap: break-word;
                flex: 0 0 auto;
                margin-right: 10px;
            }

            @media (max-width: 768px) {
                .testimonial-row {
                    gap: 15px; /* Adjust gap for mobile view */
                    padding: 10px 0;
                }

                .testimonial {
                    width: 250px; /* Adjust width for mobile */
                    height: auto; /* Adjust height for mobile */
                }
            }

            @keyframes slide {
                0% {
                    transform: translateX(100%);
                }
                100% {
                    transform: translateX(-100%);
                }
            }

            @keyframes slide-reverse {
                0% {
                    transform: translateX(-100%);
                }
                100% {
                    transform: translateX(100%);
                }
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
                background-color: #660000;
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
            .instagram-card {
                position: relative;
                width: 290px;
                height: 330px;
                background-color: #330000;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 20px;
                gap: 10px;
                border-radius: 8px;
                cursor: pointer;
                margin: 50px auto;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }

            .instagram-card::before {
                content: '';
                position: absolute;
                inset: 0;
                margin: auto;
                width: 290px;
                height: 330px;
                border-radius: 10px;
                background: linear-gradient(45deg, #fdf497 0%, #fdf497 25%, #fd5949 50%, #d6249f 75%, #285AEB 100%);
                z-index: -10;
                pointer-events: none;
                transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }

            .instagram-card::after {
                content: "";
                z-index: -1;
                position: absolute;
                inset: 0;
                background: linear-gradient(45deg, #fdf497 0%, #fdf497 25%, #fd5949 50%, #d6249f 75%, #285AEB 100%);
                transform: translate3d(0, 0, 0) scale(0.95);
                filter: blur(20px);
                transition: filter 0.3s ease, background 0.3s ease;
            }

            .instagram-card .heading {
                font-size: 22px;
                text-align: center;
                font-weight: 700;
            }

            .instagram-card p {
                font-size: 16px;
                text-align: center;
                margin: 5px 0;
            }

            .instagram-card p.unlock {
                color: #e81cff;
                font-weight: 700;
                font-size: 18px;
            }

            .instagram-card:hover::after {
                filter: blur(30px);
                background: linear-gradient(45deg, #fdf497 0%, #fdf497 25%, #fd5949 50%, #d6249f 75%, #285AEB 100%);
            }

            .instagram-card:hover::before {
                transform: rotate(-45deg) scaleX(1.34) scaleY(0.77);
            }

            .instagram-card:hover {
                transform: scale(1.05);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
            }

            .uploaded-images-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
                gap: 10px;
                justify-content: center;
            }

            @media (max-width: 768px) {
                .uploaded-images-grid {
                    grid-template-columns: repeat(3, 1fr); /* 3 columns on mobile */
                }
            }

            footer {
                text-align: center;
                padding: 20px 0;
                background: #000;
                color: #fff;
                border-top: 1px solid #ff0000;
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
            .boom-container.second {
                left: 485px;
                top: 155px;
            }
            .boom-container.second .shape.triangle,
            .boom-container.second .shape.circle,
            .boom-container.second .shape.circle.big,
            .boom-container.second .shape.disc {
                animation-delay: 1.9s;
            }
            .boom-container.second .shape.circle {
                animation-delay: 2.15s;
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
            <p>Get More Matches with the AI dating tool trained on preferences of Real Women!</p>
        </div>
    """, unsafe_allow_html=True)

    # Testimonials Section
    st.markdown("""
        <div class="testimonial-section">
            <div class="testimonial-row">
                <div class="testimonial">               <br>smooth as butter, works really well                       - Aryan</div>
                <div class="testimonial">               <br>thanks outlier, more matches than ever!                    - <strong>Sujay</strong></div>
                <div class="testimonial">               <br>tbh the profile looks better now 💃🏻                             - <strong>Eeshan</strong> </div>
                <div class="testimonial">               <br>omfg this is soo good, after using this, istg i got 4 matches in just 2 days❤️❤️                      - <strong>Aman</strong></div>
                <div class="testimonial">               <br>bhaii, jisne bhi banaya hein, badhiya banaya hein             - <strong>Adithya</strong></div>
                <div class="testimonial">               <br>works like a charm! ❤️               - <strong>Rehan</strong></div>
            </div>
            <div class="testimonial-row">
                <div class="testimonial">               <br>badhiya heinn ekdum              - <strong>Sahil</strong></div>
                <div class="testimonial">               <br>lol ai is helping me improve my profile, nice                  - <strong>Nithin</strong></div>
                <div class="testimonial">               <br>sleeeek!                         - <strong>Aditya</strong></div>
                <div class="testimonial">               <br>verge is my female bestfren from now on             - <strong>Benny</strong></div>
                <div class="testimonial">               <br>ai ai ai - all hail                         - <strong>Suyash</strong></div>
                <div class="testimonial">               <br>my profile looks so good now 🥹                 - <strong>Rahul</strong></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # File uploader for profile review
    st.markdown("""
        <h2>Want More Right Swipes? Start Here 🚀</h2>
    """, unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Upload your dating profile images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        if len(uploaded_files) > 8:
            st.error("You can upload a maximum of 8 images.")
        else:
            images = [Image.open(file) for file in uploaded_files]
            review = generate_review(images)

            if review:
                st.subheader("Profile Review 📝")
                st.write(review)

    # Instagram Follow Section
    st.markdown("""
        <a href="https://www.instagram.com/outliercrew?igsh=MXZweHk5Yzl0bWhzZg==" target="_blank" class="instagram-card" id="instagram-card" style="text-decoration: none; color: white;">
            <p class="heading2" style="font-family: 'Arial Black', Gadget, sans-serif; text-decoration: none; color: white;">CLICK HERE</p>
            <p style="color: white;">to follow us on</p>
            <p style="font-size: 20px; font-weight: 900; font-family: 'Arial Black', Gadget, sans-serif; text-decoration: none; color: white;"><strong>Instagram</strong></p>
        </a>
    """, unsafe_allow_html=True)

    # FAQ Section
    st.markdown("""
        <div class="faq">
            <h2>Frequently Asked Questions</h2>
            <button class="accordion">Q1: What is Outlier?</button>
            <div class="panel">
                <p>Outlier is a men's personal care brand dedicated to solving awareness and providing usage guidance through innovative products and content. We focus on making personal care simple, effective, and affordable for men.</p>
            </div>
            <button class="accordion">Q2: What is this dating app tool?</button>
            <div class="panel">
                <p>This tool is an AI-powered dating profile analyzer designed by Outlier to help men get more matches. It reviews your profile and provides personalized suggestions for improvement, based on insights from the preferences of over 10+ women.</p>
            </div>
            <button class="accordion">Q3: How does the tool work?</button>
            <div class="panel">
                <p>Simply upload your dating profile, and our AI will analyze it using criteria and feedback from real women. You'll receive actionable tips to enhance your profile and attract more meaningful matches.</p>
            </div>
            <button class="accordion">Q4: Why did Outlier create this tool?</button>
            <div class="panel">
                <p>At Outlier, we understand that personal care extends beyond skincare. We want to help men present their best selves, both online and offline. This tool is an extension of our mission to boost confidence and success in all aspects of life.</p>
            </div>
            <button class="accordion">Q5: Is the tool free to use?</button>
            <div class="panel">
                <p>Yes, the basic version of our tool is free. We also offer premium features for a more in-depth analysis and advanced tips.</p>
            </div>
            <button class="accordion">Q6: How accurate are the suggestions?</button>
            <div class="panel">
                <p>The suggestions are based on the collective insights of over 10+ women, ensuring that the feedback is practical and effective in improving your dating profile.</p>
            </div>
            <button class="accordion">Q7: Can I trust the privacy of my information?</button>
            <div class="panel">
                <p>Absolutely. Your privacy is our priority. We do not store or share any personal data from your dating profile. All analyses are conducted securely and anonymously.</p>
            </div>
            <button class="accordion">Q8: Can I use this tool for any dating app?</button>
            <div class="panel">
                <p>Yes, our tool is designed to work with profiles from any dating app, providing versatile and valuable insights regardless of the platform you use.</p>
            </div>
        </div>
        <script>
            var acc = document.getElementsByClassName("accordion");
            var i;

            for (i = 0; i < acc.length; i++) {
                acc[i.addEventListener("click", function() {
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
