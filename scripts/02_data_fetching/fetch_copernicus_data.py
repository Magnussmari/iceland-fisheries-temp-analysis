"""
Copernicus Marine Data Fetcher
Fetches ocean temperature and physical data for Icelandic waters
to compare with catch data (2010-2025)
"""

import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

try:
    import copernicusmarine
except ImportError:
    print("❌ Villa: copernicusmarine er ekki uppsett")
    print("\nSetja upp með:")
    print("  pip install copernicusmarine")
    sys.exit(1)


def get_catch_date_range(catch_file):
    """
    Get the date range from catch data to determine what ocean data to fetch
    """
    print(f"📊 Les aflaskrá til að finna tímabil...")

    df = pd.read_csv(catch_file, parse_dates=['Dags'])

    start_date = df['Dags'].min()
    end_date = df['Dags'].max()

    print(f"  ✓ Aflagögn spanna: {start_date.date()} til {end_date.date()}")

    return start_date, end_date


def fetch_ocean_temperature_data(
    start_date,
    end_date,
    output_dir,
    latitude_range=(63, 67),  # Iceland waters
    longitude_range=(-25, -13),
    depth_range=(0, 50)
):
    """
    Fetch sea surface temperature and physical oceanography data
    from Copernicus Marine Service for Icelandic waters

    Dataset: Global Ocean Physics Reanalysis
    Product ID: GLOBAL_MULTIYEAR_PHY_001_030
    Dataset ID: cmems_mod_glo_phy_my_0.083deg_P1D-m (daily, ~9km resolution)

    Variables:
    - thetao: Sea water potential temperature (°C)
    - so: Sea water salinity (PSU)
    - uo, vo: Eastward/Northward sea water velocity (m/s)
    - zos: Sea surface height above geoid (m)
    """

    print("\n" + "=" * 80)
    print("SÆKJUM GÖGN FRÁ COPERNICUS MARINE SERVICE")
    print("=" * 80)

    print(f"\n📍 Svæði: Íslenskt landgrunnshaf")
    print(f"  Breidd: {latitude_range[0]}°N - {latitude_range[1]}°N")
    print(f"  Lengd:  {longitude_range[0]}°E - {longitude_range[1]}°E")
    print(f"  Dýpi:   {depth_range[0]}m - {depth_range[1]}m")

    print(f"\n📅 Tímabil:")
    print(f"  Frá:    {start_date.strftime('%Y-%m-%d')}")
    print(f"  Til:    {end_date.strftime('%Y-%m-%d')}")

    print(f"\n📦 Gagnasafn:")
    print(f"  Product:  GLOBAL_MULTIYEAR_PHY_001_030")
    print(f"  Dataset:  cmems_mod_glo_phy_my_0.083deg_P1D-m")
    print(f"  Upplausn: ~9km, daglega")

    # Create output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Output filename
    output_file = output_dir / f"copernicus_iceland_ocean_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.nc"

    print(f"\n⏳ Sæki gögn frá Copernicus Marine...")
    print(f"  (Þetta getur tekið nokkrar mínútur...)")

    try:
        # Fetch data
        copernicusmarine.subset(
            dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
            variables=["thetao", "so", "uo", "vo", "zos"],
            minimum_longitude=longitude_range[0],
            maximum_longitude=longitude_range[1],
            minimum_latitude=latitude_range[0],
            maximum_latitude=latitude_range[1],
            start_datetime=start_date.strftime("%Y-%m-%d"),
            end_datetime=end_date.strftime("%Y-%m-%d"),
            minimum_depth=depth_range[0],
            maximum_depth=depth_range[1],
            output_filename=output_file.name,
            output_directory=str(output_dir),
            netcdf_compression_level=6  # Good balance between size and speed
        )

        print(f"\n✓ Gögn sótt!")
        print(f"  Skrá: {output_file}")

        # Check file size
        file_size = output_file.stat().st_size / (1024**2)  # MB
        print(f"  Stærð: {file_size:.1f} MB")

        return output_file

    except Exception as e:
        print(f"\n❌ Villa við að sækja gögn:")
        print(f"  {e}")
        print(f"\n💡 Athugaðu:")
        print(f"  1. Að þú sért með gilt Copernicus Marine aðgang")
        print(f"  2. Að þú hafir stillt credentials með:")
        print(f"     copernicusmarine login")
        print(f"  3. Að tímabilið sé innan gagnasafnsins (1993-present)")
        return None


