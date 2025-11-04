"""
Enhanced Streamlit App for Icelandic Fisheries and Ocean Temperature Analysis
Sjávarútvegs DataDemo - Afli vs Hitastig
Now with all species and all temperature stations!
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from datetime import datetime
from scipy import stats

# Page config
st.set_page_config(
    page_title="Afli vs Hitastig - Sjávarútvegs DataDemo",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Project paths - handle both local and deployed environments
try:
    # Try local development path first
    PROJECT_ROOT = Path(__file__).parent.parent
    if not (PROJECT_ROOT / "data").exists():
        # If deployed, files might be in current directory
        PROJECT_ROOT = Path(__file__).parent
except:
    PROJECT_ROOT = Path.cwd()

DATA_DIR = PROJECT_ROOT / "data" / "processed" / "comparison"
FISH_DATA_DIR = PROJECT_ROOT / "data" / "processed" / "afli_eftir_fisktegundum"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 1rem;
    }
    .disclaimer-box {
        background-color: #f8d7da;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #dc3545;
        margin: 1rem 0 2rem 0;
        text-align: center;
    }
    .branding-box {
        background-color: #e7f3ff;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border-left: 3px solid #0066cc;
        margin: 0 0 1rem 0;
        text-align: center;
        font-size: 0.9rem;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Branding
st.markdown("""
<div class="branding-box">
    📊 Prepared by <strong><a href="https://www.smarason.is" target="_blank">smarason.is</a></strong>
</div>
""", unsafe_allow_html=True)

# Title and introduction
st.markdown('<div class="main-header">🐟 Afli vs Hitastig Sjávar 🌊</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Greining á samhengi milli aflafars og sjávarhitastigs við Ísland (2010-2024)</div>', unsafe_allow_html=True)

# EDUCATIONAL DISCLAIMER
st.markdown("""
<div class="disclaimer-box">
    <h3 style="color: #dc3545; margin-top: 0;">⚠️ EDUCATIONAL PURPOSE ONLY - UNVERIFIED DATA ⚠️</h3>
    <p style="margin-bottom: 0.5rem;"><strong>This application is for educational and demonstration purposes only.</strong></p>
    <p style="margin-bottom: 0.5rem;">The data and analysis presented here have <strong>NOT been verified</strong> by official institutions.</p>
    <p style="margin-bottom: 0.5rem;">Do <strong>NOT</strong> use for decision-making, policy formulation, or scientific publication without proper validation.</p>
    <p style="margin-bottom: 0;">For verified data, consult: <a href="https://statice.is" target="_blank">Hagstofa Íslands</a> | <a href="https://www.hafogvatn.is" target="_blank">Hafrannsóknastofnun</a> | <a href="https://marine.copernicus.eu" target="_blank">Copernicus Marine Service</a></p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎛️ Stillingar")
st.sidebar.markdown("---")

# Load data
@st.cache_data
def load_all_data():
    """Load all comparison datasets including new species data"""
    try:
        # Debug: Show paths
        st.sidebar.info(f"📁 Looking for data in: {DATA_DIR}")

        # Load comprehensive catch-temperature data with all species
        species_file = DATA_DIR / "all_species_temperature_monthly.csv"
        if not species_file.exists():
            st.error(f"❌ File not found: {species_file}")
            st.info(f"Current directory: {Path.cwd()}")
            st.info(f"Project root: {PROJECT_ROOT}")
            return None, None

        all_species = pd.read_csv(species_file, parse_dates=['date'])

        # Load old data for backward compatibility
        comprehensive = pd.read_csv(DATA_DIR / "catch_temperature_comprehensive.csv", parse_dates=['date'])

        return all_species, comprehensive
    except Exception as e:
        st.error(f"❌ Villa við lestur gagna: {e}")
        st.info(f"Current directory: {Path.cwd()}")
        st.info(f"Project root: {PROJECT_ROOT}")
        st.info(f"Data directory: {DATA_DIR}")
        st.info("Keyrðu fyrst: `python scripts/03_data_processing/process_all_species_comprehensive.py`")
        return None, None

