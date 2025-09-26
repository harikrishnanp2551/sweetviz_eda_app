import streamlit as st
import pandas as pd
import sweetviz as sv
import streamlit.components.v1 as components
import os
import tempfile
import json
from io import StringIO

# Set page configuration
st.set_page_config(
    page_title="Sweetviz Data Analysis App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fee;
        border: 1px solid #fcc;
        color: #c33;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #efe;
        border: 1px solid #cfc;
        color: #3c3;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #e7f3ff;
        border: 1px solid #b3d9ff;
        color: #0066cc;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Sweetviz Data Analysis App</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload your CSV or JSON file for comprehensive automated EDA</p>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.header("Upload Data")
    st.sidebar.markdown("---")

    # File uploader
    uploaded_file = st.sidebar.file_uploader(
        "Choose a file",
        type=['csv', 'json'],
        help="Upload a CSV or JSON file (max 100k rows)"
    )

    if uploaded_file is not None:
        try:
            # Get file details
            file_details = {
                "filename": uploaded_file.name,
                "filetype": uploaded_file.type,
                "filesize": uploaded_file.size
            }

            # Display file info
            st.sidebar.success(f"✅ File uploaded: {file_details['filename']}")
            st.sidebar.info(f"📁 Size: {file_details['filesize']:,} bytes")

            # Load data based on file type
            with st.spinner("Loading data..."):
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith('.json'):
                    df = pd.read_json(uploaded_file)
                else:
                    st.error("❌ Unsupported file format!")
                    return

            # Check data size and apply filtering if necessary
            original_rows = len(df)

            if original_rows > 100000:
                error_html = f"""
                <div class="error-box">
                    <strong>⚠️ Large Dataset Warning</strong><br>
                    Your dataset has <strong>{original_rows:,}</strong> rows, which exceeds the 100,000 row limit.
                    <br><br>
                    The analysis will be performed on the <strong>first 100,000 rows</strong> only.
                </div>
                """
                st.markdown(error_html, unsafe_allow_html=True)

                df = df.head(100000)
                info_html = f"""
                <div class="info-box">
                    <strong>📊 Dataset Limited</strong><br>
                    Now working with <strong>{len(df):,}</strong> rows for analysis.
                </div>
                """
                st.markdown(info_html, unsafe_allow_html=True)

            # Display basic data information
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("📈 Rows", f"{len(df):,}")
            with col2:
                st.metric("📊 Columns", len(df.columns))
            with col3:
                st.metric("💾 Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
            with col4:
                missing_percentage = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
                st.metric("❓ Missing Data", f"{missing_percentage:.1f}%")

            # Show data preview
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)

            # Column information
            with st.expander("🔍 Column Information", expanded=False):
                col_info = pd.DataFrame({
                    'Column': df.columns,
                    'Data Type': df.dtypes,
                    'Non-Null Count': df.count(),
                    'Null Count': df.isnull().sum(),
                    'Null Percentage': (df.isnull().sum() / len(df) * 100).round(2)
                })
                st.dataframe(col_info, use_container_width=True)

            # Generate Sweetviz report
            st.subheader("🍭 Sweetviz Analysis Report")

            if st.button("🚀 Generate Analysis Report", type="primary"):
                with st.spinner("Generating Sweetviz analysis... This may take a few minutes."):
                    try:
                        # Create Sweetviz analysis
                        report = sv.analyze(df)

                        # Generate HTML report in a temporary file
                        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as tmp_file:
                            report.show_html(
                                filepath=tmp_file.name,
                                open_browser=False,
                                layout='vertical',
                                scale=1.0
                            )
                            html_file_path = tmp_file.name

                        # Read the HTML file
                        with open(html_file_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()

                        # Display the HTML report using components
                        success_html = """
                        <div class="success-box">
                            <strong>✅ Analysis Complete!</strong><br>
                            Your Sweetviz report has been generated successfully. Scroll through the report below to explore your data insights.
                        </div>
                        """
                        st.markdown(success_html, unsafe_allow_html=True)

                        # Display the HTML report
                        components.html(
                            html_content,
                            height=1000,
                            scrolling=True
                        )

                        # Clean up temporary file
                        os.unlink(html_file_path)

                        # Provide download option for the report
                        st.download_button(
                            label="📥 Download HTML Report",
                            data=html_content,
                            file_name=f"sweetviz_report_{uploaded_file.name.split('.')[0]}.html",
                            mime="text/html"
                        )

                    except Exception as e:
                        st.error(f"❌ Error generating Sweetviz report: {str(e)}")
                        st.error("Please check your data format and try again.")

        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.error("Please make sure your file is properly formatted.")

    else:
        # Instructions when no file is uploaded
        st.markdown("""
        ## 🚀 How to Use This App

        1. **📁 Upload your data file** using the sidebar file uploader
        2. **📊 Preview your data** and check the basic statistics
        3. **🍭 Generate Sweetviz report** by clicking the analysis button
        4. **📥 Download the report** for future reference

        ### 📋 Supported File Formats
        - **CSV files** (.csv)
        - **JSON files** (.json)

        ### ⚠️ Important Notes
        - Maximum dataset size: **100,000 rows**
        - Files larger than 100k rows will be automatically truncated
        - Analysis may take several minutes for large datasets
        - The generated report includes comprehensive EDA visualizations

        ### 🍭 About Sweetviz
        Sweetviz is an open-source Python library that generates beautiful, 
        high-density visualizations to kickstart EDA (Exploratory Data Analysis) 
        with just two lines of code. It provides:

        - **Detailed feature analysis** for each column
        - **Correlation matrices** and associations
        - **Missing value analysis**
        - **Statistical summaries**
        - **Distribution plots** and visualizations
        """)

        # Sample data section
        st.markdown("### 📊 Try with Sample Data")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🏠 Load Titanic Dataset"):
                # Create sample Titanic dataset
                sample_data = {
                    'PassengerId': range(1, 101),
                    'Survived': [0, 1] * 50,
                    'Pclass': [1, 2, 3] * 33 + [1],
                    'Age': [22 + i*0.5 for i in range(100)],
                    'SibSp': [0, 1, 2] * 33 + [0],
                    'Parch': [0, 1] * 50,
                    'Fare': [7.25 + i*2 for i in range(100)],
                    'Embarked': ['S', 'C', 'Q'] * 33 + ['S']
                }
                sample_df = pd.DataFrame(sample_data)

                csv = sample_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Titanic Sample CSV",
                    data=csv,
                    file_name="titanic_sample.csv",
                    mime="text/csv"
                )

        with col2:
            if st.button("🏪 Load Sales Dataset"):
                # Create sample sales dataset
                import random
                sample_sales = {
                    'Date': pd.date_range('2023-01-01', periods=100),
                    'Product': [f'Product_{chr(65+i%5)}' for i in range(100)],
                    'Sales': [random.randint(100, 1000) for _ in range(100)],
                    'Quantity': [random.randint(1, 50) for _ in range(100)],
                    'Price': [random.uniform(10, 100) for _ in range(100)],
                    'Region': ['North', 'South', 'East', 'West'] * 25
                }
                sample_sales_df = pd.DataFrame(sample_sales)

                csv = sample_sales_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Sales Sample CSV",
                    data=csv,
                    file_name="sales_sample.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
