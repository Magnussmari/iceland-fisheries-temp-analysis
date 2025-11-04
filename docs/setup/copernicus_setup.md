# Copernicus Marine Data - Quick Start Guide

## Hvað hefur verið búið til

✅ **Copernicus API fetcher** (`scripts/fetch_copernicus_data.py`)
- Sækir sjávarhitastig, seltu, strauma fyrir Ísland
- Automatic alignment með aflagögnum
- Test mode fyrir prófanir
- CSV umbreyting

✅ **Samanburðargagnasöfn** (`data/processed/comparison/`)
- 4 hreinsar CSV skrár með alignuð gögn
- Hafgögn (43 dagar) + Aflagögn (2 mánuðir)
- Merged dataset fyrir greiningar

✅ **Ítarleg skjölun**
- `docs/copernicus_api_guide.md` - API leiðbeiningar
- `data/processed/comparison/README.md` - Gagnasafnslýsing

---

## Uppsetning (5 mínútur)

### 1. Setja upp Copernicus Marine Toolbox

```bash
pip install copernicusmarine
```

### 2. Búa til aðgang (ÓKEYPIS)

1. Farðu á: https://data.marine.copernicus.eu/register
2. Skráðu þig (email + password)
3. Staðfestu email

### 3. Stilla credentials

```bash
copernicusmarine login
```

Sláðu inn username og password.

---

## Prófa að sækja gögn (2 mínútur)

```bash
python scripts/fetch_copernicus_data.py test
```

Þetta sækir:
- 1 mánuð af gögnum (feb 2018)
- Lítið svæði (Suðvesturland)
- ~10-30 MB
- Tekur 1-3 mínútur

Ef þetta virkar, þá ertu tilbúinn! 🎉

---

## Hvað næst?

### Valkostur 1: Nota fyrirliggjandi gögn

Við höfum þegar sample gögn frá feb-mars 2018:

```bash
# Skoða gögnin
python scripts/explore_netcdf.py

# Keyra samanburð
python scripts/prepare_comparison_datasets.py

# Opna í Streamlit
streamlit run streamlit_app.py
```

### Valkostur 2: Sækja fleiri gögn

Sækja öll gögn fyrir 2010-2025 (⚠️ TEKUR LANGAN TÍMA):

```bash
python scripts/fetch_copernicus_data.py full
```

⏰ **Viðvörun**: Þetta getur tekið 30-60 mínútur og myndar 2-3 GB skrá!

### Valkostur 3: Sérsniðið tímabil

```bash
python scripts/fetch_copernicus_data.py custom
# Sláðu inn dagsetningar
```

---

## Gögn sem eru sótt

### Copernicus Product

**GLOBAL_MULTIYEAR_PHY_001_030**
- Global Ocean Physics Reanalysis
- 1993 - present
- ~9km upplausn
- Dagleg meðaltöl

### Breytur

- ��� **Hitastig** sjávar (thetao)
- 🧂 **Selta** (so)
- ➡️ **Straumar** austri/norður (uo/vo)
- 🌊 **Yfirborðshæð** (zos)

### Svæði

**Ísland**: 63-67°N, 25-13°V, 0-50m dýpi

---

## Samanburðargögn

Við höfum búið til 4 CSV skrár í `data/processed/comparison/`:

1. **afli_filtered_2018-02-07_to_2018-03-21.csv**
   - Afli filtered fyrir hafgögna tímabilið
   - 196 færslur, 64 tonn

2. **ocean_daily_aggregated_2018-02-07_to_2018-03-21.csv**
   - Dagleg meðaltöl hafgagna
   - 43 dagar, 35 breytur
   - Meðal sjávarhiti: 0.84°C

3. **afli_daily_aggregated_2018-02-07_to_2018-03-21.csv**
   - Dagleg samantekt afla
   - 4 færslur (2 tegundir × 2 mánuðir)

4. **ocean_catch_merged_2018-02-07_to_2018-03-21.csv**
   - Merged dataset
   - 46 færslur
   - 2 með báðum gögnum, 42 bara hafgögn, 2 bara aflagögn

---

## Greiningardæmi

### Python

```python
import pandas as pd
import matplotlib.pyplot as plt

# Lesa merged gögn
df = pd.read_csv('data/processed/comparison/ocean_catch_merged_2018-02-07_to_2018-03-21.csv',
                 parse_dates=['Dags'])

# Sjávarhiti yfir tíma
ocean = df[df['_merge'] != 'left_only']
plt.plot(ocean['Dags'], ocean['sbe38_bow_temperature_mean'] - 273.15)
plt.xlabel('Date')
plt.ylabel('Sea Temperature (°C)')
plt.title('Ocean Temperature - Feb-Mar 2018')
plt.show()

# Fylgni (fyrir sameinuð punkta)
both = df[df['_merge'] == 'both']
if len(both) > 1:
    corr = both['Afli_heildar'].corr(both['sbe38_bow_temperature_mean'])
    print(f"Correlation: {corr:.3f}")
```

---

## Vandamál og lausnir

### "Authentication failed"

```bash
copernicusmarine login
```

### "Dataset not found"

Athugaðu dataset ID á: https://data.marine.copernicus.eu/

### Hægfara download

- Minnka tímabil
- Notaðu compression: `netcdf_compression_level=9`
- Prófaðu aftur síðar

### Disk space

Reiknaðu með:
- 1 ár: ~100-200 MB
- 16 ár (2010-2025): ~2-3 GB
- CSV format: 2-3x stærra

---

## Tenglar

📚 **Documentation**:
- Copernicus Marine: https://help.marine.copernicus.eu/
- Python API: https://help.marine.copernicus.eu/en/collections/4060068
- Product catalog: https://data.marine.copernicus.eu/products

📖 **Verkefnislýsingar**:
- `docs/copernicus_api_guide.md` - Ítarleg API leiðbeining
- `data/processed/comparison/README.md` - Gagnasafnslýsing
- `docs/copernicus_data.md` - Sample data skjölun

---

## Samantekt

**Þú ert tilbúinn til að:**

✅ Sækja hafgögn frá Copernicus Marine
✅ Bera saman haf og afla
✅ Greina tengsl umhverfis og veiða
✅ Búa til spálíkön

**Byrjaðu með:**

```bash
# 1. Prófa að sækja
python scripts/fetch_copernicus_data.py test

# 2. Skoða samanburð
python scripts/prepare_comparison_datasets.py

# 3. Opna Streamlit
streamlit run streamlit_app.py
```

Gangi þér vel! 🐟🌊

---

*Búið til: 2025-11-04*
*Útgáfa: 1.0*
