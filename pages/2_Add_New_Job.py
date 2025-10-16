import streamlit as st
import pandas as pd
import os

st.title("➕ Add New Job")

jobs_file = "jobs.csv"
if os.path.exists(jobs_file):
    jobs_df = pd.read_csv(jobs_file)
else:
    jobs_df = pd.DataFrame(columns=["Role","Company","Location","Type","Skills","Apply Link"])

role = st.text_input("Role")
company = st.text_input("Company")
location = st.text_input("Location")
job_type = st.text_input("Type")
skills = st.text_input("Skills")
apply_link = st.text_input("Apply Link")

if st.button("Add Job"):
    new_job = pd.DataFrame([{
        "Role": role,
        "Company": company,
        "Location": location,
        "Type": job_type,
        "Skills": skills,
        "Apply Link": apply_link
    }])
    jobs_df = pd.concat([jobs_df, new_job], ignore_index=True)
    jobs_df.to_csv(jobs_file, index=False)
    st.success("✅ Job added successfully!")
