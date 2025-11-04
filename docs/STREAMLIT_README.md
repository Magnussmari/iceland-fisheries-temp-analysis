# Streamlit Gagnasýning - Sjávarútvegs DataDemo

## Yfirlit

Þetta er gagnvirkt vefforrit (Streamlit app) fyrir gagnagreiningu og sjónræna framsetningu á:
1. **Aflagögnum** - Íslenskur afli eftir fisktegundum og löndunarhöfnum (2010-2025)
2. **Copernicus hafgögnum** - Sjávarhitastig, vindhraði, staðsetningar o.fl.

## Uppsetning

### 1. Setja upp Python umhverfi

```bash
# Búa til virtual environment (optional en mælt með)
python -m venv .venv

# Activate
# Á macOS/Linux:
source .venv/bin/activate
# Á Windows:
.venv\Scripts\activate
```

### 2. Setja upp nauðsynlega pakka

```bash
pip install -r requirements.txt
```

**Nauðsynlegir pakkar:**
- `streamlit` - Vefforritið sjálft
- `pandas` - Gagnavinnsla
- `plotly` - Gagnvirk myndræn framsetning
- `xarray` - NetCDF gagnavinnsla
- `netCDF4` - NetCDF file handler

### 3. Hreinsa gögn (ef ekki þegar gert)

```bash
# Hreinsa aflaskrár
python scripts/hreinsa_gogn_v4.py

# Eða sample gögn fyrir prófun
python scripts/hreinsa_gogn_v4.py --sample
```

## Keyrsla

### Ræsa Streamlit forritið

```bash
streamlit run streamlit_app.py
```

Þetta opnar vafra sjálfkrafa á `http://localhost:8501`

### Aðrar keyrsluaðferðir

```bash
# Tilgreina port
streamlit run streamlit_app.py --server.port 8502

# Opna ekki vafra sjálfkrafa
streamlit run streamlit_app.py --server.headless true

# Debug mode
streamlit run streamlit_app.py --logger.level=debug
```

## Notkun

### Aflagögn (Catch Data)

1. Veldu "Aflagögn (Catch Data)" í hliðarvalmynd
2. Stilltu síur:
   - **Fisktegund**: Veldu eina tegund eða allar
   - **Ár**: Dragðu slider til að velja tímabil
   - **Löndunarhöfn**: Veldu höfn eða allar
3. Skoðaðu gögn í flipum:
   - **📈 Tímaþróun**: Línurit og súlurit yfir tíma
   - **🗺️ Hafnir**: Topp hafnir og sundurliðun eftir tegundum
   - **📊 Tölfræði**: Tölfræðileg samantekt og dreifing
   - **📅 Árstíðir**: Mánaðarleg mynstur og hitakort

### Copernicus Hafgögn (Ocean Data)

1. Veldu "Copernicus hafgögn (Ocean Data)"
2. Veldu NetCDF skrá úr listanum
3. Veldu breytu til að skoða (t.d. sjávarhitastig, vindhraði)
4. Skoðaðu í flipum:
   - **📈 Tímaröð**: Tímaþróun valda breyta
   - **📊 Tölfræði**: Lýsandi tölfræði og dreifing
   - **🗺️ Rúmfræði**: Landfræðileg kortlagning (ef við á)
5. Notaðu "📥 Umbreyta í CSV" til að exporta gögn

## Eiginleikar

### Gagnvirk sjónræn framsetning

Öll myndrit eru gagnvirk (Plotly):
- **Zoom**: Draga til að zooma inn
- **Pan**: Shift + drag til að pompa
- **Hover**: Færa mús yfir punkta fyrir nánari upplýsingar
- **Download**: Takki í efra hægra horni til að sækja mynd

### Síun gagna

- Rauntíma uppfærsla þegar síur breytast
- Mæligildi (metrics) uppfærast samhliða
- Cached gögn fyrir hraða frammistöðu

### Export valkostir

- CSV export beint úr Copernicus gögnum
- Hnappir til að sækja (download buttons)

## Skipulag forrits

```
streamlit_app.py
├── Grunnstillingar (page config)
├── Sidebar (hliðarvalmynd)
│   ├── Gagnasafnsval
│   └── Síur
├── Aflagögn Module
│   ├── Gagnahleðsla (cached)
│   ├── Síur
│   ├── Mæligildi
│   └── 4 flipar með myndrænni framsetningu
└── Copernicus Module
    ├── NetCDF hleðsla (cached)
    ├── Upplýsingar um gagnasafn
    ├── Breytuval
    └── 3 flipar með greiningu
```

## Bestu venjur

### 1. Nota Sample gögn fyrir prófanir

Hakaðu við "Nota sample gögn" til að prófa forritið hraðar án þess að hlaða öllum gögnum.

### 2. Cache notkun

Streamlit geymir (cache) gögn sjálfkrafa:
- `@st.cache_data` fyrir gagnalestur
- Gögn endurhlaðast bara ef skrár breytast
- Til að hreinsa cache: Ýttu á `C` í vafranum

### 3. Hraðavandamál

Ef forritið er hægt:
- Notaðu sample gögn fyrst
- Takmarka tímabil með slider
- Velja færri breytur í einu

### 4. Browser compatibility

Prófað á:
- Chrome/Edge (mælt með)
- Firefox
- Safari

## Villuleit (Troubleshooting)

### "Gögn finnast ekki"

```bash
# Keyrðu hreinsunarskript
python scripts/hreinsa_gogn_v4.py
```

### "ModuleNotFoundError"

```bash
# Settu upp pakka aftur
pip install -r requirements.txt
```

### Port upptekinn

```bash
# Notaðu annan port
streamlit run streamlit_app.py --server.port 8502
```

### Hægfara keyrsla

```bash
# Hreinsaðu cache
# Í terminal þar sem streamlit keyrir: ýttu á 'c'
# Eða eyða .streamlit cache möppu
```

## Viðbætur og þróun

### Bæta við nýjum myndriti

```python
# Í viðeigandi tab:
with tab_name:
    st.subheader("Titill")

    # Búa til mynd
    fig = px.line(df, x='x_col', y='y_col')

    # Sýna
    st.plotly_chart(fig, use_container_width=True)
```

### Bæta við nýju gagnasafni

1. Bæta við vali í `dataset_type` radio
2. Búa til nýjan if-block fyrir gagnasafnið
3. Skilgreina load function með `@st.cache_data`
4. Búa til tabs og visualizations

### Styling

Streamlit styður custom CSS:

```python
st.markdown("""
<style>
.custom-class {
    color: blue;
}
</style>
""", unsafe_allow_html=True)
```

## Deployment

### Streamlit Cloud (ókeypis)

1. Push verkefni á GitHub
2. Farðu á [share.streamlit.io](https://share.streamlit.io)
3. Connect repo og deploy

### Heroku

```bash
# Bæta við Procfile:
web: sh setup.sh && streamlit run streamlit_app.py

# Deploy:
git push heroku main
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py"]
```

## Tenglar

- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Docs**: https://plotly.com/python/
- **Xarray Docs**: https://xarray.dev/

## Höfundur

Magnús Smári
Sjávarútvegs DataDemo Verkefni 2025

---

*Síðast uppfært: 2025-11-04*
