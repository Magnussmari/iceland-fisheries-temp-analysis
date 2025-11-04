"""
Streamlit App for Icelandic Fisheries and Ocean Temperature Analysis
Sjávarútvegs DataDemo - Afli vs Hitastig
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

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed" / "comparison"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
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
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.markdown('<div class="main-header">🐟 Afli vs Hitastig Sjávar 🌊</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Greining á samhengi milli aflafars og sjávarhitastigs við Ísland (2010-2025)</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎛️ Stillingar")
st.sidebar.markdown("---")

# Load data
@st.cache_data
def load_comparison_data():
    """Load all comparison datasets"""
    try:
        monthly = pd.read_csv(DATA_DIR / "catch_temperature_monthly.csv", parse_dates=['date'])
        species = pd.read_csv(DATA_DIR / "catch_temperature_by_species_monthly.csv", parse_dates=['date'])
        yearly = pd.read_csv(DATA_DIR / "catch_temperature_yearly.csv")
        species_corr = pd.read_csv(DATA_DIR / "species_temperature_correlations.csv")
        seasonal_corr = pd.read_csv(DATA_DIR / "seasonal_correlations.csv")

        return monthly, species, yearly, species_corr, seasonal_corr
    except Exception as e:
        st.error(f"❌ Villa við lestur gagna: {e}")
        st.info("Keyrðu fyrst: `python scripts/03_data_processing/create_catch_temp_comparison.py`")
        return None, None, None, None, None

monthly_df, species_df, yearly_df, species_corr_df, seasonal_corr_df = load_comparison_data()

if monthly_df is None:
    st.stop()

# Sidebar filters
st.sidebar.markdown("### 📅 Tímabil")
year_range = st.sidebar.slider(
    "Veldu árabil:",
    int(monthly_df['year'].min()),
    int(monthly_df['year'].max()),
    (int(monthly_df['year'].min()), int(monthly_df['year'].max()))
)

# Filter data
filtered_monthly = monthly_df[(monthly_df['year'] >= year_range[0]) & (monthly_df['year'] <= year_range[1])]
filtered_species = species_df[(species_df['year'] >= year_range[0]) & (species_df['year'] <= year_range[1])]

# Calculate metrics for filtered data
total_catch = filtered_monthly['total_catch_tons'].sum()
avg_temp = filtered_monthly['temp_celsius'].mean()
correlation = filtered_monthly['total_catch_tons'].corr(filtered_monthly['temp_celsius'])

# Key metrics
st.markdown("### 📊 Lykilmælikvarðar")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Heildarafli",
        f"{total_catch:,.0f} tonn",
        delta=None
    )

with col2:
    st.metric(
        "Meðalhitastig",
        f"{avg_temp:.2f}°C",
        delta=None
    )

with col3:
    corr_direction = "Neikvæð" if correlation < 0 else "Jákvæð"
    corr_strength = "sterk" if abs(correlation) > 0.5 else "miðlungs" if abs(correlation) > 0.3 else "veik"
    st.metric(
        "Fylgni (Correlation)",
        f"{correlation:.3f}",
        delta=f"{corr_direction}, {corr_strength}"
    )

with col4:
    n_months = len(filtered_monthly)
    st.metric(
        "Fjöldi mánuða",
        f"{n_months}",
        delta=None
    )

# Key insights
st.markdown("### 💡 Helstu niðurstöður")

if correlation < -0.4:
    st.markdown(f"""
    <div class="warning-box">
    <b>⚠️ Sterk neikvæð fylgni fundin!</b><br>
    Fylgnistuðull: <b>{correlation:.3f}</b><br><br>
    Þetta bendir til þess að þegar sjávarhitastig hækkar, þá <b>lækkar heildarafli</b>.
    Þetta er mikilvæg niðurstaða fyrir sjávarútveginn þar sem loftslagsbreytingar eru að hækka
    sjávarhitastig við Ísland.
    </div>
    """, unsafe_allow_html=True)
elif correlation > 0.4:
    st.markdown(f"""
    <div class="insight-box">
    <b>📈 Jákvæð fylgni fundin</b><br>
    Fylgnistuðull: <b>{correlation:.3f}</b><br><br>
    Hærra sjávarhitastig tengist hærri afla.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="insight-box">
    <b>📊 Veik eða engin bein fylgni</b><br>
    Fylgnistuðull: <b>{correlation:.3f}</b><br><br>
    Sambandið milli sjávarhitastigs og afla er ekki einfalt línulegt samband.
    </div>
    """, unsafe_allow_html=True)

# Main visualization tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Tímaþróun",
    "🔍 Fylgnigreining",
    "🐟 Tegundir",
    "🗓️ Árstíðir",
    "📊 Ítarleg greining"
])

# TAB 1: Time series
with tab1:
    st.markdown("### 📈 Afli og Hitastig yfir Tíma")

    # Dual axis plot
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add catch data
    fig.add_trace(
        go.Scatter(
            x=filtered_monthly['date'],
            y=filtered_monthly['total_catch_tons'],
            name="Afli (tonn)",
            line=dict(color='#1f77b4', width=2),
            mode='lines'
        ),
        secondary_y=False
    )

    # Add temperature data
    fig.add_trace(
        go.Scatter(
            x=filtered_monthly['date'],
            y=filtered_monthly['temp_celsius'],
            name="Hitastig (°C)",
            line=dict(color='#d62728', width=2),
            mode='lines'
        ),
        secondary_y=True
    )

    # Update axes
    fig.update_xaxes(title_text="Dagsetning")
    fig.update_yaxes(title_text="Afli (tonn)", secondary_y=False, color='#1f77b4')
    fig.update_yaxes(title_text="Hitastig (°C)", secondary_y=True, color='#d62728')

    fig.update_layout(
        title="Mánaðarlegur afli og meðalhitastig sjávar",
        hovermode='x unified',
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # Yearly comparison
    st.markdown("### 📊 Árleg samanburður")

    yearly_filtered = yearly_df[(yearly_df['year'] >= year_range[0]) & (yearly_df['year'] <= year_range[1])]

    fig_yearly = make_subplots(specs=[[{"secondary_y": True}]])

    fig_yearly.add_trace(
        go.Bar(
            x=yearly_filtered['year'],
            y=yearly_filtered['total_catch_tons'],
            name="Árlegur afli (tonn)",
            marker_color='#1f77b4',
            opacity=0.7
        ),
        secondary_y=False
    )

    fig_yearly.add_trace(
        go.Scatter(
            x=yearly_filtered['year'],
            y=yearly_filtered['temp_celsius'],
            name="Meðalhitastig (°C)",
            line=dict(color='#d62728', width=3),
            mode='lines+markers',
            marker=dict(size=8)
        ),
        secondary_y=True
    )

    fig_yearly.update_xaxes(title_text="Ár")
    fig_yearly.update_yaxes(title_text="Afli (tonn)", secondary_y=False)
    fig_yearly.update_yaxes(title_text="Hitastig (°C)", secondary_y=True)
    fig_yearly.update_layout(title="Árleg þróun - Afli og Hitastig", height=500)

    st.plotly_chart(fig_yearly, use_container_width=True)

    # Year-over-year changes
    st.markdown("### 📉 Breytingar milli ára")

    yearly_filtered_changes = yearly_filtered[yearly_filtered['catch_change_pct'].notna()].copy()

    if len(yearly_filtered_changes) > 0:
        fig_changes = go.Figure()

        # Color bars based on positive/negative
        colors = ['green' if x > 0 else 'red' for x in yearly_filtered_changes['catch_change_pct']]

        fig_changes.add_trace(go.Bar(
            x=yearly_filtered_changes['year'],
            y=yearly_filtered_changes['catch_change_pct'],
            name="Breyting á afla (%)",
            marker_color=colors,
            text=yearly_filtered_changes['catch_change_pct'].round(1),
            texttemplate='%{text}%',
            textposition='outside'
        ))

        fig_changes.update_layout(
            title="Prósentubreyting á heildarafla milli ára",
            xaxis_title="Ár",
            yaxis_title="Breyting (%)",
            height=400,
            showlegend=False
        )

        st.plotly_chart(fig_changes, use_container_width=True)

# TAB 2: Correlation analysis
with tab2:
    st.markdown("### 🔍 Fylgnigreining")

    col1, col2 = st.columns([1, 1])

    with col1:
        # Scatter plot with regression line
        st.markdown("#### Dreifirit - Afli vs Hitastig")

        # Calculate regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            filtered_monthly['temp_celsius'],
            filtered_monthly['total_catch_tons']
        )

        fig_scatter = px.scatter(
            filtered_monthly,
            x='temp_celsius',
            y='total_catch_tons',
            color='year',
            title=f"Fylgni: {correlation:.3f} (p-value: {p_value:.4f})",
            labels={
                'temp_celsius': 'Meðalhitastig sjávar (°C)',
                'total_catch_tons': 'Heildarafli (tonn)',
                'year': 'Ár'
            },
            trendline="ols",
            height=500
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

        # Interpretation
        if p_value < 0.05:
            st.success(f"✓ Tölfræðilega marktækt samband (p < 0.05)")
        else:
            st.warning(f"⚠️ Samband ekki tölfræðilega marktækt (p = {p_value:.4f})")

    with col2:
        st.markdown("#### Tölfræðileg samantekt")

        # Display correlation matrix
        corr_matrix = filtered_monthly[['total_catch_tons', 'temp_celsius']].corr()

        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto='.3f',
            color_continuous_scale='RdBu_r',
            zmin=-1, zmax=1,
            title="Fylgni fylki"
        )

        st.plotly_chart(fig_heatmap, use_container_width=True)

        # Statistics
        st.markdown("**Tölfræði:**")
        st.write(f"- Fylgnistuðull (r): {correlation:.4f}")
        st.write(f"- R² gildi: {r_value**2:.4f}")
        st.write(f"- P-gildi: {p_value:.4f}")
        st.write(f"- Hallatala: {slope:.2f} tonn/°C")
        st.write(f"- Skurðpunktur: {intercept:.2f} tonn")

        st.markdown("---")
        st.markdown("**Túlkun:**")
        if correlation < -0.3:
            st.markdown(f"""
            Neikvæð fylgni ({correlation:.3f}) bendir til þess að:
            - Þegar hitastig hækkar um 1°C, þá lækkar afli að meðaltali um **{abs(slope):.0f} tonn**
            - Þetta gæti tengst breytingum á fiskstofnum, fæðuframboði eða hegðun fiska
            """)
        elif correlation > 0.3:
            st.markdown(f"""
            Jákvæð fylgni ({correlation:.3f}) bendir til þess að:
            - Þegar hitastig hækkar um 1°C, þá hækkar afli að meðaltali um **{slope:.0f} tonn**
            """)
        else:
            st.markdown("Veik fylgni bendir til flókins sambands sem þarf frekari rannsókn")

# TAB 3: Species analysis
with tab3:
    st.markdown("### 🐟 Greining eftir Fisktegundum")

    # Species selector
    available_species = filtered_species['species'].unique()
    selected_species_display = st.multiselect(
        "Veldu tegundir til að skoða:",
        available_species,
        default=list(available_species)
    )

    if selected_species_display:
        species_filtered = filtered_species[filtered_species['species'].isin(selected_species_display)]

        col1, col2 = st.columns([2, 1])

        with col1:
            # Time series by species
            fig_species = make_subplots(specs=[[{"secondary_y": True}]])

            for species in selected_species_display:
                species_data = species_filtered[species_filtered['species'] == species]

                fig_species.add_trace(
                    go.Scatter(
                        x=species_data['date'],
                        y=species_data['catch_tons'],
                        name=species,
                        mode='lines',
                        line=dict(width=2)
                    ),
                    secondary_y=False
                )

            # Add temperature
            fig_species.add_trace(
                go.Scatter(
                    x=filtered_monthly['date'],
                    y=filtered_monthly['temp_celsius'],
                    name="Hitastig",
                    line=dict(color='red', width=2, dash='dash'),
                    mode='lines'
                ),
                secondary_y=True
            )

            fig_species.update_xaxes(title_text="Dagsetning")
            fig_species.update_yaxes(title_text="Afli (tonn)", secondary_y=False)
            fig_species.update_yaxes(title_text="Hitastig (°C)", secondary_y=True)
            fig_species.update_layout(
                title="Afli eftir tegundum og hitastig",
                height=500,
                hovermode='x unified'
            )

            st.plotly_chart(fig_species, use_container_width=True)

        with col2:
            # Species correlations
            st.markdown("#### Fylgni eftir tegundum")

            species_corr_filtered = species_corr_df[species_corr_df['species'].isin(selected_species_display)]

            fig_corr_bar = px.bar(
                species_corr_filtered.sort_values('correlation'),
                x='correlation',
                y='species',
                orientation='h',
                color='correlation',
                color_continuous_scale='RdBu_r',
                color_continuous_midpoint=0,
                title="Fylgni við hitastig"
            )

            fig_corr_bar.update_layout(height=300)
            st.plotly_chart(fig_corr_bar, use_container_width=True)

            # Table
            st.markdown("#### Tölfræði eftir tegundum")
            species_stats = species_corr_filtered[['species', 'correlation', 'avg_catch_tons', 'total_catch_tons']].copy()
            species_stats.columns = ['Tegund', 'Fylgni', 'Meðalafli (tonn)', 'Heildarafli (tonn)']
            species_stats['Fylgni'] = species_stats['Fylgni'].round(3)
            species_stats['Meðalafli (tonn)'] = species_stats['Meðalafli (tonn)'].round(0)
            species_stats['Heildarafli (tonn)'] = species_stats['Heildarafli (tonn)'].round(0)

            st.dataframe(species_stats, use_container_width=True, hide_index=True)

    # Scatter plots by species
    st.markdown("#### Dreifirit eftir tegundum")

    if selected_species_display:
        for species in selected_species_display:
            species_data = species_filtered[species_filtered['species'] == species]

            if len(species_data) > 5:
                corr = species_data['catch_tons'].corr(species_data['temp_celsius'])

                fig = px.scatter(
                    species_data,
                    x='temp_celsius',
                    y='catch_tons',
                    color='year',
                    title=f"{species} - Fylgni: {corr:.3f}",
                    labels={
                        'temp_celsius': 'Hitastig (°C)',
                        'catch_tons': 'Afli (tonn)',
                        'year': 'Ár'
                    },
                    trendline="ols",
                    height=400
                )

                st.plotly_chart(fig, use_container_width=True)

# TAB 4: Seasonal patterns
with tab4:
    st.markdown("### 🗓️ Árstíðabundin Mynstur")

    # Calculate seasonal statistics
    filtered_monthly['season'] = filtered_monthly['month'].map({
        12: 'Vetur', 1: 'Vetur', 2: 'Vetur',
        3: 'Vor', 4: 'Vor', 5: 'Vor',
        6: 'Sumar', 7: 'Sumar', 8: 'Sumar',
        9: 'Haust', 10: 'Haust', 11: 'Haust'
    })

    col1, col2 = st.columns([1, 1])

    with col1:
        # Box plot by season
        fig_box = px.box(
            filtered_monthly,
            x='season',
            y='total_catch_tons',
            color='season',
            title="Afli eftir árstíðum",
            labels={'season': 'Árstíð', 'total_catch_tons': 'Afli (tonn)'},
            category_orders={'season': ['Vetur', 'Vor', 'Sumar', 'Haust']}
        )
        st.plotly_chart(fig_box, use_container_width=True)

        # Temperature by season
        fig_temp_box = px.box(
            filtered_monthly,
            x='season',
            y='temp_celsius',
            color='season',
            title="Hitastig eftir árstíðum",
            labels={'season': 'Árstíð', 'temp_celsius': 'Hitastig (°C)'},
            category_orders={'season': ['Vetur', 'Vor', 'Sumar', 'Haust']}
        )
        st.plotly_chart(fig_temp_box, use_container_width=True)

    with col2:
        # Seasonal correlations
        st.markdown("#### Fylgni eftir árstíðum")

        # Calculate seasonal correlations from filtered data
        seasonal_stats = []
        for season in ['Vetur', 'Vor', 'Sumar', 'Haust']:
            season_data = filtered_monthly[filtered_monthly['season'] == season]
            if len(season_data) > 5:
                corr = season_data['total_catch_tons'].corr(season_data['temp_celsius'])
                seasonal_stats.append({'season': season, 'correlation': corr})

        seasonal_df = pd.DataFrame(seasonal_stats)

        fig_seasonal = px.bar(
            seasonal_df,
            x='season',
            y='correlation',
            color='correlation',
            color_continuous_scale='RdBu_r',
            color_continuous_midpoint=0,
            title="Fylgnistuðull eftir árstíðum",
            labels={'season': 'Árstíð', 'correlation': 'Fylgni'},
            category_orders={'season': ['Vetur', 'Vor', 'Sumar', 'Haust']}
        )
        st.plotly_chart(fig_seasonal, use_container_width=True)

        # Seasonal summary table
        st.markdown("#### Samantekt eftir árstíðum")
        seasonal_summary = filtered_monthly.groupby('season').agg({
            'total_catch_tons': ['mean', 'sum'],
            'temp_celsius': ['mean', 'min', 'max']
        }).round(2)

        seasonal_summary.columns = ['Meðalafli', 'Heildarafli', 'Meðalhiti', 'Lágmarkshiti', 'Hámarkshiti']
        seasonal_summary = seasonal_summary.reindex(['Vetur', 'Vor', 'Sumar', 'Haust'])

        st.dataframe(seasonal_summary, use_container_width=True)

# TAB 5: Detailed analysis
with tab5:
    st.markdown("### 📊 Ítarleg Tölfræðileg Greining")

    # Rolling averages
    st.markdown("#### Hreyfanleg meðaltöl")

    window_size = st.slider("Veldu glugga fyrir hreyfanlegt meðaltal (mánuðir):", 3, 24, 12)

    filtered_monthly_sorted = filtered_monthly.sort_values('date')
    filtered_monthly_sorted['catch_ma'] = filtered_monthly_sorted['total_catch_tons'].rolling(window=window_size, center=True).mean()
    filtered_monthly_sorted['temp_ma'] = filtered_monthly_sorted['temp_celsius'].rolling(window=window_size, center=True).mean()

    fig_ma = make_subplots(specs=[[{"secondary_y": True}]])

    # Original data (lighter)
    fig_ma.add_trace(
        go.Scatter(
            x=filtered_monthly_sorted['date'],
            y=filtered_monthly_sorted['total_catch_tons'],
            name="Afli (upprunaleg)",
            line=dict(color='lightblue', width=1),
            mode='lines',
            opacity=0.3
        ),
        secondary_y=False
    )

    # Moving average
    fig_ma.add_trace(
        go.Scatter(
            x=filtered_monthly_sorted['date'],
            y=filtered_monthly_sorted['catch_ma'],
            name=f"Afli ({window_size} mán. MA)",
            line=dict(color='blue', width=3),
            mode='lines'
        ),
        secondary_y=False
    )

    # Temperature MA
    fig_ma.add_trace(
        go.Scatter(
            x=filtered_monthly_sorted['date'],
            y=filtered_monthly_sorted['temp_ma'],
            name=f"Hitastig ({window_size} mán. MA)",
            line=dict(color='red', width=3),
            mode='lines'
        ),
        secondary_y=True
    )

    fig_ma.update_xaxes(title_text="Dagsetning")
    fig_ma.update_yaxes(title_text="Afli (tonn)", secondary_y=False)
    fig_ma.update_yaxes(title_text="Hitastig (°C)", secondary_y=True)
    fig_ma.update_layout(title="Hreyfanleg meðaltöl - Afli og Hitastig", height=500)

    st.plotly_chart(fig_ma, use_container_width=True)

    # Anomalies
    st.markdown("#### Frávik frá meðaltali")

    mean_catch = filtered_monthly['total_catch_tons'].mean()
    mean_temp = filtered_monthly['temp_celsius'].mean()

    filtered_monthly['catch_anomaly'] = filtered_monthly['total_catch_tons'] - mean_catch
    filtered_monthly['temp_anomaly'] = filtered_monthly['temp_celsius'] - mean_temp

    fig_anom = go.Figure()

    colors = ['green' if x > 0 else 'red' for x in filtered_monthly['catch_anomaly']]

    fig_anom.add_trace(go.Bar(
        x=filtered_monthly['date'],
        y=filtered_monthly['catch_anomaly'],
        name="Frávik í afla",
        marker_color=colors,
        opacity=0.7
    ))

    fig_anom.update_layout(
        title="Frávik frá meðalafla",
        xaxis_title="Dagsetning",
        yaxis_title="Frávik (tonn)",
        height=400
    )

    st.plotly_chart(fig_anom, use_container_width=True)

    # Statistical summary
    st.markdown("#### Tölfræðileg samantekt")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Afli:**")
        catch_stats = filtered_monthly['total_catch_tons'].describe()
        st.dataframe(catch_stats.to_frame('Gildi').round(2))

    with col2:
        st.markdown("**Hitastig:**")
        temp_stats = filtered_monthly['temp_celsius'].describe()
        st.dataframe(temp_stats.to_frame('Gildi').round(2))

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><b>Sjávarútvegs DataDemo</b></p>
    <p>Gögn: Hagstofa Íslands (afli) & Copernicus Marine Service (sjávarhitastig)</p>
    <p>Tímabil: 2010-2025 | Uppfært: """ + datetime.now().strftime("%Y-%m-%d") + """</p>
</div>
""", unsafe_allow_html=True)

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📚 Um verkefnið

Þetta verkfæri greinir samband milli aflafars og sjávarhitastigs við Ísland.

**Helstu niðurstöður:**
- Sterk neikvæð fylgni (-0.55) milli hitastigs og afla
- Þegar hitastig hækkar, lækkar afli
- Þetta tengist líklega breytingum á fiskstofnum og fæðuframboði

**Lykiltegundir:**
- Þorskur (Cod)
- Ýsa (Haddock)

**Gagnheimildir:**
- Aflagögn: Hagstofa Íslands
- Sjávarhitastig: Copernicus Marine Service (GLORYS12V1)

**Aðferðir:**
- Rúmleg og tímaleg samlögun
- Fylgnigreining
- Tölfræðileg marktektarpróf
""")

st.sidebar.markdown("---")
st.sidebar.info("💡 Þessi greining styður umræðu um viðnámsþrótt íslensks sjávarútvegs í ljósi loftslagsbreytinga.")
