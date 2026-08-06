import streamlit as st
from openai import OpenAI
import pypdf

# Page Setup
st.set_page_config(page_title="ISB Batch MBB Resume Evaluator", page_icon="💼", layout="wide")

st.title("🎯 ISB Batch MBB Resume Evaluator")
st.markdown("Upload your resume (PDF) to get an MBB-tailored score, feedback, and line-by-line bullet rewrites.")

# Sidebar for OpenAI API Key
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password", help="Get your key from platform.openai.com")

# MBB Evaluation Prompt
SYSTEM_PROMPT = """
You are a top-tier MBB (McKinsey, Bain, BCG) resume screener evaluating business school candidates. 
Analyze the provided resume against strict management consulting standards.

Provide a detailed evaluation with:
1. Overall MBB Fit Rating (out of 10)
2. Key Strengths (Impact, leadership, quantitative proof)
3. Critical Areas to Fix (Jargon, weak verbs, vague impact, line density)
4. Line-by-Line Refinement Suggestions (Provide concrete 'Before' and 'After' rewrites)

Maintain a candid, peer-like, and highly actionable tone.
"""

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file and api_key:
    if st.button("Evaluate Resume"):
        with st.spinner("Analyzing resume against MBB benchmarks with GPT..."):
            try:
                # Read PDF text
                pdf_reader = pypdf.PdfReader(uploaded_file)
                resume_text = ""
                for page in pdf_reader.pages:
                    resume_text += page.extract_text() + "\n"

                # Initialize OpenAI client
                client = OpenAI(api_key=api_key)

                # Call ChatGPT API
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"Resume Text:\n{resume_text}"}
                    ]
                )

                st.success("Evaluation Complete!")
                st.markdown("---")
                st.markdown(response.choices[0].message.content)

            except Exception as e:
                st.error(f"Error processing resume: {str(e)}")

elif uploaded_file and not api_key:
    st.info("👈 Please enter your OpenAI API Key in the sidebar to get started.")
