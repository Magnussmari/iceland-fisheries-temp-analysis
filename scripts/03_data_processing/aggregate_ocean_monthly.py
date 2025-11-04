#!/usr/bin/env python3
"""
Aggregate daily ocean data to monthly means.

Takes the daily spatially-averaged ocean data and aggregates to monthly
to match the temporal resolution of the catch data.

Input:  data/processed/oceantemp/Ocean_temp_*_DAILY.csv
Output: data/processed/oceantemp/Ocean_temp_*_MONTHLY.csv

Author: Claude Code
Date: 2025-11-04
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Project paths
project_root = Path(__file__).resolve().parent.parent
data_dir = project_root / "data"
input_dir = data_dir / "processed" / "oceantemp"
output_dir = data_dir / "processed" / "oceantemp"


def find_daily_file():
    """Find the most recent daily ocean data file."""
    daily_files = list(input_dir.glob("Ocean_temp_*_DAILY.csv"))

    if not daily_files:
        print("❌ No daily ocean data files found in:")
        print(f"   {input_dir}")
        print("\n💡 Run aggregate_ocean_spatial.py first to create daily data.")
        sys.exit(1)

    # Use most recent file
    daily_file = sorted(daily_files)[-1]
    return daily_file


def aggregate_monthly(daily_file):
    """Aggregate daily data to monthly means."""
    print("=" * 80)
    print("MONTHLY AGGREGATION - OCEAN DATA")
    print("=" * 80)
    print(f"\n📂 Input file:")
    print(f"   {daily_file.name}")

    # Load daily data
    print(f"\n⏳ Loading daily data...")
    df = pd.read_csv(daily_file, parse_dates=['Dags'])

    print(f"\n✓ Data loaded!")
    print(f"   Total days: {len(df)}")
    print(f"   Date range: {df['Dags'].min().date()} to {df['Dags'].max().date()}")
    print(f"   Variables: {', '.join([c for c in df.columns if c != 'Dags'])}")

    # Aggregate to monthly
    print(f"\n⚙️ Aggregating to monthly means...")
    print("   Using month-start dates to match catch data...")

    # Set date as index
    df = df.set_index('Dags')

    # Resample to monthly, using month start ('MS')
    # This matches the catch data which uses first day of month
    monthly = df.resample('MS').mean()

    # Reset index
    monthly = monthly.reset_index()

    # Round numeric values to reasonable precision
    numeric_cols = monthly.select_dtypes(include=[np.number]).columns
    monthly[numeric_cols] = monthly[numeric_cols].round(4)

    print(f"\n✓ Aggregation complete!")
    print(f"\n📈 Result summary:")
    print(f"   Total months: {len(monthly)}")
    print(f"   Date range: {monthly['Dags'].min().date()} to {monthly['Dags'].max().date()}")

    # Show statistics
    print(f"\n📊 Monthly ocean variable statistics:")
    stats = monthly[numeric_cols].describe()
    print(stats.to_string())

    # Show first few months as example
    print(f"\n📋 First 5 months:")
    print(monthly.head().to_string(index=False))

    return monthly


def save_monthly_csv(df, daily_file):
    """Save aggregated monthly data to CSV."""
    # Create output filename
    # Input: Ocean_temp_20100101_20250916_DAILY.csv
    # Output: Ocean_temp_20100101_20250916_MONTHLY.csv
    output_name = daily_file.name.replace('_DAILY.csv', '_MONTHLY.csv')
    output_file = output_dir / output_name

    print(f"\n💾 Saving to CSV:")
    print(f"   {output_file}")

    df.to_csv(output_file, index=False)

    # Check output size
    output_size_kb = output_file.stat().st_size / 1024
    print(f"   Size: {output_size_kb:.1f} KB")

    print(f"\n✅ Monthly aggregated data saved successfully!")

    return output_file


def main():
    """Main execution."""
    print("\n" + "=" * 80)
    print("OCEAN DATA - MONTHLY AGGREGATION")
    print("=" * 80)

    # Find input file
    daily_file = find_daily_file()

    # Aggregate to monthly
    df = aggregate_monthly(daily_file)

    # Save to CSV
    output_file = save_monthly_csv(df, daily_file)

    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("\n1. View the monthly data:")
    print(f"   head {output_file}")

    print("\n2. Compare with catch data:")
    print("   python scripts/prepare_comparison_datasets.py")

    print("\n3. Visualize in Streamlit:")
    print("   streamlit run streamlit_app.py")

    print("\n" + "=" * 80)
    print("ABOUT MONTHLY AGGREGATION")
    print("=" * 80)
    print("""
The monthly data uses 'Month Start' dates (1st of each month) to match
the catch data format. This allows direct merging on the 'Dags' column.

For example:
  - Daily data: 2018-01-01, 2018-01-02, ..., 2018-01-31
  - Monthly data: 2018-01-01 (average of all January days)

This matches the catch data which reports monthly totals on the 1st of each month.
    """)

    print("\n" + "=" * 80)
    print(f"✓ Monthly aggregation complete!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
