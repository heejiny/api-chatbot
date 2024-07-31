import streamlit as st
import requests
from bs4 import BeautifulSoup

def extract_text_from_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

st.title("HTML to Markdown/Text Converter")

url = st.text_input("Enter the URL of the website:")
file_type = st.radio("Select file type to download:", (".md", ".txt"))

if st.button("Extract Text"):
    if url:
        try:
            extracted_text = extract_text_from_html(url)
            if file_type == ".md":
                filename = "extracted_text.md"
                content = f"# Extracted Text\n\n{extracted_text}"
            else:
                filename = "extracted_text.txt"
                content = extracted_text
            
            st.download_button(label="Download File", data=content, file_name=filename, mime="text/plain")
            st.success(f"Text extracted and ready for download as {filename}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter a valid URL.")
