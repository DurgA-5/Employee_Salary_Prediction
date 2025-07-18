import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Cache the data loading to improve performance
@st.cache_data
def load_data():
    """Loads the employee dataset from a CSV file."""
    try:
        return pd.read_csv("data/employee_data.csv")  # Adjust path if needed
    except FileNotFoundError:
        st.error("Dataset 'employee_data.csv' not found. Please place it in the 'data' directory.")
        st.stop()

def show():
    # ------------------- Page Styling (CSS) -------------------
    st.markdown("""
        <style>
        /* General App Style */
        .stApp {
            background-color: #f0f2f6; /* A clean, light grey background */
            font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
        }

        /* Main Title */
        .main-title {
            font-size: 2.8rem;
            font-weight: 700;
            color: #2C3E50; /* Dark slate blue for high contrast */
            text-align: center;
            padding-bottom: 20px;
            margin-bottom: 30px;
            border-bottom: 2px solid #e0e0e0;
        }

        /* Section Headers (for non-collapsible sections) */
        .section-header {
            color: #2C3E50;
            font-size: 1.8rem;
            font-weight: 600;
            border-left: 5px solid #1abc9c; /* A modern teal accent */
            padding-left: 15px;
            margin-top: 40px;
            margin-bottom: 20px;
        }
        
        /* Container for Filters and Metrics */
        .card-container {
            background-color: #FFFFFF;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Use markdown for the styled title
    st.markdown("<h1 class='main-title'>📊 Data Exploration & Insights</h1>", unsafe_allow_html=True)

    # Load dataset
    df = load_data()

    # --- Dataset Overview (Remains visible) ---
    st.markdown("<h2 class='section-header'>📋 Dataset Overview</h2>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='card-container'>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Employees", f"{len(df):,}")
        col2.metric("Features", len(df.columns))
        col3.metric("Avg Salary", f"₹{df['Salary'].mean() / 100000:.2f} L")
        col4.metric("Salary Range", f"₹{df['Salary'].min() / 100000:.2f} L - ₹{df['Salary'].max() / 100000:.2f} L")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Filters (Remains visible) ---
    st.markdown("<h2 class='section-header'>🎛️ Data Filters</h2>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='card-container'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        departments = ["All"] + sorted(df["Department"].unique())
        cities = ["All"] + sorted(df["CityTier"].unique())
        dept = col1.selectbox("Filter by Department", departments)
        city = col2.selectbox("Filter by City Tier", cities)
        exp_range = col3.slider(
            "Filter by Years of Experience",
            float(df["Experience"].min()), float(df["Experience"].max()),
            (float(df["Experience"].min()), float(df["Experience"].max()))
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Apply filters
    filtered_df = df.copy()
    if dept != "All": filtered_df = filtered_df[filtered_df["Department"] == dept]
    if city != "All": filtered_df = filtered_df[filtered_df["CityTier"] == city]
    filtered_df = filtered_df[(filtered_df["Experience"] >= exp_range[0]) & (filtered_df["Experience"] <= exp_range[1])]

    st.write(f"🔍 **Filtered Dataset Preview** ({len(filtered_df):,} employees matching criteria)")
    st.dataframe(filtered_df.head(10))

    # --- Visualizations (only if data exists) ---
    if len(filtered_df) > 0:
        # Create Experience Group for better bucketing
        filtered_df["Experience Group"] = pd.cut(
            filtered_df["Experience"],
            bins=[0, 2, 5, 10, 20, filtered_df["Experience"].max() + 1],
            labels=["0-2 yrs", "2-5 yrs", "5-10 yrs", "10-20 yrs", "20+ yrs"], right=False
        )

        # --- MODIFIED: Sections are now in collapsible expanders ---
        
        with st.expander("📈 Salary Analysis", expanded=False):
            fig_box = px.box(
                filtered_df, x="Department", y="Salary", color="Department",
                title="Salary Distribution by Department"
            )
            st.plotly_chart(fig_box, use_container_width=True)

        with st.expander("👥 Demographics Overview", expanded=False):
            tab1, tab2 = st.tabs(["🔘 Pie Charts", "📊 Bar Charts"])

            # Pie Charts Tab
            with tab1:
                col1, col2 = st.columns(2)
                col1.plotly_chart(px.pie(filtered_df, names="Gender", title="Gender Distribution", hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel), use_container_width=True)
                col2.plotly_chart(px.pie(filtered_df, names="Education", title="Education Level", hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3), use_container_width=True)
                col3, col4 = st.columns(2)
                col3.plotly_chart(px.pie(filtered_df, names="Experience Group", title="Experience Level", hole=0.4, color_discrete_sequence=px.colors.qualitative.Vivid), use_container_width=True)
                col4.plotly_chart(px.pie(filtered_df, names="CityTier", title="City Tier Spread", hole=0.4, color_discrete_sequence=px.colors.qualitative.Safe), use_container_width=True)

            # Bar Charts Tab
            with tab2:
                col1, col2 = st.columns(2)
                col1.plotly_chart(px.bar(filtered_df["Gender"].value_counts().reset_index(), x="Gender", y="count", color="Gender", title="Gender Distribution (Bar)"), use_container_width=True)
                col2.plotly_chart(px.bar(filtered_df["Education"].value_counts().reset_index(), x="Education", y="count", color="Education", title="Education Levels (Bar)"), use_container_width=True)
                col3, col4 = st.columns(2)
                exp_bar = filtered_df["Experience Group"].value_counts().sort_index().reset_index()
                col3.plotly_chart(px.bar(exp_bar, x="Experience Group", y="count", color="Experience Group", title="Experience Levels (Bar)"), use_container_width=True)
                col4.plotly_chart(px.bar(filtered_df["CityTier"].value_counts().reset_index(), x="CityTier", y="count", color="CityTier", title="City Tier Spread (Bar)"), use_container_width=True)

        with st.expander("🏢 Company Insights", expanded=False):
            company_avg_salary = filtered_df.groupby("CompanyType")["Salary"].mean().reset_index()
            fig_company = px.bar(company_avg_salary, x="CompanyType", y="Salary", title="Avg Salary by Company Type", color="CompanyType")
            st.plotly_chart(fig_company, use_container_width=True)

        with st.expander("🔗 Correlation Heatmap", expanded=False):
            num_df = filtered_df.select_dtypes(include=['float64', 'int64'])
            corr = num_df.corr()
            
            fig_heatmap, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(corr, annot=True, cmap="viridis", fmt=".2f", ax=ax, linewidths=.5)
            st.pyplot(fig_heatmap)
    else:
        st.warning("⚠️ No data available for the selected filters. Please adjust your selections.")

if __name__ == "__main__":
    show()