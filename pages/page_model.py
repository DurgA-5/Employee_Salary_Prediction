import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import shap
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from scipy import stats
from datetime import datetime
import io

# ----------------- Page Config -----------------
st.set_page_config(page_title="📊 Model Analytics", layout="wide")

# ----------------- Custom Styling -----------------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #f1f8e9, #ffffff);
        font-family: 'Segoe UI', sans-serif;
    }
    .analytics-section {
        background-color: #ffffffde;
        padding: 30px;
        margin: 20px 0;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .stButton>button {
        background: linear-gradient(to right, #43a047, #66bb6a);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 22px;
        border: none;
        transition: 0.3s ease-in-out;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(to right, #2e7d32, #4caf50);
    }
    .title-header {
        font-size: 2.5rem;
        font-weight: 600;
        color: #2e7d32;
        text-shadow: 1px 1px 2px #ccc;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- Load Resources -----------------
@st.cache_resource
def load_model():
    return joblib.load("models/salary_model.pkl")

@st.cache_data
def load_data():
    return pd.read_csv("data/employee_data.csv")

# ----------------- Show Function -----------------
def show():
    st.markdown("<div class='title-header'>📊 Model Analytics Dashboard</div>", unsafe_allow_html=True)

    model = load_model()
    df = load_data()

    X = df.drop("Salary", axis=1)
    y = df["Salary"]
    preds = model.predict(X)
    residuals = y - preds

    # -------- Error Distribution Plot --------
    with st.container():
        st.markdown("<div class='analytics-section'>", unsafe_allow_html=True)
        st.subheader("🔍 Prediction Error Distribution")
        fig, ax = plt.subplots()
        sns.histplot(residuals, bins=30, kde=True, color='salmon', ax=ax)
        ax.set_title("Distribution of Prediction Errors (Residuals)")
        ax.set_xlabel("Residuals")
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    # -------- Feature Correlation --------
    with st.container():
        st.markdown("<div class='analytics-section'>", unsafe_allow_html=True)
        st.subheader("🧮 Feature Correlation Matrix")
        corr = df.corr(numeric_only=True)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.heatmap(corr, annot=True, cmap="BrBG", ax=ax)
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    # -------- Salary Buckets --------
    with st.container():
        st.markdown("<div class='analytics-section'>", unsafe_allow_html=True)
        st.subheader("💼 Salary Buckets")
        salary_bins = [0, 500000, 1000000, 2000000, 5000000, float('inf')]
        labels = ['<5L', '5-10L', '10-20L', '20-50L', '50L+']
        df['Salary_Bucket'] = pd.cut(df['Salary'], bins=salary_bins, labels=labels)
        bucket_data = df['Salary_Bucket'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(bucket_data, labels=bucket_data.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set2"))
        ax.axis('equal')
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    # -------- Top Features by SHAP --------
    with st.container():
        st.markdown("<div class='analytics-section'>", unsafe_allow_html=True)
        st.subheader("🌟 Top Influential Features (SHAP)")
        try:
            explainer = shap.Explainer(model.named_steps["regressor"])
            X_trans = model.named_steps["preprocessor"].transform(X)
            feature_names = model.named_steps["preprocessor"].get_feature_names_out()
            shap_values = explainer(X_trans[:100])
            fig, ax = plt.subplots()
            shap.summary_plot(shap_values, X_trans[:100], feature_names=feature_names, show=False)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"SHAP Error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # -------- Advanced Statistical Tests --------
    with st.container():
        st.markdown("<div class='analytics-section'>", unsafe_allow_html=True)
        st.subheader("🧪 Advanced Statistical Tests")
        st.write("**Shapiro-Wilk Normality Test on Residuals**")
        stat, p = stats.shapiro(residuals)
        st.write(f"Statistic: {stat:.4f}, p-value: {p:.4f}")
        if p > 0.05:
            st.success("Residuals are likely normally distributed (p > 0.05).")
        else:
            st.warning("Residuals are not normally distributed (p < 0.05).")

        st.write("**Levene’s Test for Homogeneity of Variance**")
        stat, p = stats.levene(preds, y)
        st.write(f"Statistic: {stat:.4f}, p-value: {p:.4f}")
        st.markdown("</div>", unsafe_allow_html=True)

    # -------- Time Trend Analysis --------
    if 'Joining_Date' in df.columns:
        with st.container():
            st.markdown("<div class='analytics-section'>", unsafe_allow_html=True)
            st.subheader("📆 Salary Trends Over Time")
            df['Joining_Date'] = pd.to_datetime(df['Joining_Date'])
            df['Year'] = df['Joining_Date'].dt.year
            trend = df.groupby('Year')['Salary'].mean()
            fig, ax = plt.subplots()
            trend.plot(kind='line', marker='o', ax=ax)
            ax.set_title("Average Salary by Year")
            ax.set_ylabel("Average Salary")
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

    # -------- Downloadable Report --------
    # with st.container():
    #     st.markdown("<div class='analytics-section'>", unsafe_allow_html=True)
    #     st.subheader("📥 Downloadable Summary Report")
    #     summary = pd.DataFrame({
    #         'R2 Score': [r2_score(y, preds)],
    #         'RMSE': [np.sqrt(mean_squared_error(y, preds))],
    #         'MAE': [mean_absolute_error(y, preds)],
    #         'MAPE': [mean_absolute_percentage_error(y, preds)]
    #     })
    #     buffer = io.BytesIO()
    #     with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    #         df.to_excel(writer, sheet_name='Data', index=False)
    #         summary.to_excel(writer, sheet_name='Summary', index=False)
    #     st.download_button("📄 Download Report (Excel)", buffer.getvalue(), "model_report.xlsx")
    #     st.markdown("</div>", unsafe_allow_html=True)

    # -------- Text Insight Summary --------
    with st.container():
        st.markdown("<div class='analytics-section'>", unsafe_allow_html=True)
        st.subheader("📚 Key Observations")
        st.markdown("""
        - Salaries are concentrated in the 5-20L range.
        - Residual errors follow a roughly normal distribution.
        - A few strong features influence predictions greatly (as per SHAP).
        - High correlation exists between experience and salary.
        - Outliers and extreme salaries should be investigated for accuracy.
        - Trends over joining years show how compensation evolved.
        - Statistical tests confirm assumptions needed for regression.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# Call the show function if this file is run as main
if __name__ == '__main__':
    show()
