# Quick Start Guide - Afli vs Hitastig Greining

## Þú ert Kominn!

Öll gögn hafa verið unnin og Streamlit appið er tilbúið til notkunar!

---

## 🎯 Það sem hefur verið gert

### ✅ Gagnasöfn Unnin

1. **Aflagögn (Catch Data)**
   - ✓ 19,277 færslur hreinsuð
   - ✓ Tímabil: 2010-2025
   - ✓ Tegundir: Þorskur, Ýsa
   - ✓ Staðsetning: `/data/processed/afli_eftir_fisktegundum/Catch_data.csv`

2. **Sjávarhitastigsgögn (Ocean Temperature)**
   - ✓ 1.7GB NetCDF skrá
   - ✓ Tímabil: 2010-01-01 til 2025-09-16 (5,738 dagar)
   - ✓ Svæði: Ísland EEZ (63°N-67°N, 25°W-13°W)
   - ✓ Staðsetning: `/data/raw/Copernicus/fetched/`

3. **Comparison Datasets (Samanburðargögn)**
   - ✓ Mánaðarleg samantekt: afli + hitastig
   - ✓ Fylgnigreiningar reiknað
   - ✓ Árstíðamynstur
   - ✓ Staðsetning: `/data/processed/comparison/`

### ✅ Tölfræðilegar Niðurstöður

**Lykilniðurstaða: Fylgni = -0.5499** (sterk neikvæð fylgni)
- Þegar hitastig hækkar, lækkar afli
- Tölfræðilega marktækt samband (p < 0.0001)
- Sterkust í haust og vetur, veikari í sumar

---

## 🚀 Hvernig á að nota

### 1. Opna Streamlit Appið

Appið er nú þegar í gangi á: **http://localhost:8501**

**Ef þú þarft að ræsa það aftur:**

```bash
streamlit run src/streamlit_app.py
```

### 2. Skoða Mismunandi Flipa

Appið er skipulagt í 5 tabs:

#### 📈 Tab 1: Tímaþróun
- Tvöfaldur ás línurit: Afli (blátt) + Hitastig (rautt)
- Árleg samanburður með súluritum
- Year-over-year prósentubreytingar

**Hvað á að leita að:**
- Hvort línurnar fara í gagnstæðar áttir (inverse relationship)
- 2025: Mikil hitahækkun (+1.05°C) með miklum aflaláki (-26.3%)

#### 🔍 Tab 2: Fylgnigreining
- Dreifirit (scatter plot) með regression línu
- Correlation matrix
- Tölfræðileg samantekt

**Hvað á að leita að:**
- Neikvæð hallatala á regression línunni
- P-value < 0.05 (tölfræðilega marktækt)
- Fyrir hvern °C hækkunar lækkar afli um ~3,500 tonn

#### 🐟 Tab 3: Tegundir
- Samanburður milli þorsks og ýsu
- Fylgni per tegund
- Scatter plots per tegund

**Hvað á að leita að:**
- Þorskur: -0.52 fylgni (sterkari en ýsa)
- Ýsa: -0.31 fylgni
- Báðar tegundir sýna neikvæða fylgni

#### 🗓️ Tab 4: Árstíðir
- Box plots eftir árstíðum
- Seasonal correlations
- Samantektartöflur

**Hvað á að leita að:**
- Haust og vetur: Sterkust neikvæð fylgni (-0.58, -0.53)
- Sumar: Veikust fylgni (-0.09)
- Árstíðabundin mynstur í bæði afla og hitastigi

#### 📊 Tab 5: Ítarleg Greining
- Hreyfanleg meðaltöl (moving averages)
- Anomaly detection (frávik)
- Tölfræðileg samantekt

**Hvað á að leita að:**
- Langtímaþróun með moving averages
- Outliers og óvenjulegar mánuðir
- Distribution af afla og hitastigi

### 3. Nota Síur (Filters)

**Árabils síurnar í hliðarslánni:**
- Dragðu til að velja tímabil (t.d. 2015-2020)
- Öll gröf og tölfræði uppfærast sjálfkrafa

---

## 📊 Helstu Niðurstöður til að Nefna

### 1. Sterk Neikvæð Fylgni

> "Við fundum **-0.55 fylgni** milli sjávarhitastigs og aflafars. Það þýðir að fyrir hvern gráðu sem hitastigið hækkar, lækkar mánaðarlegur afli að meðaltali um **3,500 tonn**."

### 2. 2025 Áhyggjur

> "Árið 2025 sáum við +1.05°C hækkun í hitastigi samhliða **-26.3% lækkun á afla**. Þetta er sterkasta dæmið af inverse relationship sem við sjáum í gögnunum."

### 3. Árstíðamunur

