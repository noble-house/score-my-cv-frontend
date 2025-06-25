import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Backend base URL
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

                        # ✅ Radar Chart for KYS Skills
                        if "kys_scores" in result and result["kys_scores"]:
                            kys_scores = result["kys_scores"]
                            st.markdown("### 🧠 Know Your Skills (KYS) – Radar Chart")
                            st.json(kys_scores)  # Debug output

                            labels = list(kys_scores.keys())
                            scores = [int(kys_scores[k]) for k in labels]

                            # Ensure loop closure for radar chart
                            labels += [labels[0]]
                            scores += [scores[0]]

                            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
                            angles += angles[:1]

                            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
                            ax.plot(angles, scores, color="blue", linewidth=2)
                            ax.fill(angles, scores, color="skyblue", alpha=0.3)
                            ax.set_yticks([20, 40, 60, 80, 100])
                            ax.set_yticklabels(["20", "40", "60", "80", "100"])
                            ax.set_xticks(angles)
                            ax.set_xticklabels(labels, fontsize=10)
                            ax.set_title("KYS Radar Chart", size=14, weight="bold", pad=20)

                            st.pyplot(fig)

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
