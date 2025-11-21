"""
Streamlit single-page compact dashboard: India Healthcare Interactive Dashboard
Filename: streamlit_india_healthcare_compact.py

How to run:
1. python -m venv venv
2. pip install -r requirements.txt
3. streamlit run streamlit_india_healthcare_compact.py

Requirements (requirements.txt):
streamlit
pandas
numpy
plotly
scikit-learn
matplotlib
openpyxl
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
from io import BytesIO
import plotly.graph_objects as go

# Page config with custom CSS for compact layout
st.set_page_config(layout="wide", page_title="India Healthcare 2025", page_icon="🏥")

# Custom CSS for ultra-compact layout
st.markdown("""
<style>
    /* Remove all default padding and margins */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }
    
    /* Compact headers */
    h1 {
        font-size: 1.8rem !important;
        margin-bottom: 0.3rem !important;
        padding-top: 0 !important;
    }
    
    h3 {
        font-size: 1.1rem !important;
        margin-top: 0.3rem !important;
        margin-bottom: 0.3rem !important;
    }
    
    /* Remove spacing between elements */
    .element-container {
        margin-bottom: 0rem !important;
    }
    
    /* Compact metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.2rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Compact dataframe */
    .dataframe {
        font-size: 0.75rem !important;
    }
    
    /* Reduce vertical spacing */
    .stPlotlyChart {
        margin-bottom: 0 !important;
    }
    
    div[data-testid="stHorizontalBlock"] {
        gap: 0.5rem !important;
    }
    
    /* Hide sidebar completely */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Interactive filter bar styling */
    div[data-testid="stHorizontalBlock"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Style selectboxes and multiselects */
    .stSelectbox label, .stMultiSelect label, .stSlider label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    
    /* Make widgets pop */
    .stSelectbox > div > div, .stMultiSelect > div > div {
        background: white !important;
        border-radius: 8px !important;
        border: 2px solid #764ba2 !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover, .stMultiSelect > div > div:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(118, 75, 162, 0.3);
    }
    
    /* Animated metrics */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    /* Gradient title */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    
    /* Chart container animations */
    .stPlotlyChart {
        transition: all 0.3s ease;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .stPlotlyChart:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(17, 153, 142, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --------------------------- Helper functions ---------------------------
@st.cache_data
def generate_sample_data(seed: int = 42) -> pd.DataFrame:
    """Generate a reproducible sample dataset across a handful of Indian states and years."""
    np.random.seed(seed)
    states = [
        ("Maharashtra", 19.7513, 75.7139),
        ("Uttar Pradesh", 26.8467, 80.9462),
        ("Tamil Nadu", 11.1271, 78.6569),
        ("Karnataka", 15.3173, 75.7139),
        ("Kerala", 10.8505, 76.2711),
        ("West Bengal", 22.9868, 87.8550),
        ("Gujarat", 22.2587, 71.1924),
        ("Rajasthan", 27.0238, 74.2179),
    ]

    rows = []
    for state, lat, lon in states:
        for year in range(2015, 2029):
            base_pop = np.random.randint(3_000_000, 150_000_00)
            doctors = int(base_pop / np.random.randint(800, 2200))
            nurses = int(base_pop / np.random.randint(300, 900))
            beds = int(base_pop / np.random.randint(2000, 8000))
            spending = round(np.random.uniform(1.2, 10.0) * 1e4, 2)
            accessibility = round(np.random.uniform(20, 80), 1)
            affordability = round(np.random.uniform(30, 70), 1)
            shortfall = max(0, int((base_pop / 1000) * 0.8 - doctors))

            rows.append({
                "state": state, "year": year, "population": base_pop,
                "doctors": doctors, "nurses": nurses, "beds": beds,
                "spending_index": spending, "accessibility_pct": accessibility,
                "affordability_pct": affordability, "shortfall": shortfall,
                "lat": lat, "lon": lon,
            })

    return pd.DataFrame(rows)

def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Return CSV bytes for download"""
    return df.to_csv(index=False).encode('utf-8')

# --------------------------- Load data ---------------------------
sample_df = generate_sample_data()

# Sidebar controls - ultra compact
# Initialize with sample data (no file upload)
df = sample_df.copy()

# Convert types
for c in ["year", "population", "doctors", "nurses", "beds", "shortfall"]:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

# Fill lat/lon
if 'lat' not in df.columns or 'lon' not in df.columns:
    sample_coords = sample_df[['state', 'lat', 'lon']].drop_duplicates()
    df = df.merge(sample_coords, on='state', how='left')

states = sorted(df['state'].dropna().unique().tolist())
year_min = int(df['year'].min())
year_max = int(df['year'].max())

# Interactive filter bar at the top
with st.container():
    filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns([1.5, 1.2, 2, 2, 2])
    
    with filter_col1:
        selected_state = st.selectbox("🗺️ State Filter", options=["All"] + states, label_visibility="visible")
    
    with filter_col2:
        selected_year = st.slider("📅 Year", min_value=year_min, max_value=year_max, value=year_max, label_visibility="visible")
    
    with filter_col3:
        category = st.multiselect("👥 Workforce Categories", options=["doctors", "nurses", "beds"], 
                                 default=["doctors", "nurses", "beds"], label_visibility="visible")
    
    with filter_col4:
        state_compare = st.multiselect("🔍 Compare States", options=states, default=states[:3], label_visibility="visible")
    
    with filter_col5:
        show_predict = st.checkbox("🔮 Show Forecast", value=True)
        csv_bytes = df_to_csv_bytes(df[df['year'] == selected_year])
        st.download_button("⬇️ Export Data", data=csv_bytes, file_name="healthcare_data.csv", mime="text/csv")

# --------------------------- Main Dashboard Layout ---------------------------
st.title("🏥 India Healthcare Analytics 2025")

# KPIs
kpi_df = df[df['year'] == selected_year]
if selected_state != "All":
    kpi_df = kpi_df[kpi_df['state'] == selected_state]

kpi1 = int(kpi_df['doctors'].sum()) if 'doctors' in kpi_df.columns else 0
kpi2 = round(kpi_df['accessibility_pct'].mean(), 1) if 'accessibility_pct' in kpi_df.columns else 0
kpi3 = int(kpi_df['shortfall'].sum()) if 'shortfall' in kpi_df.columns else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("👨‍⚕️ Total Doctors", f"{kpi1:,}")
col2.metric("📍 Accessibility", f"{kpi2}%")
col3.metric("⚠️ Shortfall", f"{kpi3:,}")
col4.metric("📆 Year", f"{selected_year}")

# Filter data for visuals
view_df = df[df['year'] == selected_year].copy()
if selected_state != "All":
    view_df = view_df[view_df['state'] == selected_state]

# Main grid layout - 3 rows
row1_col1, row1_col2, row1_col3 = st.columns([2, 1.5, 1.5])

# Row 1: Workforce chart, Map, Pie
with row1_col1:
    if selected_state == "All":
        stacked = df[df['year'] == selected_year].groupby('state')[['doctors', 'nurses', 'beds']].sum().reset_index()
        stacked = stacked.melt(id_vars='state', value_vars=['doctors', 'nurses', 'beds'], 
                              var_name='category', value_name='count')
        fig = px.bar(stacked, x='state', y='count', color='category', barmode='group',
                    title='Workforce Distribution by State', height=280)
        fig.update_layout(margin=dict(l=20, r=20, t=40, b=60), xaxis_tickangle=-45, showlegend=True,
                         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        timeseries = df[df['state'] == selected_state].sort_values('year')
        if len(category) > 0:
            fig = px.line(timeseries, x='year', y=category, 
                         title=f"{selected_state} - Workforce Trends", markers=True, height=280)
            fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), showlegend=True,
                             legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with row1_col2:
    if not view_df.empty:
        fig_map = px.scatter_geo(view_df, lat='lat', lon='lon', size='doctors', hover_name='state',
                                projection='natural earth', title='Geographic Distribution', height=280)
        fig_map.update_geos(fitbounds="locations", visible=False)
        fig_map.update_layout(margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_map, use_container_width=True, config={'displayModeBar': False})

with row1_col3:
    pie_df = view_df[['doctors', 'nurses', 'beds']].sum().reset_index()
    pie_df.columns = ['category', 'count']
    fig2 = px.pie(pie_df, names='category', values='count', title='Workforce Share', height=280)
    fig2.update_layout(margin=dict(l=0, r=0, t=40, b=0), showlegend=True,
                      legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5))
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

# Row 2: Accessibility, Affordability, Shortfall
row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    fig3 = px.histogram(df[df['year'] == selected_year], x='accessibility_pct', nbins=10, 
                       title='Accessibility Distribution', height=240)
    fig3.update_layout(margin=dict(l=20, r=20, t=40, b=40), showlegend=False)
    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

with row2_col2:
    fig4 = px.histogram(df[df['year'] == selected_year], x='affordability_pct', nbins=10,
                       title='Affordability Distribution', height=240)
    fig4.update_layout(margin=dict(l=20, r=20, t=40, b=40), showlegend=False)
    st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})

with row2_col3:
    short_df = df[df['year'] == selected_year][['state', 'shortfall']].sort_values('shortfall', ascending=False).head(8)
    fig5 = px.bar(short_df, x='state', y='shortfall', title='Top Shortfall States', height=240)
    fig5.update_layout(margin=dict(l=20, r=20, t=40, b=60), xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False})

# Row 3: State comparison & Prediction
row3_col1, row3_col2 = st.columns([2, 1.5])

with row3_col1:
    if state_compare:
        compare_df = df[(df['state'].isin(state_compare)) & (df['year'] >= year_min)].groupby(['year', 'state'])[['doctors']].sum().reset_index()
        fig6 = px.line(compare_df, x='year', y='doctors', color='state', markers=True,
                      title='State Comparison - Doctor Trends', height=240)
        fig6.update_layout(margin=dict(l=20, r=20, t=40, b=40), showlegend=True,
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig6, use_container_width=True, config={'displayModeBar': False})

with row3_col2:
    if show_predict and states:
        predict_state = states[0]
        data_for_pred = df[df['state'] == predict_state].sort_values('year')
        X = data_for_pred[['year']].values
        y = data_for_pred['doctors'].values if 'doctors' in data_for_pred.columns else np.array([])

        if len(X) >= 3 and len(y) >= 3 and not np.isnan(y).all():
            model = LinearRegression()
            model.fit(X, y)
            future_years = np.arange(int(data_for_pred['year'].max()) + 1, 
                                    int(data_for_pred['year'].max()) + 6).reshape(-1, 1)
            preds = model.predict(future_years).astype(int)
            
            historical = data_for_pred[['year', 'doctors']].rename(columns={'doctors': 'value'}).assign(type='historical')
            predicted = pd.DataFrame({'year': future_years.ravel(), 'value': preds, 'type': 'predicted'})
            combined = pd.concat([historical, predicted], ignore_index=True)

            fig_pred = px.line(combined, x='year', y='value', color='type',
                             title=f"5-Year Forecast - {predict_state}", height=240)
            fig_pred.update_layout(margin=dict(l=20, r=20, t=40, b=40), showlegend=True,
                                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_pred, use_container_width=True, config={'displayModeBar': False})