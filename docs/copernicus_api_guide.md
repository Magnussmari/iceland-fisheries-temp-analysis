# Copernicus Marine API - Leiðbeiningar

## Yfirlit

Þessi leiðbeining útskýrir hvernig á að sækja hafgögn frá Copernicus Marine Service til að bera saman við íslensk aflagögn.

## Uppsetning

### 1. Setja upp Copernicus Marine Toolbox

```bash
pip install copernicusmarine
```

### 2. Stilla aðgangsgögn

Þú þarft ókeypis aðgang að Copernicus Marine Service:

1. Farðu á: https://data.marine.copernicus.eu/register
2. Skráðu þig (ókeypis)
3. Stilltu credentials:

```bash
copernicusmarine login
```

Sláðu inn username og password þegar beðið er um það.

## Notkun á fetch skriptunni

### Prófunargögn (MÆLT MEÐ FYRST!)

Sækir lítið próf (1 mánuður, lítið svæði) til að prófa að allt virki:

```bash
python scripts/fetch_copernicus_data.py
# Veldu: 1 (Test)
```

**Eða beint:**
```bash
python scripts/fetch_copernicus_data.py test
```

Þetta sækir:
- **Svæði**: Suðvesturland (63.5-64.5°N, 21-24°V)
- **Tímabil**: Febrúar 2018
- **Stærð**: ~10-50 MB
- **Tími**: 1-3 mínútur

### Full gagnaöflun

Sækir öll gögn fyrir sama tímabil og aflagögn (2010-2025):

```bash
python scripts/fetch_copernicus_data.py
# Veldu: 2 (Full)
```

⚠️ **VIÐVÖRUN**:
- Getur tekið 30-60 mínútur eða lengur
- Skráin getur orðið nokkur GB
- Notaðu góða netsamb

andi

### Sérsniðið tímabil

```bash
python scripts/fetch_copernicus_data.py
# Veldu: 3 (Custom)
# Sláðu inn dagsetningar
```

## Gagnasafn sem er sótt

### Product Information

**Product**: GLOBAL_MULTIYEAR_PHY_001_030
**Dataset**: cmems_mod_glo_phy_my_0.083deg_P1D-m

- **Upplausn**: ~9 km (0.083°)
- **Tíðni**: Dagleg meðaltöl
- **Tímabil**: 1993 - nútími
- **Uppfært**: Mánaðarlega

### Breytur sem eru sóttar

| Breyta | Lýsing | Eining |
|--------|--------|--------|
| `thetao` | Hitastig sjávar | °C |
| `so` | Selta sjávar | PSU (Practical Salinity Unit) |
| `uo` | Austurvindstraumur | m/s |
| `vo` | Norðurvindstraumur | m/s |
| `zos` | Hæð sjávarflatar | m |

### Landsvæði

**Íslensku landgrunnssvæðið:**
- Breidd: 63°N - 67°N
- Lengd: 25°V - 13°V
- Dýpi: 0 - 50m (yfirborðslag)

## Úttaksskrár

### NetCDF Format (.nc)

Upprunalegt snið frá Copernicus:

```python
import xarray as xr

# Opna skrá
ds = xr.open_dataset('copernicus_iceland_ocean_20100101_20251001.nc')

# Skoða
print(ds)

# Velja hitastig
temp = ds['thetao']
print(temp.mean())
```

### CSV Format (.csv)

Umreiknað fyrir auðveldari greiningu:

```python
import pandas as pd

# Lesa CSV
df = pd.read_csv('copernicus_iceland_ocean_20100101_20251001.csv')

# Meðalhiti
print(df['thetao'].mean())
```

## Algengar villur og lausnir

### 1. "Authentication failed"

**Lausn:**
```bash
copernicusmarine login
```

Athugaðu að þú sért með rétt username/password.

### 2. "Dataset not found"

**Ástæða**: Gagnasafnið gæti verið með annað nafn eða útgáfu.

**Lausn**: Athugaðu dataset ID á:
https://data.marine.copernicus.eu/

### 3. "Time range out of bounds"

**Ástæða**: Gagnasafnið nær bara til 1993-present.

**Lausn**: Takmarka tímabilið við 1993 eða síðar.

### 4. Hægt að sækja / timeout

**Ástæðir:**
- Stór beiðni
- Hæg nettenging
- Þjónusta upptekinn

**Lausnir:**
- Minnka svæði eða tímabil
- Reyndu aftur síðar
- Notaðu `netcdf_compression_level=9` fyrir minni skrá

## Ábendingar

### Hraða niðurhal

1. **Minnka upplausn**: Nota grófa gagnasafn ef til er
2. **Takmarka breytur**: Bara sækja það sem þarf
3. **Compression**: Nota `netcdf_compression_level=6` eða hærra
4. **Zarr format**: Hraðara en NetCDF fyrir stór gögn

### Sækja í hlutum

Ef full öflun mistekst, sæktu í árabútum:

```python
for year in range(2010, 2026):
    fetch_ocean_temperature_data(
        start_date=f"{year}-01-01",
        end_date=f"{year}-12-31",
        output_dir=f"data/raw/Copernicus/year_{year}"
    )
```

### Disk space

Reiknaðu með:
- **1 ár, Ísland, daglega**: ~100-200 MB
- **16 ár (2010-2025)**: ~2-3 GB
- **CSV umbreytingar**: 2-3x stærra

## Frekari upplýsingar

### Copernicus Marine Documentation

- **Main docs**: https://help.marine.copernicus.eu/
- **Python API**: https://help.marine.copernicus.eu/en/collections/4060068-copernicus-marine-toolbox
- **Product catalog**: https://data.marine.copernicus.eu/products

### Product details

Product page:
https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030

Inniheldur:
- Hraunvarp (reanalysis) gögn frá 1993
- Global Ocean model (GLORYS12v1)
- Assimilated með observation data
- Uppfært mánaðarlega

## Næstu skref

Eftir að hafa sótt gögnin:

1. **Skoða**: Nota `explore_netcdf.py` til að skoða
2. **Bera saman**: Keyra `prepare_comparison_datasets.py`
3. **Sjónræna**: Opna í Streamlit app
4. **Greina**: Kanna fylgni milli hitastigs og afla

---

*Skjal síðast uppfært: 2025-11-04*
*Útgáfa: 1.0*
