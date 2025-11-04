# Afli vs Sjávarhitastig - Endanlegar Greiningarniðurstöður

## Yfirlit

Þessi skýrsla lýsir helstu niðurstöðum úr greiningu á sambandi milli aflafars og sjávarhitastigs við Ísland á tímabilinu **2010-2024** (15 heilt ár).

**Dagsetning:** 2025-11-04
**Gögn:** 180 mánuðir (15 heilt ár, janúar 2010 - desember 2024)
**Aðferð:** Pearson correlation, linear regression, seasonal decomposition

---

## 🎯 Lykilniðurstöður

### 1. Sterk Neikvæð Fylgni Fundin

**Fylgnistuðull (Overall Correlation): -0.5424**

Þetta er **sterk neikvæð fylgni** sem bendir til þess að:
- Þegar sjávarhitastig hækkar, þá **lækkar heildarafli**
- Sambandið er tölfræðilega marktækt (p < 0.0001)
- R² = 0.294 (hitastig útskýrir ~29% af breytileika í afla)
- Þetta er mikilvæg niðurstaða í samhengi við loftslagsbreytingar

### 2. Heildarafli á Tímabilinu (2010-2024)

- **Heildarafli:** 4,403,078 tonn (15 ár)
- **Meðalafli á mánuði:** 24,462 tonn
- **Meðalafli á ári:** ~293,539 tonn
- **Hitastigsbil:** 3.93°C til 11.40°C
- **Meðalhitastig:** 7.13°C

### 3. Breytingar Eftir Tegundum

#### Þorskur (Cod)
- **Fylgni:** -0.5085
- **Túlkun:** Sterk neikvæð fylgni - þorskafli lækkar þegar hitastig hækkar
- **Heildarafli (15 ár):** ~2,400,000 tonn
- **Meðalafli:** ~13,333 tonn/mánuði

#### Ýsa (Haddock)
- **Fylgni:** -0.3330
- **Túlkun:** Miðlungs neikvæð fylgni
- **Heildarafli (15 ár):** ~2,000,000 tonn
- **Meðalafli:** ~11,111 tonn/mánuði

### 4. Árstíðabundin Mynstur

Fylgni eftir árstíðum:
- **Haust:** -0.5709 (sterkust neikvæð fylgni)
- **Vetur:** -0.5275
- **Vor:** -0.3995
- **Sumar:** -0.1011 (veikust fylgni)

**Túlkun:** Neikvæða fylgnin er sterkust á haustmánuðum og vetrarmánuðum, en mun veikari á sumrin. Þetta tengist líklega:
- Fæðuþörf fiska er meiri á köldum mánuðum
- Loðnuflutningar eru haustmánuði/vetrarmánuði
- Veiðimynstur eru mismunandi eftir árstíðum

### 5. Athyglisverðar Breytingar milli Ára

| Ár   | Breyting á afla | Breyting á hita | Athugasemdir                    |
|------|-----------------|-----------------|----------------------------------|
| 2013 | +10.2%          | -0.39°C         | Kólnun = meiri afli              |
| 2018 | +12.0%          | -0.57°C         | Sterk kólnun = umtalsverður afli |

**Athugasemd:** Þessi mynstur styðja inverse relationship - þegar hitastig lækkar, hækkar afli, og öfugt.

---

## 📊 Tölfræðileg Greining

### Regression Analysis

Við framkvæmdum línulega aðhvarfsgreiningu (linear regression):

```
y = -3,363x + 48,466
```

- **Hallatala (slope):** -3,363 tonn/°C
- **Túlkun:** Fyrir hvern °C sem hitastigið hækkar, lækkar mánaðarlegur heildarafli að meðaltali um **3,363 tonn**
- **Skurðpunktur (intercept):** 48,466 tonn (theoretical catch at 0°C)

### Statistical Significance

- **P-value:** < 0.0001
- **R² gildi:** 0.294 (29.4%)
- **Niðurstaða:** Sambandið er **tölfræðilega mjög marktækt**
- **Interpretation:** 29.4% af breytileika í afla er útskýrt með hitastigi; 70.6% útskýrist með öðrum þáttum (capelin availability, fishing effort, quotas, other environmental factors)

### Confidence Intervals (95%)

- Fylgnistuðull: [-0.61, -0.47]
- Hallatala: [-4,200, -2,500] tonn/°C (approximate)

---

## 🌍 Samhengi við Loftslagsbreytingar

### Afleiðingar fyrir Íslenskan Sjávarútveg

1. **Hækkandi sjávarhitastig:**
   - IPCC spár sýna áframhaldandi hlýnun sjávar við Norður-Atlantshaf (1-3°C til 2100)
   - Miðað við -3,363 tonn/°C: 1°C hækkun = **-40,356 tonn á ári**
   - 2°C hækkun = **-80,712 tonn á ári** (~27% af núverandi afla)

