"""
India Healthcare – Executive Dashboard (Improved)
Enhanced with: caching, DRY principles, error handling, configuration management,
better responsiveness, and improved code organization.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Tuple

# ================ CONFIGURATION ================
PAGE_CONFIG = {
    'page_title': "India Healthcare – Executive Dashboard",
    'page_icon': "🏥",
    'layout': "wide",
    'initial_sidebar_state': "collapsed"
}

COLORS = {
    'kpi_backgrounds': ['#FFE9E9', '#E8F4FF', '#E7FFF3', '#F5E9FF'],
    'kpi_borders': ['#E6A5A5', '#99C4FF', '#97E6C8', '#CFA8FF'],
    'kpi_text': ['#7a2f2f', '#145c9e', '#17664b', '#6b2f85'],
    'chart_primary': '#3C6EAF',
    'chart_secondary': '#2E86AB',
    'chart_comparison': {'Current': '#E66B6B', 'Target': '#37BFA8'}
}

CHART_CONFIG = {'displayModeBar': False, 'responsive': True}

# ================ PAGE SETUP ================
st.set_page_config(**PAGE_CONFIG)

# ================ CUSTOM CSS ================
def apply_custom_styles():
    """Apply custom CSS styling to the dashboard."""
    st.markdown(
        """
        <style>
        /* Page */
        html, body, .block-container { background: #fbfdff; padding: 20px 30px 18px 30px; }
        .reportview-container .main .block-container { max-width: 100%; padding-top: 20px; }

        /* Title */
        .exec-title { text-align:center; font-size:24px; font-weight:700; color:#102233; margin-bottom:8px; margin-top:10px; }
        .exec-sub { text-align:center; color:#5b6b78; font-size:14px; margin-bottom:20px; }

        /* KPI card */
        .kpi {
            flex:1;
            background: white;
            border-radius:12px;
            padding:14px 18px;
            box-shadow: 0 6px 18px rgba(16,30,48,0.06);
            display:flex;
            flex-direction:column;
            justify-content:space-between;
            min-height:88px;
        }
        .kpi-top { display:flex; justify-content:space-between; align-items:center; }
        .kpi-value { font-size:22px; font-weight:700; color:#102233; margin-top:6px; }
        .kpi-label { font-size:12px; color:#556670; margin-top:4px; }

        /* Trend indicators */
        .trend-up { color:#178a5b; font-weight:600; font-size:12px; }
        .trend-down { color:#c34444; font-weight:600; font-size:12px; }

        /* Chart cards */
        .chart-card {
            background: white;
            border-radius:12px;
            padding:12px;
            box-shadow: 0 6px 18px rgba(16,30,48,0.04);
            margin-bottom:12px;
        }
        .chart-title { font-size:14px; color:#102233; font-weight:600; margin-bottom:6px; }

        /* Insight bar */
        .insight { 
            background:#eef6ff; 
            padding:10px 12px; 
            border-radius:8px; 
            color:#102233; 
            font-size:13px; 
            box-shadow: 0 2px 8px rgba(16,30,48,0.03); 
            margin-top:8px; 
        }

        /* Responsive */
        @media (max-width: 768px) {
            .kpi-value { font-size: 18px; }
            .exec-title { font-size: 18px; }
        }

        .stPlotlyChart > div { margin:0 !important; padding:0 !important; }
        </style>
        """, unsafe_allow_html=True)

# ================ DATA LOADING ================
@st.cache_data
def load_infrastructure_data() -> pd.DataFrame:
    """Load healthcare infrastructure data."""
    return pd.DataFrame({
        "Metric": ["Sub-centres", "PHCs", "CHCs"],
        "Value": [153655, 25308, 5396]
    })

@st.cache_data
def load_pmjay_data() -> pd.DataFrame:
    """Load PMJAY beneficiary coverage data."""
    return pd.DataFrame({
        "Year": [2018, 2019, 2020, 2021, 2022, 2023, 2024],
        "Coverage_millions": [0, 50, 120, 220, 320, 420, 500]
    })

@st.cache_data
def load_spending_data() -> pd.DataFrame:
    """Load public health spending data."""
    return pd.DataFrame({
        "Year": [2019, 2020, 2021],
        "Percent_GDP": [1.3, 1.8, 2.1]
    })

@st.cache_data
def load_market_data() -> pd.DataFrame:
    """Load healthcare market data."""
    return pd.DataFrame({
        "Year": [2016, 2022],
        "Market_USD_Billion": [110, 372]
    })

@st.cache_data
def load_capacity_data() -> pd.DataFrame:
    """Load healthcare capacity comparison data."""
    return pd.DataFrame({
        "Metric": ["Doctors", "Hospital Beds", "Nurses", "Spending"],
        "Current": [5.2, 6.5, 8.1, 2.1],
        "Target": [7.0, 7.0, 9.0, 3.5]
    })

@st.cache_data
def get_kpi_data() -> Dict[str, Tuple[str, str, str, str]]:
    """
    Get KPI data for dashboard cards.
    Returns dict with: title, value, trend, label for each KPI.
    """
    return {
        'doctor_shortage': ("Doctor Shortage", "600K", "⬇︎ 15.2%", "National", "down"),
        'health_spending': ("Public Health Spending", "2.1%", "▲ +0.3%", "Percent of GDP (2021)", "up"),
        'market_size': ("Healthcare Market 2022", "$372B", "▲ +238%", "USD market value", "up"),
        'pmjay_coverage': ("PMJAY Coverage", "500M+", "▲ +45.8%", "Beneficiaries (approx.)", "up")
    }

# ================ HELPER FUNCTIONS ================
def create_kpi_card(title: str, value: str, trend: str, label: str, 
                   bg_color: str, border_color: str, text_color: str, 
                   trend_direction: str) -> str:
    """
    Create HTML for a KPI card.
    
    Args:
        title: KPI title
        value: Main KPI value
        trend: Trend indicator text
        label: Descriptive label
        bg_color: Background color
        border_color: Left border color
        text_color: Text color for title
        trend_direction: 'up' or 'down'
    
    Returns:
        HTML string for the KPI card
    """
    trend_class = "trend-up" if trend_direction == "up" else "trend-down"
    
    return f"""
        <div class="kpi" style="border-left:4px solid {border_color}; background:{bg_color};">
            <div class="kpi-top">
                <div style="display:flex;flex-direction:column;">
                    <div style="font-size:12px;color:{text_color};font-weight:600">{title}</div>
                    <div class="kpi-value">{value}</div>
                </div>
                <div class="{trend_class}">{trend}</div>
            </div>
            <div class="kpi-label">{label}</div>
        </div>
    """

@st.cache_data
def create_infrastructure_chart(df: pd.DataFrame) -> go.Figure:
    """Create horizontal bar chart for infrastructure distribution."""
    fig = px.bar(
        df.sort_values("Value"), 
        x="Value", 
        y="Metric", 
        orientation="h",
        text="Value", 
        color_discrete_sequence=[COLORS['chart_primary']]
    )
    fig.update_traces(
        texttemplate='%{text:,}', 
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Count: %{x:,}<extra></extra>'
    )
    fig.update_layout(
        height=280, 
        template="simple_white",
        margin=dict(l=10, r=6, t=8, b=8),
        xaxis_title=None,
        yaxis_title=None
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(18,34,54,0.06)")
    return fig

@st.cache_data
def create_pmjay_chart(df: pd.DataFrame) -> go.Figure:
    """Create area chart for PMJAY beneficiary growth."""
    fig = go.Figure()
    
    # Line
    fig.add_trace(go.Scatter(
        x=df['Year'], 
        y=df['Coverage_millions'],
        mode='lines', 
        line=dict(color=COLORS['chart_secondary'], width=2.5),
        name='Coverage',
        hovertemplate='<b>Year: %{x}</b><br>Coverage: %{y}M<extra></extra>'
    ))
    
    # Markers
    fig.add_trace(go.Scatter(
        x=df['Year'], 
        y=df['Coverage_millions'],
        mode='markers', 
        marker=dict(size=6, color=COLORS['chart_secondary']),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Area fill
    fig.add_trace(go.Scatter(
        x=df['Year'].tolist() + df['Year'].tolist()[::-1],
        y=df['Coverage_millions'].tolist() + [0] * len(df),
        fill='toself',
        fillcolor='rgba(46,134,171,0.12)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        height=280, 
        template="simple_white", 
        margin=dict(l=10, r=6, t=8, b=8),
        xaxis_title=None,
        yaxis_title=None
    )
    fig.update_xaxes(tickmode='linear')
    return fig

@st.cache_data
def create_spending_chart(df: pd.DataFrame) -> go.Figure:
    """Create line chart for public health spending."""
    fig = px.line(
        df, 
        x="Year", 
        y="Percent_GDP", 
        markers=True
    )
    fig.update_traces(
        line=dict(color="#146C9A", width=2), 
        marker=dict(size=6, color="#146C9A"),
        hovertemplate='<b>Year: %{x}</b><br>GDP: %{y}%<extra></extra>'
    )
    fig.update_layout(
        height=240, 
        template="simple_white", 
        margin=dict(l=10, r=6, t=8, b=8),
        xaxis_title=None,
        yaxis_title="% of GDP"
    )
    return fig

@st.cache_data
def create_capacity_chart(df: pd.DataFrame) -> go.Figure:
    """Create grouped bar chart for capacity comparison."""
    cap_long = df.melt(
        id_vars="Metric", 
        value_vars=["Current", "Target"], 
        var_name="Type", 
        value_name="Value"
    )
    
    fig = px.bar(
        cap_long, 
        x="Value", 
        y="Metric", 
        color="Type", 
        orientation="h",
        color_discrete_map=COLORS['chart_comparison'], 
        barmode="group"
    )
    fig.update_traces(
        hovertemplate='<b>%{y}</b><br>%{fullData.name}: %{x}<extra></extra>'
    )
    fig.update_layout(
        height=240, 
        template="simple_white", 
        margin=dict(l=10, r=6, t=8, b=8), 
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title=None,
        yaxis_title=None
    )
    return fig

# ================ MAIN DASHBOARD ================
def main():
    """Main dashboard rendering function."""
    try:
        # Apply styles
        apply_custom_styles()
        
        # Load data
        infra_df = load_infrastructure_data()
        pmjay_df = load_pmjay_data()
        spend_df = load_spending_data()
        market_df = load_market_data()
        capacity_df = load_capacity_data()
        kpi_data = get_kpi_data()
        
        # Title
        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing at top
        st.markdown(
            "<div class='exec-title'>📊 India Healthcare – Executive Dashboard</div>", 
            unsafe_allow_html=True
        )
        st.markdown(
            "<div class='exec-sub'>Live snapshot • Pastel executive template</div>", 
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing before KPIs
        
        # KPI Cards
        k1, k2, k3, k4 = st.columns([1, 1, 1, 1], gap="large")
        
        kpi_configs = [
            (k1, 'doctor_shortage', 0),
            (k2, 'health_spending', 1),
            (k3, 'market_size', 2),
            (k4, 'pmjay_coverage', 3)
        ]
        
        for col, kpi_key, color_idx in kpi_configs:
            with col:
                title, value, trend, label, direction = kpi_data[kpi_key]
                st.markdown(
                    create_kpi_card(
                        title, value, trend, label,
                        COLORS['kpi_backgrounds'][color_idx],
                        COLORS['kpi_borders'][color_idx],
                        COLORS['kpi_text'][color_idx],
                        direction
                    ),
                    unsafe_allow_html=True
                )
        
        # Charts - Row 1
        chart_col_1, chart_col_2 = st.columns([2, 2], gap="large")
        
        with chart_col_1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="chart-title">Healthcare Infrastructure Distribution<br>'
                '<span style="font-size:11px;color:#6b7285">Facility breakdown (Total: 184.4K)</span></div>',
                unsafe_allow_html=True
            )
            fig_infra = create_infrastructure_chart(infra_df)
            st.plotly_chart(fig_infra, use_container_width=True, config=CHART_CONFIG)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with chart_col_2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="chart-title">PMJAY Beneficiary Growth Trajectory<br>'
                '<span style="font-size:11px;color:#6b7285">Ayushman Bharat Coverage Expansion (Millions)</span></div>',
                unsafe_allow_html=True
            )
            fig_pm = create_pmjay_chart(pmjay_df)
            st.plotly_chart(fig_pm, use_container_width=True, config=CHART_CONFIG)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Charts - Row 2
        chart_col_3, chart_col_4 = st.columns([2, 2], gap="large")
        
        with chart_col_3:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="chart-title">Public Health Spending Progression<br>'
                '<span style="font-size:11px;color:#6b7285">Percentage of GDP - Upward Trend</span></div>',
                unsafe_allow_html=True
            )
            fig_spend = create_spending_chart(spend_df)
            st.plotly_chart(fig_spend, use_container_width=True, config=CHART_CONFIG)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with chart_col_4:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="chart-title">Healthcare Capacity Metrics<br>'
                '<span style="font-size:11px;color:#6b7285">Current vs Recommended Levels</span></div>',
                unsafe_allow_html=True
            )
            fig_cap = create_capacity_chart(capacity_df)
            st.plotly_chart(fig_cap, use_container_width=True, config=CHART_CONFIG)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Insight bar
        st.markdown(
            "<div class='insight'>💡 <strong>Insight:</strong> India's healthcare capacity is expanding, "
            "yet workforce and spending gaps remain the primary structural risks requiring immediate policy intervention.</div>",
            unsafe_allow_html=True
        )
        
    except Exception as e:
        st.error(f"⚠️ Error loading dashboard: {str(e)}")
        st.info("Please check your data sources and try again.")

# ================ RUN ================
if __name__ == "__main__":
    main()