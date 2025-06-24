import streamlit as st
import requests

BACKEND_URL = "https://score-my-cv-backend-production.up.railway.app/analyze-resume"

st.set_page_config(page_title="ScoreMyCV - AI Resume Strength Checker")
st.title("📄 ScoreMyCV: Resume Strength Analyzer")

st.markdown("Upload your resume and get an AI-powered evaluation with a score, feedback, and role suggestions.")

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    if st.button("🚀 Analyze Resume"):
        with st.spinner("Analyzing resume..."):
            files = {"file": uploaded_file.getvalue()}
            try:
                response = requests.post(BACKEND_URL, files={"file": uploaded_file})
                if response.status_code == 200:
                    result = response.json()

                    st.subheader(f"✅ Resume Score: {result['score']} / 100")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### 💪 Strengths")
                        for s in result["strengths"]:
                            st.success(f"• {s}")

                    with col2:
                        st.markdown("### 🛠️ Areas for Improvement")
                        for i in result["improvements"]:
                            st.warning(f"• {i}")

                    st.markdown("### 🧭 Suitable Job Roles")
                    for r in result["suggested_roles"]:
                        st.info(f"• {r}")

                else:
                    st.error("❌ Failed to analyze resume. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