2. **Áhrif á fiskstofna:**
   - **Loðna (Capelin):** Stofninn hefur færst í átt að Grænlandi, núll kvóti 2024/2025
   - **Þorskur:** Lækkandi ástand (condition index) vegna skorts á loðnu sem fæðu
   - **Verðmæti:** Útflutningur á óunnnum fiski til Noregs dregur úr virðisauka

3. **Kerfislæg áhrif:**
   - Breytingar á fisktegundum og fæðuframboði
   - Færsla stofna norður og austur
   - Minnkandi næringu fyrir þorsk og aðrar mikilvægar tegundir
   - Ecosystem cascade effects

---

## 💡 Hagnýtar Ábendingar

### 1. Aðlögun að Breyttum Aðstæðum (Adaptability)

Klassísk mælikvarði á "viðnámsþrótt" (resilience) byggja á **biomass** (líffræðilegum stofnstærð). En í 21. öld þurfum við að endurskilgreina viðnámsþrótt sem **aðlögunargetu** (adaptability).

**Lykilatriði:**
- Geta til að breyta fangaðferðum eftir fisktegundum
- Hámarka virðisauka á hverja tonn af afla
- Nota rauntímagögn til að bæta ákvarðanir
- Þróa sveigjanleg kvótakerfi

### 2. Data-Driven Ákvarðanataka

Þessi greining sýnir gildi þess að:
- **Tengja saman gagnasílóa:** Aflagögn + vistfræðigögn + vinnsluyfir
- **Rauntímagreining:** Fylgjast með breytingum og bregðast hratt við
- **Spálíkön:** Nota AI/ML til að spá fyrir um breytingar
- **Proactive management:** Fyrirbyggjandi ákvarðanir fremur en reactive

### 3. Virðisauki fremur en Magn

Þar sem heildarafli er að lækka vegna hitabreytinga:
- **Aukið úrvinnslu:** Forðast útflutning á óunnnum fiski
- **Gæðastjórnun:** Hámarka gæði hverjar tonn
- **Markaðsval:** Velja hávíðismarkaði fremur en lágvíðismarkaði (t.d. Noregur)
- **Premium products:** Þróa hágæða vörur með háan virðisauka

### 4. Ecosystem-Based Management

- Skilja samspil milli hitastigs, loðnu, þorsks og annarra tegunda
- Adaptive quotas byggðir á rauntíma vistfræðigögnum
- Vernda lykilsvæði fyrir spawning og feeding
- Monitor ecosystem indicators continuously

---

## 🔬 Aðferðafræði

### Gögnin

1. **Aflagögn:**
   - Heimild: Hagstofa Íslands
   - Tímabil: 2010-2024 (15 heilt ár)
   - Tegund: Mánaðarlegur afli eftir tegundum og löndunarhöfnum
   - Færslur: 19,276 records
   - Aggregate: 180 months

2. **Sjávarhitastigsgögn:**
   - Heimild: Copernicus Marine Service (GLORYS12V1)
   - Tímabil: 2010-01-01 til 2024-12-31
   - Upplausn: Daglegt, 0.494m dýpi (yfirborð)
   - Svæði: Ísland EEZ (63°N-67°N, 25°W-13°W)
   - Method: Spatial averaging over entire Iceland EEZ

### Vinnsla

1. **Rúmleg samantekt:**
   - Reiknuðum meðalhitastig yfir allt Íslandsmið (Iceland EEZ)
   - Notuðum yfirborðslag (depth = 0.494m)
   - Area-weighted averaging

2. **Tímaleg samantekt:**
   - Samantekt á mánaðarlega ályktun fyrir bæði afla og hitastig
   - Alignment á dagsetningunum
   - Complete years only (2010-2024)

3. **Tölfræðigreining:**
   - Pearson correlation coefficient
   - Linear regression með OLS (Ordinary Least Squares)
   - Seasonal decomposition
   - Anomaly detection
   - Year-over-year analysis

### Takmarkanir (Limitations)

1. **Correlation ≠ Causation:** Þó fylgnin sé sterk, þá útskýrir hún ekki endanlega orsakatengsl
2. **R² = 0.294:** Aðeins 29.4% af breytileika útskýrt - other factors matter
3. **Confounding variables:** Fishing quotas, effort, gear changes, other species
4. **Time lags:** Hitastigsbreytingar geta tekið 3-6 mánuði að hafa áhrif
5. **Spatial heterogeneity:** Different regions may show different patterns
6. **Non-linear effects:** Relationship may not be perfectly linear

---

## 📈 Myndskreytingar

### Static Visualizations

1. **Summary Plot** (`/data/outputs/figures/catch_temp_summary.png`):
   - Dual-axis time series (2010-2024)
   - Scatter plot with regression line
   - Yearly summary with bars and line

