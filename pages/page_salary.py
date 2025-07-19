import streamlit as st
import pandas as pd
import joblib
from fpdf import FPDF
import datetime
import os
from PyPDF2 import PdfReader

def show():
    """
    Renders the Salary Prediction page with advanced features.
    This function encapsulates all the UI and logic for this specific page.
    """
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
            model_pipeline = joblib.load("models/salary_model.pkl")  # Your trained pipeline
            return model_pipeline
        except FileNotFoundError:
            st.error("Model file not found. Please ensure 'salary_model.pkl' is in the 'models' folder.")
            st.stop()
        except Exception as e:
            st.error(f"Error loading model: {e}")
            st.stop()

    model = load_model()

    # ------------------- Input Form -------------------
    with st.form("salary_form"):
        st.markdown("<div class='input-section'>", unsafe_allow_html=True)
        st.subheader("👤 Enter Employee Information")

        col1, col2 = st.columns(2)
        with col1:
            age = st.slider("Age", 22, 60, 30)
            gender = st.selectbox("Gender", ["Male", "Female"])
            education = st.selectbox("Education Level", ["High School", "Bachelors", "Masters", "PhD"])
            experience = st.slider("Years of Experience", 0.0, 40.0, 5.0, 0.5)
            department = st.selectbox("Department", ["Tech", "HR", "Finance", "Marketing", "Operations", "Support"])
            title = st.selectbox("Job Title", ["Engineer", "Manager", "Analyst", "Lead", "Executive"])
        with col2:
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
            "Age": age, "Gender": gender, "Education": education,
            "Experience": experience, "Department": department, "Title": title,
            "Performance": performance, "CityTier": city, "CompanySize": size,
            "CompanyType": ctype, "TechSkill": tech, "Certs": certs,
            "English": "Advanced"  # Default value (can be changed later)
        }

        input_df = pd.DataFrame([input_data])
        try:
            prediction_value = model.predict(input_df)[0]
            st.session_state.prediction = prediction_value
        except Exception as e:
            st.error(f"Prediction failed. Please check input values. Error: {e}")
            st.session_state.prediction = None

    # ------------------- Prediction Result and Report -------------------
    if st.session_state.prediction is not None:
        st.markdown(f"<div class='stSuccess'>Predicted Salary: ₹{int(st.session_state.prediction):,}</div>", unsafe_allow_html=True)
        st.markdown("---")

        # --- PDF Report Generator ---
        def generate_pdf_report(salary, inputs):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "Employee Salary Prediction Report", ln=True, align='C')
            pdf.ln(10)

            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, f"Predicted Salary: Rs. {int(salary):,}", ln=True, align='L')
            pdf.ln(5)

            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, "Input Parameters:", ln=True)
            pdf.set_font("Arial", '', 11)

            for key, value in inputs.items():
                pdf.cell(0, 8, f"- {key}: {value}", ln=True)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Salary_Report_{timestamp}.pdf"
            os.makedirs("downloads", exist_ok=True)
            filepath = os.path.join("downloads", filename)
            pdf.output(filepath)
            return filepath

        try:
            report_path = generate_pdf_report(st.session_state.prediction, input_data)
            with open(report_path, "rb") as pdf_file:
                st.download_button(
                    label="📄 Download Salary Report",
                    data=pdf_file.read(),
                    file_name=os.path.basename(report_path),
                    mime="application/octet-stream",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"Failed to generate report: {e}")

    # ------------------- Resume Parser (Optional) -------------------
    st.markdown("---")
    with st.expander("📄 Upload Resume to Parse (Optional)"):
        uploaded_file = st.file_uploader("Upload your resume in PDF format", type="pdf", key="resume_uploader")
        if uploaded_file:
            try:
                reader = PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                st.text_area("📑 Extracted Resume Text", text, height=250, help="This is the raw text extracted from your PDF.")
            except Exception as e:
                st.error(f"⚠️ Could not read the PDF file. It might be corrupted or image-based. Error: {e}")

# To run directly
if __name__ == "__main__":
    show()
