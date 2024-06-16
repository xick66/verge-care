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
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 100px 50px;
                background: linear-gradient(135deg, #ff0000, #000);
                border-radius: 15px;
                margin-bottom: 60px;
                position: relative;
                overflow: hidden;
            }
            .hero-text {
                max-width: 50%;
            }
            .hero h1 {
                font-size: 60px;
                margin-bottom: 20px;
                text-align: left;
            }
            .hero p {
                font-size: 22px;
                margin-bottom: 40px;
                text-align: left;
            }
            .card {
                position: relative;
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
            .card::before {
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
            .card::after {
                content: "";
                z-index: -1;
                position: absolute;
                inset: 0;
                background: linear-gradient(-45deg, #fc00ff 0%, #00dbde 100%);
                transform: translate3d(0, 0, 0) scale(0.95);
                filter: blur(20px);
            }
            .card:hover::after {
                filter: blur(30px);
            }
            .card:hover::before {
                transform: rotate(-90deg) scaleX(1.34) scaleY(0.77);
            }
            .heading {
                font-size: 20px;
                text-transform: capitalize;
                font-weight: 700;
            }
            .card p:not(.heading) {
                font-size: 14px;
            }
            .card p:last-child {
                color: #e81cff;
                font-weight: 600;
            }
            .cards {
                display: flex;
                justify-content: space-around;
                flex-wrap: wrap;
                margin-bottom: 60px;
            }
            .feature-card {
                backdrop-filter: blur(5px) saturate(84%);
                -webkit-backdrop-filter: blur(5px) saturate(84%);
                background-color: rgba(167, 7, 7, 0.64);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.125);
                padding: 30px;
                margin: 20px;
                width: 350px;
                text-align: center;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s;
            }
            .feature-card:hover {
                transform: scale(1.05);
            }
            .testimonial-container {
                display: flex;
                justify-content: space-around;
                margin-bottom: 60px;
                overflow: hidden;
            }
            .testimonial {
                background: rgba(255, 6, 6, 0.35);
                border-radius: 16px;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(5.1px);
                -webkit-backdrop-filter: blur(5.1px);
                border: 1px solid rgba(255, 6, 6, 0.24);
                padding: 20px;
                width: 300px;
                text-align: center;
                animation: slide1 10s linear infinite;
                margin-right: 20px;
            }
            .testimonial-row2 .testimonial {
                animation: slide2 10s linear infinite;
            }
            @keyframes slide1 {
                0% { transform: translateX(100%); }
                100% { transform: translateX(-100%); }
            }
            @keyframes slide2 {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }
            footer {
                text-align: center;
                padding: 40px 0;
                background: #000;
                color: #fff;
                border-top: 1px solid #ff0000;
            }
            .faq {
                margin-bottom: 60px;
            }
            .faq h2 {
                font-size: 30px;
                margin-bottom: 20px;
            }
            .faq p {
                font-size: 18px;
                margin-bottom: 10px;
            }
            .faq .faq-item {
                margin-bottom: 20px;
            }
            .faq .faq-item button {
                width: 100%;
                text-align: left;
                padding: 10px;
                background-color: #222;
                border: none;
                color: white;
                font-size: 18px;
                cursor: pointer;
                border-radius: 5px;
            }
            .faq .faq-item button:hover {
                background-color: #333;
            }
            .faq .faq-item .faq-answer {
                display: none;
                padding: 10px;
                background-color: #111;
                border-radius: 5px;
                margin-top: 5px;
            }
        </style>
        <script>
            function toggleAnswer(id) {
                var x = document.getElementById(id);
                if (x.style.display === "none") {
                    x.style.display = "block";
                } else {
                    x.style.display = "none";
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
        <div class="testimonial-container">
            <div class="testimonial">
                <div class="card">
                    <div class="card-image"></div>
                    <div class="category">Verge User</div>
                    <div class="heading">Verge transformed my dating profile! The tips were specific and extremely helpful.
                        <div class="author">By <span class="name">Alex</span> 4 days ago</div>
                    </div>
                </div>
            </div>
            <div class="testimonial">
                <div class="card">
                    <div class="card-image"></div>
                    <div class="category">Verge User</div>
                    <div class="heading">The AI feedback was spot on and helped me attract more matches.
                        <div class="author">By <span class="name">Jamie</span> 3 days ago</div>
                    </div>
                </div>
            </div>
            <div class="testimonial">
                <div class="card">
                    <div class="card-image"></div>
                    <div class="category">Verge User</div>
                    <div class="heading">Thanks to Verge, my profile now stands out and I've received more matches!
                        <div class="author">By <span class="name">Taylor</span> 5 days ago</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="testimonial-container testimonial-row2">
            <div class="testimonial">
                <div class="card">
                    <div class="card-image"></div>
                    <div class="category">Verge User</div>
                    <div class="heading">The AI insights were amazing. My profile looks much better now!
                        <div class="author">By <span class="name">Chris</span> 6 days ago</div>
                    </div>
                </div>
            </div>
            <div class="testimonial">
                <div class="card">
                    <div class="card-image"></div>
                    <div class="category">Verge User</div>
                    <div class="heading">I got great tips that helped me get more matches.
                        <div class="author">By <span class="name">Sam</span> 2 days ago</div>
                    </div>
                </div>
            </div>
            <div class="testimonial">
                <div class="card">
                    <div class="card-image"></div>
                    <div class="category">Verge User</div>
                    <div class="heading">Highly recommend Verge for anyone looking to improve their dating profile.
                        <div class="author">By <span class="name">Pat</span> 7 days ago</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # FAQ Section
    st.markdown("""
        <div class="faq">
            <h2>Frequently Asked Questions</h2>
            <div class="faq-item">
                <button onclick="toggleAnswer('faq1')">What is Verge?</button>
                <div id="faq1" class="faq-answer">
                    Verge is an AI-powered platform designed to optimize your dating profile with detailed reviews and personalized tips.
                </div>
            </div>
            <div class="faq-item">
                <button onclick="toggleAnswer('faq2')">How does Verge work?</button>
                <div id="faq2" class="faq-answer">
                    Simply upload your dating profile images, and our AI will analyze them to provide specific improvement tips.
                </div>
            </div>
            <div class="faq-item">
                <button onclick="toggleAnswer('faq3')">Is Verge free to use?</button>
                <div id="faq3" class="faq-answer">
                    Yes, Verge offers a free version with basic features. For advanced tips and detailed reviews, you can upgrade to our premium plan.
                </div>
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