def fetch_subset_for_testing(output_dir):
    """
    Fetch a small subset of data for testing (1 month, limited area)
    Much faster than full dataset!
    """

    print("\n" + "=" * 80)
    print("PRÓFUNARSETT - Einn mánuður fyrir Suðvesturland")
    print("=" * 80)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "copernicus_test_subset_feb2018.nc"

    print(f"\n📍 Svæði: Suðvesturland")
    print(f"  Breidd: 63.5°N - 64.5°N")
    print(f"  Lengd:  -24°E - -21°E")

    print(f"\n📅 Tímabil: Febrúar 2018 (1 mánuður)")

    print(f"\n⏳ Sæki prófunargögn...")

    try:
        copernicusmarine.subset(
            dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
            variables=["thetao", "so"],
            minimum_longitude=-24,
            maximum_longitude=-21,
            minimum_latitude=63.5,
            maximum_latitude=64.5,
            start_datetime="2018-02-01",
            end_datetime="2018-02-28",
            minimum_depth=0,
            maximum_depth=50,
            output_filename=output_file.name,
            output_directory=str(output_dir),
            netcdf_compression_level=6
        )

        print(f"\n✓ Prófunargögn sótt!")
        print(f"  Skrá: {output_file}")

        file_size = output_file.stat().st_size / (1024**2)
        print(f"  Stærð: {file_size:.1f} MB")

        return output_file

    except Exception as e:
        print(f"\n❌ Villa: {e}")
        return None


def convert_netcdf_to_csv(netcdf_file, output_csv=None):
    """
    Convert NetCDF file to CSV for easier analysis
    """
    try:
        import xarray as xr

        print(f"\n📝 Umbreyti NetCDF í CSV...")

        ds = xr.open_dataset(netcdf_file)

        # Convert to dataframe
        df = ds.to_dataframe().reset_index()

        # Output file
        if output_csv is None:
            output_csv = netcdf_file.with_suffix('.csv')

        df.to_csv(output_csv, index=False)

        print(f"  ✓ CSV skrá: {output_csv}")
        print(f"  ✓ {len(df):,} línur, {len(df.columns)} dálkar")

        return output_csv

    except Exception as e:
        print(f"  ❌ Villa við umbreytingu: {e}")
        return None


def main():
    """
    Main execution function
    """
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Paths
    catch_file = project_root / "data/processed/afli_eftir_fisktegundum/afli_hreinsad_FULL.csv"
    output_dir = project_root / "data/raw/Copernicus/fetched"

    print("=" * 80)
    print("COPERNICUS MARINE GAGNAHLEÐSLA")
    print("=" * 80)
    print(f"Keyrði: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Check for command line arguments
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        print("Veldu aðgerð:")
        print("  1. Test - Sækja prófunarsett (1 mánuður, lítið svæði)")
        print("  2. Full - Sækja öll gögn fyrir aflaskrá tímabil (GETUR TEKIÐ LANGAN TÍMA!)")
        print("  3. Custom - Tilgreina sérsniðið tímabil")

        choice = input("\nVal (1/2/3): ").strip()

        if choice == "1":
            mode = "test"
        elif choice == "2":
            mode = "full"
        elif choice == "3":
            mode = "custom"
        else:
            print("Ógilt val")
            return

    if mode == "test":
        # Fetch small test subset
        netcdf_file = fetch_subset_for_testing(output_dir)

        if netcdf_file:
            # Convert to CSV
            csv_file = convert_netcdf_to_csv(netcdf_file)

            print("\n" + "=" * 80)
            print("✓ LOKIÐ")
            print("=" * 80)
            print(f"\nGögn vistuð í:")
            print(f"  NetCDF: {netcdf_file}")
            if csv_file:
                print(f"  CSV:    {csv_file}")

    elif mode == "full":
        # Get date range from catch data
        if not catch_file.exists():
            print(f"❌ Villa: Aflaskrá fannst ekki: {catch_file}")
            print("   Keyrðu fyrst: python scripts/hreinsa_gogn_v4.py")
            return

        start_date, end_date = get_catch_date_range(catch_file)

        # Warn about large download
        print(f"\n⚠️  VIÐVÖRUN!")
        print(f"  Þetta mun sækja gögn fyrir {(end_date - start_date).days} daga")
        print(f"  Skráin gæti orðið mjög stór (möguleg nokkur GB)")
        print(f"  Þetta getur tekið 30-60 mínútur eða lengur")

        confirm = input(f"\nHalda áfram? (j/n): ").lower()

        if confirm != 'j':
            print("Hætt við")
            return

        # Fetch full dataset
        netcdf_file = fetch_ocean_temperature_data(
            start_date,
            end_date,
            output_dir
        )

        if netcdf_file:
            print("\n✓ Gögn sótt!")

            # Ask about CSV conversion
            convert = input(f"\nUmbreyta í CSV? (j/n): ").lower()
            if convert == 'j':
                convert_netcdf_to_csv(netcdf_file)

    elif mode == "custom":
        print("\nTilgreindu tímabil:")
        start_str = input("  Byrjar (YYYY-MM-DD): ").strip()
        end_str = input("  Endar (YYYY-MM-DD): ").strip()

        try:
            start_date = pd.to_datetime(start_str)
            end_date = pd.to_datetime(end_str)

            netcdf_file = fetch_ocean_temperature_data(
                start_date,
                end_date,
                output_dir
            )

            if netcdf_file:
                convert_netcdf_to_csv(netcdf_file)

        except Exception as e:
            print(f"❌ Villa: {e}")


if __name__ == "__main__":
    main()
