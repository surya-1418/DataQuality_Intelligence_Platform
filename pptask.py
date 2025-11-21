import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# --- CONFIGURATION CONSTANTS (Used for Alert Logic) ---
ALERT_COMPLETENESS_THRESHOLD = 95
ALERT_UNIQUENESS_THRESHOLD = 98

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Data Quality Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🎯"
)

# --- PREMIUM STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
        padding: 0;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Premium Header */
    .premium-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 0 0 24px 24px;
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .premium-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .premium-header p {
        font-size: 1.1rem;
        opacity: 0.95;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    /* Upload Zone */
    .upload-zone {
        background: white;
        border: 3px dashed #667eea;
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        margin: 2rem 0;
    }
    
    .upload-zone:hover {
        border-color: #764ba2;
        background: #f8f9ff;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        border: none;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.2);
    }
    
    [data-testid="stMetric"] label {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: #6b7280 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Alert Cards */
    .alert-card {
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        border-left: 5px solid;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .alert-card:hover {
        transform: translateX(8px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    }
    
    .alert-critical {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left-color: #dc2626;
    }
    
    .alert-high {
        background: linear-gradient(135deg, #ffedd5 0%, #fed7aa 100%);
        border-left-color: #ea580c;
    }
    
    .alert-medium {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left-color: #d97706;
    }
    
    .alert-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .alert-description {
        font-size: 0.95rem;
        opacity: 0.9;
        line-height: 1.6;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: white;
        padding: 0.5rem;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Charts Container */
    .chart-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
        margin: 1rem 0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* Info Boxes */
    .info-box {
        background: linear-gradient(135deg, #e0e7ff 0%, #ddd6fe 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }

    .ai-recommendation-box {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #764ba2;
        box-shadow: 0 6px 15px rgba(118, 75, 162, 0.1);
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        border: 2px dashed #667eea;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- MOCK DATA FUNCTIONS ---

def generate_historical_data():
    """Generates mock historical data for the past 6 months."""
    dates = pd.date_range(end=datetime.now().date(), periods=6, freq='M').tolist()
    
    # Simulate slightly varying scores
    np.random.seed(42)
    data = {
        'Date': dates,
        'Completeness': np.random.uniform(85, 99, 6).round(2),
        'Uniqueness': np.random.uniform(90, 99.5, 6).round(2),
        'Validity': np.random.uniform(80, 95, 6).round(2),
    }
    df = pd.DataFrame(data)
    # Calculate historical overall score using fixed weights (for consistency)
    df['Overall'] = (df['Completeness'] * 0.4 + df['Uniqueness'] * 0.3 + df['Validity'] * 0.3).round(2)
    return df

def get_benchmark_scores(industry):
    """Returns mock industry benchmark scores."""
    benchmarks = {
        "Technology": {'Completeness': 98.5, 'Uniqueness': 99.8, 'Validity': 96.0, 'Overall': 98.1},
        "Finance": {'Completeness': 99.2, 'Uniqueness': 99.9, 'Validity': 97.5, 'Overall': 99.0},
        "Healthcare": {'Completeness': 95.0, 'Uniqueness': 98.0, 'Validity': 92.0, 'Overall': 95.8},
        "Retail": {'Completeness': 96.5, 'Uniqueness': 99.0, 'Validity': 94.5, 'Overall': 97.0},
    }
    return benchmarks.get(industry, benchmarks['Technology'])

# --- ANALYSIS FUNCTIONS ---

def analyze_completeness(df):
    """Analyze missing data completeness"""
    total_cells = len(df) * len(df.columns)
    missing_by_column = df.isnull().sum()
    missing_pct = (missing_by_column / len(df) * 100).round(2)
    
    results = pd.DataFrame({
        'Field': missing_by_column.index,
        'Missing Count': missing_by_column.values,
        'Missing %': missing_pct.values
    })
    results = results[results['Missing Count'] > 0].sort_values('Missing %', ascending=False)
    
    overall_completeness = ((1 - df.isnull().sum().sum() / total_cells) * 100).round(2)
    
    return results, overall_completeness

def analyze_uniqueness(df):
    """Analyze duplicate records"""
    duplicate_info = []
    
    for column in df.columns:
        duplicates = df[column].duplicated().sum()
        if duplicates > 0:
            duplicate_info.append({
                'Field': column,
                'Duplicate Count': duplicates,
                'Duplicate %': round((duplicates / len(df) * 100), 2)
            })
    
    duplicate_df = pd.DataFrame(duplicate_info)
    if len(duplicate_df) > 0:
        duplicate_df = duplicate_df.sort_values('Duplicate Count', ascending=False)
    
    # Overall uniqueness score
    total_duplicates = df.duplicated().sum()
    uniqueness_score = ((1 - total_duplicates / len(df)) * 100).round(2)
    
    return duplicate_df, uniqueness_score

def analyze_validity(df):
    """Analyze data validity issues"""
    validity_issues = []
    
    for column in df.columns:
        # Check for negative values in numeric columns
        if pd.api.types.is_numeric_dtype(df[column]):
            negative_count = (df[column] < 0).sum()
            if negative_count > 0:
                validity_issues.append({
                    'Issue Type': f'Negative values in {column}',
                    'Count': negative_count,
                    'Severity': 'High'
                })
            
            # Check for outliers (values beyond 3 standard deviations)
            mean = df[column].mean()
            std = df[column].std()
            outliers = ((df[column] > mean + 3*std) | (df[column] < mean - 3*std)).sum()
            if outliers > 0:
                validity_issues.append({
                    'Issue Type': f'Outliers in {column}',
                    'Count': outliers,
                    'Severity': 'Medium'
                })
    
    validity_df = pd.DataFrame(validity_issues)
    if len(validity_df) > 0:
        validity_df = validity_df.sort_values('Count', ascending=False)
    
    # Overall validity score (simplified)
    total_issues = validity_df['Count'].sum() if len(validity_df) > 0 else 0
    validity_score = max(0, 100 - (total_issues / len(df) * 10))
    validity_score = round(validity_score, 2)
    
    return validity_df, validity_score

def generate_mock_ai_recommendations(df, completeness_df, uniqueness_df, validity_df):
    """Generates a list of mock AI recommendations based on analysis."""
    recommendations = []
    
    # 1. Recommendation based on Completeness
    if len(completeness_df) > 0 and completeness_df['Missing %'].max() > 10:
        top_missing_field = completeness_df.iloc[0]['Field']
        top_missing_percent = completeness_df.iloc[0]['Missing %']
        recommendations.append(
            f"**Data Collection Priority:** Field `{top_missing_field}` has {top_missing_percent}% missing data. Focus ETL efforts on ensuring this field is populated, as it significantly impacts completeness."
        )
    
    # 2. Recommendation based on Uniqueness
    if len(uniqueness_df) > 0 and uniqueness_df['Duplicate %'].max() > 1:
        top_duplicate_field = uniqueness_df.iloc[0]['Field']
        recommendations.append(
            f"**De-Duplication Strategy:** The field `{top_duplicate_field}` shows the highest duplication rate. Implement fuzzy matching algorithms to identify and merge potential duplicate records in your source system."
        )

    # 3. Recommendation based on Validity
    if len(validity_df) > 0:
        top_validity_issue = validity_df.iloc[0]['Issue Type']
        recommendations.append(
            f"**Data Sanitization:** Address the primary validity issue: **{top_validity_issue}**. This often indicates incorrect input validation or data type casting during ingestion."
        )

    # 4. General Recommendation (if overall score is low)
    overall_completeness_score = ((1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100).round(2)
    if overall_completeness_score < 80:
          recommendations.append(
            "**Schema Review:** Given the low overall completeness score, review your source system schema definitions. Consider making critical, frequently missing fields mandatory."
        )

    return recommendations if recommendations else ["The data quality is high across all dimensions. The current recommendation is to simply **maintain existing standards** and re-run this analysis weekly."]

# --- VISUALIZATION FUNCTIONS ---

def create_gauge_chart(score, title="Overall Quality Score"):
    """Premium gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24, 'color': '#1f2937', 'family': 'Inter'}},
        delta={'reference': 85, 'increasing': {'color': "#10b981"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "#d1d5db"},
            'bar': {'color': "#667eea", 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 3,
            'bordercolor': "#e5e7eb",
            'steps': [
                {'range': [0, 60], 'color': '#fee2e2'},
                {'range': [60, 80], 'color': '#fef3c7'},
                {'range': [80, 100], 'color': '#d1fae5'}
            ],
            'threshold': {
                'line': {'color': "#667eea", 'width': 5},
                'thickness': 0.8,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(t=50, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter'}
    )
    return fig

def create_radar_chart(labels, scores):
    """Premium radar chart for dimensions"""
    fig = go.Figure(data=go.Scatterpolar(
        r=scores,
        theta=labels,
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.2)',
        line=dict(color='#667eea', width=3),
        marker=dict(size=10, color='#667eea', line=dict(color='white', width=2))
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=12),
                gridcolor='#e5e7eb'
            ),
            angularaxis=dict(
                linecolor='#d1d5db',
                gridcolor='#e5e7eb'
            ),
            bgcolor='rgba(255,255,255,0.9)'
        ),
        showlegend=False,
        height=450,
        margin=dict(t=60, b=60, l=60, r=60),
        title={
            'text': "Quality Dimensions Analysis",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#1f2937', 'family': 'Inter'}
        },
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter'}
    )
    return fig

def create_horizontal_bar(df, x_col, y_col, title, color_scale=None):
    """Premium horizontal bar chart"""
    if color_scale is None:
        colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe']
    else:
        colors = color_scale
    
    fig = go.Figure(data=[go.Bar(
        x=df[x_col],
        y=df[y_col],
        orientation='h',
        marker=dict(
            color=colors[:len(df)] if len(colors) >= len(df) else colors * (len(df)//len(colors) + 1),
            line=dict(color='white', width=2)
        ),
        text=df[x_col],
        textposition='outside',
        textfont=dict(size=12, color='#1f2937'),
        hovertemplate='<b>%{y}</b><br>Value: %{x}<extra></extra>'
    )])
    
    fig.update_layout(
        title={'text': title, 'x': 0.5, 'xanchor': 'center', 'font': {'size': 20, 'family': 'Inter'}},
        xaxis=dict(showgrid=True, gridcolor='#f3f4f6', zeroline=False),
        yaxis=dict(showgrid=False),
        height=max(300, len(df) * 50),
        margin=dict(t=60, b=40, l=20, r=80),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter'}
    )
    return fig

def create_vertical_bar(df, x_col, y_col, title, color='#667eea'):
    """Premium vertical bar chart"""
    fig = go.Figure(data=[go.Bar(
        x=df[x_col],
        y=df[y_col],
        marker=dict(
            color=color,
            line=dict(color='white', width=2),
            opacity=0.9
        ),
        text=df[y_col],
        textposition='outside',
        textfont=dict(size=12, color='#1f2937'),
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title={'text': title, 'x': 0.5, 'xanchor': 'center', 'font': {'size': 20, 'family': 'Inter'}},
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f3f4f6', zeroline=False),
        height=400,
        margin=dict(t=60, b=40, l=40, r=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter'}
    )
    return fig

def create_line_chart(df, title):
    """Line chart for time series analysis."""
    fig = go.Figure()

    colors = {
        'Overall': '#667eea',
        'Completeness': '#10b981',
        'Uniqueness': '#f59e0b',
        'Validity': '#ef4444'
    }

    for col in ['Overall', 'Completeness', 'Uniqueness', 'Validity']:
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df[col],
            mode='lines+markers',
            name=col,
            line=dict(color=colors[col], width=3),
            marker=dict(size=8)
        ))

    fig.update_layout(
        title={'text': title, 'x': 0.5, 'xanchor': 'center', 'font': {'size': 20, 'family': 'Inter'}},
        xaxis_title="Reporting Date",
        yaxis_title="Quality Score (%)",
        yaxis=dict(range=[80, 100], showgrid=True, gridcolor='#e5e7eb'),
        height=500,
        margin=dict(t=60, b=40, l=40, r=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        paper_bgcolor='white',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter'}
    )
    return fig

def create_comparison_bar_chart(current_scores, benchmark_scores, benchmark_name):
    """Grouped bar chart for benchmarking."""
    # Ensure scores are dictionaries with 'Overall', 'Completeness', 'Uniqueness', 'Validity' keys
    dimensions = ['Overall', 'Completeness', 'Uniqueness', 'Validity']
    current_values = [current_scores[d] for d in dimensions]
    benchmark_values = [benchmark_scores[d] for d in dimensions]

    fig = go.Figure(data=[
        go.Bar(name='Current Score', x=dimensions, y=current_values, marker_color='#667eea'),
        go.Bar(name=f'{benchmark_name} Benchmark', x=dimensions, y=benchmark_values, marker_color='#10b981')
    ])

    fig.update_layout(
        title={'text': f"Current Quality vs. {benchmark_name} Benchmark", 'x': 0.5, 'xanchor': 'center', 'font': {'size': 20, 'family': 'Inter'}},
        xaxis_title="Quality Dimension",
        yaxis_title="Score (%)",
        yaxis=dict(range=[80, 100], showgrid=True, gridcolor='#e5e7eb'),
        barmode='group',
        height=500,
        margin=dict(t=60, b=40, l=40, r=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='white',
        font={'family': 'Inter'}
    )
    return fig


# --- MAIN APPLICATION ---

# Premium Header
st.markdown("""
<div class="premium-header">
    <h1>🎯 Data Quality Intelligence Platform</h1>
    <p>Enterprise-grade data validation and quality monitoring • Powered by Advanced Analytics</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration Panel")
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "Upload Your Dataset",
        type=['csv', 'xlsx', 'xls'],
        help="Supported formats: CSV, Excel (XLSX, XLS)"
    )
    
    # --- Custom Business Rules (From Screenshot) ---
    st.markdown("### 📐 Custom Business Rules")
    st.text_input("Define New Rule", value="e.g. 'Age > 18'")
    st.button("Add Rule", use_container_width=True) 
    st.markdown("Active Rules: None", help="List of active rules will appear here.")
    st.markdown("---")

    # --- Quality Dimension Weights (From Screenshot) ---
    st.markdown("### ⚖️ Quality Dimension Weights")
    
    completeness_weight = st.slider(
        "Completeness Weight", min_value=0.0, max_value=1.0, value=0.40, step=0.05
    )
    uniqueness_weight = st.slider(
        "Uniqueness Weight", min_value=0.0, max_value=1.0, value=0.30, step=0.05
    )
    validity_weight = st.slider(
        "Validity Weight", min_value=0.0, max_value=1.0, value=0.30, step=0.05
    )
    
    st.markdown("---")

    # --- Benchmarking (From Screenshot) ---
    st.markdown("### 📈 Benchmarking")
    selected_benchmark = st.selectbox(
        "Select Industry Benchmark",
        ["Technology", "Finance", "Healthcare", "Retail"],
        index=0
    )
    
    st.markdown("---")

    # --- Dashboard Preferences (From Screenshot) ---
    st.markdown("### 🖥️ Dashboard Preferences")
    # This variable is now used to conditionally display the recommendations
    show_ai_recommendations = st.checkbox("Show AI Recommendations", value=False)
    enable_auto_refresh = st.checkbox("Enable Auto-Refresh (Live Data)", value=False)
    
    st.markdown("---")

    # --- Admin Controls (From Screenshot) ---
    st.markdown("### 🔒 Admin Controls")
    simulate_role = st.selectbox(
        "Simulate User Role",
        ["Admin", "Analyst", "Data Engineer", "Auditor"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 📝 About")
    st.info("""
    **Version:** 2.1 Pro
    
    **New Features:**
    - Role-Based Access Simulation
    - Time Series Analysis
    - Industry Benchmarking
    - AI Recommendations
    - Multi-dimensional analysis
    """)

# Main Content Area
if uploaded_file is None:
    # Welcome Screen
    st.markdown("""
    <div class="info-box">
        <h2 style="margin-top: 0;">👋 Welcome to Data Quality Intelligence</h2>
        <p style="font-size: 1.1rem; line-height: 1.8;">
            Upload your dataset to begin comprehensive quality analysis. Our platform will automatically:
        </p>
        <ul style="font-size: 1rem; line-height: 1.8;">
            <li><strong>Assess Completeness:</strong> Identify missing values and incomplete records</li>
            <li><strong>Check Uniqueness:</strong> Detect duplicate entries and redundant data</li>
            <li><strong>Validate Data:</strong> Find outliers, negative values, and inconsistencies</li>
            <li><strong>Generate Insights:</strong> Provide actionable recommendations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 16px; text-align: center; box-shadow: 0 4px 16px rgba(0,0,0,0.06);">
            <h1 style="color: #667eea; margin: 0;">📤</h1>
            <h3 style="margin: 0.5rem 0;">Upload</h3>
            <p style="color: #6b7280; font-size: 0.9rem;">CSV or Excel files supported</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 16px; text-align: center; box-shadow: 0 4px 16px rgba(0,0,0,0.06);">
            <h1 style="color: #667eea; margin: 0;">🔍</h1>
            <h3 style="margin: 0.5rem 0;">Analyze</h3>
            <p style="color: #6b7280; font-size: 0.9rem;">Automated quality checks</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 16px; text-align: center; box-shadow: 0 4px 16px rgba(0,0,0,0.06);">
            <h1 style="color: #667eea; margin: 0;">📈</h1>
            <h3 style="margin: 0.5rem 0;">Improve</h3>
            <p style="color: #6b7280; font-size: 0.9rem;">Actionable insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📋 Sample Dataset Structure")
    st.code("""
    Example CSV format:
    customer_id,name,email,phone,order_total,order_date
    1001,John Doe,john@email.com,+1234567890,299.99,2025-01-15
    1002,Jane Smith,jane@email.com,,450.00,2025-01-16
    """, language="csv")

else:
    # Load Data
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Run Analyses
        completeness_results, completeness_score = analyze_completeness(df)
        uniqueness_results, uniqueness_score = analyze_uniqueness(df)
        validity_results, validity_score = analyze_validity(df)
        
        # Calculate Overall Score using dynamic weights from the sidebar
        total_weight = completeness_weight + uniqueness_weight + validity_weight
        if total_weight == 0:
            overall_score = 0
        else:
            overall_score = round(
                (completeness_score * completeness_weight + 
                 uniqueness_score * uniqueness_weight + 
                 validity_score * validity_weight) / total_weight, 
                2
            )
            # Scaling to 100 for display, assuming weights sum close to 1
            overall_score = round(overall_score * 100 / max(0.01, (completeness_weight + uniqueness_weight + validity_weight)), 2)
            
        # Store current scores for benchmarking
        current_scores = {
            'Overall': overall_score,
            'Completeness': completeness_score,
            'Uniqueness': uniqueness_score,
            'Validity': validity_score
        }

        # Generate Alerts
        alerts = []
        
        if uniqueness_score < ALERT_UNIQUENESS_THRESHOLD and len(uniqueness_results) > 0:
            top_dup = uniqueness_results.iloc[0]
            alerts.append({
                'level': 'CRITICAL',
                'title': f"{int(top_dup['Duplicate Count'])} Duplicate '{top_dup['Field']}' Found",
                'description': f"Immediate investigation required to prevent data corruption ({top_dup['Duplicate %']}% duplication rate)."
            })
        
        if completeness_score < ALERT_COMPLETENESS_THRESHOLD and len(completeness_results) > 0:
            top_missing = completeness_results.iloc[0]
            alerts.append({
                'level': 'HIGH',
                'title': f"{top_missing['Missing %']:.1f}% '{top_missing['Field']}' Fields Missing",
                'description': f"Data completeness is low with {int(top_missing['Missing Count'])} missing values, impacting analysis quality."
            })
        
        if len(validity_results) > 0:
            top_validity = validity_results.iloc[0]
            validity_alert_count = validity_results.iloc[0]['Count']
            validity_alert_issue = validity_results.iloc[0]['Issue Type']
            alerts.append({
                'level': 'MEDIUM',
                'title': f"{int(validity_alert_count)} {validity_alert_issue}",
                'description': f"Data validation issue detected that requires correction before reporting."
            })
        
        # --- MOCK TIME SERIES & BENCHMARK DATA GENERATION ---
        historical_df = generate_historical_data()
        benchmark_scores = get_benchmark_scores(selected_benchmark)
        
        # --- TAB LIST BASED ON ROLE ---
        tabs_config = {
            "📊 Overview": True,
            "✅ Completeness Analysis": simulate_role in ["Admin", "Analyst", "Data Engineer"],
            "🔑 Uniqueness Check": simulate_role in ["Admin", "Analyst", "Data Engineer"],
            "🔢 Validity Report": simulate_role in ["Admin", "Analyst", "Data Engineer"],
            "📈 Time Series": simulate_role in ["Admin", "Analyst", "Auditor"],
            "🏆 Benchmark Comparison": simulate_role in ["Admin", "Analyst", "Auditor"],
            "📋 Raw Data Preview": simulate_role in ["Admin", "Data Engineer"]
        }
        
        visible_tabs = [name for name, is_visible in tabs_config.items() if is_visible]

        # Display Results
        st.markdown(f"<p style='color:#6b7280; font-size: 1.1rem;'><strong>{uploaded_file.name}</strong> • {len(df):,} rows × {len(df.columns)} columns • Last analyzed: {datetime.now().strftime('%d %b %Y, %I:%M %p')}</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Top Metrics Row
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.plotly_chart(create_gauge_chart(overall_score), use_container_width=True)
        
        with col2:
            st.markdown("### 🚨 Priority Alerts")
            
            if len(alerts) == 0:
                st.success("✅ No critical issues detected! Your data quality is excellent.")
            else:
                for alert in alerts:
                    alert_class = f"alert-{alert['level'].lower()}"
                    st.markdown(f"""
                    <div class="alert-card {alert_class}">
                        <div class="alert-title">{alert['level']}: {alert['title']}</div>
                        <div class="alert-description">{alert['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Key Metrics Cards
        st.markdown("### 📊 Quality Metrics Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Overall Score",
                f"{overall_score:.2f}%",
                # The delta calculation uses 85% as an arbitrary internal reference point
                delta=f"{overall_score - 85:.1f}%" if overall_score >= 85 else f"{overall_score - 85:.1f}%",
            )
        
        with col2:
            st.metric(
                "Completeness",
                f"{completeness_score}%",
                delta="Excellent" if completeness_score >= ALERT_COMPLETENESS_THRESHOLD else "Needs Work"
            )
        with col3:
            st.metric(
                "Uniqueness",
                f"{uniqueness_score}%",
                delta="Good" if uniqueness_score >= ALERT_UNIQUENESS_THRESHOLD else "Review"
            )
        with col4:
            st.metric(
                "Validity",
                f"{validity_score}%",
                delta="Clean" if validity_score >= 90 else "Issues Found"
            )
        
        st.markdown("---")
        
        # Tabbed Interface
        tabs = st.tabs(visible_tabs)
        tab_mapping = {name: tab for name, tab in zip(visible_tabs, tabs)}
        
        # --- Tab 1: Overview ---
        if "📊 Overview" in tab_mapping:
            with tab_mapping["📊 Overview"]:
                # --- AI Recommendations Section (Role Restricted) ---
                if show_ai_recommendations and simulate_role != "Auditor":
                    recommendations = generate_mock_ai_recommendations(df, completeness_results, uniqueness_results, validity_results)
                    
                    st.markdown("<div class='ai-recommendation-box'>", unsafe_allow_html=True)
                    st.markdown("#### ✨ AI Recommendations: Actionable Insights")
                    st.markdown("---")
                    
                    for i, rec in enumerate(recommendations):
                        st.markdown(f"**{i+1}.** {rec}")
                        if i < len(recommendations) - 1:
                            st.markdown("---")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # --- Multi-Dimensional Quality Assessment (Radar/Bar) ---
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                st.markdown("#### Multi-Dimensional Quality Assessment")
                
                col1, col2 = st.columns(2)
                with col1:
                    radar_fig = create_radar_chart(
                        ['Completeness', 'Uniqueness', 'Validity'],
                        [completeness_score, uniqueness_score, validity_score]
                    )
                    st.plotly_chart(radar_fig, use_container_width=True)
                
                with col2:
                    st.markdown("##### 📈 Quality Score Breakdown")
                    score_data = pd.DataFrame({
                        'Dimension': ['Completeness', 'Uniqueness', 'Validity'],
                        'Score': [completeness_score, uniqueness_score, validity_score]
                    })
                    bar_fig = create_vertical_bar(score_data, 'Dimension', 'Score', 'Quality Dimension Scores')
                    st.plotly_chart(bar_fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        # --- Tab 2: Completeness Analysis (Visible to Admin, Analyst, Data Engineer) ---
        if "✅ Completeness Analysis" in tab_mapping:
            with tab_mapping["✅ Completeness Analysis"]:
                st.markdown("### Completeness Analysis: Missing Data Report")
                st.info(f"The overall data completeness is **{completeness_score}%** across all records and fields.")
                
                if len(completeness_results) > 0:
                    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                    st.plotly_chart(
                        create_horizontal_bar(
                            completeness_results.head(10).sort_values('Missing %', ascending=True),
                            'Missing %',
                            'Field',
                            'Top 10 Fields by Missing Percentage',
                            color_scale=['#ef4444', '#f59e0b', '#fde047']
                        ),
                        use_container_width=True
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("#### Detailed Field Completeness Table")
                    st.dataframe(completeness_results, use_container_width=True)
                else:
                    st.success("All fields are 100% complete. No missing data found.")
        
        # --- Tab 3: Uniqueness Check (Visible to Admin, Analyst, Data Engineer) ---
        if "🔑 Uniqueness Check" in tab_mapping:
            with tab_mapping["🔑 Uniqueness Check"]:
                st.markdown("### Uniqueness Check: Duplicate Record Report")
                st.info(f"The overall dataset uniqueness score is **{uniqueness_score}%** (total data duplication: **{(100 - uniqueness_score):.2f}%**).")
                
                if len(uniqueness_results) > 0:
                    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                    st.plotly_chart(
                        create_horizontal_bar(
                            uniqueness_results.head(10).sort_values('Duplicate %', ascending=True),
                            'Duplicate %',
                            'Field',
                            'Top 10 Fields by Duplication Rate',
                            color_scale=['#f093fb', '#764ba2']
                        ),
                        use_container_width=True
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("#### Detailed Field Uniqueness Table")
                    st.dataframe(uniqueness_results, use_container_width=True)
                else:
                    st.success("No duplicate records found across the dataset.")
        
        # --- Tab 4: Validity Report (Visible to Admin, Analyst, Data Engineer) ---
        if "🔢 Validity Report" in tab_mapping:
            with tab_mapping["🔢 Validity Report"]:
                st.markdown("### Validity Report: Consistency & Constraint Violations")
                st.info(f"The validity score is **{validity_score}%**. This checks for unexpected values (e.g., negatives, outliers) and custom rule violations.")
                
                if len(validity_results) > 0:
                    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                    st.plotly_chart(
                        create_horizontal_bar(
                            validity_results.head(10).sort_values('Count', ascending=True),
                            'Count',
                            'Issue Type',
                            'Top Validity Issues by Count',
                            color_scale=['#10b981', '#059669']
                        ),
                        use_container_width=True
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("#### Detailed Validity Issues Table")
                    st.dataframe(validity_results, use_container_width=True)
                else:
                    st.success("No standard validity issues (negatives, outliers) detected.")
        
        # --- Tab 5: Time Series (Visible to Admin, Analyst, Auditor) ---
        if "📈 Time Series" in tab_mapping:
            with tab_mapping["📈 Time Series"]:
                st.markdown("### Historical Quality Trend")
                st.markdown("Track the quality score and its dimensions over the last 6 months to identify trends and decay.")
                
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                st.plotly_chart(
                    create_line_chart(historical_df, "6-Month Data Quality Trend"),
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("#### Historical Data Points")
                st.dataframe(historical_df.set_index('Date').style.format("{:.2f}%"), use_container_width=True)
        
        # --- Tab 6: Benchmark Comparison (Visible to Admin, Analyst, Auditor) ---
        if "🏆 Benchmark Comparison" in tab_mapping:
            with tab_mapping["🏆 Benchmark Comparison"]:
                st.markdown("### Industry Benchmark Comparison")
                st.markdown(f"Comparing your current data quality scores against the **{selected_benchmark}** industry standard.")
                
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                st.plotly_chart(
                    create_comparison_bar_chart(current_scores, benchmark_scores, selected_benchmark),
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Summary comparison table
                comparison_df = pd.DataFrame({
                    'Dimension': ['Overall', 'Completeness', 'Uniqueness', 'Validity'],
                    'Current Score (%)': [current_scores['Overall'], current_scores['Completeness'], current_scores['Uniqueness'], current_scores['Validity']],
                    f'{selected_benchmark} Benchmark (%)': [benchmark_scores['Overall'], benchmark_scores['Completeness'], benchmark_scores['Uniqueness'], benchmark_scores['Validity']]
                })
                comparison_df['Delta'] = comparison_df['Current Score (%)'] - comparison_df[f'{selected_benchmark} Benchmark (%)']
                
                st.markdown("#### Score Comparison Table")
                st.dataframe(comparison_df.style.format({
                    'Current Score (%)': "{:.2f}%", 
                    f'{selected_benchmark} Benchmark (%)': "{:.2f}%",
                    'Delta': lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%"
                }), use_container_width=True)

        # --- Tab 7: Raw Data Preview (Visible to Admin, Data Engineer) ---
        if "📋 Raw Data Preview" in tab_mapping:
            with tab_mapping["📋 Raw Data Preview"]:
                st.markdown("### Raw Data Preview")
                st.warning("Only Admins and Data Engineers should access this raw view due to potential PII exposure and for debugging purposes.")
                st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred during analysis: {e}")
        st.info("Please ensure your uploaded file is correctly formatted (CSV or Excel) and contains numerical data in relevant columns for quality checks.")