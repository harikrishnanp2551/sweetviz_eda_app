
import os
import tempfile
import pandas as pd
import streamlit as st
import sweetviz as sv
import streamlit.components.v1 as components
from sklearn.model_selection import train_test_split

# ----------------------------
# Page config & styling
# ----------------------------
st.set_page_config(
    page_title="Sweetviz Data Analysis App",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .main-header { font-size: 2.5rem; color: #1f77b4; text-align: center; margin-bottom: .5rem; }
    .sub-header  { font-size: 1.1rem; color: #666; text-align: center; margin-bottom: 1.5rem; }
    .error-box   { padding: 1rem; border-radius: .5rem; background-color: #fee; border: 1px solid #fcc; color: #c33; margin: 1rem 0; }
    .success-box { padding: 1rem; border-radius: .5rem; background-color: #efe; border: 1px solid #cfc; color: #3c3; margin: 1rem 0; }
    .info-box    { padding: 1rem; border-radius: .5rem; background-color: #e7f3ff; border: 1px solid #b3d9ff; color: #0066cc; margin: 1rem 0; }
    .warning-box { padding: 1rem; border-radius: .5rem; background-color: #fff3cd; border: 1px solid #ffeaa7; color: #856404; margin: 1rem 0; }
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# Helpers
# ----------------------------
def load_and_validate_data(uploaded_file, max_rows=100000):
    """Load CSV/JSON and truncate beyond max_rows."""
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.lower().endswith(".json"):
            df = pd.read_json(uploaded_file)
        else:
            return None, "Unsupported file format!"
        original_rows = len(df)
        warning = None
        if original_rows > max_rows:
            df = df.head(max_rows)
            warning = f"Dataset truncated from {original_rows:,} to {max_rows:,} rows."
        return df, warning
    except Exception as e:
        return None, f"Error loading file: {e}"

def display_dataset_info(df, title):
    st.subheader(f" {title}")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📈 Rows", f"{len(df):,}")
    with c2:
        st.metric("📊 Columns", len(df.columns))
    with c3:
        st.metric("💾 Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    with c4:
        missing_pct = (df.isnull().sum().sum() / max(1, len(df) * max(1, len(df.columns)))) * 100
        st.metric("❓ Missing Data", f"{missing_pct:.1f}%")
    with st.expander(f"🔍 Preview {title}", expanded=False):
        st.dataframe(df.head(10), use_container_width=True)

def generate_sweetviz_report(report_obj, report_name, download_filename):
    """Render Sweetviz HTML once and offer a download."""
    with st.spinner("Generating Sweetviz analysis... This may take a few minutes."):
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as tmp:
                report_obj.show_html(
                    filepath=tmp.name,
                    open_browser=False,
                    layout="vertical",
                    scale=1.0,
                )
                html_path = tmp.name
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            st.markdown(
                f"""
<div class="success-box">
  <strong>✅ {report_name} Complete!</strong><br>
  Scroll to explore interactive insights; use the button below to download the full HTML report.
</div>
""",
                unsafe_allow_html=True,
            )
            components.html(html_content, height=1000, scrolling=True)
            os.unlink(html_path)
            st.download_button(
                label="📥 Download HTML Report",
                data=html_content,
                file_name=download_filename,
                mime="text/html",
            )
            return True
        except Exception as e:
            st.error(f"❌ Error generating Sweetviz report: {e}")
            return False

def show_instructions():
    st.markdown(
        """
##  How to proceed

- Use the sidebar to select an analysis type and upload the required dataset(s).  
- When a dataset is uploaded, the app previews rows and shows key stats before generating a Sweetviz report.  
- Reports are embedded below and can be downloaded as standalone HTML.  
""",
    )

# ----------------------------
# Main UI
# ----------------------------
st.markdown('<h1 class="main-header">📊 Sweetviz Data Analysis App</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Automated EDA for single datasets, comparisons, train/test splits, and sub-populations</p>', unsafe_allow_html=True)

st.sidebar.header("📋 Analysis Type")
analysis_type = st.sidebar.selectbox(
    "Choose Analysis Type",
    [
        "📊 Single Dataset Analysis",
        "🔄 Compare Two Datasets",
        "📈 Train/Test Split Comparison",
        "🎯 Sub-population Comparison",
    ],
)

st.sidebar.markdown("---")

# =========================================================
# 1) Single Dataset Analysis
# =========================================================
if analysis_type == "📊 Single Dataset Analysis":
    st.sidebar.header("📁 Upload Data")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a file",
        type=["csv", "json"],
        key="single_file",
        help="Upload a CSV or JSON file (max 100k rows)",
    )
    if uploaded_file is None:
        show_instructions()
    else:
        df, warning = load_and_validate_data(uploaded_file)
        if df is None:
            st.error(f"❌ {warning}")
        else:
            if warning:
                st.markdown(
                    f"""
<div class="warning-box">
  <strong>⚠️ Dataset Size Warning</strong><br>{warning}
</div>
""",
                    unsafe_allow_html=True,
                )
            st.sidebar.success(f"✅ File uploaded: {uploaded_file.name}")
            st.sidebar.info(f"📁 Size: {uploaded_file.size:,} bytes")
            display_dataset_info(df, "Dataset Overview")
            target_feature = st.selectbox(
                "🎯 Select Target Feature (Optional)",
                ["None"] + list(df.columns),
                help="Improve insights by specifying the target",
            )
            if st.button("🚀 Generate Analysis Report", type="primary"):
                target_feat = None if target_feature == "None" else target_feature
                report = sv.analyze([df, uploaded_file.name], target_feat=target_feat)
                generate_sweetviz_report(
                    report,
                    "Analysis",
                    f"sweetviz_analysis_{uploaded_file.name.split('.')[0]}.html",
                )

# =========================================================
# 2) Compare Two Datasets
# =========================================================
elif analysis_type == "🔄 Compare Two Datasets":
    st.sidebar.header("📁 Upload Datasets")
    c1, c2 = st.sidebar.columns(2)
    with c1:
        file1 = st.file_uploader(
            "Source Dataset",
            type=["csv", "json"],
            key="src_file",
            help="First dataset to compare",
        )
    with c2:
        file2 = st.file_uploader(
            "Compare Dataset",
            type=["csv", "json"],
            key="cmp_file",
            help="Second dataset to compare",
        )
    if not file1 or not file2:
        show_instructions()
    else:
        df1, warn1 = load_and_validate_data(file1)
        df2, warn2 = load_and_validate_data(file2)
        if df1 is None or df2 is None:
            if df1 is None:
                st.error(f"❌ Source Dataset: {warn1}")
            if df2 is None:
                st.error(f"❌ Compare Dataset: {warn2}")
        else:
            if warn1:
                st.warning(f"⚠️ Source Dataset: {warn1}")
            if warn2:
                st.warning(f"⚠️ Compare Dataset: {warn2}")
            colA, colB = st.columns(2)
            with colA:
                display_dataset_info(df1, f"Source Dataset ({file1.name})")
            with colB:
                display_dataset_info(df2, f"Compare Dataset ({file2.name})")
            common_cols = set(df1.columns) & set(df2.columns)
            if len(common_cols) == 0:
                st.error("❌ Datasets have no common columns; comparison may not be meaningful.")
            else:
                st.success(f"✅ Found {len(common_cols)} common columns for comparison")
            all_columns = list(set(df1.columns) | set(df2.columns))
            target_feature = st.selectbox(
                "🎯 Select Target Feature (Optional)",
                ["None"] + all_columns,
                help="Must exist in both datasets if selected",
            )
            if st.button("🔄 Generate Comparison Report", type="primary"):
                target_feat = None if target_feature == "None" else target_feature
                if target_feat and (target_feat not in df1.columns or target_feat not in df2.columns):
                    st.error(f"❌ Target feature '{target_feat}' not found in both datasets.")
                else:
                    compare_report = sv.compare(
                        source=[df1, file1.name],
                        compare=[df2, file2.name],
                        target_feat=target_feat,
                    )
                    generate_sweetviz_report(
                        compare_report,
                        "Comparison Analysis",
                        f"sweetviz_compare_{file1.name.split('.')[0]}_vs_{file2.name.split('.')[0]}.html",
                    )

# =========================================================
# 3) Train/Test Split Comparison
# =========================================================
elif analysis_type == "📈 Train/Test Split Comparison":
    st.sidebar.header("📁 Upload Dataset")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a file", type=["csv", "json"], key="split_file"
    )
    if uploaded_file is None:
        show_instructions()
    else:
        df, warning = load_and_validate_data(uploaded_file)
        if df is None:
            st.error(f"❌ {warning}")
        else:
            if warning:
                st.warning(f"⚠️ {warning}")
            display_dataset_info(df, "Full Dataset")
            st.subheader("⚙️ Split Configuration")
            c1, c2, c3 = st.columns(3)
            with c1:
                train_size = st.slider("Training Set Size", 0.1, 0.9, 0.8, 0.05)
            with c2:
                random_state = st.number_input("Random State", 0, 10000, 42)
            with c3:
                stratify_col = st.selectbox(
                    "Stratify by Column (Optional)",
                    ["None"] + list(df.columns),
                    help="Maintain class distribution in splits",
                )
            target_feature = st.selectbox(
                "🎯 Select Target Feature (Optional)",
                ["None"] + list(df.columns),
            )
            if st.button("📈 Generate Train/Test Comparison", type="primary"):
                try:
                    stratify = df[stratify_col] if stratify_col != "None" else None
                    train_df, test_df = train_test_split(
                        df, train_size=train_size, random_state=random_state, stratify=stratify
                    )
                    cA, cB = st.columns(2)
                    with cA:
                        display_dataset_info(train_df, f"Training Set ({len(train_df):,} rows)")
                    with cB:
                        display_dataset_info(test_df, f"Test Set ({len(test_df):,} rows)")
                    target_feat = None if target_feature == "None" else target_feature
                    compare_report = sv.compare(
                        source=[train_df, "Training Set"],
                        compare=[test_df, "Test Set"],
                        target_feat=target_feat,
                    )
                    generate_sweetviz_report(
                        compare_report,
                        "Train/Test Comparison",
                        f"sweetviz_train_test_{uploaded_file.name.split('.')[0]}.html",
                    )
                except Exception as e:
                    st.error(f"❌ Error creating train/test split: {e}")

# =========================================================
# 4) Sub-population Comparison
# =========================================================
elif analysis_type == "🎯 Sub-population Comparison":
    st.sidebar.header("📁 Upload Dataset")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a file", type=["csv", "json"], key="subpop_file"
    )
    if uploaded_file is None:
        show_instructions()
    else:
        df, warning = load_and_validate_data(uploaded_file)
        if df is None:
            st.error(f"❌ {warning}")
        else:
            if warning:
                st.warning(f"⚠️ {warning}")
            display_dataset_info(df, "Full Dataset")
            st.subheader("⚙️ Sub-population Configuration")
            condition_column = st.selectbox(
                "📊 Select Column for Grouping", df.columns
            )
            if condition_column:
                unique_vals = df[condition_column].dropna().unique()
                if len(unique_vals) < 2:
                    st.error("❌ Selected column must have at least 2 unique values for comparison.")
                else:
                    if len(unique_vals) <= 20 or df[condition_column].dtype == "object":
                        condition_value = st.selectbox(
                            f"Select Value for Group 1 ({condition_column})", unique_vals
                        )
                        condition_series = df[condition_column] == condition_value
                        group1_name = f"{condition_column}={condition_value}"
                        group2_name = f"{condition_column}≠{condition_value}"
                    else:
                        threshold = st.number_input(
                            f"Threshold for {condition_column}",
                            value=float(pd.to_numeric(df[condition_column], errors="coerce").median()),
                            help="Group 1: values <= threshold, Group 2: values > threshold",
                        )
                        condition_series = pd.to_numeric(
                            df[condition_column], errors="coerce"
                        ) <= threshold
                        group1_name = f"{condition_column}≤{threshold}"
                        group2_name = f"{condition_column}>{threshold}"
                    g1, g2 = int(condition_series.sum()), int(len(df) - condition_series.sum())
                    c1, c2 = st.columns(2)
                    with c1:
                        st.metric("📊 Group 1 Size", f"{g1:,}")
                        st.caption(group1_name)
                    with c2:
                        st.metric("📊 Group 2 Size", f"{g2:,}")
                        st.caption(group2_name)
                    if g1 == 0 or g2 == 0:
                        st.error("❌ One of the groups is empty. Adjust the condition.")
                    else:
                        target_feature = st.selectbox(
                            "🎯 Select Target Feature (Optional)", ["None"] + list(df.columns)
                        )
                        force_num_cols = st.multiselect(
                            "🔢 Force Numerical Treatment (optional)", list(df.columns)
                        )
                        if st.button("🎯 Generate Sub-population Comparison", type="primary"):
                            try:
                                feat_cfg = sv.FeatureConfig(force_num=force_num_cols) if force_num_cols else None
                                target_feat = None if target_feature == "None" else target_feature
                                compare_report = sv.compare_intra(
                                    df,
                                    condition_series,
                                    [group1_name, group2_name],
                                    feat_cfg=feat_cfg,
                                    target_feat=target_feat,
                                )
                                generate_sweetviz_report(
                                    compare_report,
                                    "Sub-population Comparison",
                                    f"sweetviz_subpop_{uploaded_file.name.split('.')[0]}.html",
                                )
                            except Exception as e:
                                st.error(f"❌ Error creating sub-population comparison: {e}")
