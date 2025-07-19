import streamlit as st
import pandas as pd
import joblib
from fpdf import FPDF
import datetime
import os

def show():
    # --------- Custom CSS (Background changed only) ---------
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to right, #e0f7fa, #ffffff);
            font-family: 'Segoe UI', sans-serif;
        }
        .title-header {
            font-size: 2.5rem;
            font-weight: 700;
            text-align: center;
            color: #1f2937;
            padding-top: 1rem;
        }
        .form-container {
            background-color: #ffffff;
            max-width: 600px;
            margin: 2rem auto;
            padding: 40px 30px;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        }
        .form-container h3 {
            font-size: 1.4rem;
            margin-bottom: 1.5rem;
            color: #111827;
            border-bottom: 1px solid #e5e7eb;
            padding-bottom: 10px;
        }
        label {
            font-weight: 600 !important;
            color: #374151 !important;
        }
        .stSelectbox, .stNumberInput {
            margin-bottom: 1.5rem;
        }
        .stButton>button {
            background: #10b981;
            color: white;
            padding: 12px 0;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(16, 185, 129, 0.4);
        }
        .stButton>button:hover {
            background: #059669;
            transform: scale(1.02);
        }
        .stSuccess {
            background-color: #ecfdf5;
            border-left: 5px solid #10b981;
            padding: 1rem;
            border-radius: 8px;
            color: #065f46;
            font-weight: bold;
            text-align: center;
            margin-top: 1.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='title-header'>💼 Salary Prediction Form</div>", unsafe_allow_html=True)

    @st.cache_resource
    def load_model():
        try:
            return joblib.load("models/salary_model.pkl")
        except Exception as e:
            st.error(f"Model load error: {e}")
            st.stop()

    model = load_model()

    # --------- Form ----------
    with st.form("predict_form"):
        st.markdown("<div class='form-container'><h3>📋 Fill Employee Details</h3>", unsafe_allow_html=True)

        age = st.selectbox("Age", list(range(18, 61)), index=10)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        education = st.selectbox("Education Level", [
            "High School", "Bachelors", "Masters", "PhD", "Other",
            "Diploma", "Certification", "Vocational Training", "Associate Degree",
            "Professional Degree", "Secondary School", "Primary School", "No Formal Education"
        ])
        experience = st.selectbox("Years of Experience", [round(i * 0.5, 1) for i in range(0, 81)], index=10)
        department = st.selectbox("Department", [
            "Tech", "HR", "Finance", "Marketing", "Operations", "Support", "Sales", "AI/ML",
            "Data Science", "Cloud Computing", "Cybersecurity", "DevOps", "Blockchain",
            "Product Management", "UI/UX Design", "Business Intelligence", "Remote Operations",
            "Sustainability & ESG", "Customer Experience (CX)", "Growth Marketing",
            "Digital Transformation", "Platform Engineering", "Other"
        ])
        title = st.selectbox("Job Title", [
            "Engineer", "Manager", "Analyst", "Lead", "Executive", "AI Engineer", "Data Scientist",
            "ML Engineer", "Prompt Engineer", "DevOps Engineer", "Cloud Architect", "Cybersecurity Specialist",
            "Blockchain Developer", "Product Manager", "UX/UI Designer", "Software Developer",
            "Frontend Developer", "Backend Developer", "Full Stack Developer", "Business Analyst",
            "BI Analyst", "Operations Manager", "Marketing Specialist", "Digital Strategist",
            "Growth Hacker", "Sales Executive", "Customer Success Manager", "Technical Recruiter",
            "HR Business Partner", "Finance Analyst", "CTO", "CIO", "COO", "Chief Data Officer",
            "Head of Engineering", "VP of Product", "Director of Marketing", "Strategy Consultant"
        ])
        performance = st.selectbox("Performance Rating", list(range(1, 6)), index=3)
        city = st.selectbox("City Tier", [
            "Tier 1 - Metro (e.g., Mumbai, Delhi, Bangalore)",
            "Tier 2 - Developing Cities (e.g., Pune, Kochi, Indore)",
            "Tier 3 - Small Towns / Rural Areas"
        ])
        size = st.selectbox("Company Size", [
            "Startup - <100 employees", "Mid - 100-999 employees", "Enterprise - 1000+ employees"
        ])
        ctype = st.selectbox("Company Type", [
            "Private", "Public", "MNC", "Government", "Non-Profit", "Joint Venture"
        ])
        tech = st.selectbox("Technical Skills Score", list(range(0, 101, 5)), index=15)
        certs = st.selectbox("Certifications Count", list(range(0, 11)), index=1)

        submitted = st.form_submit_button("💰 Predict Salary")
        st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        raw_data = {
            "Age": age, "Gender": gender, "Education": education,
            "Experience": experience, "Department": department, "Title": title,
            "Performance": performance, "CityTier": city, "CompanySize": size,
            "CompanyType": ctype, "TechSkill": tech, "Certs": certs,
            "English": "Advanced"
        }

        try:
            # Ensure correct order of features
            expected_cols = list(model.feature_names_in_)
            df = pd.DataFrame([[raw_data[col] for col in expected_cols]], columns=expected_cols)

            prediction = model.predict(df)[0]
            st.session_state.prediction = prediction
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            return

        st.markdown(f"<div class='stSuccess'>Predicted Salary: Rs. {int(prediction):,}</div>", unsafe_allow_html=True)

        def generate_pdf(salary, details):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "Employee Salary Prediction Report", ln=True, align='C')
            pdf.ln(8)

            pdf.set_font("Arial", 'B', 14)
            pdf.set_fill_color(240, 248, 255)
            pdf.cell(0, 12, f"Predicted Salary: Rs. {int(salary):,}", ln=True, fill=True)
            pdf.ln(10)

            pdf.set_font("Arial", 'B', 12)
            pdf.set_fill_color(220, 220, 220)
            pdf.cell(70, 10, "Attribute", border=1, fill=True)
            pdf.cell(0, 10, "Value", border=1, fill=True)
            pdf.ln()

            pdf.set_font("Arial", '', 11)
            fill = False
            for key, value in details.items():
                safe_key = str(key).replace("–", "-").encode("latin-1", "ignore").decode("latin-1")
                safe_value = str(value).replace("–", "-").encode("latin-1", "ignore").decode("latin-1")
                pdf.set_fill_color(245, 245, 245) if fill else pdf.set_fill_color(255, 255, 255)
                pdf.cell(70, 9, safe_key, border=1, fill=True)
                pdf.cell(0, 9, safe_value, border=1, fill=True)
                pdf.ln()
                fill = not fill

            os.makedirs("downloads", exist_ok=True)
            filename = f"Salary_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.join("downloads", filename)
            pdf.output(filepath)
            return filepath

        try:
            path = generate_pdf(prediction, raw_data)
            with open(path, "rb") as f:
                st.download_button("📄 Download PDF Report", f.read(), file_name=os.path.basename(path), mime="application/pdf", use_container_width=True)
        except Exception as e:
            st.error(f"PDF generation error: {e}")

# Run directly if needed
if __name__ == "__main__":
    show()