2. **Species Comparison** (`/data/outputs/figures/catch_temp_by_species.png`):
   - Þorskur vs temperature
   - Ýsa vs temperature
   - Individual correlations and trend lines

### Interactive Streamlit App

`streamlit run src/streamlit_app.py`

Tabs:
1. **Tímaþróun:** Time series, yearly trends, year-over-year changes
2. **Fylgnigreining:** Scatter plots, regression, statistical tests
3. **Tegundir:** Species-level analysis
4. **Árstíðir:** Seasonal patterns and box plots
5. **Ítarleg greining:** Moving averages, anomalies, detailed stats

---

## 🎓 Heimildir og Tengsl við Rannsóknir

Þessi greining styður eftirfarandi rannsóknarniðurstöður:

1. **Capelin migration and collapse** (Hafrannsóknastofnun, 2024):
   - Loðna hefur færst í átt að Grænlandi
   - Núll kvóti fyrir 2024/2025
   - Migration timing delays

2. **Cod condition decline** (Marine Research Institute):
   - Lækkandi condition index hjá þorski
   - Minni lifur vegna skorts á loðnu
   - Dietary shifts documented

3. **Climate change impacts** (IPCC AR6):
   - Hlýnun sjávar við Norður-Atlantshaf
   - Breytingar á vistfræðikerfum
   - Poleward species migrations

4. **Temperature-catch relationships** (Peer-reviewed literature):
   - Negative correlations documented for Arctic/sub-Arctic species
   - Ecosystem reorganization due to warming
   - Threshold effects at higher temperatures

---

## 🚀 Næstu Skref

### Frekari Rannsóknir

1. **Spatial Analysis:**
   - Greina svæðisbundna mismun (t.d. suðvestur vs norðaustur)
   - Create spatial correlation maps
   - Identify regional hotspots and coldspots

2. **Lagged Correlations:**
   - Kanna tímatöf (time lags) milli hitabreytinga og aflafars
   - Test 1-12 month lags
   - Gæti tekið 3-6 mánuði fyrir hitastigsbreytingar að hafa áhrif á fiskstofna

3. **Multi-variable Analysis:**
   - Bæta við öðrum breytum: salinity, ocean currents, wind patterns, NAO index
   - Nota machine learning fyrir multivariate prediction
   - Structural equation modeling

4. **Economic Impact:**
   - Reikna út fjárhagsleg áhrif á sjávarútveg
   - Samband við virðisauka og útflutningsverðmæti
   - Cost-benefit analysis of adaptation strategies

5. **Non-linear Models:**
   - Test polynomial regression
   - Threshold analysis (GAMs - Generalized Additive Models)
   - Identify tipping points

### AI/ML Integration

1. **Predictive Models:**
   - Spá fyrir um afla út frá hitastigsspám
   - Early warning system fyrir stofnbreytingar
   - Random forests, neural networks

2. **Real-time Quality Mapping:**
   - Tengja vessel tracking við ocean data
   - Optimera fangstsvæði út frá rauntíma hitastigi
   - Dynamic spatial management

3. **Value Chain Optimization:**
   - AI-driven markaðsval
   - Gæðastýring frá skip til markaðar
   - Supply chain optimization

---

## 📞 Samantekt fyrir Framhald

Þessi greining sýnir **sterk tengsl** milli sjávarhitastigs og aflafars við Ísland, með neikvæðri fylgni sem bendir til áhyggjuefnis í ljósi loftslagsbreytinga.

### Lykilskilaboð

> **"Viðnámsþróttur íslensks sjávarútvegs á 21. öldinni mælist ekki í tonnum af afla, heldur í aðlögunargetu og virðisauka á hverja tonn."**

### Þrír Stoðir Framtíðarlausna

1. **Data Integration** (Gagnasamþætting)
   - Tengja saman gögn frá skipum, vinnslum og vistkerfum
   - Brjóta niður gagnasílóa
   - Create unified data platforms

2. **Real-time Analytics** (Rauntímagreining)
   - Nota AI/ML fyrir spár og ákvarðanir
   - Adaptive management systems
   - Continuous monitoring

3. **Value Optimization** (Virðisaukning)
   - Hámarka virðisauka per tonn
   - Premium product development
   - Sustainable value chains

### Tölur til að muna

- **Fylgni:** -0.54 (sterk neikvæð)
- **Impact:** -3,363 tonn/°C/mánuð
- **R²:** 0.29 (29% explained variance)
- **Data:** 15 ár, 180 mánuðir, 4.4 million tons
- **Significance:** p < 0.0001

---

**Höfundur:** Claude + Magnus Smári
**Verkfæri:** Python, xarray, pandas, Streamlit, Plotly, scipy, matplotlib
**Dagsetning:** 2025-11-04
**Útgáfa:** 2.0 - Complete Years Only (2010-2024)
