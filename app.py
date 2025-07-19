import streamlit as st

# --- Set Page Config ---
st.set_page_config(page_title="Salary Predictor", layout="wide")

# --- SESSION STATE NAVIGATION ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# --- SIDEBAR NAVIGATION --
st.sidebar.markdown("<h2 style='color:gold;'>🌿 Navigation</h2>", unsafe_allow_html=True)

if st.sidebar.button("🏠 Home"):
    st.session_state.current_page = "Home"
if st.sidebar.button("💸 Salary Prediction"):
    st.session_state.current_page = "Salary Prediction"
if st.sidebar.button("📊 Data Exploration"):
    st.session_state.current_page = "Data Exploration"
if st.sidebar.button("📈 Model Analytics"):
    st.session_state.current_page = "Model Analytics"
if st.sidebar.button("ℹ️ About"):
    st.session_state.current_page = "About"

# --- USER PROFILE CARD WITH AVATAR ---
st.sidebar.markdown("""
<div class='user-card'>
    <img src='https://avatars.githubusercontent.com/u/9919?s=200&v=4' alt='Profile Picture'>
    <h4>Durga Prasad</h4>
    <p>AI/ML Developer</p>
    <p>📧 papuganidurgaprasad@email.com</p>
</div>
""", unsafe_allow_html=True)

# --- CUSTOM CSS ---
st.markdown("""
<style>
/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Lora:wght@600&display=swap');

/* Animation for fade-in */
html, body, [class*="css"] {
    font-family: 'Lato', sans-serif;
    animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

/* Responsive header */
.main-title {
    font-family: 'Lora', serif;
    font-size: 2.8rem;
    font-weight: 600;
    color: #3D405B;
    text-align: center;
    margin-top: 20px;
}
.subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: #7A7D91;
    margin-bottom: 50px;
}

/* Sidebar Style */
[data-testid="stSidebar"] {
    background-color:  black; /* Light background */
    border-right: 5px solid yellow; /* Light border */
    border-left: 5px solid yellow; /* Light border */
    padding: 1.5rem;
    box-shadow: 5px 0 8px rgba(0,0,0,0.05);
}
section[data-testid="stSidebar"] button {
    background: linear-gradient(to right,gold);
    color: black;
    font-weight: 1000;
    border-radius: 100px;
    margin: 1px 0;
    width: 100%;
    text-align: center;
    transition: 0.25s;
}
section[data-testid="stSidebar"] button:hover {
    background: linear-gradient(to right, LIGHTGREEN, gold);
    transform: translateX(4px);
}
/* Avatar Card Inside Navigation Sidebar */
.user-card {
    margin: 20px auto;
    padding: 16px;
    border-radius: 12px; /* Rectangular card */
    background: lightblue;
    border-left: 4px solid yellow;
    text-align: center;
    width: 90%;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* Avatar Image - Rectangular */
.user-card img {
    width: 100px;
    height: 100px;
    border-radius: 10px; /* Make the image rectangular with slight curve */
    object-fit: cover;
    margin-bottom: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
}

/* Name */
.user-card h4 {
    margin: 0;
    font-weight: 700;
    color: #3D405B;
    font-size: 1.2rem;
}

/* Role / Info */
.user-card p {
    margin: 5px 0 0;
    color: #3D405B;
    font-size: 0.85rem;
}


/* Animated background */
body::before {
    content: '';
    position: fixed;
    width: 100%;
    height: 100%;
    background: linear-gradient(-45deg, #FDE2E4, #E0BBE4, #957DAD, #D291BC);
    background-size: 400% 400%;
    animation: gradientMove 15s ease infinite;
    z-index: -1;
    top: 0;
    left: 0;
    opacity: 0.3;
}

@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Simulated Loading Animation (only on Home for now) ---
if st.session_state.current_page == "Home":
    with st.spinner("Loading Home Page..."):
        st.markdown("""
        <div class='main-title'>Employee Salary Prediction System</div>
        <div class='subtitle'>Smart AI-powered platform to predict salaries of employees in the Indian job market using advanced machine learning models.</div>

        <img src="data:image/jpeg;base64,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"  width="50%" style="border-radius: 20px; margin-bottom: 30px; display: block; margin-left: auto; margin-right: auto;"/>
        <br/>
                    
        ### 🎯 Overview
        - 📌 Predict employee salaries in real-time.
        - 📌 Benchmark compensation using industry data.
        - 📌 Automate salary forecasting for HR professionals and analysts.

        ### 🧠 Key Features
        - ✅ **What-If Scenario Testing**
        - ✅ **Resume Upload (PDF Parsing)**
        - ✅ **Model Interpretability with SHAP**
        - ✅ **Downloadable PDF Salary Report (Upcoming)**
        - ✅ **Time Series Salary Forecasting (Planned)**

        ### 📊 Technology Stack
        | Category           | Tools Used                                  |
        |--------------------|---------------------------------------------|
        | Programming        | Python                                      |
        | Data Processing    | Pandas, NumPy                               |
        | Machine Learning   | Scikit-learn, Random Forest, XGBoost        |
        | Visualization      | Seaborn, Matplotlib                         |
        | Frontend           | Streamlit (for interactive UI)              |
        | Backend/Deployment | Flask (for model API), Render/Streamlit Cloud |

        ### 📈 Model Performance
        | Metric            | Value              |
        |------------------|--------------------|
        | 📊 R² Score        | **87.3%** (Random Forest) |
        | 📉 RMSE            | ₹1.2 Lakhs         |
        | 🧾 Dataset Size     | 10,000+ records    |
        | 🧠 Features Used    | 20+ features       |

        ### 👤 About the Developer
        > **Durga Prasad Papugani**  
        > Passionate AI/ML Developer & Intern at IBM SkillsBuild & SmartBridge.  
        > 📧 papugandurgaprasad@email.com  
        > 🌐 GitHub | LinkedIn
        """, unsafe_allow_html=True)

# --- ROUTING TO OTHER PAGES ---
elif st.session_state.current_page == "Salary Prediction":
    from pages import page_salary
    page_salary.show()

elif st.session_state.current_page == "Data Exploration":
    from pages import page_data
    page_data.show()

elif st.session_state.current_page == "Model Analytics":
    from pages import page_model
    page_model.show()

elif st.session_state.current_page == "About":
    from pages import page_about
    page_about.show()
