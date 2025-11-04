#!/usr/bin/env python3
"""
Process catch data for all species from Hagstofa Íslands
Includes: Ufsi (Haddock), Þorskur (Cod), Síld (Herring), Loðna (Capelin),
          Steinbítur (Catfish), Hlýri (Halibut), Úthafskarfi (Redfish)
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "Afli eftir fisktegundum"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "afli_eftir_fisktegundum"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Species mapping (Icelandic to English)
SPECIES_MAP = {
    'Ufsi': 'Haddock',
    'Þorskur': 'Cod',  # We need to check if this exists
    'Síld': 'Herring',
    'Loðna': 'Capelin',
    'Steinbítur': 'Catfish',
    'Hlýri': 'Halibut',
    'Úthafskarfi': 'Redfish'
}

def process_catch_data():
    """Process the new catch data file with all species"""

    # Read the CSV file
    input_file = RAW_DATA_DIR / "SJA01101_20251104-162732.csv"

    print(f"\n📊 Processing All Species Catch Data")
    print(f"=" * 60)
    print(f"Input file: {input_file}")

    # Read with semicolon delimiter
    df = pd.read_csv(input_file, sep=';', encoding='utf-8')

    print(f"Original shape: {df.shape}")
    print(f"\nColumns: {list(df.columns[:5])}...")
    print(f"Species found: {df['Fisktegund'].unique().tolist()}")

    # Filter to complete years only (2010-2024)
    # The columns are: Fisktegund, Löndunarhöfn, 2024 Alls, 2024 janúar, etc.

    # Get all month columns for 2010-2024
    year_cols = []
    month_cols = []

    for year in range(2010, 2025):
        year_cols.append(f"{year} Alls")
        for month_name in ['janúar', 'febrúar', 'mars', 'apríl', 'maí', 'júní',
                           'júlí', 'ágúst', 'september', 'október', 'nóvember', 'desember']:
            month_cols.append(f"{year} {month_name}")

    # Aggregate by species (sum across all ports)
    print(f"\n📍 Aggregating catch by species...")

    species_data = []

    for species in df['Fisktegund'].unique():
        species_df = df[df['Fisktegund'] == species].copy()

        # Sum across all ports
        species_total = {}
        species_total['Fisktegund'] = species
        species_total['English_Name'] = SPECIES_MAP.get(species, species)

        # Sum annual totals
        for year in range(2010, 2025):
            col = f"{year} Alls"
            if col in species_df.columns:
                # Replace '..' with 0
                values = species_df[col].replace('..', '0').astype(str).str.replace(' ', '').astype(float)
                species_total[year] = values.sum()

        species_data.append(species_total)

    # Create annual summary
    annual_df = pd.DataFrame(species_data)

    print(f"\n✅ Annual summary shape: {annual_df.shape}")
    print(annual_df)

    # Save annual summary
    annual_file = PROCESSED_DIR / "all_species_annual.csv"
    annual_df.to_csv(annual_file, index=False)
    print(f"\n💾 Saved: {annual_file}")

    # Now create monthly time series
    print(f"\n📅 Creating monthly time series...")

    monthly_records = []

    month_mapping = {
        'janúar': 1, 'febrúar': 2, 'mars': 3, 'apríl': 4,
        'maí': 5, 'júní': 6, 'júlí': 7, 'ágúst': 8,
        'september': 9, 'október': 10, 'nóvember': 11, 'desember': 12
    }

    for species in df['Fisktegund'].unique():
        species_df = df[df['Fisktegund'] == species].copy()

        for year in range(2010, 2025):
            for month_name, month_num in month_mapping.items():
                col = f"{year} {month_name}"
                if col in species_df.columns:
                    # Replace '..' with 0
                    values = species_df[col].replace('..', '0').astype(str).str.replace(' ', '').astype(float)
                    total = values.sum()

                    monthly_records.append({
                        'date': f"{year}-{month_num:02d}-01",
                        'year': year,
                        'month': month_num,
                        'species_icelandic': species,
                        'species_english': SPECIES_MAP.get(species, species),
                        'catch_kg': total,
                        'catch_tons': total / 1000  # Convert kg to tons
                    })

    # Create monthly DataFrame
    monthly_df = pd.DataFrame(monthly_records)
    monthly_df['date'] = pd.to_datetime(monthly_df['date'])
    monthly_df = monthly_df.sort_values(['species_icelandic', 'date'])

    # Filter to complete years only (exclude 2025)
    monthly_df = monthly_df[monthly_df['year'] <= 2024]

    print(f"\n✅ Monthly data shape: {monthly_df.shape}")
    print(f"Date range: {monthly_df['date'].min()} to {monthly_df['date'].max()}")
    print(f"Total catch (all species, 2010-2024): {monthly_df['catch_tons'].sum():,.0f} tons")

    # Save monthly time series
    monthly_file = PROCESSED_DIR / "all_species_monthly.csv"
    monthly_df.to_csv(monthly_file, index=False)
    print(f"\n💾 Saved: {monthly_file}")

    # Create summary by species
    print(f"\n📊 Catch Summary by Species (2010-2024):")
    print("=" * 60)
    species_summary = monthly_df.groupby('species_icelandic').agg({
        'catch_tons': ['sum', 'mean', 'std']
    }).round(0)
    species_summary.columns = ['Total (tons)', 'Mean Monthly (tons)', 'Std Dev']
    print(species_summary.sort_values('Total (tons)', ascending=False))

    return monthly_df, annual_df

def merge_with_temperatures():
    """Merge catch data with all three temperature datasets"""

    print(f"\n🌡️  Merging with Temperature Data")
    print(f"=" * 60)

    # Load monthly catch data
    catch_file = PROCESSED_DIR / "all_species_monthly.csv"
    catch_df = pd.read_csv(catch_file, parse_dates=['date'])

    # Load temperature data
    temp_comp_file = PROJECT_ROOT / "data" / "processed" / "comparison" / "catch_temperature_comprehensive.csv"
    temp_df = pd.read_csv(temp_comp_file, parse_dates=['date'])

    # Select temperature columns
    temp_cols = ['date', 'year', 'month', 'temp_copernicus', 'temp_grimsey', 'temp_vestmann', 'temp_three_station_avg']
    temp_df = temp_df[temp_cols]

    # Merge
    merged_df = catch_df.merge(temp_df, on=['year', 'month'], how='left', suffixes=('', '_temp'))

    # Drop duplicate date column if exists
    if 'date_temp' in merged_df.columns:
        merged_df = merged_df.drop('date_temp', axis=1)

    print(f"✅ Merged data shape: {merged_df.shape}")
    print(f"Columns: {merged_df.columns.tolist()}")

    # Save comprehensive dataset
    output_file = PROJECT_ROOT / "data" / "processed" / "comparison" / "all_species_temperature_monthly.csv"
    merged_df.to_csv(output_file, index=False)
    print(f"\n💾 Saved: {output_file}")

    # Calculate correlations by species
    print(f"\n📈 Correlation Analysis by Species:")
    print("=" * 60)

    correlations = []
    for species in merged_df['species_icelandic'].unique():
        species_df = merged_df[merged_df['species_icelandic'] == species].copy()
        species_df = species_df.dropna(subset=['catch_tons', 'temp_copernicus'])

        if len(species_df) > 10:  # Need enough data points
            corr = species_df['catch_tons'].corr(species_df['temp_copernicus'])
            correlations.append({
                'Species (Icelandic)': species,
                'Species (English)': species_df['species_english'].iloc[0],
                'Correlation': corr,
                'N': len(species_df)
            })

    corr_df = pd.DataFrame(correlations).sort_values('Correlation')
    print(corr_df.to_string(index=False))

    return merged_df

if __name__ == "__main__":
    # Process catch data
    monthly_df, annual_df = process_catch_data()

    # Merge with temperatures
    merged_df = merge_with_temperatures()

    print(f"\n✅ ALL PROCESSING COMPLETE!")
    print(f"=" * 60)
    print(f"Output files:")
    print(f"  - data/processed/afli_eftir_fisktegundum/all_species_monthly.csv")
    print(f"  - data/processed/afli_eftir_fisktegundum/all_species_annual.csv")
    print(f"  - data/processed/comparison/all_species_temperature_monthly.csv")
