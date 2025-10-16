import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="SmartJobs - Jobs", layout="wide")
st.title("💼 Job Listings")

# --- Check login ---
if 'logged_in_user' not in st.session_state:
    st.warning("⚠️ Please log in first on the main page.")
    st.stop()

jobs_file = "jobs.csv"
if not os.path.exists(jobs_file):
    st.error("jobs.csv not found!")
    st.stop()

jobs_df = pd.read_csv(jobs_file)

# --- Filters ---
role_filter = st.selectbox("Filter by Role", ["All"] + sorted(jobs_df['Role'].dropna().unique()))
type_filter = st.selectbox("Filter by Type", ["All"] + sorted(jobs_df['Type'].dropna().unique()))
location_filter = st.selectbox("Filter by Location", ["All"] + sorted(jobs_df['Location'].dropna().unique()))

filtered_jobs = jobs_df.copy()
if role_filter != "All":
    filtered_jobs = filtered_jobs[filtered_jobs['Role'] == role_filter]
if type_filter != "All":
    filtered_jobs = filtered_jobs[filtered_jobs['Type'] == type_filter]
if location_filter != "All":
    filtered_jobs = filtered_jobs[filtered_jobs['Location'] == location_filter]

# --- Display job cards ---
if not filtered_jobs.empty:
    for _, row in filtered_jobs.iterrows():
        st.markdown(f"""
        <div style="
            background-color:#f9f9f9;
            border:1px solid #e0e0e0;
            border-radius:12px;
            padding:20px;
            margin-bottom:15px;
            box-shadow:0 2px 6px rgba(0,0,0,0.1);
        ">
            <h3 style="color:#007bff;">{row['Role']}</h3>
            <p><b>🏢 Company:</b> {row['Company']}</p>
            <p><b>📍 Location:</b> {row['Location']}</p>
            <p><b>💼 Type:</b> {row['Type']}</p>
            <p><b>🧠 Skills:</b> {row['Skills']}</p>
            <a href="{row['Apply Link']}" target="_blank">
                <button style="
                    background-color:#007bff;
                    color:white;
                    border:none;
                    padding:8px 16px;
                    border-radius:8px;
                    cursor:pointer;
                    font-size:14px;
                ">View & Apply</button>
            </a>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No jobs found.")
