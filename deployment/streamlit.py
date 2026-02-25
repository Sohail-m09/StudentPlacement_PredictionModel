'''
import streamlit as st
import pickle
import pandas as pd


with open("experiment/artifacts/best_model.pkl", "rb") as f:
    best_model = pickle.load(f)

st.set_page_config(page_title="Student Salary Predictor")
st.title("🎓 Student Placement Salary Predictor")
st.write("Enter student details below:")
age = st.number_input("Age", min_value=18, max_value=35)
gender = st.selectbox("Gender", ["Male", "Female"])
cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0)
branch = st.selectbox("Branch", ["IT", "CSE", "EEE", "Mechanical", "Civil"])
college_tier = st.selectbox("College Tier", ["Tier 1", "Tier 2", "Tier 3"])
internships_count = st.number_input("Internships Count", min_value=0)
certifications_count = st.number_input("Certifications Count", min_value=0)
coding_skill_score = st.number_input("Coding Skill Score", min_value=0.0, max_value=100.0)
hackathons_participated = st.number_input("Hackathons Participated", min_value=0)
github_repos = st.number_input("GitHub Repos", min_value=0)
linkedin_connections = st.number_input("LinkedIn Connections", min_value=0)
mock_interview_score = st.number_input("Mock Interview Score", min_value=0.0, max_value=100.0)
attendance_percentage = st.number_input("Attendance Percentage", min_value=0.0, max_value=100.0)
backlogs = st.number_input("Backlogs", min_value=0)
extracurricular_score = st.number_input("Extracurricular Score", min_value=0.0, max_value=100.0)
volunteer_experience = st.selectbox("Volunteer Experience", ["Yes", "No"])
study_hours_per_day = st.number_input("Study Hours Per Day", min_value=0.0, max_value=24.0)

if st.button("Predict Salary"):

    user_input = pd.DataFrame(columns=best_model.feature_names_in_)
    user_input.loc[0] = [
        age,
        gender,
        cgpa,
        branch,
        college_tier,
        internships_count,
        certifications_count,
        coding_skill_score,
        hackathons_participated,
        github_repos,
        linkedin_connections,
        mock_interview_score,
        attendance_percentage,
        backlogs,
        extracurricular_score,
        volunteer_experience,
        study_hours_per_day
    ]

    prediction = best_model.predict(user_input)[0]

    st.success(f"Predicted Salary: {round(prediction, 2)} LPA")
'''


import streamlit as st
import pickle
import pandas as pd
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Salary Predictor", layout="wide")

# --- CUSTOM CSS FOR CLEAN UI ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007BFF;
        color: white;
        font-weight: bold;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #007BFF;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD MODEL ---
@st.cache_resource
def load_model():
    # Using relative path based on your folder structure
    model_path = "experiment/artifacts/best_model.pkl"
    with open(model_path, "rb") as f:
        return pickle.load(f)

best_model = load_model()

# --- HEADER ---
st.title("🎓 Student Placement Salary Predictor")
st.markdown("---")

# --- INPUT GRID ---
# We use 3 columns to fit 17 inputs on one screen
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👤 Personal Info")
    age = st.number_input("Age", min_value=18, max_value=35, step=1)
    gender = st.selectbox("Gender", ["Male", "Female"])
    college_tier = st.selectbox("College Tier", ["Tier 1", "Tier 2", "Tier 3"])
    branch = st.selectbox("Branch", ["IT", "CSE", "EEE", "Mechanical", "Civil"])

with col2:
    st.subheader("📚 Academic Profile")
    cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, format="%.2f")
    backlogs = st.number_input("Backlogs", min_value=0, step=1)
    attendance_percentage = st.number_input("Attendance %", min_value=0.0, max_value=100.0)
    study_hours_per_day = st.number_input("Study Hours/Day", min_value=0.0, max_value=24.0)

with col3:
    st.subheader("🏆 Skills & Experience")
    internships_count = st.number_input("Internships", min_value=0, step=1)
    certifications_count = st.number_input("Certifications", min_value=0, step=1)
    coding_skill_score = st.number_input("Coding Score", min_value=0.0, max_value=100.0)
    extracurricular_score = st.number_input("Extra-curricular", min_value=0.0, max_value=100.0)

# Extra details in a narrower row to save vertical space
st.markdown("#### 🔗 Online Presence & Others")
c1, c2, c3, c4, c5 = st.columns(5)
with c1: github_repos = st.number_input("GitHub Repos", min_value=0)
with c2: linkedin_connections = st.number_input("LinkedIn Conn.", min_value=0)
with c3: hackathons_participated = st.number_input("Hackathons", min_value=0)
with c4: mock_interview_score = st.number_input("Mock Int. Score", min_value=0.0, max_value=100.0)
with c5: volunteer_experience = st.selectbox("Volunteer?", ["Yes", "No"])

st.markdown("---")

# --- PREDICTION LOGIC ---
if st.button("🚀 Predict My Salary"):
    # Prepare data
    user_input = pd.DataFrame(columns=best_model.feature_names_in_)
    user_input.loc[0] = [
        age, gender, cgpa, branch, college_tier, internships_count,
        certifications_count, coding_skill_score, hackathons_participated,
        github_repos, linkedin_connections, mock_interview_score,
        attendance_percentage, backlogs, extracurricular_score,
        volunteer_experience, study_hours_per_day
    ]

    prediction = best_model.predict(user_input)[0]
    
    # Result Display
    st.balloons()
    st.metric(label="Estimated Salary Package", value=f"{round(prediction, 2)} LPA")
