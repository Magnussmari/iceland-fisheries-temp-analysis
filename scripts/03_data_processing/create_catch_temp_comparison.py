#!/usr/bin/env python3
"""
Create Catch vs Ocean Temperature Comparison Dataset
====================================================
This script processes the NetCDF ocean temperature data and catch data
to create temporal aligned datasets for comparison and correlation analysis.

Key steps:
1. Load and aggregate ocean temperature data (spatial average)
2. Load catch data
3. Align temporally (monthly aggregation)
4. Calculate correlations and identify patterns
5. Save processed datasets for visualization
"""

import xarray as xr
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_OCEAN_PATH = BASE_DIR / "data/raw/Copernicus/fetched/copernicus_iceland_ocean_20100101_20250930.nc"
CATCH_PATH = BASE_DIR / "data/processed/afli_eftir_fisktegundum/Catch_data.csv"
OUTPUT_DIR = BASE_DIR / "data/processed/comparison"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("CATCH vs OCEAN TEMPERATURE COMPARISON ANALYSIS")
print("=" * 80)

# ============================================================================
# STEP 1: Process Ocean Temperature Data
# ============================================================================
print("\n[1/5] Loading ocean temperature NetCDF data...")
ds = xr.open_dataset(RAW_OCEAN_PATH)
print(f"  ✓ Loaded: {RAW_OCEAN_PATH.name}")
print(f"  - Time range: {pd.to_datetime(ds.time.values[0]).date()} to {pd.to_datetime(ds.time.values[-1]).date()}")
print(f"  - Dimensions: {dict(ds.dims)}")

# Extract surface temperature (depth=0) and calculate spatial mean
print("\n[2/5] Processing surface temperature (depth=0)...")
surface_temp = ds['thetao'].sel(depth=0.494, method='nearest')  # Surface layer
print(f"  - Surface layer depth: {ds.depth.values[0]:.3f} m")

# Calculate Iceland-wide spatial mean for each day
print("  - Calculating spatial mean over Iceland EEZ...")
temp_daily_mean = surface_temp.mean(dim=['latitude', 'longitude'])
temp_df = temp_daily_mean.to_dataframe(name='surface_temp_mean').reset_index()
temp_df = temp_df[['time', 'surface_temp_mean']]
temp_df['date'] = pd.to_datetime(temp_df['time']).dt.date
print(f"  ✓ Created daily temperature dataset: {len(temp_df)} days")

# Aggregate to monthly
print("  - Aggregating to monthly averages...")
temp_df['year'] = pd.to_datetime(temp_df['time']).dt.year
temp_df['month'] = pd.to_datetime(temp_df['time']).dt.month
temp_monthly = temp_df.groupby(['year', 'month']).agg({
    'surface_temp_mean': 'mean'
}).reset_index()
temp_monthly.columns = ['year', 'month', 'temp_celsius']
print(f"  ✓ Monthly temperature data: {len(temp_monthly)} months")

# ============================================================================
# STEP 2: Process Catch Data
# ============================================================================
print("\n[3/5] Loading and processing catch data...")
catch_df = pd.read_csv(CATCH_PATH, encoding='utf-8-sig')
print(f"  ✓ Loaded: {len(catch_df)} records")

# Month name mapping
month_map = {
    'janúar': 1, 'febrúar': 2, 'mars': 3, 'apríl': 4,
    'maí': 5, 'júní': 6, 'júlí': 7, 'ágúst': 8,
    'september': 9, 'október': 10, 'nóvember': 11, 'desember': 12
}
catch_df['month'] = catch_df['Mánuður'].map(month_map)
catch_df['year'] = catch_df['Ár']

# Aggregate by year, month, and species
print("  - Aggregating catch by year, month, and species...")
catch_monthly = catch_df.groupby(['year', 'month', 'Fisktegund']).agg({
    'Afli': 'sum'
}).reset_index()
catch_monthly.columns = ['year', 'month', 'species', 'catch_kg']
print(f"  ✓ Monthly catch by species: {len(catch_monthly)} records")

# Total catch per month (all species)
catch_total_monthly = catch_df.groupby(['year', 'month']).agg({
    'Afli': 'sum'
}).reset_index()
catch_total_monthly.columns = ['year', 'month', 'total_catch_kg']
print(f"  ✓ Total monthly catch: {len(catch_total_monthly)} months")

# ============================================================================
# STEP 3: Merge Datasets
# ============================================================================
print("\n[4/5] Merging catch and temperature data...")

# Merge total catch with temperature
comparison_df = pd.merge(
    catch_total_monthly,
    temp_monthly,
    on=['year', 'month'],
    how='inner'
)
comparison_df['date'] = pd.to_datetime(comparison_df[['year', 'month']].assign(day=1))
comparison_df['total_catch_tons'] = comparison_df['total_catch_kg'] / 1000

# FILTER TO COMPLETE YEARS ONLY (2010-2024)
comparison_df = comparison_df[comparison_df['year'] <= 2024]
print(f"  ✓ Merged dataset (complete years 2010-2024): {len(comparison_df)} months")

# Merge catch by species with temperature
comparison_species_df = pd.merge(
    catch_monthly,
    temp_monthly,
    on=['year', 'month'],
    how='inner'
)
comparison_species_df['date'] = pd.to_datetime(comparison_species_df[['year', 'month']].assign(day=1))
comparison_species_df['catch_tons'] = comparison_species_df['catch_kg'] / 1000

