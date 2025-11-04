# Samanburðargagnasöfn - Ocean & Catch Data Comparison

## Yfirlit

Þessi mappa inniheldur gagnasöfn sem hafa verið unnin til samanburðar á **hafgögnum** (sjávarhitastig, straumar, selta) og **aflagögnum** (veiðar eftir tegundum og höfnum).

Tilgangurinn er að greina tengsl milli umhverfisaðstæðna í sjónum og veiðiafkomu íslenskra fiskiskipa.

---

## Skrár í þessari möppu

### 1. **afli_filtered_2018-02-07_to_2018-03-21.csv**

**Lýsing**: Aflagögn síuð fyrir sama tímabil og hafgögnin
**Tímabil**: 7. febrúar - 21. mars 2018
**Fjöldi færslna**: 196
**Heildarafli**: 63,766,603 kg (~64 þúsund tonn)

**Dálkar**:
- `Dags` - Dagsetning (fyrsti dagur mánaðar)
- `Ár` - Ár (2018)
- `Mánuður` - Íslenskt nafn mánaðar (febrúar, mars)
- `Fisktegund` - Þorskur eða Ýsa
- `Löndunarhöfn` - Nafn hafnar
- `Afli` - Magn í kílógrömmum

**Notkun**: Upphafleg aflaskrá með mánaðarlegri upplausn fyrir rannsóknartímabilið.

---

### 2. **ocean_daily_aggregated_2018-02-07_to_2018-03-21.csv**

**Lýsing**: Hafgögn sameinuð í daglegt meðaltal
**Tímabil**: 7. febrúar - 21. mars 2018
**Fjöldi daga**: 43
**Upprunaleg tíðni**: 10 mínútna mælingar → dagleg meðaltöl

**Lykilbreytur** (allar með _mean, _std, _min, _max):
- `sbe38_bow_temperature` - Sjávarhitastig í Kelvin
- `water_speed_nmea` - Skipshraði (m/s)
- `heading_nmea` - Stefna skips (gráður)
- `wind_direction` - Vindátt (gráður)
- `latitude_nmea` / `longitude_nmea` - GPS staðsetning
- `measured_air_temperature` - Lofthitastig (K)
- `measured_air_pressure` - Loftþrýstingur (Pa)
- `measured_relative_humidity` - Rakastig (%)

**Tölfræði**:
- Meðal sjávarhiti: 0.84°C (273.99K)
- Hitastig svið: -0.05°C til 3.48°C
- Svæði: 65-76°N, 28-3°V (Íslenskt landgrunnssvæði)

**Notkun**: Dagleg samantekt á umhverfisgögnum til að passa við aflaskrána.

---

### 3. **afli_daily_aggregated_2018-02-07_to_2018-03-21.csv**

**Lýsing**: Aflagögn sameinuð í daglega samantekt eftir tegundum
**Fjöldi dagsetningar**: 4 (2 mánuðir × 2 tegundir)
**Heildarafli**: 63,766,603 kg

**Dálkar**:
- `Dags` - Dagsetning
- `Fisktegund` - Þorskur eða Ýsa
- `Afli_heildar` - Heildarafli fyrir tegund á þeim degi (kg)
- `Afli_medal` - Meðalafli per höfn (kg)
- `Fjoldi_hafna` - Fjöldi hafna með aflann þann dag
- `Hafnir` - Listi yfir hafnir

**Notkun**: Sameinað aflayfirlit til að bera saman við hafgögn.

---

### 4. **ocean_catch_merged_2018-02-07_to_2018-03-21.csv**

**Lýsing**: Sameinuð gagnasafn með bæði haf- og aflagögnum
**Fjöldi færslna**: 46
**Merge vísir**: `_merge` dálkur segir til um hvort gögn séu frá báðum, bara hafgögnum, eða bara aflagögnum

**_merge gildi**:
- `both` (2 færslur) - Báðir gagnagjafar hafa upplýsingar
- `left_only` (2 færslur) - Bara aflagögn (ekki hafgögn þann dag)
- `right_only` (42 færslur) - Bara hafgögn (ekki afli þann dag, þar sem afli er mánaðarlega)

**Innihald**: Öll dálkar frá bæði ocean_daily og afli_daily

**Notkun**: Aðalgagnasafnið fyrir greiningar á tengslum milli umhverfis og afla.

