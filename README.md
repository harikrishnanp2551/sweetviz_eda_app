# Sweetviz Streamlit Data Analysis App

A comprehensive data analysis web application built with Streamlit and Sweetviz for automated Exploratory Data Analysis (EDA).

## Features

🚀 **Easy File Upload**: Support for CSV and JSON files  
📊 **Data Preview**: Instant data preview with basic statistics  
🍭 **Sweetviz Integration**: Comprehensive automated EDA reports  
📥 **Download Reports**: Export analysis as HTML files  
⚠️ **Large Dataset Handling**: Automatic filtering for datasets > 100k rows  
🎨 **Beautiful UI**: Clean, professional interface  

## How to Use

1. **Upload your data file** using the sidebar file uploader
2. **Preview your data** and check the basic statistics  
3. **Generate Sweetviz report** by clicking the analysis button
4. **Download the report** for future reference

## Installation & Setup

### Local Development

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run sweetviz_streamlit_app.py
```

### Deploy on Streamlit Cloud

1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Connect your GitHub repository
4. Deploy the app using `sweetviz_streamlit_app.py` as the main file

## File Format Support

- **CSV files** (.csv) - Comma-separated values
- **JSON files** (.json) - JavaScript Object Notation

## Important Notes

- Maximum dataset size: **100,000 rows**
- Files larger than 100k rows will be automatically truncated to the first 100k rows
- Analysis may take several minutes for large datasets
- All processing is done server-side for security

## About Sweetviz

Sweetviz is an open-source Python library that generates beautiful, high-density visualizations for EDA with minimal code. The reports include:

- Detailed feature analysis for each column
- Correlation matrices and associations  
- Missing value analysis
- Statistical summaries
- Distribution plots and visualizations

## Sample Data

The app includes sample datasets you can download and test:
- Titanic dataset sample
- Sales data sample

## License

This project is open source and available under the MIT License.
