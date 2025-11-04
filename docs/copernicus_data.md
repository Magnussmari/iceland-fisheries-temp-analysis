# Copernicus Hafgögn - Ocean Data Documentation

## Yfirlit

Þessi skrá inniheldur meteorólógísk og sjávargögn frá **Copernicus Marine Service** sem safnað var með **WindCube LIDAR** kerfinu og öðrum skynjurum um borð í rannsóknarskipi.

**Skráarsnið**: NetCDF4
**Tímabil**: 7. febrúar 2018 - 21. mars 2018
**Tíðni**: 10 mínútna bil
**Fjöldi mælinga**: 6,067 tímapunktar

## Gagnaskipulag

### Víddir (Dimensions)

- **time**: 6,067 mælingar yfir ~42 daga

### Lykilbreytur (Key Variables)

#### 1. Sjávarhitastig (Sea Temperature)
**`sbe38_bow_temperature`**
- Lýsing: Hitastig sjávar mælt með SBE38 skynjara
- Eining: Kelvin (K)
- Gildisvið: 271.35K til 277.50K (-1.8°C til 4.3°C)
- Meðaltal: 273.84K (0.7°C)

#### 2. Skipshraði og stefna
**`water_speed_nmea`**
- Lýsing: Hraði skips yfir vatn (NMEA)
- Eining: m/s
- Gildisvið: -0.57 til 7.97 m/s
- Meðaltal: 3.00 m/s (~5.8 hnútar)

**`heading_nmea`**
- Lýsing: Stefna skips
- Eining: gráður (degree)
- Gildisvið: 2.1° til 356.9°

#### 3. Vindhraði og stefna
**`wind_direction`**
- Lýsing: Vindátt mæld í 40m hæð með LIDAR
- Eining: gráður
- Gildisvið: 0.7° til 360°
- Meðaltal: 133.4°

**`wind_speed`**
- Lýsing: Vindhraði mældur með LIDAR
- Eining: m/s

#### 4. Staðsetning
**`latitude_nmea`**
- Lýsing: Breiddarstaða (NMEA GPS)
- Eining: degree_north
- Gildisvið: 65.11°N til 75.74°N
- Meðaltal: 69.54°N (Suður- til Norður-Ísland)

**`longitude_nmea`**
- Lýsing: Lengdarstaða (NMEA GPS)
- Eining: degree_east
- Gildisvið: -28.39° til -2.90°
- Meðaltal: -17.09° (Vestur af Íslandi)

#### 5. Loftþrýstingur og hitastig
**`atmospheric_pressure`**
- Lýsing: Loftþrýstingur
- Eining: Pa (Pascal)

**`air_temperature`**
- Lýsing: Lofthitastig
- Eining: K (Kelvin)

**`relative_humidity`**
- Lýsing: Rakastig
- Eining: %

## Gagnagæði

### Tíðni gilda

Breytur hafa mismunandi fjölda gildra mælinga:

| Breyta | Gildar mælingar | Hlutfall |
|--------|-----------------|----------|
| `water_speed_nmea` | 5,887 | 97.0% |
| `latitude/longitude_nmea` | 5,887 | 97.0% |
| `wind_direction` | 3,837 | 63.2% |
| `sbe38_bow_temperature` | 3,651 | 60.2% |

### Þekkt vandamál

1. **Vantar mælingar**: Sumar breytur hafa umtalsverðan fjölda NaN gilda (up to 40%)
2. **Outliers**: `platform_heading_lidar` hefur skráð gildi allt að 1e20 (mögulega villumerki)
3. **Neikvæður hraði**: `water_speed_nmea` hefur lágmark -0.57 m/s (mögulega bakslag)

## Landsvæði

Miðað við GPS hnit (latitude/longitude) er gagnaöflun aðallega á svæðinu:
- **Breiddargráða**: 65°N - 76°N
- **Lengdargráða**: 28°V - 3°V

Þetta nær yfir:
- Suðvesturströnd Íslands
- Vestfirði
- Norðurland
- Svæði út á Atlantshaf vestur af Íslandi

## Tímagreining

