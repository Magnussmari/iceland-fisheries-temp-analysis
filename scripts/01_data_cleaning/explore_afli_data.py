"""
Könnun á hreinsaðri aflaskrá - Data Exploration Script
Explores the cleaned catch data and generates statistics
"""

import pandas as pd
import os
from datetime import datetime

def explore_afli_data(data_file):
    """
    Skoðar hreinsaða aflaskrá og prentar út tölfræði
    """
    print("=" * 80)
    print(f"GAGNAKÖNNUN: {os.path.basename(data_file)}")
    print("=" * 80)
    print(f"Keyrði: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Load data
    df = pd.read_csv(data_file, parse_dates=['Dags'])

    # Basic info
    print("📊 GRUNNTÖLFRÆÐI")
    print("-" * 80)
    print(f"Heildarfjöldi raða:          {len(df):,}")
    print(f"Fjöldi dálka:                {len(df.columns)}")
    print(f"Minnisnotkun:                {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"Dagsetningasvið:             {df['Dags'].min().strftime('%Y-%m-%d')} til {df['Dags'].max().strftime('%Y-%m-%d')}")
    print(f"Fjöldi ára:                  {df['Ár'].nunique()}")
    print()

    # Species breakdown
    print("🐟 FISKITEGUNDIR")
    print("-" * 80)
    species_stats = df.groupby('Fisktegund').agg({
        'Afli': ['count', 'sum', 'mean', 'min', 'max']
    }).round(0)
    species_stats.columns = ['Fjöldi færslna', 'Heildarafli (kg)', 'Meðalafli (kg)', 'Lágmark (kg)', 'Hámark (kg)']
    print(species_stats)
    print()

    # Port breakdown
    print("⚓ HELSTU LÖNDUNARHAFNIR (Topp 10)")
    print("-" * 80)
    port_stats = df.groupby('Löndunarhöfn')['Afli'].sum().sort_values(ascending=False).head(10)
    for i, (port, total) in enumerate(port_stats.items(), 1):
        pct = (total / df['Afli'].sum()) * 100
        print(f"{i:2d}. {port:20s} {total:15,.0f} kg  ({pct:5.2f}%)")
    print(f"\nFjöldi hafna samtals:        {df['Löndunarhöfn'].nunique()}")
    print()

    # Yearly trends
    print("📅 ÁRLEGAR TÖLUR")
    print("-" * 80)
    yearly = df.groupby('Ár')['Afli'].agg(['sum', 'count', 'mean']).round(0)
    yearly.columns = ['Heildarafli (kg)', 'Fjöldi færslna', 'Meðalafli (kg)']
    print(yearly)
    print()

    # Monthly patterns
    print("📆 MÁNAÐARLEG MYNSTUR")
    print("-" * 80)
    # Create month order
    month_order = ['janúar', 'febrúar', 'mars', 'apríl', 'maí', 'júní',
                   'júlí', 'ágúst', 'september', 'október', 'nóvember', 'desember']
    df['Mánuður'] = pd.Categorical(df['Mánuður'], categories=month_order, ordered=True)

    monthly = df.groupby('Mánuður')['Afli'].agg(['sum', 'mean']).round(0)
    monthly.columns = ['Heildarafli (kg)', 'Meðalafli (kg)']
    print(monthly)
    print()

    # Recent trends (last 3 years)
    print("📈 NÝLEGAR TÖLUR (Síðustu 3 ár)")
    print("-" * 80)
    recent_years = sorted(df['Ár'].unique())[-3:]
    recent_df = df[df['Ár'].isin(recent_years)]

    recent_by_species = recent_df.groupby(['Ár', 'Fisktegund'])['Afli'].sum().unstack(fill_value=0)
    print(recent_by_species.applymap(lambda x: f"{x:,.0f}"))
    print()

    # Missing data analysis
    print("❓ GÆÐAEFTIRLIT")
    print("-" * 80)
    print(f"Fjöldi núllgildi í afla:     {(df['Afli'] == 0).sum():,}")
    print(f"Fjöldi neikvæðra gilda:      {(df['Afli'] < 0).sum():,}")
    print(f"Vantar fisktegund:           {df['Fisktegund'].isna().sum():,}")
    print(f"Vantar löndunarhöfn:         {df['Löndunarhöfn'].isna().sum():,}")
    print(f"Vantar dagsetningu:          {df['Dags'].isna().sum():,}")
    print()

    # Summary statistics by species
    print("📊 TÖLFRÆÐI EFTIR TEGUND")
    print("-" * 80)
    for species in df['Fisktegund'].unique():
        species_df = df[df['Fisktegund'] == species]
        print(f"\n{species}:")
        print(f"  Heildarafli:               {species_df['Afli'].sum():,.0f} kg")
        print(f"  Meðalafli pr. færslu:      {species_df['Afli'].mean():,.0f} kg")
        print(f"  Miðgildi:                  {species_df['Afli'].median():,.0f} kg")
        print(f"  Staðalfrávik:              {species_df['Afli'].std():,.0f} kg")
        print(f"  Fjöldi færslna:            {len(species_df):,}")
        print(f"  Fjöldi hafna:              {species_df['Löndunarhöfn'].nunique()}")
        print(f"  Mest veiddar hafnir (top 3):")
        top3 = species_df.groupby('Löndunarhöfn')['Afli'].sum().sort_values(ascending=False).head(3)
        for i, (port, amount) in enumerate(top3.items(), 1):
            print(f"    {i}. {port}: {amount:,.0f} kg")

    print()
    print("=" * 80)
    print("✓ KÖNNUN LOKIÐ")
    print("=" * 80)

    return df


def generate_quick_stats(data_file, output_file=None):
    """
    Býr til stutt samantekt í textaskrá
    """
    df = pd.read_csv(data_file, parse_dates=['Dags'])

    stats_text = f"""
AFLI EFTIR FISKTEGUNDUM - STUTTUR SAMANTEKT
{'=' * 60}
Dagsetning: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Gagnaheimild: {os.path.basename(data_file)}

GRUNNUPPLÝSINGAR
{'-' * 60}
Fjöldi færslna:              {len(df):,}
Tímabil:                     {df['Ár'].min()}-{df['Ár'].max()}
Fjöldi fiskitegunda:         {df['Fisktegund'].nunique()}
Fjöldi löndunarhafna:        {df['Löndunarhöfn'].nunique()}

HEILDARAFLI
{'-' * 60}
"""

    for species in df['Fisktegund'].unique():
        total = df[df['Fisktegund'] == species]['Afli'].sum()
        stats_text += f"{species:20s}  {total:20,.0f} kg\n"

    stats_text += f"\nSAMANLAGT:           {df['Afli'].sum():20,.0f} kg\n"

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(stats_text)
        print(f"\nSamantekt vistuð í: {output_file}")

    return stats_text


if __name__ == "__main__":
    import sys

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # Check for sample flag
    use_sample = '--sample' in sys.argv or '-s' in sys.argv

    if use_sample:
        data_file = os.path.join(project_root, 'data/processed/sample/afli_hreinsad_sample.csv')
        stats_file = os.path.join(project_root, 'data/processed/sample/afli_stats_sample.txt')
    else:
        data_file = os.path.join(project_root, 'data/processed/afli_eftir_fisktegundum/afli_hreinsad.csv')
        stats_file = os.path.join(project_root, 'data/processed/afli_eftir_fisktegundum/afli_stats.txt')

    # Check if file exists
    if not os.path.exists(data_file):
        print(f"Villa: Skrá fannst ekki: {data_file}")
        print("Keyra fyrst: python scripts/hreinsa_gogn_v4.py")
        sys.exit(1)

    # Explore data
    df = explore_afli_data(data_file)

    # Generate quick stats file
    generate_quick_stats(data_file, stats_file)
