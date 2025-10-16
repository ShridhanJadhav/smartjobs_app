import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="SmartJobs", layout="wide")

# --- Files ---
users_file = "users.csv"

# --- Load or create users CSV ---
if os.path.exists(users_file):
    users_df = pd.read_csv(users_file, dtype=str).fillna("")
else:
    users_df = pd.DataFrame(columns=["username","password","referral_id","signup_date","trial_end","free_month_unlocked"])

st.title("🔐 SmartJobs - Login / Signup")

# --- Inputs ---
username = st.text_input("Username")
password = st.text_input("Password", type="password")

col1, col2 = st.columns(2)
signup_btn = col1.button("Signup")
login_btn = col2.button("Login")

# --- Signup logic ---
if signup_btn:
    username_clean = username.strip().lower()
    password_clean = password.strip()

    users_df['username'] = users_df['username'].str.strip().str.lower()

    if username_clean in users_df['username'].values:
        st.warning("⚠️ Username already exists!")
    else:
        referral_id = str(uuid.uuid4())[:8]
        signup_date = datetime.now()
        trial_end = signup_date + timedelta(days=8)
        new_user = pd.DataFrame([{
            "username": username_clean,
            "password": password_clean,
            "referral_id": referral_id,
            "signup_date": signup_date.strftime("%Y-%m-%d %H:%M:%S"),
            "trial_end": trial_end.strftime("%Y-%m-%d %H:%M:%S"),
            "free_month_unlocked": "False"
        }])
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        users_df.to_csv(users_file, index=False)
        st.success(f"✅ Signup successful! Your referral ID: {referral_id}")
        st.info(f"🎁 8-day trial ends on {trial_end.strftime('%Y-%m-%d')}")

# --- Login logic ---
if login_btn:
    username_clean = username.strip().lower()
    password_clean = password.strip()

    users_df['username'] = users_df['username'].astype(str).str.strip().str.lower()
    users_df['password'] = users_df['password'].astype(str).str.strip()

    user = users_df[(users_df['username'] == username_clean) & (users_df['password'] == password_clean)]

    if not user.empty:
        st.session_state['logged_in_user'] = username_clean
        st.success(f"🎉 Welcome {username_clean}!")
        st.info(f"Trial ends on {user['trial_end'].values[0]}")
        st.write(f"Referral link: http://localhost:8501?ref={user['referral_id'].values[0]}")
        st.info("✅ You can now go to other pages from the sidebar!")
    else:
        st.error("❌ Incorrect username or password.")
