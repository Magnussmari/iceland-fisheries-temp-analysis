import pandas as pd

# Icelandic month mapping
ICELANDIC_MONTHS = {
    'janúar': 1, 'febrúar': 2, 'mars': 3, 'apríl': 4,
    'maí': 5, 'júní': 6, 'júlí': 7, 'ágúst': 8,
    'september': 9, 'október': 10, 'nóvember': 11, 'desember': 12
}

def hreinsa_aflaskra(input_skra_nafn, output_skra_nafn):
    """
    Les inn hráu aflaskrána, hreinsar hana og vistar á "löngu" formati.
    """
    print(f"Hef hreinsun á {input_skra_nafn}...")

    # 1. Lesa CSV með multi-level headers
    df = pd.read_csv(
        input_skra_nafn,
        sep=';',
        skiprows=3,
        header=[0, 1],
        na_values='..',
    )

    print(f"Lesið inn: {len(df)} línur, {len(df.columns)} dálkar")

    # 2. Flattena dálkahausakeilinn - IMPROVED VERSION
    new_cols = []
    current_year = None

    for col_tuple in df.columns:
        level0 = str(col_tuple[0]).strip() if pd.notna(col_tuple[0]) else ''
        level1 = str(col_tuple[1]).strip() if pd.notna(col_tuple[1]) else ''

        # Fjarlægja 'Unnamed' og 'nan'
        if 'Unnamed' in level0:
            level0 = ''
        if level0 == 'nan':
            level0 = ''
        if level1 == 'nan':
            level1 = ''

        # Check if level0 is a year (4 digits starting with 20)
        if level0.isdigit() and len(level0) == 4 and level0.startswith('20'):
            current_year = level0
            # Year column itself might be empty or have data, skip using it
            continue  # Don't add year columns as separate columns

        # Check if level1 is a year
        if level1.isdigit() and len(level1) == 4 and level1.startswith('20'):
            current_year = level1

        # Build column names
        # If level0 is a month name and we have a current year
        if level0 in ICELANDIC_MONTHS and current_year:
            new_cols.append(f'{current_year}_{level0}')
        # If level1 is a month name and we have a current year
        elif level1 in ICELANDIC_MONTHS and current_year:
            new_cols.append(f'{current_year}_{level1}')
        # First two columns (Fisktegund, Löndunarhöfn)
        elif level1 and not level1.isdigit():  # Non-numeric level1 values are the real headers
            new_cols.append(level1)
        elif level0 and not level0.isdigit():
            new_cols.append(level0)
        else:
            # This is likely data, not a header - skip
            pass

    print(f"Búnar til {len(new_cols)} dálkar")
    print(f"Dæmi um dálkanöfn: {new_cols[:15]}")

    # Make sure we have the right number of columns
    if len(new_cols) != len(df.columns):
        print(f"VIÐVÖRUN: Fjöldi nýrra dálka ({len(new_cols)}) passar ekki við fjölda eldri dálka ({len(df.columns)})")
        # We need to handle this differently - let's use a different approach

    # ALTERNATIVE APPROACH: Read without multi-level, parse headers manually
    print("\nNýting á annarri aðferð - les hráar hauslínur...")

    # Read the year line
    with open(input_skra_nafn, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
        year_line = lines[2].strip().split(';')  # Line with years
        month_line = lines[3].strip().split(';')  # Line with months

    print(f"Ár lína: {len(year_line)} stök")
    print(f"Mánuðar lína: {len(month_line)} stök")
    print(f"Fyrstu 20 ár gildi: {year_line[:20]}")
    print(f"Fyrstu 20 mánuðar gildi: {month_line[:20]}")

    # Build column names by forward-filling years
    col_names = []
    current_year = None

    for i in range(len(month_line)):
        # Check if there's a year at this position
        if i < len(year_line) and year_line[i] and year_line[i].strip():
            potential_year = year_line[i].strip()
            if potential_year.isdigit() and len(potential_year) == 4:
                current_year = potential_year

        # Get month at this position
        month = month_line[i].strip() if i < len(month_line) else ''

        # Build column name
        if i == 0:
            col_names.append('Fisktegund')
        elif i == 1:
            col_names.append('Löndunarhöfn')
        elif month in ICELANDIC_MONTHS and current_year:
            col_names.append(f'{current_year}_{month}')
        elif month:
            col_names.append(month)
        else:
            col_names.append(f'Col_{i}')

    print(f"\nBúnar til {len(col_names)} dálkanöfn")
    print(f"Dæmi: {col_names[:20]}")
    print(f"Síðustu: {col_names[-10:]}")

    # Now read the data with simple header
    df = pd.read_csv(
        input_skra_nafn,
        sep=';',
        skiprows=4,  # Skip to data rows
        header=None,
        na_values='..',
        names=col_names
    )

    print(f"\nLesið gögn: {len(df)} línur, {len(df.columns)} dálkar")

    # 3. Hreinsun
    df['Fisktegund'] = df['Fisktegund'].ffill()
    df = df[df['Löndunarhöfn'] != 'Allar löndunartegundir']
    df = df.dropna(subset=['Fisktegund', 'Löndunarhöfn'])

    print(f"Eftir fyrstu hreinsun: {len(df)} línur")

    # 4. Melt - only columns that match YEAR_MONTH pattern
    time_cols = [col for col in df.columns if '_' in col and any(month in col for month in ICELANDIC_MONTHS)]
    print(f"Tíma dálkar fundnir: {len(time_cols)}")

    df_langt = df.melt(
        id_vars=['Fisktegund', 'Löndunarhöfn'],
        value_vars=time_cols,
        var_name='Tími',
        value_name='Afli'
    )

    print(f"Eftir melt: {len(df_langt)} línur")
    print(f"Dæmi um 'Tími' gildi: {df_langt['Tími'].head(10).tolist()}")

    # 5. Greina Ár og Mánuður
    df_langt[['Ár_str', 'Mánuður']] = df_langt['Tími'].str.split('_', n=1, expand=True)

    # 6. Hreinsun
    df_langt['Afli'] = pd.to_numeric(df_langt['Afli'], errors='coerce')
    df_langt['Ár'] = pd.to_numeric(df_langt['Ár_str'], errors='coerce')
    df_langt = df_langt.dropna(subset=['Afli', 'Ár', 'Mánuður'])
    df_langt = df_langt[df_langt['Afli'] > 0]

    print(f"Eftir númeríska hreinsun: {len(df_langt)} línur")

    # 7. Dagsetning
    df_langt['Mánaðarnúmer'] = df_langt['Mánuður'].map(ICELANDIC_MONTHS)
    df_langt = df_langt.dropna(subset=['Mánaðarnúmer'])

    print(f"Eftir mánaðarkortlagningu: {len(df_langt)} línur")

    df_langt['Dags'] = pd.to_datetime(
        df_langt['Ár'].astype(int).astype(str) + '-' +
        df_langt['Mánaðarnúmer'].astype(int).astype(str) + '-01',
        format='%Y-%m-%d'
    )

    # 8. Endanleg útboð
    df_hreint = df_langt[['Dags', 'Ár', 'Mánuður', 'Fisktegund', 'Löndunarhöfn', 'Afli']].copy()
    df_hreint['Ár'] = df_hreint['Ár'].astype(int)
    df_hreint['Afli'] = df_hreint['Afli'].astype(int)
    df_hreint = df_hreint.sort_values('Dags').reset_index(drop=True)

    # 9. Vista
    df_hreint.to_csv(output_skra_nafn, index=False, encoding='utf-8-sig')

    print(f"\n{'='*60}")
    print(f"✓ HREINSUN LOKIÐ!")
    print(f"{'='*60}")
    print(f"✓ {len(df_hreint):,} raðir vistaðar í:")
    print(f"  {output_skra_nafn}")
    print(f"\nTölfræði:")
    print(f"  Árasvið: {df_hreint['Ár'].min()} - {df_hreint['Ár'].max()}")
    print(f"  Fjöldi fiskitegunda: {df_hreint['Fisktegund'].nunique()}")
    print(f"  Fjöldi hafna: {df_hreint['Löndunarhöfn'].nunique()}")
    print(f"  Heildarafli: {df_hreint['Afli'].sum():,.0f} kg")
    print(f"\nDæmi úr niðurstöðum:")
    print(df_hreint.head(10))


# --- Keyrsla ---
if __name__ == "__main__":
    import os
    import sys

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # Check command line argument
    use_sample = '--sample' in sys.argv or '-s' in sys.argv

    if use_sample:
        print("\n" + "="*60)
        print("KEYRIR Á SAMPLE GÖGNUM")
        print("="*60 + "\n")
        hraskra_nafn = os.path.join(project_root, 'data/sampledata/Afli_eftir_fisktegundum_FULL_CSV_Sample.csv')
        hreinskra_nafn = os.path.join(project_root, 'data/processed/afli_hreinsad_sample.csv')
    else:
        print("\n" + "="*60)
        print("KEYRIR Á FULLUM GÖGNUM")
        print("="*60 + "\n")
        hraskra_nafn = os.path.join(project_root, 'data/raw/Afli_eftir_fisktegundum_FULL_CSV.csv')
        hreinskra_nafn = os.path.join(project_root, 'data/processed/afli_hreinsad.csv')

    hreinsa_aflaskra(hraskra_nafn, hreinskra_nafn)