all_species_df, comprehensive_df = load_all_data()

if all_species_df is None or comprehensive_df is None:
    st.stop()

# Sidebar filters
st.sidebar.markdown("### 📅 Tímabil")
year_range = st.sidebar.slider(
    "Veldu árabil:",
    int(all_species_df['year'].min()),
    int(all_species_df['year'].max()),
    (int(all_species_df['year'].min()), int(all_species_df['year'].max()))
)

# Filter data by year range
filtered_species_df = all_species_df[
    (all_species_df['year'] >= year_range[0]) &
    (all_species_df['year'] <= year_range[1])
].copy()

# Species selection
st.sidebar.markdown("### 🐟 Fisktegundir")
available_species = sorted(filtered_species_df['species_icelandic'].unique())
selected_species = st.sidebar.multiselect(
    "Veldu tegundir:",
    options=available_species,
    default=available_species[:3]  # Default to first 3 species
)

if not selected_species:
    selected_species = available_species  # Select all if none selected

# Temperature dataset selection
st.sidebar.markdown("### 🌡️ Hitamælistöðvar")
temp_dataset = st.sidebar.radio(
    "Veldu hitamælingu:",
    options=[
        "Copernicus (EEZ meðaltal)",
        "Grímsey (Norðurland)",
        "Vestmannaeyjar (Suðurland)",
        "Þriggja stöðva meðaltal"
    ],
    index=0
)

# Map selection to column name
temp_col_map = {
    "Copernicus (EEZ meðaltal)": "temp_copernicus",
    "Grímsey (Norðurland)": "temp_grimsey",
    "Vestmannaeyjar (Suðurland)": "temp_vestmann",
    "Þriggja stöðva meðaltal": "temp_three_station_avg"
}
temp_col = temp_col_map[temp_dataset]

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Yfirlit",
    "🌡️ Hitamælingar",
    "🐟 Tegundir",
    "📈 Fylgni",
    "📋 Gögn"
])

