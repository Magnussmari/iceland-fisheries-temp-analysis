"""
Dataset Comparison Preparation Script
Aligns ocean temperature data with catch data for the same time period
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import sys

def load_ocean_data(file_path):
    """
    Load and process ocean temperature data from CSV
    """
    print(f"📊 Hleð inn hafgögnum frá: {file_path}")

    df = pd.read_csv(file_path, parse_dates=['time'])

    print(f"  ✓ {len(df):,} mælingar frá {df['time'].min()} til {df['time'].max()}")
    print(f"  ✓ {len(df.columns)} breytur")

    return df


def load_catch_data(file_path):
    """
    Load and process catch data from CSV
    """
    print(f"🐟 Hleð inn aflagögnum frá: {file_path}")

    df = pd.read_csv(file_path, parse_dates=['Dags'])

    print(f"  ✓ {len(df):,} færslur frá {df['Dags'].min()} til {df['Dags'].max()}")
    print(f"  ✓ {df['Fisktegund'].nunique()} tegundir, {df['Löndunarhöfn'].nunique()} hafnir")

    return df


def filter_catch_by_ocean_period(catch_df, ocean_df):
    """
    Filter catch data to match the time period of ocean data
    """
    ocean_start = pd.to_datetime(ocean_df['time'].min())
    ocean_end = pd.to_datetime(ocean_df['time'].max())

    print(f"\n🔍 Síun aflagagna fyrir tímabilið:")
    print(f"  Byrjar: {ocean_start.date()}")
    print(f"  Endar:  {ocean_end.date()}")

    # Filter catch data (convert to start of month for catch data which is monthly)
    # Get month range
    start_month = ocean_start.replace(day=1)
    end_month = ocean_end.replace(day=1)

    # Filter catch data
    filtered = catch_df[
        (catch_df['Dags'] >= start_month) &
        (catch_df['Dags'] <= end_month)
    ].copy()

    print(f"  ✓ {len(filtered):,} aflafærslur í sama tímabili")
    print(f"  ✓ {filtered['Afli'].sum():,.0f} kg heildarafli")

    return filtered


def aggregate_ocean_daily(ocean_df):
    """
    Aggregate ocean data to daily averages to match catch data granularity
    """
    print(f"\n📅 Útreikningur á daglegu meðaltali fyrir hafgögn...")

    # Create date column
    ocean_df['date'] = ocean_df['time'].dt.date

    # Select numeric columns for aggregation
    numeric_cols = ocean_df.select_dtypes(include=[np.number]).columns.tolist()

    # Aggregate by day
    daily = ocean_df.groupby('date')[numeric_cols].agg(['mean', 'std', 'min', 'max']).reset_index()

    # Flatten column names
    daily.columns = ['_'.join(col).strip('_') if col[1] else col[0] for col in daily.columns.values]
    daily = daily.rename(columns={'date': 'Dags'})
    daily['Dags'] = pd.to_datetime(daily['Dags'])

    print(f"  ✓ {len(daily)} dagar með meðaltölum")

    return daily


def aggregate_catch_daily(catch_df):
    """
    Aggregate catch data to daily totals (already monthly, but ensure daily format)
    """
    print(f"\n🐟 Samantekt á aflagögnum...")

    # Catch data is already at monthly level (Dags = first of month)
    # We'll aggregate by species and date
    daily = catch_df.groupby(['Dags', 'Fisktegund']).agg({
        'Afli': ['sum', 'mean', 'count'],
        'Löndunarhöfn': lambda x: list(x.unique())
    }).reset_index()

    # Flatten columns
    daily.columns = ['Dags', 'Fisktegund', 'Afli_heildar', 'Afli_medal', 'Fjoldi_hafna', 'Hafnir']

    print(f"  ✓ {len(daily)} dagsetningar með gögnum")

    return daily


def merge_datasets(ocean_daily, catch_daily):
    """
    Merge ocean and catch data on date
    """
    print(f"\n🔗 Samræming gagnasafna...")

    # Merge on date
    merged = pd.merge(
        catch_daily,
        ocean_daily,
        on='Dags',
        how='outer',
        indicator=True
    )

    # Add merge statistics
    both_count = (merged['_merge'] == 'both').sum()
    catch_only = (merged['_merge'] == 'left_only').sum()
    ocean_only = (merged['_merge'] == 'right_only').sum()

    print(f"  ✓ Færslur með báðum gögnum: {both_count}")
    print(f"  ✓ Aðeins aflagögn: {catch_only}")
    print(f"  ✓ Aðeins hafgögn: {ocean_only}")

    return merged


def create_comparison_datasets(ocean_file, catch_file, output_dir):
    """
    Main function to create aligned comparison datasets
    """
    print("=" * 80)
    print("UNDIRBÚNINGUR SAMANBURÐARGAGNASAFNA")
    print("=" * 80)
    print(f"Keyrði: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Create output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    ocean_df = load_ocean_data(ocean_file)
    catch_df = load_catch_data(catch_file)

    # Get time period from ocean data
    ocean_start = ocean_df['time'].min()
    ocean_end = ocean_df['time'].max()

    # Filter catch data to match ocean period
    catch_filtered = filter_catch_by_ocean_period(catch_df, ocean_df)

    # Aggregate to daily
    ocean_daily = aggregate_ocean_daily(ocean_df)
    catch_daily = aggregate_catch_daily(catch_filtered)

    # Merge datasets
    merged = merge_datasets(ocean_daily, catch_daily)

    # Save datasets
    print(f"\n💾 Vista gagnasöfn...")

    # 1. Filtered catch data (original granularity)
    catch_filtered_path = output_dir / "afli_filtered_2018-02-07_to_2018-03-21.csv"
    catch_filtered.to_csv(catch_filtered_path, index=False, encoding='utf-8-sig')
    print(f"  ✓ {catch_filtered_path.name}: {len(catch_filtered):,} færslur")

    # 2. Daily aggregated ocean data
    ocean_daily_path = output_dir / "ocean_daily_aggregated_2018-02-07_to_2018-03-21.csv"
    ocean_daily.to_csv(ocean_daily_path, index=False, encoding='utf-8-sig')
    print(f"  ✓ {ocean_daily_path.name}: {len(ocean_daily):,} dagar")

    # 3. Daily aggregated catch data
    catch_daily_path = output_dir / "afli_daily_aggregated_2018-02-07_to_2018-03-21.csv"
    catch_daily.to_csv(catch_daily_path, index=False, encoding='utf-8-sig')
    print(f"  ✓ {catch_daily_path.name}: {len(catch_daily):,} færslur")

    # 4. Merged dataset
    merged_path = output_dir / "ocean_catch_merged_2018-02-07_to_2018-03-21.csv"
    merged.to_csv(merged_path, index=False, encoding='utf-8-sig')
    print(f"  ✓ {merged_path.name}: {len(merged):,} færslur")

    # Generate statistics
    print(f"\n📊 Tölfræði fyrir sameinað gagnasafn:")

    # Ocean temperature stats
    if 'sbe38_bow_temperature_mean' in merged.columns:
        temp_col = 'sbe38_bow_temperature_mean'
        temp_stats = merged[temp_col].describe()
        print(f"\n  Sjávarhitastig (K):")
        print(f"    Meðaltal: {temp_stats['mean']:.2f}K ({temp_stats['mean']-273.15:.2f}°C)")
        print(f"    Lágmark:  {temp_stats['min']:.2f}K ({temp_stats['min']-273.15:.2f}°C)")
        print(f"    Hámark:   {temp_stats['max']:.2f}K ({temp_stats['max']-273.15:.2f}°C)")

    # Catch stats
    if 'Afli_heildar' in merged.columns:
        catch_stats = merged['Afli_heildar'].describe()
        print(f"\n  Afli (kg):")
        print(f"    Heildarafli: {merged['Afli_heildar'].sum():,.0f} kg")
        print(f"    Meðaltal/dag: {catch_stats['mean']:,.0f} kg")
        print(f"    Hámark/dag: {catch_stats['max']:,.0f} kg")

    print("\n" + "=" * 80)
    print("✓ UNDIRBÚNINGUR LOKIÐ")
    print("=" * 80)
    print(f"\nGagnasöfn vistuð í: {output_dir}")

    return {
        'catch_filtered': catch_filtered,
        'ocean_daily': ocean_daily,
        'catch_daily': catch_daily,
        'merged': merged,
        'output_dir': output_dir
    }


if __name__ == "__main__":
    # Paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Input files
    ocean_file = project_root / "data/processed/oceantemp/Ocean_temp_FULL.csv"
    catch_file = project_root / "data/processed/afli_eftir_fisktegundum/afli_hreinsad_FULL.csv"

    # Output directory
    output_dir = project_root / "data/processed/comparison"

    # Check if files exist
    if not ocean_file.exists():
        print(f"❌ Villa: Hafgagnaskrá fannst ekki: {ocean_file}")
        sys.exit(1)

    if not catch_file.exists():
        print(f"❌ Villa: Aflaskrá fannst ekki: {catch_file}")
        sys.exit(1)

    # Create comparison datasets
    results = create_comparison_datasets(ocean_file, catch_file, output_dir)

    print(f"\n💡 Til að skoða gögnin:")
    print(f"   import pandas as pd")
    print(f"   df = pd.read_csv('{results['output_dir']}/ocean_catch_merged_2018-02-07_to_2018-03-21.csv')")
    print(f"   print(df.head())")
