# pages/page_about.py

import streamlit as st

def show():
    # --- PAGE TITLE & HEADER ---
    st.markdown("<h1 style='text-align: center; color: #3D405B;'>ℹ️ About the Salary Predictor</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # --- PROJECT MISSION ---
    st.header("🎯 Project Mission")
    st.markdown("""
    <div style="background-color:#F0F8FF; padding: 20px; border-radius: 10px; border-left: 5px solid #81B29A;">
    <p style="font-size: 1.1rem; color: #333;">
    The goal of the <strong>Employee Salary Prediction System</strong> is to harness the power of machine learning to provide transparent, data-driven salary insights. We aim to empower HR professionals, job seekers, and data analysts with a reliable tool to understand compensation trends in the Indian job market, fostering fairer and more informed salary negotiations.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # --- SYSTEM ARCHITECTURE ---
    st.header("🏗️ System Architecture")
    st.markdown("""
    - **Frontend:** Built with Streamlit for real-time interactivity.
    - **Backend Model:** Trained using scikit-learn, Random Forest, and XGBoost.
    - **Model API (Planned):** Flask-based REST API for integration with other systems.
    - **Hosting:** Currently runs locally or on Streamlit Cloud.
    - **User Interaction Flow:**
        1. Upload dataset
        2. Select features and target
        3. Train model
        4. Predict & visualize
    """)

    # --- MACHINE LEARNING PIPELINE ---
    st.header("🛠️ Machine Learning Pipeline")
    st.markdown("""
    - 🔄 **Data Cleaning** – Handle missing values, remove outliers
    - 🧠 **Feature Engineering** – Encode categoricals, normalize numeric data
    - 🔍 **Feature Selection** – Correlation analysis, model-based importance
    - ⚙️ **Model Training** – Linear Regression, Random Forest, XGBoost
    - ✅ **Evaluation** – R², RMSE, MAE
    - 💡 **Interpretability** – SHAP values (planned)
    """)

    # --- HOW IT WORKS ---
    st.header("🔍 How It Works")
    st.markdown("""
    1. **Upload your employee dataset** (CSV).
    2. **Select the target column** (e.g., Salary).
    3. The system trains a model in real-time.
    4. Predicts salaries based on user input or the test data.
    5. Explore model performance, feature importance, and download results.
    """)

    # --- USE CASES ---
    st.header("📌 Real-World Use Cases")
    st.markdown("""
    - 📊 **HR Analytics** – Budget forecasting, salary planning.
    - 👨‍💼 **Career Planning** – Estimate your worth based on profile.
    - 📈 **Compensation Benchmarking** – Compare salaries across roles and locations.
    - 🧑‍💻 **EdTech / LMS Projects** – Real-world capstone project showcase.
    """)

    # --- FUTURE ENHANCEMENTS ---
    st.header("🚀 Future Enhancements")
    st.markdown("""
    - 📄 Resume Parsing using NLP
    - 🧠 SHAP-based model interpretability
    - 📥 PDF Salary Report Generation
    - ⏳ Time-Series Forecasting for Salary Growth
    - 🏙️ Region-wise market insights using clustering
    """)

    # --- TESTING & VALIDATION ---
    st.header("🧪 Testing & Validation")
    st.markdown("""
    - ✅ R² Score: **87.3%**
    - 📉 RMSE: ₹1.2 Lakhs
    - 🔀 5-Fold Cross-Validation
    - 🧾 Dataset: Synthesized data of 10,000+ Indian employees
    - 🛡️ Outlier detection and handling using IQR method
    """)

    # --- MEET THE DEVELOPER ---
    st.header("👨‍💻 Meet the Developer")
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.image(
            "https://avatars.githubusercontent.com/u/9919?s=200&v=4", 
            width=200, 
            caption="Durga Prasad Papugani"
        )

    with col2:
        st.subheader("Durga Prasad Papugani")
        st.write("**AI/ML Developer | Intern at IBM SkillsBuild & SmartBridge**")
        st.write("""
        I am a passionate and results-driven AI/ML developer focused on solving real-world problems through machine learning and data science.
        This project reflects my commitment to learning, applying, and delivering solutions in the AI domain.
        """)
        st.markdown("""
        **Certifications & Internships:**
        - 🎓 IBM SkillsBuild – AI/ML Internship (2025)
        - 🎓 SmartBridge – Applied AI Internship
        - 🏅 NPTEL: German-I, Effective Writing, Innovation & Design Thinking
        """)
        st.markdown("""
        **Connect with me:**
        - 📧 **Email:** <a href="mailto:durga@email.com">durga@email.com</a>
        - 🌐 **LinkedIn:** <a href="https://www.linkedin.com/in/durgaprasadpapugani" target="_blank">linkedin.com/in/durgaprasadpapugani</a>
        - 🐱 **GitHub:** <a href="https://github.com/durgaprasadpapugani" target="_blank">github.com/durgaprasadpapugani</a>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- ACKNOWLEDGEMENTS ---
    st.header("🙏 Acknowledgements & Data")
    st.markdown("""
    - 📦 **Technologies Used:** Python, Pandas, Scikit-learn, XGBoost, Streamlit
    - 📈 **Visualization:** Matplotlib, Seaborn
    - 💾 **Model Hosting (Future):** Flask API + Render or Hugging Face Spaces
    - 🧠 **Data:** Synthesized from multiple open datasets and anonymized for privacy
    """)

    # --- USEFUL LINKS ---
    st.header("🔗 Useful Links")
    st.markdown("""
    - 📂 [Project GitHub Repository](https://github.com/durgaprasadpapugani/employee-salary-predictor)
    - 📽️ [Presentation Slides (if available)](https://slides.com/)
    - 📄 [Technical Documentation (Markdown / PDF)](https://docs.google.com/)
    """)

    # --- DISCLAIMER ---
    st.markdown("---")
    st.header("⚖️ Disclaimer")
    st.warning(
        """
        **For Informational Purposes Only:** This salary predictor is an educational project built using machine learning.
        While it offers valuable insights, the predictions should not be considered as financial advice.
        """
    )