---

## Tímabilsgreining

### Hvers vegna febrúar-mars 2018?

Þetta tímabil var valið vegna:

1. **Vetrarveður**: Febrúar og mars eru vetrarmánuðir með lágan sjávarhita
2. **Hrygningartími**: Þorskur hrygn enda vetrar/byrjun vors
3. **Gagnafræði**: Copernicus sample gögn náðu yfir þetta tímabil
4. **Veiðiár**: Mikilvægur tími í íslenskum sjávarútvegi

### Takmörk á gögnum

**Vandamál**:
- Aflagögn eru **mánaðarleg** (fyrsti dagur mánaðar)
- Hafgögn eru **dagleg** meðaltöl
- Þetta veldur því að merge hefur aðeins 2 sameiginlega punkta

**Lausn fyrir framtíðargreiningar**:
1. Safna fleiri árum af hafgögnum
2. Nota mánaðarlega meðaltöl fyrir bæði gagnasöfn
3. Nota interpolation til að fylla inn í göt

---

## Hvernig voru gögnin búin til?

### Keyrsluskript

```bash
python scripts/prepare_comparison_datasets.py
```

### Ferlið

1. **Hleðsla**:
   - Les `Ocean_temp_FULL.csv` (6,067 10-mínútna mælingar)
   - Les `afli_hreinsad_FULL.csv` (19,276 mánaðarlegar færslur)

2. **Síun**:
   - Sýnar aflagögn fyrir sama tímabil og hafgögn
   - Býr til 196 aflafærslur fyrir feb-mars 2018

3. **Samanlögð**:
   - Reiknar daglegt meðaltal fyrir hafgögn (43 dagar)
   - Safnar saman afla eftir degi og tegund (4 færslur)

4. **Sameinun**:
   - Merge á dagsetningum
   - Býr til merged gagnasafn með merge indicator

5. **Vistun**:
   - 4 CSV skrár í `data/processed/comparison/`

---

## Notkun í greiningum

### Python dæmi

```python
import pandas as pd
import matplotlib.pyplot as plt

# Lesa sameinuð gögn
df = pd.read_csv('data/processed/comparison/ocean_catch_merged_2018-02-07_to_2018-03-21.csv',
                 parse_dates=['Dags'])

# Skoða gögn með báðum uppruna
both_df = df[df['_merge'] == 'both']
print(both_df[['Dags', 'Fisktegund', 'Afli_heildar', 'sbe38_bow_temperature_mean']])

# Teikna sjávarhita yfir tíma
ocean_df = df[df['_merge'].isin(['both', 'right_only'])]
plt.figure(figsize=(12, 5))
plt.plot(ocean_df['Dags'], ocean_df['sbe38_bow_temperature_mean'] - 273.15)
plt.xlabel('Dagsetning')
plt.ylabel('Sjávarhitastig (°C)')
plt.title('Sjávarhiti - Feb-Mars 2018')
plt.grid(True)
plt.show()

# Fylgnigreining (fyrir þá daga sem hafa bæði)
if len(both_df) > 0:
    correlation = both_df['Afli_heildar'].corr(both_df['sbe38_bow_temperature_mean'])
    print(f"Fylgni milli afla og hitastigs: {correlation:.3f}")
```

### R dæmi

```r
library(tidyverse)

# Lesa gögn
df <- read_csv('data/processed/comparison/ocean_catch_merged_2018-02-07_to_2018-03-21.csv')

# Filter fyrir sameinuð gögn
both_df <- df %>% filter(`_merge` == 'both')

# Teikna
ggplot(both_df, aes(x = sbe38_bow_temperature_mean - 273.15, y = Afli_heildar / 1e6)) +
  geom_point(aes(color = Fisktegund), size = 3) +
  geom_smooth(method = 'lm') +
  labs(
    title = 'Afli vs Sjávarhitastig',
    x = 'Sjávarhitastig (°C)',
    y = 'Afli (þúsund tonn)',
    color = 'Tegund'
  ) +
  theme_minimal()
```

---

## Mögulegar greiningar

### 1. Tengsl hitastigs og afla

**Spurnir**:
- Er fylgni milli sjávarhitastigs og aflastærðar?
- Hafa mismunandi tegundir mismunandi hitaskýli?
- Hverjir eru ákjósanlegir hitamörk fyrir Þorsk/Ýsu?

