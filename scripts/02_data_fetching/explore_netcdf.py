"""
NetCDF Data Explorer - Copernicus Ocean Data
Explores meteorological and oceanographic data from NetCDF files
"""

import xarray as xr
import pandas as pd
import numpy as np
from pathlib import Path
import sys

def explore_netcdf(file_path):
    """
    Explore a NetCDF file and print comprehensive information
    """
    print("=" * 80)
    print(f"NETCDF GAGNAKÖNNUN")
    print("=" * 80)
    print(f"Skrá: {Path(file_path).name}")
    print(f"Slóð: {file_path}")
    print()

    try:
        # Open dataset
        ds = xr.open_dataset(file_path)

        print("📊 GRUNNTÖLFRÆÐI")
        print("-" * 80)
        print(f"Gagnasnið: NetCDF")
        print(f"Fjöldi breyta: {len(ds.data_vars)}")
        print(f"Fjöldi vídda: {len(ds.dims)}")
        print(f"Fjöldi eiginda: {len(ds.attrs)}")
        print()

        # Dimensions
        print("📐 VÍDDIR (DIMENSIONS)")
        print("-" * 80)
        for dim, size in ds.dims.items():
            print(f"  {dim:20s} : {size:,} gildi")
        print()

        # Coordinates
        print("📍 HNIT (COORDINATES)")
        print("-" * 80)
        for coord_name, coord_var in ds.coords.items():
            coord_info = f"  {coord_name:20s} : {coord_var.dims}"
            if coord_var.size > 0:
                try:
                    if np.issubdtype(coord_var.dtype, np.datetime64):
                        first_val = pd.Timestamp(coord_var.values[0])
                        last_val = pd.Timestamp(coord_var.values[-1])
                        coord_info += f" [{first_val} til {last_val}]"
                    else:
                        first_val = float(coord_var.values[0])
                        last_val = float(coord_var.values[-1])
                        coord_info += f" [{first_val:.4f} til {last_val:.4f}]"
                except:
                    pass
            print(coord_info)
        print()

        # Variables
        print("🔢 BREYTUR (VARIABLES)")
        print("-" * 80)
        for var_name, var in ds.data_vars.items():
            print(f"\n  {var_name}")
            print(f"    Víddir: {var.dims}")
            print(f"    Stærð: {var.shape}")
            print(f"    Gerð: {var.dtype}")

            # Get attributes
            if hasattr(var, 'long_name'):
                print(f"    Nafn: {var.long_name}")
            if hasattr(var, 'units'):
                print(f"    Eining: {var.units}")
            if hasattr(var, 'standard_name'):
                print(f"    Staðlað nafn: {var.standard_name}")

            # Basic statistics for numeric data
            if np.issubdtype(var.dtype, np.number):
                try:
                    values = var.values
                    valid_values = values[~np.isnan(values)]
                    if len(valid_values) > 0:
                        print(f"    Tölfræði:")
                        print(f"      Lágmark:   {np.nanmin(values):.4f}")
                        print(f"      Hámark:    {np.nanmax(values):.4f}")
                        print(f"      Meðaltal:  {np.nanmean(values):.4f}")
                        print(f"      Miðgildi:  {np.nanmedian(values):.4f}")
                        print(f"      Std.fráv.: {np.nanstd(values):.4f}")
                        print(f"      Fjöldi gilt gildi: {len(valid_values):,}")
                        print(f"      Fjöldi NaN: {np.isnan(values).sum():,}")
                except Exception as e:
                    print(f"      (Villa við útreikning tölfræði: {e})")
        print()

        # Global attributes
        print("🏷️  EIGINDI (GLOBAL ATTRIBUTES)")
        print("-" * 80)
        for attr_name, attr_value in ds.attrs.items():
            attr_str = str(attr_value)
            if len(attr_str) > 70:
                attr_str = attr_str[:67] + "..."
            print(f"  {attr_name:30s} : {attr_str}")
        print()

        # Memory usage
        print("💾 MINNISNOTKUN")
        print("-" * 80)
        total_bytes = sum(var.nbytes for var in ds.data_vars.values())
        print(f"  Heildarminnisnotkun: {total_bytes / 1024**2:.2f} MB")
        for var_name, var in ds.data_vars.items():
            print(f"    {var_name:20s} : {var.nbytes / 1024**2:.2f} MB")
        print()

        # Suggest potential analyses
        print("💡 MÖGULEGAR GREININGAR")
        print("-" * 80)

        # Check for time dimension
        time_dims = [d for d in ds.dims if 'time' in d.lower()]
        if time_dims:
            print(f"  ✓ Tímaraðagreining (time dimension: {time_dims[0]})")

        # Check for spatial dimensions
        spatial_dims = []
        for d in ds.dims:
            if any(x in d.lower() for x in ['lat', 'lon', 'x', 'y']):
                spatial_dims.append(d)
        if len(spatial_dims) >= 2:
            print(f"  ✓ Landfræðileg kortlagning (dimensions: {', '.join(spatial_dims)})")

        # Check for depth/level
        depth_dims = [d for d in ds.dims if any(x in d.lower() for x in ['depth', 'level', 'z'])]
        if depth_dims:
            print(f"  ✓ Dýptar/hæðargreining (dimension: {depth_dims[0]})")

        print("  ✓ Tölfræðileg samantekt")
        print("  ✓ Dreifirit (histograms)")
        print("  ✓ Fylgnifylki milli breyta")

        print()
        print("=" * 80)
        print("✓ KÖNNUN LOKIÐ")
        print("=" * 80)

        return ds

    except Exception as e:
        print(f"❌ VILLA: {e}")
        import traceback
        traceback.print_exc()
        return None


def extract_to_csv(ds, output_path, variables=None, flatten_time=True):
    """
    Extract data from NetCDF to CSV format
    """
    print(f"\n📝 Umbreyti í CSV...")

    if variables is None:
        variables = list(ds.data_vars.keys())

    # Convert to DataFrame
    df = ds[variables].to_dataframe()

    if flatten_time:
        df = df.reset_index()

    df.to_csv(output_path, index=False)
    print(f"✓ Vistað í: {output_path}")
    print(f"  Fjöldi raða: {len(df):,}")
    print(f"  Fjöldi dálka: {len(df.columns)}")

    return df


if __name__ == "__main__":
    import os

    # Default file path (adjusted for scripts/02_data_fetching/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent

    default_file = project_root / "data/raw/Copernicus/igp_alliance_surface_met_20180207_qc3_10min.nc"

    # Check command line arguments
    if len(sys.argv) > 1:
        nc_file = Path(sys.argv[1])
    else:
        nc_file = default_file

    if not nc_file.exists():
        print(f"❌ Villa: Skrá fannst ekki: {nc_file}")
        sys.exit(1)

    # Explore the file
    ds = explore_netcdf(str(nc_file))

    if ds is not None:
        # Ask if user wants to export to CSV
        print("\n" + "=" * 80)
        response = input("Viltu vista gögnin sem CSV? (j/n): ").lower()

        if response in ['j', 'já', 'y', 'yes']:
            output_file = project_root / "data/processed/copernicus" / f"{nc_file.stem}.csv"
            output_file.parent.mkdir(parents=True, exist_ok=True)

            extract_to_csv(ds, str(output_file))

        ds.close()
