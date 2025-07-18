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

        <img src="https://th.bing.com/th/id/OIP.IQszNd8EzN1YOsfVwLhzzwHaHa?w=184&h=183&c=7&r=0&o=5&dpr=1.3&pid=1.7"  width="50%" style="border-radius: 20px; margin-bottom: 30px; display: block; margin-left: auto; margin-right: auto;"/>
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
        | 📊 R² Score        | **90.3%** (Random Forest) |
        | 📉 RMSE            | ₹1.2 Lakhs         |
        | 🧾 Dataset Size     | 10,000+ records    |
        | 🧠 Features Used    | 25+ features       |

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