### Tímabil
- Byrjar: 7. febrúar 2018, 00:00 UTC
- Endar: 21. mars 2018, 03:00 UTC
- Lengd: ~42 dagar

### Árstíð
Gögn safnað á **vetrarmánuðum** (feb-mars), sem er mikilvægt samhengi fyrir:
- Lága sjávarhita (0-4°C)
- Vetrarveður og vindaskilyrði
- Vetrarveiðitímabil í íslenskum sjávarútvegi

## Notkun

### Python með xarray

```python
import xarray as xr
import matplotlib.pyplot as plt

# Opna gagnaskrá
ds = xr.open_dataset('igp_alliance_surface_met_20180207_qc3_10min.nc')

# Skoða uppbygging
print(ds)

# Teikna sjávarhita yfir tíma
ds['sbe38_bow_temperature'].plot()
plt.title('Sjávarhitastig - feb-mars 2018')
plt.ylabel('Hitastig (K)')
plt.show()

# Búa til kort af skipaleið
plt.scatter(ds['longitude_nmea'], ds['latitude_nmea'],
           c=ds['sbe38_bow_temperature'], cmap='coolwarm')
plt.colorbar(label='Sjávarhiti (K)')
plt.xlabel('Lengdargráða')
plt.ylabel('Breiddargráða')
plt.title('Skipaleið með sjávarhita')
plt.show()
```

### Könnunarskript

```bash
# Skoða gagnaskrá í terminal
python scripts/explore_netcdf.py

# Eða tilgreina aðra skrá
python scripts/explore_netcdf.py /path/to/file.nc
```

### Streamlit forrit

```bash
# Keyra gagnvirkt forrit
streamlit run streamlit_app.py
```

## Tengsl við rannsóknarverkefnið

Þessi gögn eru mikilvæg fyrir að sýna:

### 1. Umhverfisbreytingar
- Sjávarhitamælingar sýna rauntíma hitaskilyrði
- Hægt að bera saman við sögulegar mælingar
- Tengsl við vistkerfisbreytingar (loðnubrest, þorskastand)

### 2. Veiðiskilyrði
- Skipshraði og staðsetning sýna veiðisvæði
- Veðurskilyrði (vindur, loftþrýstingur) hafa áhrif á veiðar
- Sjávarhiti hefur áhrif á fiskihegðun

### 3. Gagnadrifin stjórnun
- Rauntímagögn frá skipum
- Samþætting við veiðigögn
- Grundvöllur fyrir AI/ML spálíkön

### 4. Loftslagsbreytingar
- Langtímaþróun sjávarhita
- Breytingar á vindmynstri
- Áhrif á vistkerfi

## Framhald

### Mögulegar greiningar

1. **Tímaraðagreining**
   - Þróun sjávarhita yfir tímabil
   - Árstíðabundnar sveiflur
   - Fylgni milli breyta

2. **Landfræðileg greining**
   - Kortlagning skipaleið
   - Hitakort sjávarhita
   - Tengsl við veiðisvæði

3. **Veðurgreining**
   - Vindhraði og stefna
   - Loftþrýstingsbreytingar
   - Áhrif á skip og veiðar

4. **Samþætting**
   - Tengja við aflaskrár
   - Bera saman við hafrannsóknargögn
   - Spálíkön fyrir veiðar

### Viðbótargögn

Copernicus veitir aðgang að:
- Langtíma sjávarhitamælingum
- Seltumælingum
- Straumamælingum
- Gervihnattargögnum

Nánar: https://marine.copernicus.eu/

## Tilvísanir

**Heimild**: Copernicus Marine Service
**Mælingatæki**: WindCube LIDAR + SBE38 + NMEA GPS
**Gagnagæði**: QC3 (Quality Control level 3)
**Tíðni**: 10 mínútna meðaltöl

## Tengdar skrár

- `data/raw/Copernicus/igp_alliance_surface_met_20180207_qc3_10min.nc` - Upprunaleg NetCDF skrá
- `scripts/explore_netcdf.py` - Könnunarskript
- `streamlit_app.py` - Gagnvirkt vefforrit
- `requirements.txt` - Python pakkar

---

*Skjal síðast uppfært: 2025-11-04*
*Útgáfa: 1.0*