# FILTER TO COMPLETE YEARS ONLY (2010-2024)
comparison_species_df = comparison_species_df[comparison_species_df['year'] <= 2024]
print(f"  ✓ Species-level merged dataset (complete years 2010-2024): {len(comparison_species_df)} records")

# ============================================================================
# STEP 4: Calculate Key Metrics and Correlations
# ============================================================================
print("\n[5/5] Calculating correlations and trends...")

# Overall correlation
overall_corr = comparison_df['total_catch_tons'].corr(comparison_df['temp_celsius'])
print(f"\n  Overall Correlation (Total Catch vs Temperature): {overall_corr:.4f}")

# Species-specific correlations
print("\n  Species-specific correlations:")
species_correlations = []
for species in comparison_species_df['species'].unique():
    species_data = comparison_species_df[comparison_species_df['species'] == species]
    if len(species_data) > 10:  # Only if enough data points
        corr = species_data['catch_tons'].corr(species_data['temp_celsius'])
        species_correlations.append({
            'species': species,
            'correlation': corr,
            'n_months': len(species_data),
            'avg_catch_tons': species_data['catch_tons'].mean(),
            'total_catch_tons': species_data['catch_tons'].sum()
        })
        print(f"    {species}: {corr:+.4f} (n={len(species_data)})")

species_corr_df = pd.DataFrame(species_correlations).sort_values('correlation')

# Year-over-year changes
print("\n  Year-over-year analysis:")
yearly_summary = comparison_df.groupby('year').agg({
    'total_catch_tons': 'sum',
    'temp_celsius': 'mean'
}).reset_index()
yearly_summary['catch_change_pct'] = yearly_summary['total_catch_tons'].pct_change() * 100
yearly_summary['temp_change'] = yearly_summary['temp_celsius'].diff()

print("\n  Notable changes (catch vs temperature):")
for idx, row in yearly_summary.iterrows():
    if pd.notna(row['catch_change_pct']) and pd.notna(row['temp_change']):
        if abs(row['catch_change_pct']) > 10:  # Significant catch change
            print(f"    {int(row['year'])}: Catch {row['catch_change_pct']:+.1f}%, Temp {row['temp_change']:+.2f}°C")

# Seasonal patterns
comparison_df['season'] = comparison_df['month'].map({
    12: 'Winter', 1: 'Winter', 2: 'Winter',
    3: 'Spring', 4: 'Spring', 5: 'Spring',
    6: 'Summer', 7: 'Summer', 8: 'Summer',
    9: 'Fall', 10: 'Fall', 11: 'Fall'
})

seasonal_corr = comparison_df.groupby('season').apply(
    lambda x: x['total_catch_tons'].corr(x['temp_celsius'])
).reset_index()
seasonal_corr.columns = ['season', 'correlation']

print("\n  Seasonal correlations:")
for _, row in seasonal_corr.iterrows():
    print(f"    {row['season']}: {row['correlation']:+.4f}")

# ============================================================================
# STEP 5: Save Processed Datasets
# ============================================================================
print("\n" + "=" * 80)
print("SAVING PROCESSED DATASETS")
print("=" * 80)

# Save main comparison dataset
output_file = OUTPUT_DIR / "catch_temperature_monthly.csv"
comparison_df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"✓ Saved: {output_file}")

# Save species-level comparison
output_file_species = OUTPUT_DIR / "catch_temperature_by_species_monthly.csv"
comparison_species_df.to_csv(output_file_species, index=False, encoding='utf-8-sig')
print(f"✓ Saved: {output_file_species}")

# Save yearly summary
output_file_yearly = OUTPUT_DIR / "catch_temperature_yearly.csv"
yearly_summary.to_csv(output_file_yearly, index=False, encoding='utf-8-sig')
print(f"✓ Saved: {output_file_yearly}")

# Save species correlations
output_file_corr = OUTPUT_DIR / "species_temperature_correlations.csv"
species_corr_df.to_csv(output_file_corr, index=False, encoding='utf-8-sig')
print(f"✓ Saved: {output_file_corr}")

# Save seasonal correlations
output_file_seasonal = OUTPUT_DIR / "seasonal_correlations.csv"
seasonal_corr.to_csv(output_file_seasonal, index=False, encoding='utf-8-sig')
print(f"✓ Saved: {output_file_seasonal}")

# Save daily temperature data for detailed analysis
output_file_temp_daily = OUTPUT_DIR / "iceland_surface_temp_daily.csv"
temp_df[['date', 'surface_temp_mean']].to_csv(output_file_temp_daily, index=False, encoding='utf-8-sig')
print(f"✓ Saved: {output_file_temp_daily}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print(f"\n✓ COMPLETE YEARS ONLY: {comparison_df['year'].min()}-{comparison_df['year'].max()}")
print(f"✓ Months analyzed: {len(comparison_df)} months (15 complete years)")
print(f"✓ Total catch analyzed: {comparison_df['total_catch_tons'].sum():,.0f} tons")
print(f"✓ Temperature range: {comparison_df['temp_celsius'].min():.2f}°C to {comparison_df['temp_celsius'].max():.2f}°C")
print(f"✓ Average monthly catch: {comparison_df['total_catch_tons'].mean():,.0f} tons")
print(f"✓ Average temperature: {comparison_df['temp_celsius'].mean():.2f}°C")
print(f"\n🎯 Datasets ready for visualization in Streamlit app!")
