import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI
import openai

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Initialize the OpenAI API client with the provided API key.
    openai.api_key = openai_api_key

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .pdf)", type=("txt", "pdf")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:
        # Process the uploaded file and question.
        if uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            document = ""
            for page in reader.pages:
                document += page.extract_text()
        else:
            document = uploaded_file.read().decode("utf-8")

        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        try:
            # Generate an answer using the OpenAI API without streaming.
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            # Extract and display the response.
            answer = response.choices[0].message['content']
            st.write("### Answer")
            st.write(answer)

        except Exception as e:
            st.error(f"An error occurred: {e}")
