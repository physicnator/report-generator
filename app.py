import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="AI Report Generator", page_icon="📄")
st.title("📄 Mobile Report Generator")
st.write("Upload PDFs or images to extract details and generate a structured report.")

# Input for Gemini API Key
api_key = st.text_input("Enter your Gemini API Key:", type="password")

# File uploader allowing images and documents
uploaded_files = st.file_uploader(
    "Choose PDF or Image files", 
    type=["pdf", "png", "jpg", "jpeg", "webp"], 
    accept_multiple_files=True
)

if st.button("Generate Report", type="primary"):
    if not api_key:
        st.error("Please enter your Gemini API Key above.")
    elif not uploaded_files:
        st.warning("Please upload at least one file.")
    else:
        with st.spinner("Analyzing files and drafting report..."):
            try:
                client = genai.Client(api_key=api_key)
                gemini_contents = []

                for file in uploaded_files:
                    data = file.read()
                    mime_type = file.type
                    
                    # Fallback for generic mime types
                    if not mime_type or mime_type == "application/octet-stream":
                        ext = file.name.split(".")[-1].lower()
                        mime_type = "application/pdf" if ext == "pdf" else "image/jpeg"

                    gemini_contents.append(
                        types.Part.from_bytes(data=data, mime_type=mime_type)
                    )

                instruction = """
                Examine the attached documents/images in detail. Extract and analyze all visible text, dates, names, figures, and context.
                
                Generate a professional, structured report with:
                - **Executive Summary / Purpose**
                - **Key Facts, Figures & Data Highlights**
                - **Chronological / Event Details**
                - **Remarks & Conclusion**
                
                Format cleanly with bold headers and bullet points.
                """
                gemini_contents.append(instruction)

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=gemini_contents
                )

                st.success("Report Generated!")
                st.markdown(response.text)
                
                # Download button for the generated report
                st.download_button(
                    label="Download Report as Text",
                    data=response.text,
                    file_name="generated_report.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error: {str(e)}")