> "Neikvæða fylgnin er sterkust á haustmánuðum (-0.58) og vetrarmánuðum (-0.53), en mun veikari á sumrin (-0.09)."

### 4. Tegundiramunur

> "Þorskur sýnir sterkari neikvæða fylgni (-0.52) en ýsa (-0.31), sem gæti tengst mismunandi fæðuþörfum og aðlögunareleiðum."

### 5. Capelin Tenging

> "Þessar niðurstöður eru í samræmi við rannsóknir Hafrannsóknastofnunar sem sýna að loðna (capelin) hefur færst í átt að Grænlandi þar sem hitastigið hækkar, sem hefur bein áhrif á þorskstofninn þar sem loðna er aðalfæða þorsks."

---

## 🎓 Fyrir Kynningu/Framhald

### Lykilskilaboð

**Thesis:**
> Viðnámsþróttur (resilience) íslensks sjávarútvegs á 21. öldinni mælist ekki í tonnum af afla, heldur í **aðlögunargetu** (adaptability) og **virðisauka á hverja tonn**.

**Rökstuðningur:**
1. Heildarafli mun halda áfram að lækka vegna loftslagsbreytinga
2. Hitastig sjávar er að hækka samkvæmt IPCC spám
3. Það sem skiptir máli er hvernig við **aðlagast** þessum breytingum

**Lausnir:**
1. **Data Integration:** Tengja saman gögn frá skipum, vinnslum og vistfræði
2. **Real-time Analytics:** Nota rauntímagögn til að taka betri ákvarðanir
3. **AI/ML fyrir spár:** Spá fyrir um breytingar og bregðast hratt við
4. **Virðisauki:** Auka virðisauka á hverja tonn í stað þess að einblína á magn

### Quotes til að nota

> "Gögn sýna að fyrir hvern °C sem hitastigið hækkar, þá lækkar mánaðarlegur afli um 3,500 tonn. Með IPCC spám um 2-4°C hlýnun á næstu áratugum er þetta ekki bara áhyggjuefni - það er raunveruleikinn sem við þurfum að undirbúa okkur fyrir."

> "Árið 2025 er perfect case study: +1°C hitahækkun, -26% aflalækkun. Þetta er ekki tilviljun - þetta er kerfislæg breyting sem við þurfum að skilja og aðlagast að."

> "Klassískir mælikvarðar á 'resilience' horfa á biomass - hversu mikinn fisk getum við veitt? En í 21. öld þurfum við að endurskilgreina resilience sem adaptability - hversu vel getum við lagað okkur að breyttum aðstæðum?"

---

## 📁 Mikilvægar Skrár

### Gögn
- **Afli:** `/data/processed/afli_eftir_fisktegundum/Catch_data.csv`
- **Hitastig:** `/data/raw/Copernicus/fetched/copernicus_iceland_ocean_20100101_20250930.nc`
- **Comparison:** `/data/processed/comparison/` (6 CSV skrár)

### Scripts
- **Comparison greining:** `/scripts/03_data_processing/create_catch_temp_comparison.py`

### App
- **Streamlit:** `/src/streamlit_app.py`

### Skýrslur
- **Niðurstöður:** `/ANALYSIS_RESULTS.md` (þessi skrá!)
- **Quick Start:** `/QUICK_START.md`

---

## 🔧 Troubleshooting

### Appið opnast ekki

```bash
# Athugaðu hvort það sé þegar í gangi
lsof -i:8501

# Drepa gamla process
lsof -ti:8501 | xargs kill -9

# Ræsa aftur
streamlit run src/streamlit_app.py
```

### Gögn finnast ekki

```bash
# Athugaðu hvort öll gögn séu til staðar
ls -lh data/processed/comparison/

# Ef ekki, keyrðu comparison scriptuna aftur
python scripts/03_data_processing/create_catch_temp_comparison.py
```

### Import villur

```bash
# Athugaðu dependencies
pip list | grep -E "(pandas|numpy|xarray|streamlit|plotly|scipy)"

# Ef eitthvað vantar
pip install -r requirements.txt
```

---

## 🎉 Gangi þér vel!

Ef þú hefur spurningar eða vilt gera breytingar:

1. **Breyta litum/stílum:** Opnaðu `src/streamlit_app.py` og breyttu CSS í byrjun skrárinnar
2. **Bæta við visualization:** Bættu við í viðeigandi tab í `src/streamlit_app.py`
3. **Endurkeyra greiningu:** `python scripts/03_data_processing/create_catch_temp_comparison.py`

**Pro tip:** Notaðu screenshot verkfærið í vafranum til að taka myndir af gröfunum fyrir kynninguna!

---

**Appið er núna í gangi á: http://localhost:8501**

**Opnaðu í vafranum og skoðaðu!** 🎯
