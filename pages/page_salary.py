import streamlit as st
import pandas as pd
import joblib
from fpdf import FPDF
import datetime
import os

def show():
    # ------------------- Page Styling -------------------
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to right, #f4f7fc, #ffffff);
            font-family: 'Segoe UI', sans-serif;
        }
        .title-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #64ca0a;
            padding-bottom: 1rem;
            text-align: center;
            text-shadow: 1px 1px 2px #ccc;
        }
        .input-section {
            background-color: #ffffff;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            border: 1px solid #e0e0e0;
        }
        .stButton>button {
            background: linear-gradient(to right, #1e3c72, #2a5298);
            color: white;
            font-weight: bold;
            width: 100%;
            padding: 12px 24px;
            border-radius: 8px;
            border: none;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: all 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background: linear-gradient(to right, #0f2b61, #22438c);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        }
        .stSuccess {
            background-color: #e6ffed;
            border-left: 5px solid #28a745;
            padding: 1rem;
            border-radius: 8px;
            font-size: 1.2rem;
            font-weight: bold;
            color: #155724;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='title-header'>Salary Prediction Tool</div>", unsafe_allow_html=True)

    # ------------------- Load ML Model -------------------
    @st.cache_resource
    def load_model():
        try:
            return joblib.load("models/salary_model.pkl")
        except Exception as e:
            st.error(f"❌ Error loading model: {e}")
            st.stop()

    model = load_model()

    # ------------------- Form-based Input -------------------
    with st.form("salary_form"):
        st.markdown("<div class='input-section'>", unsafe_allow_html=True)
        st.subheader("📝 Enter Employee Details")

        col1, col2 = st.columns(2)
        with col1:
            age = st.slider("Age", 20, 60, 30)
            gender = st.selectbox("Gender", ["Male", "Female"])
            education = st.selectbox("Education Level", ["High School", "Bachelors", "Masters", "PhD"])
            experience = st.slider("Years of Experience", 0.0, 40.0, 5.0, 0.5)
            department = st.selectbox("Department", ["Tech", "HR", "Finance", "Marketing", "Operations", "Support"])
        with col2:
            title = st.selectbox("Job Title", ["Engineer", "Manager", "Analyst", "Lead", "Executive"])
            performance = st.slider("Performance Rating (1-5)", 1, 5, 4)
            city = st.selectbox("City Tier", ["Tier 1", "Tier 2", "Tier 3"])
            size = st.selectbox("Company Size", ["Startup", "Mid", "Enterprise"])
            ctype = st.selectbox("Company Type", ["Private", "Public", "MNC"])

        tech = st.slider("Technical Skills Score (0-100)", 0, 100, 75)
        certs = st.slider("Number of Certifications", 0, 10, 1)

        submitted = st.form_submit_button("💰 Predict Salary")
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------- Prediction Logic -------------------
    if 'prediction' not in st.session_state:
        st.session_state.prediction = None

    if submitted:
        input_data = {
            "Age": age,
            "Gender": gender,
            "Education": education,
            "Experience": experience,
            "Department": department,
            "Title": title,
            "Performance": performance,
            "CityTier": city,
            "CompanySize": size,
            "CompanyType": ctype,
            "TechSkill": tech,
            "Certs": certs,
            "English": "Advanced"  # Hardcoded or can be added as dropdown
        }

        input_df = pd.DataFrame([input_data])
        try:
            st.session_state.prediction = model.predict(input_df)[0]
        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
            st.session_state.prediction = None

    # ------------------- Show Result & Generate Report -------------------
    if st.session_state.prediction is not None:
        st.markdown(f"<div class='stSuccess'>Predicted Salary: ₹{int(st.session_state.prediction):,}</div>", unsafe_allow_html=True)
        st.markdown("---")

        def generate_pdf_report(salary, inputs):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "Employee Salary Prediction Report", ln=True, align='C')
            pdf.ln(10)

            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, f"Predicted Salary: ₹{int(salary):,}", ln=True)
            pdf.ln(5)

            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, "Employee Details:", ln=True)
            pdf.set_font("Arial", '', 11)
            for key, value in inputs.items():
                pdf.cell(0, 8, f"- {key}: {value}", ln=True)

            os.makedirs("downloads", exist_ok=True)
            filename = f"Salary_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            path = os.path.join("downloads", filename)
            pdf.output(path)
            return path

        try:
            pdf_path = generate_pdf_report(st.session_state.prediction, input_data)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Download PDF Report",
                    data=f.read(),
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"❌ Could not generate PDF: {e}")

# Run standalone
if __name__ == "__main__":
    show()
