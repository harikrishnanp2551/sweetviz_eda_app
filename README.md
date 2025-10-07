# Enhanced Sweetviz Streamlit Data Analysis App

A comprehensive data analysis web application built with Streamlit and Sweetviz for automated Exploratory Data Analysis (EDA) with advanced comparison capabilities.

### Four Analysis Types Available:

1. **Single Dataset Analysis**
   - Upload one dataset for comprehensive EDA
   - Optional target feature analysis  
   - Perfect for initial data exploration

2. **Compare Two Datasets**
   - Upload two separate datasets to compare
   - Useful for comparing different data sources
   - Example: Comparing data from different time periods or sources

3. **Train/Test Split Comparison**
   - Upload one dataset and automatically split it
   - Compare training vs testing distributions
   - Configurable split ratios and stratification
   - Ensure no data leakage between splits

4. **Sub-population Comparison**
   - Compare sub-groups within the same dataset
   - Group by categorical values or numerical thresholds  
   - Example: Compare different customer segments, age groups, etc.

##  Key Features

🚀 **Easy File Upload**: Support for CSV and JSON files  
📊 **Multiple Analysis Types**: Single, comparison, split, and sub-population analysis  
🍭 **Full Sweetviz Integration**: All three core functions (analyze, compare, compare_intra)  
📥 **Download Reports**: Export all analysis types as HTML files  
⚠️ **Large Dataset Handling**: Automatic filtering for datasets > 100k rows   

## 📋 Analysis Examples

### Compare Two Datasets
Perfect for comparing:
- Training vs Test datasets
- Data from different time periods
- Different data sources
- Before vs After preprocessing

### Train/Test Split Comparison  
Automatically splits your dataset and compares:
- Feature distributions between splits
- Target variable balance
- Missing value patterns
- Statistical differences

### Sub-population Comparison
Compare different groups within your data:
- Male vs Female customers
- Different age groups (Above/Below median)
- High vs Low performers
- Different categories or regions

## Installation & Setup

### Local Development

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements_enhanced.txt
```

3. Run the app:
```bash
streamlit run sweetviz_streamlit_app_enhanced.py
```

### Deploy on Streamlit Cloud

1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Connect your GitHub repository
4. Deploy the app using `sweetviz_streamlit_app_enhanced.py` as the main file
5. Ensure `requirements_enhanced.txt` is in your repository

## File Format Support

- **CSV files** (.csv) - Comma-separated values
- **JSON files** (.json) - JavaScript Object Notation

## Important Notes

- Maximum dataset size: **100,000 rows** per dataset
- Files larger than 100k rows will be automatically truncated to the first 100k rows
- Analysis may take several minutes for large datasets
- All processing is done server-side for security
- Reports are fully interactive and can be shared independently

## Advanced Configuration Options

### Sub-population Analysis
- **Categorical Grouping**: Select any categorical column for grouping
- **Numerical Thresholds**: Set custom thresholds for numerical columns  
- **Force Numerical**: Treat categorical-encoded features as numerical

### Train/Test Split
- **Configurable Split Ratio**: 10% to 90% training size
- **Stratification**: Maintain class distribution in splits
- **Random State**: Reproducible splits with custom random seeds

### Target Analysis
- All analysis types support optional target feature selection
- Enhanced insights when target is specified
- Automatic handling of categorical and numerical targets

## About Sweetviz Integration

This app implements all three core Sweetviz functions:

- **`sv.analyze()`** - Single dataset analysis
- **`sv.compare()`** - Compare two datasets  
- **`sv.compare_intra()`** - Compare sub-populations within same dataset

Each generates comprehensive reports with:
- Detailed feature analysis for each column
- Correlation matrices and associations
- Missing value analysis and patterns  
- Statistical summaries and distributions
- Beautiful, interactive visualizations

## Sample Data

The app includes downloadable sample datasets:
- **Titanic Dataset** - Classic ML dataset for testing
- **Sales Data** - Business analytics sample with multiple categories


