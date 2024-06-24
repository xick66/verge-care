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

def generate_reply(chat_image):
    try:
        prompt = """
        Generate fun and cheeky reply to the last message at the bottom of the screen, the right part of the images contains my messages and the left part contains my crush's messages, consider all the messages we both have sent and generate a reply only for the last message on the left and suggest me some good puns and jokes to use considering the texting style.
        """
        image = Image.open(chat_image)
        response = model_text.generate_content([prompt, image])
        return response.text.strip()
    except Exception as e:
        st.error(f"An error occurred while generating the reply: {e}")
        return 'No response'

def main():
    st.set_page_config(
        page_title="Reply Generator",
        layout="wide",
        menu_items={}
    )

    st.title("Generate a Reply")

    chat_image = st.file_uploader("Upload your chat screenshot", type=["jpg", "jpeg", "png"], key="chat")

    if chat_image:
        reply = generate_reply(chat_image)
        if reply:
            st.subheader("Generated Reply")
            st.write(reply)

if __name__ == "__main__":
    main()