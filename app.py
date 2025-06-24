import streamlit as st
import requests
import pandas as pd

# Backend base URL (without /analyze-resume so we can reuse for both endpoints)
BACKEND_URL = "https://score-my-cv-backend-production.up.railway.app"

st.set_page_config(page_title="ScoreMyCV - AI Resume Strength Checker", layout="wide")
st.title("📄 ScoreMyCV – AI Resume Strength Analyzer")

# === Tab Layout ===
tab1, tab2 = st.tabs(["📤 Upload Resume", "📊 Dashboard"])

# === Tab 1: Resume Upload & Analysis ===
with tab1:
    st.subheader("Upload your resume to get an AI-powered audit")

    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

    if uploaded_file:
        if st.button("🚀 Analyze Resume"):
            with st.spinner("Analyzing resume..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/analyze-resume",
                        files={"file": uploaded_file}
                    )
                    if response.status_code == 200:
                        result = response.json()

                        st.success(f"🎯 Resume Score: {result['score']} / 100")

                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("### 💪 Strengths")
                            for s in result["strengths"]:
                                st.success(f"• {s}")

                        with col2:
                            st.markdown("### 🛠️ Areas for Improvement")
                            for i in result["improvements"]:
                                st.warning(f"• {i}")

                        st.markdown("### 🧭 Suggested Job Roles")
                        for r in result["suggested_roles"]:
                            st.info(f"• {r}")
                    else:
                        st.error("❌ Failed to analyze resume. Please try again.")
                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")

# === Tab 2: Dashboard Analytics ===
with tab2:
    st.subheader("📊 Dashboard – Insights from All Analyzed Resumes")

    try:
        response = requests.get(f"{BACKEND_URL}/dashboard-summary")
        if response.status_code == 200:
            data = response.json()

            col1, col2, col3 = st.columns(3)
            col1.metric("📈 Average Score", data["avg_score"])
            col2.metric("🔝 Highest Score", data["max_score"])
            col3.metric("🔻 Lowest Score", data["min_score"])

            st.markdown("### 📊 Score Distribution")
            score_df = pd.DataFrame.from_dict(data["score_distribution"], orient="index", columns=["Count"])
            st.bar_chart(score_df)

            st.markdown("### 💪 Top Strengths")
            strength_df = pd.DataFrame.from_dict(data["top_strengths"], orient="index", columns=["Count"])
            st.dataframe(strength_df)

            st.markdown("### 🛠️ Top Improvements")
            improvement_df = pd.DataFrame.from_dict(data["top_weaknesses"], orient="index", columns=["Count"])
            st.dataframe(improvement_df)

            st.markdown("### 🧭 Top Suggested Job Roles")
            role_df = pd.DataFrame.from_dict(data["top_roles"], orient="index", columns=["Count"])
            st.dataframe(role_df)

        else:
            st.error("❌ Failed to load dashboard data.")
    except Exception as e:
        st.error(f"⚠️ Dashboard error: {e}")