# ============================================================================
# TAB 1: Overview
# ============================================================================
with tab1:
    st.header("📊 Yfirlit yfir afla og hitastig")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_catch = filtered_species_df['catch_tons'].sum()
        st.metric(
            "Heildarafli",
            f"{total_catch:,.0f} tonn",
            help="Heildarafli allra tegunda á tímabilinu"
        )

    with col2:
        avg_temp = filtered_species_df[temp_col].mean()
        st.metric(
            f"Meðalhitastig ({temp_dataset.split('(')[0].strip()})",
            f"{avg_temp:.2f}°C",
            help=f"Meðal sjávarhitastig á tímabilinu - {temp_dataset}"
        )

    with col3:
        n_months = len(filtered_species_df['date'].unique())
        st.metric(
            "Fjöldi mánaða",
            f"{n_months}",
            help="Fjöldi mánaða í greiningu"
        )

    with col4:
        n_species = len(selected_species)
        st.metric(
            "Fjöldi tegunda",
            f"{n_species}",
            help="Fjöldi tegunda í greiningu"
        )

    # Total catch over time
    st.markdown("### 📈 Heildarafli yfir tíma")

    # Aggregate by date and species
    time_series = filtered_species_df[filtered_species_df['species_icelandic'].isin(selected_species)].copy()

    fig = px.area(
        time_series,
        x='date',
        y='catch_tons',
        color='species_icelandic',
        title='Afli eftir tegundum yfir tíma',
        labels={
            'date': 'Dagsetning',
            'catch_tons': 'Afli (tonn)',
            'species_icelandic': 'Tegund'
        }
    )
    fig.update_layout(height=500, hovermode='x unified')
    st.plotly_chart(fig, width="stretch")

    # Temperature trends
    st.markdown(f"### 🌡️ Hitaþróun - {temp_dataset}")

    # Get temperature data (drop duplicates since multiple species share same temp)
    temp_data = comprehensive_df[
        (comprehensive_df['year'] >= year_range[0]) &
        (comprehensive_df['year'] <= year_range[1])
    ].copy()

    fig_temp = go.Figure()

    # Add all temperature datasets
    fig_temp.add_trace(go.Scatter(
        x=temp_data['date'],
        y=temp_data['temp_copernicus'],
        name='Copernicus (EEZ)',
        mode='lines',
        line=dict(color='blue')
    ))

    fig_temp.add_trace(go.Scatter(
        x=temp_data['date'],
        y=temp_data['temp_grimsey'],
        name='Grímsey (Norður)',
        mode='lines',
        line=dict(color='cyan')
    ))

    fig_temp.add_trace(go.Scatter(
        x=temp_data['date'],
        y=temp_data['temp_vestmann'],
        name='Vestmannaeyjar (Suður)',
        mode='lines',
        line=dict(color='red')
    ))

    fig_temp.add_trace(go.Scatter(
        x=temp_data['date'],
        y=temp_data['temp_three_station_avg'],
        name='Meðaltal þriggja stöðva',
        mode='lines',
        line=dict(color='green', width=2, dash='dash')
    ))

    fig_temp.update_layout(
        title='Samanburður hitamælinga frá þremur stöðvum',
        xaxis_title='Dagsetning',
        yaxis_title='Hitastig (°C)',
        height=500,
        hovermode='x unified'
    )
    st.plotly_chart(fig_temp, width="stretch")

    # Key insights
    st.markdown("### 🔍 Helstu niðurstöður")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="insight-box">
        <h4>🌊 Sjávarhitastig</h4>
        <ul>
        <li><strong>Copernicus EEZ meðaltal:</strong> Víðtækasta mælingin, nær yfir allt efnahagslögsögu</li>
        <li><strong>Grímsey (66.5°N):</strong> Norðurströnd Íslands, á heimskautsbaugnum</li>
        <li><strong>Vestmannaeyjar (63.4°N):</strong> Suðurströnd Íslands</li>
        <li><strong>Hitamunur norður-suður:</strong> ~3°C</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Calculate total catch by species
        species_totals = filtered_species_df[filtered_species_df['species_icelandic'].isin(selected_species)].groupby('species_icelandic')['catch_tons'].sum().sort_values(ascending=False)

        top_species_html = "<ul>"
        for species, total in species_totals.head(5).items():
            pct = (total / species_totals.sum()) * 100
            top_species_html += f"<li><strong>{species}:</strong> {total:,.0f} tonn ({pct:.1f}%)</li>"
        top_species_html += "</ul>"

        st.markdown(f"""
        <div class="success-box">
        <h4>🐟 Helstu tegundir</h4>
        {top_species_html}
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 2: Temperature Comparison
# ============================================================================
with tab2:
    st.header("🌡️ Hitamælingar - Samanburður stöðva")

    st.markdown("""
    ### Þrjár óháðar hitamælingar

    Greiningin byggir á þremur óháðum hitamælingum:
    1. **Copernicus GLORYS12V1**: Hnattræn hafrýnigreining með staðfestingu við gervihnatta- og in-situ mælingar
    2. **Grímsey**: Dagleg in-situ mæling á heimskautsbaugnum (Marine Research Institute)
    3. **Vestmannaeyjar**: Dagleg in-situ mæling á suðurströnd (Marine Research Institute)
    """)

    # Temperature statistics
    col1, col2, col3 = st.columns(3)

    temp_stats = comprehensive_df[
        (comprehensive_df['year'] >= year_range[0]) &
        (comprehensive_df['year'] <= year_range[1])
    ]

    with col1:
        st.markdown("### Copernicus (EEZ)")
        st.metric("Meðaltal", f"{temp_stats['temp_copernicus'].mean():.2f}°C")
        st.metric("Staðalfrávik", f"{temp_stats['temp_copernicus'].std():.2f}°C")
        st.metric("Min / Max", f"{temp_stats['temp_copernicus'].min():.2f}°C / {temp_stats['temp_copernicus'].max():.2f}°C")

    with col2:
        st.markdown("### Grímsey (Norður)")
        st.metric("Meðaltal", f"{temp_stats['temp_grimsey'].mean():.2f}°C")
        st.metric("Staðalfrávik", f"{temp_stats['temp_grimsey'].std():.2f}°C")
        st.metric("Min / Max", f"{temp_stats['temp_grimsey'].min():.2f}°C / {temp_stats['temp_grimsey'].max():.2f}°C")

    with col3:
        st.markdown("### Vestmannaeyjar (Suður)")
        st.metric("Meðaltal", f"{temp_stats['temp_vestmann'].mean():.2f}°C")
        st.metric("Staðalfrávik", f"{temp_stats['temp_vestmann'].std():.2f}°C")
        st.metric("Min / Max", f"{temp_stats['temp_vestmann'].min():.2f}°C / {temp_stats['temp_vestmann'].max():.2f}°C")

    # Correlation matrix between temperature datasets
    st.markdown("### 📊 Fylgni milli hitamælinga")

    temp_corr = temp_stats[['temp_copernicus', 'temp_grimsey', 'temp_vestmann', 'temp_three_station_avg']].corr()

    fig_corr = px.imshow(
        temp_corr,
        labels=dict(x="Stöð", y="Stöð", color="Fylgni"),
        x=['Copernicus', 'Grímsey', 'Vestmannaeyjar', 'Meðaltal'],
        y=['Copernicus', 'Grímsey', 'Vestmannaeyjar', 'Meðaltal'],
        color_continuous_scale='RdBu_r',
        aspect='auto',
        text_auto='.2f'
    )
    fig_corr.update_layout(height=500)
    st.plotly_chart(fig_corr, width="stretch")

    # Geographic gradient
    st.markdown("### 🗺️ Landfræðilegur hitamunur")

    avg_grimsey = temp_stats['temp_grimsey'].mean()
    avg_vestmann = temp_stats['temp_vestmann'].mean()
    gradient = avg_vestmann - avg_grimsey

    st.markdown(f"""
    <div class="insight-box">
    <h4>Norður-suður hitastigsmunur</h4>
    <ul>
    <li><strong>Grímsey (norður):</strong> {avg_grimsey:.2f}°C meðaltal</li>
    <li><strong>Vestmannaeyjar (suður):</strong> {avg_vestmann:.2f}°C meðaltal</li>
    <li><strong>Munur:</strong> {gradient:.2f}°C kaldara á norðurströnd</li>
    </ul>
    <p>Þetta endurspeglar áhrif norðanstrauma og Golfstraumsins.</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# TAB 3: Species Analysis
# ============================================================================
with tab3:
    st.header("🐟 Greining eftir fisktegundum")

    # Species selection for this tab
    species_for_analysis = st.multiselect(
        "Veldu tegundir til samanburðar:",
        options=available_species,
        default=available_species[:4],
        key="species_tab3"
    )

    if species_for_analysis:
        # Catch by species over time
        st.markdown("### 📈 Afli eftir tegundum")

        species_time = filtered_species_df[filtered_species_df['species_icelandic'].isin(species_for_analysis)].copy()

        fig = px.line(
            species_time,
            x='date',
            y='catch_tons',
            color='species_icelandic',
            title='Afli eftir tegundum yfir tíma',
            labels={
                'date': 'Dagsetning',
                'catch_tons': 'Afli (tonn)',
                'species_icelandic': 'Tegund'
            }
        )
        fig.update_layout(height=500, hovermode='x unified')
        st.plotly_chart(fig, width="stretch")

        # Correlation with temperature by species
        st.markdown(f"### 📊 Fylgni við hitastig - {temp_dataset}")

        correlations = []
        for species in species_for_analysis:
            species_data = filtered_species_df[filtered_species_df['species_icelandic'] == species].copy()
            species_data = species_data.dropna(subset=['catch_tons', temp_col])

            if len(species_data) > 10:
                corr, pval = stats.pearsonr(species_data['catch_tons'], species_data[temp_col])
                correlations.append({
                    'Tegund': species,
                    'Fylgni': corr,
                    'P-gildi': pval,
                    'N': len(species_data)
                })

        if correlations:
            corr_df = pd.DataFrame(correlations).sort_values('Fylgni')

            fig_corr = px.bar(
                corr_df,
                x='Fylgni',
                y='Tegund',
                orientation='h',
                title='Fylgni aflafars við hitastig eftir tegundum',
                labels={'Fylgni': 'Pearson fylgnistuðull', 'Tegund': 'Fisktegund'},
                color='Fylgni',
                color_continuous_scale='RdBu_r',
                color_continuous_midpoint=0
            )
            fig_corr.add_vline(x=0, line_dash="dash", line_color="black")
            fig_corr.update_layout(height=400)
            st.plotly_chart(fig_corr, width="stretch")

            # Show table
            st.dataframe(
                corr_df.style.format({
                    'Fylgni': '{:.3f}',
                    'P-gildi': '{:.2e}',
                    'N': '{:.0f}'
                }),
                width="stretch"
            )

            # Interpretation
            st.markdown("""
            <div class="insight-box">
            <h4>🔍 Túlkun</h4>
            <ul>
            <li><strong>Neikvæð fylgni:</strong> Meiri afli þegar kaldara er (kaldsjávartegund)</li>
            <li><strong>Jákvæð fylgni:</strong> Meiri afli þegar hlýrra er (hlýsjávartegund)</li>
            <li><strong>P-gildi < 0.05:</strong> Tölfræðilega marktækt samband</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# TAB 4: Correlation Analysis
# ============================================================================
with tab4:
    st.header("📈 Fylgnigreining - Afli vs Hitastig")

    # Overall correlation for selected species
    combined_data = filtered_species_df[filtered_species_df['species_icelandic'].isin(selected_species)].copy()
    combined_data = combined_data.dropna(subset=['catch_tons', temp_col])

    if len(combined_data) > 10:
        # Aggregate by date (sum across species)
        agg_data = combined_data.groupby('date').agg({
            'catch_tons': 'sum',
            temp_col: 'first'  # Temperature is same for all species on same date
        }).reset_index()

        corr, pval = stats.pearsonr(agg_data['catch_tons'], agg_data[temp_col])

        # Display metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Fylgnistuðull", f"{corr:.3f}")

        with col2:
            st.metric("P-gildi", f"{pval:.2e}")

        with col3:
            significance = "✅ Marktækt" if pval < 0.05 else "❌ Ekki marktækt"
            st.metric("Marktækni", significance)

        # Scatter plot
        st.markdown(f"### 📊 Punktarit - {temp_dataset}")

        fig = px.scatter(
            agg_data,
            x=temp_col,
            y='catch_tons',
            trendline='ols',
            title=f'Afli vs {temp_dataset}',
            labels={
                temp_col: f'Hitastig (°C) - {temp_dataset}',
                'catch_tons': 'Afli (tonn)'
            }
        )
        fig.update_traces(marker=dict(size=8, opacity=0.6))
        fig.update_layout(height=500)
        st.plotly_chart(fig, width="stretch")

        # Time series with dual axis
        st.markdown("### 📈 Tímaraðir - Tvöfaldur ás")

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(
                x=agg_data['date'],
                y=agg_data['catch_tons'],
                name="Afli",
                line=dict(color='blue')
            ),
            secondary_y=False
        )

        fig.add_trace(
            go.Scatter(
                x=agg_data['date'],
                y=agg_data[temp_col],
                name=f"Hitastig - {temp_dataset.split('(')[0].strip()}",
                line=dict(color='red')
            ),
            secondary_y=True
        )

        fig.update_xaxes(title_text="Dagsetning")
        fig.update_yaxes(title_text="Afli (tonn)", secondary_y=False)
        fig.update_yaxes(title_text="Hitastig (°C)", secondary_y=True)
        fig.update_layout(height=500, hovermode='x unified')

        st.plotly_chart(fig, width="stretch")

        # Interpretation based on correlation
        if corr < -0.3 and pval < 0.05:
            st.markdown("""
            <div class="warning-box">
            <h4>⚠️ Sterk neikvæð fylgni!</h4>
            <p>Gögnin sýna tölfræðilega marktæka <strong>neikvæða fylgni</strong> milli aflafars og hitastigs.
            Þetta bendir til þess að meiri afli er þegar sjórinn er kaldari. Þetta er í samræmi við lífríki kaldsjávartegunda
            eins og þorsks og ýsu sem kjósa kaldara sjávarhita (4-7°C).</p>
            </div>
            """, unsafe_allow_html=True)
        elif corr > 0.3 and pval < 0.05:
            st.markdown("""
            <div class="success-box">
            <h4>✅ Sterk jákvæð fylgni!</h4>
            <p>Gögnin sýna tölfræðilega marktæka <strong>jákvæða fylgni</strong> milli aflafars og hitastigs.
            Þetta bendir til þess að meiri afli er þegar sjórinn er hlýrri. Þetta gæti bent til hlýsjávartegunda.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="insight-box">
            <h4>ℹ️ Veik eða engin línuleg fylgni</h4>
            <p>Gögnin sýna ekki sterka línulega fylgni milli aflafars og hitastigs.
            Aðrir þættir (kvótar, veiðiátak, stjórnun) kunna að hafa meiri áhrif.</p>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# TAB 5: Data Table
# ============================================================================
with tab5:
    st.header("📋 Hrá gögn")

    st.markdown("### 🐟 Afli og hitastig - Allar tegundir")

    # Display options
    show_all = st.checkbox("Sýna öll gögn (getur verið hægt)", value=False)

    if show_all:
        display_data = filtered_species_df[filtered_species_df['species_icelandic'].isin(selected_species)]
    else:
        display_data = filtered_species_df[filtered_species_df['species_icelandic'].isin(selected_species)].head(100)
        st.info("Sýni fyrstu 100 línurnar. Hakaðu í kassann til að sjá allt.")

    st.dataframe(
        display_data.style.format({
            'catch_kg': '{:,.0f}',
            'catch_tons': '{:,.1f}',
            'temp_copernicus': '{:.2f}',
            'temp_grimsey': '{:.2f}',
            'temp_vestmann': '{:.2f}',
            'temp_three_station_avg': '{:.2f}'
        }),
        width="stretch",
        height=600
    )

    # Download button
    csv = filtered_species_df[filtered_species_df['species_icelandic'].isin(selected_species)].to_csv(index=False)
    st.download_button(
        label="📥 Sækja gögn (CSV)",
        data=csv,
        file_name=f"afli_hitastig_{year_range[0]}_{year_range[1]}.csv",
        mime="text/csv"
    )

    # Data summary
    st.markdown("### 📊 Yfirlit gagna")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Fjöldi ára:**")
        st.write(f"{year_range[1] - year_range[0] + 1} ár")

        st.markdown("**Fjöldi mánaða:**")
        st.write(f"{len(filtered_species_df['date'].unique())} mánuðir")

        st.markdown("**Fjöldi tegunda:**")
        st.write(f"{len(selected_species)} tegundir")

    with col2:
        st.markdown("**Heildarafli:**")
        st.write(f"{filtered_species_df[filtered_species_df['species_icelandic'].isin(selected_species)]['catch_tons'].sum():,.0f} tonn")

        st.markdown(f"**Meðalhitastig ({temp_dataset}):**")
        st.write(f"{filtered_species_df[temp_col].mean():.2f}°C")

        st.markdown("**Gagnalind:**")
        st.write("Hagstofa Íslands, Hafrannsóknastofnun, Copernicus")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>📊 Sjávarútvegs DataDemo | 🐟 Afli vs 🌡️ Hitastig</p>
    <p>Gögn: Hagstofa Íslands, Hafrannsóknastofnun, Copernicus Marine Service</p>
    <p>Tímabil: 2010-2024 | Þrefaldar hitamælingar: Copernicus EEZ + Grímsey + Vestmannaeyjar</p>
    <p style="margin-top: 1rem;"><strong>⚠️ EDUCATIONAL DEMO - UNVERIFIED DATA ⚠️</strong></p>
    <p>Prepared by <a href="https://www.smarason.is" target="_blank" style="color: #0066cc;">www.smarason.is</a></p>
</div>
""", unsafe_allow_html=True)
