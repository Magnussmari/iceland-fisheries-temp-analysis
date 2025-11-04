#!/usr/bin/env python3
"""
Aggregate Copernicus ocean data spatially to daily Iceland averages.

Takes the multi-year NetCDF file and creates a daily CSV with spatial averages
across all grid points in Iceland waters.

Input:  data/raw/Copernicus/fetched/copernicus_iceland_ocean_*.nc
Output: data/processed/oceantemp/Ocean_temp_*_DAILY.csv

Author: Claude Code
Date: 2025-11-04
"""

import xarray as xr
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Project paths
project_root = Path(__file__).resolve().parent.parent
data_dir = project_root / "data"
fetched_dir = data_dir / "raw" / "Copernicus" / "fetched"
output_dir = data_dir / "processed" / "oceantemp"

def find_netcdf_file():
    """Find the most recent Copernicus NetCDF file."""
    nc_files = list(fetched_dir.glob("copernicus_iceland_ocean_*.nc"))

    if not nc_files:
        print("❌ No NetCDF files found in:")
        print(f"   {fetched_dir}")
        print("\n💡 Run fetch_copernicus_data.py first to download ocean data.")
        sys.exit(1)

    # Use most recent file
    nc_file = sorted(nc_files)[-1]
    return nc_file


def aggregate_spatially(nc_file):
    """
    Aggregate NetCDF data spatially to daily means.

    Takes all grid points (lat, lon, depth) and computes daily averages
    for the entire Iceland region.
    """
    print("=" * 80)
    print("SPATIAL AGGREGATION - COPERNICUS OCEAN DATA")
    print("=" * 80)
    print(f"\n📂 Input file:")
    print(f"   {nc_file.name}")

    # Check file size
    file_size_mb = nc_file.stat().st_size / (1024**2)
    print(f"   Size: {file_size_mb:.1f} MB")

    print(f"\n⏳ Loading NetCDF data...")
    print("   (This may take a few minutes for large files...)")

    try:
        # Open dataset
        ds = xr.open_dataset(nc_file)

        print(f"\n✓ Data loaded!")
        print(f"\n📊 Dataset dimensions:")
        for dim, size in ds.dims.items():
            print(f"   {dim}: {size}")

        print(f"\n🌊 Variables found:")
        for var in ds.data_vars:
            print(f"   - {var}: {ds[var].attrs.get('long_name', 'No description')}")

        # Compute spatial means
        print(f"\n⚙️ Computing spatial averages...")
        print("   Averaging over latitude, longitude, and depth dimensions...")

        # Average over spatial dimensions
        spatial_dims = [d for d in ['latitude', 'longitude', 'depth'] if d in ds.dims]
        daily_avg = ds.mean(dim=spatial_dims)

        # Convert to DataFrame
        print(f"\n⚙️ Converting to DataFrame...")
        df = daily_avg.to_dataframe().reset_index()

        # Clean up column names
        if 'time' in df.columns:
            df = df.rename(columns={'time': 'Dags'})

        # Convert temperature from Kelvin to Celsius if needed
        if 'thetao' in df.columns:
            # Check if values are in Kelvin (> 100)
            if df['thetao'].mean() > 100:
                print("   Converting temperature from Kelvin to Celsius...")
                df['thetao'] = df['thetao'] - 273.15

        # Sort by date
        df = df.sort_values('Dags').reset_index(drop=True)

        print(f"\n✓ Aggregation complete!")
        print(f"\n📈 Result summary:")
        print(f"   Total days: {len(df)}")
        print(f"   Date range: {df['Dags'].min()} to {df['Dags'].max()}")
        print(f"   Variables: {', '.join([c for c in df.columns if c != 'Dags'])}")

        # Show statistics
        print(f"\n📊 Ocean variable statistics:")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        stats = df[numeric_cols].describe()
        print(stats.to_string())

        # Close dataset
        ds.close()

        return df

    except Exception as e:
        print(f"\n❌ Error processing NetCDF file:")
        print(f"   {e}")
        sys.exit(1)


def save_daily_csv(df, nc_file):
    """Save aggregated daily data to CSV."""
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Extract date range from input filename for output name
    # Input: copernicus_iceland_ocean_20100101_20250916.nc
    # Output: Ocean_temp_20100101_20250916_DAILY.csv
    filename_parts = nc_file.stem.split('_')
    if len(filename_parts) >= 5:
        start_date = filename_parts[-2]
        end_date = filename_parts[-1]
        output_name = f"Ocean_temp_{start_date}_{end_date}_DAILY.csv"
    else:
        output_name = "Ocean_temp_DAILY.csv"

    output_file = output_dir / output_name

    print(f"\n💾 Saving to CSV:")
    print(f"   {output_file}")

    df.to_csv(output_file, index=False)

    # Check output size
    output_size_kb = output_file.stat().st_size / 1024
    print(f"   Size: {output_size_kb:.1f} KB")

    print(f"\n✅ Daily aggregated data saved successfully!")

    return output_file


def main():
    """Main execution."""
    print("\n" + "=" * 80)
    print("COPERNICUS OCEAN DATA - SPATIAL AGGREGATION")
    print("=" * 80)

    # Find input file
    nc_file = find_netcdf_file()

    # Aggregate spatially
    df = aggregate_spatially(nc_file)

    # Save to CSV
    output_file = save_daily_csv(df, nc_file)

    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("\n1. View the daily data:")
    print(f"   head {output_file}")

    print("\n2. Aggregate to monthly (to match catch data):")
    print("   python scripts/aggregate_ocean_monthly.py")

    print("\n3. Create comparison datasets:")
    print("   python scripts/prepare_comparison_datasets.py")

    print("\n4. Visualize in Streamlit:")
    print("   streamlit run streamlit_app.py")

    print("\n" + "=" * 80)
    print(f"✓ Spatial aggregation complete!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
