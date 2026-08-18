import streamlit as st

from src.career.recommend_jobs import recommend_jobs


st.set_page_config(
    page_title="AI Career Intelligence",
    page_icon="💼",
    layout="wide",
)

st.title("AI Career Intelligence Platform")

st.write(
    "Enter your skills and get the best matching Data/AI jobs "
    "based on TF-IDF and cosine similarity."
)

user_skills = st.text_input(
    "Your Skills",
    placeholder="python sql excel power bi data analysis",
)

if st.button("Find Jobs"):
    if not user_skills.strip():
        st.warning("Please enter at least one skill.")
    else:
        recommendations = recommend_jobs(
            user_skills=user_skills,
            limit=5,
        )

        st.subheader("Top Recommended Jobs")

        for index, job in enumerate(recommendations, start=1):
            st.markdown(f"### {index}. {job['title']}")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f"**Company:** {job['company']}")

            with col2:
                st.write(
                    f"**Location:** {job['location'] or 'Unknown'}"
                )

            with col3:
                st.write(
                    f"**Match:** {job['score']:.1%}"
                )

            if job["url"]:
                st.link_button(
                    "View Job",
                    job["url"],
                )

            st.divider()