#!/usr/bin/env python3
"""
Comprehensive processing of ALL fish species catch data
Combines two data sources:
1. Afli_eftir_fisktegundum_FULL_CSV.csv - Has Þorskur (Cod) and Ýsa (Haddock)
2. SJA01101_20251104-162732.csv - Has Ufsi (Saithe), Síld, Loðna, etc.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "Afli eftir fisktegundum"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "afli_eftir_fisktegundum"
COMPARISON_DIR = PROJECT_ROOT / "data" / "processed" / "comparison"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Complete species mapping (Icelandic to English)
SPECIES_MAP = {
    'Þorskur': 'Cod',
    'Ýsa': 'Haddock',
    'Ufsi': 'Saithe',  # NOT Haddock! Different species
    'Síld': 'Herring',
    'Loðna': 'Capelin',
    'Steinbítur': 'Catfish',
    'Hlýri': 'Halibut',
    'Úthafskarfi': 'Redfish'
}

def process_full_csv():
    """Process the FULL CSV with Þorskur and Ýsa"""

    print(f"\n📊 Processing FULL CSV (Þorskur & Ýsa)")
    print(f"=" * 60)

    input_file = RAW_DATA_DIR / "Afli_eftir_fisktegundum_FULL_CSV.csv"

    # Read the file - it has a complex header
    df = pd.read_csv(input_file, sep=';', encoding='utf-8', skiprows=3)

    print(f"Shape: {df.shape}")
    print(f"Columns (first 5): {df.columns[:5].tolist()}")

    # First column is species, second is "Allar löndunartegundir"
    df.columns = ['Fisktegund', 'Port'] + df.columns[2:].tolist()

    # Filter to "Allar löndunartegundir" (all ports)
    df = df[df['Port'] == 'Allar löndunartegundir'].copy()

    print(f"Species found: {df['Fisktegund'].unique().tolist()}")

    # Get month columns for 2010-2024
    month_mapping = {
        'janúar': 1, 'febrúar': 2, 'mars': 3, 'apríl': 4,
        'maí': 5, 'júní': 6, 'júlí': 7, 'ágúst': 8,
        'september': 9, 'október': 10, 'nóvember': 11, 'desember': 12
    }

    monthly_records = []

    for species in df['Fisktegund'].unique():
        if species not in ['Þorskur', 'Ýsa']:
            continue  # Only process these two from this file

        species_row = df[df['Fisktegund'] == species].iloc[0]

        # The columns are organized as: 2025 months, 2024 months, etc.
        # We need to map column positions to years and months
        col_idx = 2  # Start after Fisktegund and Port

        for year in range(2025, 2009, -1):  # 2025 down to 2010
            for month_name, month_num in month_mapping.items():
                if col_idx < len(df.columns):
                    col_name = df.columns[col_idx]
                    value = species_row.iloc[col_idx]

                    # Convert to numeric, handle '..' as NaN
                    if pd.isna(value) or value == '..' or value == '':
                        value_numeric = 0
                    else:
                        value_numeric = float(str(value).replace(' ', ''))

                    monthly_records.append({
                        'date': f"{year}-{month_num:02d}-01",
                        'year': year,
                        'month': month_num,
                        'species_icelandic': species,
                        'species_english': SPECIES_MAP.get(species, species),
                        'catch_kg': value_numeric,
                        'catch_tons': value_numeric / 1000
                    })

                    col_idx += 1

    # Create DataFrame
    monthly_df = pd.DataFrame(monthly_records)
    monthly_df['date'] = pd.to_datetime(monthly_df['date'])

    # Filter to 2010-2024 only
    monthly_df = monthly_df[(monthly_df['year'] >= 2010) & (monthly_df['year'] <= 2024)]
    monthly_df = monthly_df.sort_values(['species_icelandic', 'date'])

    print(f"\n✅ Processed {len(monthly_df)} monthly records")
    print(f"Date range: {monthly_df['date'].min()} to {monthly_df['date'].max()}")

    return monthly_df

def process_new_csv():
    """Process the new CSV with other species"""

    print(f"\n📊 Processing New CSV (Ufsi, Síld, Loðna, etc.)")
    print(f"=" * 60)

    input_file = RAW_DATA_DIR / "SJA01101_20251104-162732.csv"

    df = pd.read_csv(input_file, sep=';', encoding='utf-8')

    print(f"Shape: {df.shape}")
    print(f"Species found: {df['Fisktegund'].unique().tolist()}")

    month_mapping = {
        'janúar': 1, 'febrúar': 2, 'mars': 3, 'apríl': 4,
        'maí': 5, 'júní': 6, 'júlí': 7, 'ágúst': 8,
        'september': 9, 'október': 10, 'nóvember': 11, 'desember': 12
    }

    monthly_records = []

    for species in df['Fisktegund'].unique():
        species_df = df[df['Fisktegund'] == species].copy()

        for year in range(2010, 2025):
            for month_name, month_num in month_mapping.items():
                col = f"{year} {month_name}"
                if col in species_df.columns:
                    # Sum across all ports
                    values = species_df[col].replace('..', '0').astype(str).str.replace(' ', '').astype(float)
                    total = values.sum()

                    monthly_records.append({
                        'date': f"{year}-{month_num:02d}-01",
                        'year': year,
                        'month': month_num,
                        'species_icelandic': species,
                        'species_english': SPECIES_MAP.get(species, species),
                        'catch_kg': total,
                        'catch_tons': total / 1000
                    })

    # Create DataFrame
    monthly_df = pd.DataFrame(monthly_records)
    monthly_df['date'] = pd.to_datetime(monthly_df['date'])

    # Filter to 2010-2024 only
    monthly_df = monthly_df[monthly_df['year'] <= 2024]
    monthly_df = monthly_df.sort_values(['species_icelandic', 'date'])

    print(f"\n✅ Processed {len(monthly_df)} monthly records")
    print(f"Date range: {monthly_df['date'].min()} to {monthly_df['date'].max()}")

    return monthly_df

def combine_and_save():
    """Combine both datasets and save"""

    print(f"\n🔄 Combining All Species Data")
    print(f"=" * 60)

    # Process both sources
    full_df = process_full_csv()  # Þorskur, Ýsa
    new_df = process_new_csv()    # Ufsi, Síld, Loðna, etc.

    # Combine
    combined_df = pd.concat([full_df, new_df], ignore_index=True)
    combined_df = combined_df.sort_values(['species_icelandic', 'date'])

    print(f"\n✅ Combined data shape: {combined_df.shape}")
    print(f"Total species: {len(combined_df['species_icelandic'].unique())}")
    print(f"Species: {sorted(combined_df['species_icelandic'].unique())}")

    # Save
    output_file = PROCESSED_DIR / "all_species_monthly_comprehensive.csv"
    combined_df.to_csv(output_file, index=False)
    print(f"\n💾 Saved: {output_file}")

    # Summary by species
    print(f"\n📊 Catch Summary by Species (2010-2024):")
    print("=" * 60)
    species_summary = combined_df.groupby('species_icelandic').agg({
        'catch_tons': ['sum', 'mean', 'std']
    }).round(0)
    species_summary.columns = ['Total (tons)', 'Mean Monthly (tons)', 'Std Dev']
    print(species_summary.sort_values('Total (tons)', ascending=False))

    return combined_df

def merge_with_temperatures(catch_df):
    """Merge catch data with all three temperature datasets"""

    print(f"\n🌡️  Merging with Temperature Data")
    print(f"=" * 60)

    # Load temperature data
    temp_file = COMPARISON_DIR / "catch_temperature_comprehensive.csv"
    temp_df = pd.read_csv(temp_file, parse_dates=['date'])

    # Select temperature columns
    temp_cols = ['date', 'year', 'month', 'temp_copernicus', 'temp_grimsey', 'temp_vestmann', 'temp_three_station_avg']
    temp_df = temp_df[temp_cols].drop_duplicates()

    # Merge
    merged_df = catch_df.merge(temp_df, on=['year', 'month'], how='left', suffixes=('', '_temp'))

    # Drop duplicate date column if exists
    if 'date_temp' in merged_df.columns:
        merged_df = merged_df.drop('date_temp', axis=1)

    print(f"✅ Merged data shape: {merged_df.shape}")

    # Save comprehensive dataset
    output_file = COMPARISON_DIR / "all_species_temperature_monthly.csv"
    merged_df.to_csv(output_file, index=False)
    print(f"\n💾 Saved: {output_file}")

    # Calculate correlations by species
    print(f"\n📈 Correlation Analysis by Species (vs Copernicus):")
    print("=" * 60)

    correlations = []
    for species in merged_df['species_icelandic'].unique():
        species_df = merged_df[merged_df['species_icelandic'] == species].copy()
        species_df = species_df.dropna(subset=['catch_tons', 'temp_copernicus'])

        if len(species_df) > 10:
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
    # Combine both data sources
    combined_catch_df = combine_and_save()

    # Merge with temperatures
    final_df = merge_with_temperatures(combined_catch_df)

    print(f"\n✅ ALL PROCESSING COMPLETE!")
    print(f"=" * 60)
    print(f"Output files:")
    print(f"  - data/processed/afli_eftir_fisktegundum/all_species_monthly_comprehensive.csv")
    print(f"  - data/processed/comparison/all_species_temperature_monthly.csv")
    print(f"\n🐟 Species included:")
    for ice, eng in sorted(SPECIES_MAP.items()):
        print(f"  - {ice} ({eng})")