**Aðferðir**:
- Correlation analysis
- Linear/polynomial regression
- Moving averages

### 2. Landfræðileg greining

**Spurningar**:
- Hvar í sjónum voru mælingarnar teknar?
- Passa veiðisvæði við hitaskilyrði?
- Er munur á afla eftir svæðum?

**Aðferðir**:
- Mapping (GPS coordinates)
- Spatial clustering
- Heatmaps

### 3. Tímaraðagreining

**Spurningar**:
- Hvernig þróaðist hitastigið yfir tímabilið?
- Er árstíðabundið mynstur í afla?
- Eru lag-áhrif (delayed effects)?

**Aðferðir**:
- Time series decomposition
- Cross-correlation með lags
- Trend analysis

### 4. Fjölþátta greining

**Spurningar**:
- Hvernig hafa vindur + hitastig + selta áhrif á afla?
- Hvaða umhverfisbreytur skýra best veiðiafkomu?
- Má spá fyrir um afla með umhverfisgögnum?

**Aðferðir**:
- Multiple regression
- Random Forest / ML models
- Principal Component Analysis (PCA)

---

## Takmarkanir og viðvaranir

### Gagnagæði

1. **Tímabil stuttu**: Aðeins 1.5 mánuðir með gögnum
2. **Temporal mismatch**: Afli mánaðarlegur, hafgögn dagleg
3. **Spatial mismatch**: Hafmælingar eru punktmælingar, afli er heildarafli fyrir allt landið
4. **Fáir sameiginlegir punktar**: Bara 2 dagsetningar hafa bæði haf- og aflagögn

### Túlkun

⚠️ **Varúð við að draga of sterkar ályktanir!**

- Lítið tímabil gerir fylgnigreiningar óstöðugar
- Correlation ≠ Causation
- Afli hefur margþættar orsakir (kvóti, veður, markaður, tækni)
- Umhverfisgögn eru frá einum stað, ekki öllu Íslandi

### Bæta gagnasafnið

**Til að fá betri greiningar**:

1. **Sækja fleiri ár** frá Copernicus (2010-2025)
2. **Setja saman** mánaðarlega meðaltöl fyrir bæði gagnasöfn
3. **Bæta við** fleiri umhverfisbreytum (primary productivity, etc.)
4. **Safna** stöðvargögnum frá sértækum veiðisvæðum

---

## Heimildir og tilvísanir

### Gagnasafn

**Aflagögn**:
- Heimild: Fiskistofa / Hagstofa Íslands
- Tímabil: 2010-2025
- Upprunalegt format: SJA01101 tafla
- Hreinsunarskript: `scripts/hreinsa_gogn_v4.py`

**Hafgögn**:
- Heimild: Copernicus Marine Service (IGP Alliance rannsóknarferð)
- Skjal: `igp_alliance_surface_met_20180207_qc3_10min.nc`
- Tímabil: 2018-02-07 til 2018-03-21
- Mælingatíðni: 10 mínútur
- Gæðastýring: QC3 level

### Vinnslu skjöl

- Hreinsunarskript: `scripts/hreinsa_gogn_v4.py`
- Samanburðarskript: `scripts/prepare_comparison_datasets.py`
- NetCDF könnunarskript: `scripts/explore_netcdf.py`

### Tengd skjöl

- `docs/afli_eftir_fisktegundum.md` - Aflagagna skjölun
- `docs/copernicus_data.md` - Hafgagna skjölun
- `README.md` - Aðal verkefnislýsing

---

## Framhald

### Næstu skref

1. ✅ Búa til samanburðargagnasöfn
2. ⏳ Sækja fleiri ár af Copernicus gögnum
3. ⏳ Setja upp mánaðarlega sameiningu
4. ⏳ Keyra fylgnigreiningar
5. ⏳ Búa til spálíkan (ML model)
6. ⏳ Sjónræn framsetning í Streamlit

### Frekari rannsóknir

- Tengja við loðnubrestgögn (2024-2025)
- Bera saman við þorskaastand gögn
- Greina áhrif loftslagsbreytinga yfir lengri tíma
- Kortleggja veiðisvæði með umhverfisgögnum

---

*Skjal síðast uppfært: 2025-11-04*
*Útgáfa: 1.0*
*Höfundur: Magnús Smári - Sjávarútvegs DataDemo*
