import streamlit as st
import fitz
from PIL import Image
import io
import json
import google.generativeai as genai
import os
import pyperclip
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize GenerativeModel
model_vision = genai.GenerativeModel('gemini-pro-vision')
model_text = genai.GenerativeModel("gemini-1.5-pro-latest")

# Paths
INTERMEDIATE_JSON_PATH = "temp.json"
INTERMEDIATE_JOB_DESC_PATH = "temp_job_desc.txt"

def load_prompt(prompt_file_path):
    with open(prompt_file_path, "r") as file:
        return file.read()

# Function to process PDF and extract content
def process_pdf_and_save_job_desc(uploaded_file, job_description):
    if not uploaded_file:
        return None, "No file provided"

    # Read the PDF content
    pdf_content = uploaded_file.read()

    # Convert PDF to image
    doc = fitz.open(stream=pdf_content, filetype="pdf")
    page = doc.load_page(0)
    pix = page.get_pixmap()
    img_bytes = pix.tobytes("png")
    image = Image.open(io.BytesIO(img_bytes))
    doc.close()

    # Further processing with the image
    prompt = load_prompt("prompts/resume_parsing_prompt.txt")
    response = model_vision.generate_content([prompt, image])
    
    json_data = response.text

    # Save the JSON data for other tabs to access
    with open(INTERMEDIATE_JSON_PATH, "w") as json_file:
        json.dump(json_data, json_file)

    with open(INTERMEDIATE_JOB_DESC_PATH, "w") as file:
        file.write(job_description)

    return image, json_data



# Function to generate interview questions
def generate_interview_questions_for_employer():
    with open(INTERMEDIATE_JSON_PATH, "r") as json_file:
        json_data = json.load(json_file)
    
    prompt = load_prompt("prompts/interview_questions_prompt.txt") + json_data
    responses = model_text.generate_content(prompt)

    try:
        return responses.text
    except:
        st.write(responses)

def generate_interview_questions_for_employee():
    with open(INTERMEDIATE_JSON_PATH, "r") as json_file:
        json_data = json.load(json_file)
    
    prompt = load_prompt("prompts/interview_Questions_employee.txt") + json_data
    responses = model_text.generate_content(prompt)

    try:
        return responses.text
    except:
        st.write(responses)

# Function to generate job-related questions
def generate_job_related_questions(resume_data, job_description):
    # Create prompt
    prompt = load_prompt("prompts/job_questions_prompt.txt").replace(
            "job_description", job_description).replace("resume_description", resume_data)

    # Generate responses using the model
    responses = model_text.generate_content(prompt)
    try:
        return responses.text
    except:
        st.write(responses)

# Modify generate_cover_letter to take job description input
def generate_cover_letter():
    try:
        # Read the saved job description
        with open(INTERMEDIATE_JOB_DESC_PATH, "r") as file:
            job_description = file.read()

        # Read the saved resume data (JSON)
        with open(INTERMEDIATE_JSON_PATH, "r") as file:
            json_data = file.read()

        # Create a prompt for the cover letter
        prompt = load_prompt("prompts/cover_letter_prompt.txt").replace(
            "job_description", job_description).replace("json_data", json_data)

        # Generate the cover letter using the model
        response = model_text.generate_content(prompt, stream=True)
        response.resolve()

        return response.text

    except Exception as e:
        return f"An error occurred: {e}"
    
def generate_rating(resume_data, job_description):
    prompt = load_prompt("prompts/ratings_prompt.txt").replace(
        "job_description", job_description).replace("resume_data",resume_data)
    responses = model_text.generate_content(prompt)
    try:
        return int(responses.text)
    except:
        return 'No response'

def loadingScreen():
    st.text("🔍Processing your resume...")
    st.text("📝Generating personalized content...")
    st.text("🎯Analyzing your qualifications...")
    st.text("🚀Success! Your content is ready!")

def star_rating(rating):
    # Display stars based on the rating
    stars = '★' * int(rating) + '☆' * (10 - int(rating))
    return stars    

def get_fit_level(rating):
    if rating <= 2:
        return "Not a great fit"
    elif rating <= 4:
        return "Below average fit"
    elif rating <= 6:
        return "Average fit"
    elif rating <= 8:
        return "Good fit"
    else:
        return "Best fit"    


def main():
    st.set_page_config(page_title="CareerCraft", 
                   page_icon="images/logo.png",
                   layout="wide",
                   initial_sidebar_state="expanded"
                   )
    # st.title("Resume Processor and Job Assistant")

    st.sidebar.header('🎯Please select your role:')
    nav = st.sidebar.radio('',['New to this!','JobSeeker', 'Recruiter'])
    st.sidebar.write('')
    st.sidebar.write('')
    st.sidebar.write('')


    if nav == 'New to this!':
