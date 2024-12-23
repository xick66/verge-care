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

def generate_reply(chat_image):
    try:
        prompt = """
        Generate fun and cheeky reply to the last message at the bottom of the screen, the right part of the images contains my messages and the left part contains my crush's messages, consider all the messages we both have sent and generate a reply only for the last message on the left and suggest me some good puns and jokes to use considering the texting style.
        """
        image = Image.open(chat_image)
        response = model_text.generate_content(
            [prompt, image],
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        return response.text.strip()
    except Exception as e:
        st.error(f"An error occurred while generating the reply: {e}")
        return 'No response'

def main():
    st.set_page_config(
        page_title="Reply Generator",
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

    st.title("Generate a Reply")
    st.markdown("*Crop out your match’s PFP for better response and privacy purposes.*")

    chat_image = st.file_uploader("Upload your chat screenshot, hide contact names and pfps from the screenshot for better response. ", type=["jpg", "jpeg", "png"], key="chat")

    if chat_image:
        reply = generate_reply(chat_image)
        if reply:
            st.subheader("Generated Reply")
            st.write(reply)

if __name__ == "__main__":
    main()