# Header for What is CareerCraft
        st.image("images/logo.png",width=100)
        st.markdown("## What is CareerCraft?")
        st.markdown("CareerCraft is a sophisticated platform designed to streamline the hiring process for both job seekers and employers. It empowers users to optimize resumes, generate personalized cover letters, and efficiently match candidates with job openings.")

        # Header for How students can use the benefit
        st.markdown("## How Students Can Benefit from CareerCraft")
        st.markdown("Students can leverage CareerCraft to enhance their job search by:")
        st.markdown("- **Optimizing Resumes**: Craft compelling resumes tailored to specific job postings.")
        st.markdown("- **Generating Personalized Cover Letters**: Create impactful cover letters customized for each application.")
        st.markdown("- **Matching with Job Openings**: Find relevant job opportunities based on their qualifications and preferences.")

        # Header for How Recruiters can use the application
        st.markdown("## How Recruiters Can Use CareerCraft")
        st.markdown("Recruiters can maximize their hiring process efficiency through CareerCraft by:")
        st.markdown("- **Crafting Customized Job Descriptions**: Generate detailed job postings tailored to specific requirements.")
        st.markdown("- **Efficient Resume Scanning**: Quickly identify top candidates by scanning and analyzing resumes.")
        st.markdown("- **Job Matching**: Match job openings with qualified candidates using advanced algorithms.")
    
    # Incsae of Job Seeker 

    if nav == 'JobSeeker':
        st.title("👋Hola Candidate!")
        # st.markdown("<h5 style='text-align: left; font-size:15px;'>Welcome, candidates! Upload your resume, generate customized cover letters based on job descriptions, and receive interview questions tailored to your qualifications. Let's streamline your job search and boost your success. Get started now!</h5>", unsafe_allow_html=True)
        st.markdown(" Upload your resume, generate customized cover letters based on job descriptions, and receive interview questions tailored to your qualifications.")
        st.markdown("Let's streamline your job search and boost your success. **Get started now!**")

        st.markdown('___')

        uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    
        # Input job description
        job_description_input = st.text_area("Enter job description")
        # Display multiple options to the user using checkboxes
        
        st.text("✅Select the options you want to perform:")
        extractResumeOption = st.checkbox('🧬Extract Resume Information')
        generateCoverLetterOption = st.checkbox('📫Generate Personalized Cover Letter')
        generatePersonalizedQuestionsOption = st.checkbox('✨Generate Personalized Interview Questions')

        if st.button("Process"):
            if uploaded_file and job_description_input:

                image, json_data = process_pdf_and_save_job_desc(uploaded_file, job_description_input)

                ratingval =generate_rating(json_data, job_description_input)
                st.write("____")
                st.write("⭐"*ratingval+get_fit_level(ratingval))


                # Display processed PDF and extracted J
                if extractResumeOption:
                    st.image(image, caption="Processed PDF")
                    st.subheader("Extracted JSON Content:")
                    st.write(json_data)

                
                if generateCoverLetterOption:
                    st.subheader("Generated Cover Letter")
                    
                    result = generate_cover_letter()
                    st.write(result)
                    st.button("Copy to Clipboard", on_click=lambda: pyperclip.copy(result))
                    # st.write(result)
                    # st.write('<script>alert("This is a toast notification!")</script>', unsafe_allow_html=True)
                    # # st.write(generate_cover_letter())

                # Generate personalized interview questions
                if generatePersonalizedQuestionsOption:
                    st.subheader("Personalized Interview Questions")
                    st.text_area(generate_interview_questions_for_employee())
    elif nav == 'Recruiter':
        st.title("👋Hola Recruiter!")
        st.markdown("Welcome, recruiters! Streamline your candidate evaluations by uploading resumes and generating interview questions directly from candidate profiles.")
        st.markdown( "Let's optimize your hiring process and find the perfect match for your team. **Get started now!**")
        st.markdown('___')

        uploaded_file = st.file_uploader("Upload candidate's resume (PDF)", type=["pdf"])
    
        # Input job description
        job_description_input = st.text_area("Enter the job description")
        
        st.text("✅Select the options you want to perform:")
        extractResumeOption = st.checkbox('🧬Extract Resume Information')
        generateIVCandidateOption = st.checkbox('✨Generate Personalized Interview Questions from Candidate profile')
        generatePersonalizedQuestionsOption = st.checkbox('💼Generate Personalized Interview Questions for the role')


        if st.button("Process"):
            if uploaded_file and job_description_input:

                image, json_data = process_pdf_and_save_job_desc(uploaded_file, job_description_input)

                # Display processed PDF and extracted JSON content
                if extractResumeOption:
                    st.image(image, caption="Processed PDF")
                    st.subheader("Extracted JSON Content:")
                    st.write(json_data)
                # Process the uploaded PDF and save job description
                # Generate personalized interview questions
                if generateIVCandidateOption:
                    st.subheader("Personalized Interview Questions")
                    st.write(generate_interview_questions_for_employer())

                # Generate job-related questions
                if generatePersonalizedQuestionsOption:
                    st.subheader("Job-related Questions")
                    st.write(generate_job_related_questions(json_data, job_description_input))


# # Radio button to select user type
#     user_type = st.radio("Are you an employee or an employer?", ('Employee', 'Employer'))

#     # Upload PDF file
    

#     # Button to trigger processing
   
            

#             if user_type == 'Employee':
#                 # Generate cover letter
#                 st.subheader("Generated Cover Letter")
#                 st.write(generate_cover_letter())

#                 # Generate personalized interview questions
#                 st.subheader("Personalized Interview Questions")
#                 st.write(generate_interview_questions_for_employee())
#             elif user_type == 'Employer':
            


if __name__ == "__main__":
    main()