# Afli eftir Fisktegundum - Gagnasafn

## Yfirlit

Þetta gagnasafn inniheldur upplýsingar um landaðan afla íslenskra fiskiskipa, sundurliðað eftir fiskitegundum og löndunarhöfnum fyrir tímabilið **janúar 2010 til september 2025**.

**Heimild**: Fiskistofa / Hagstofa Íslands
**Töflukóði**: SJA01101
**Eining**: kg (kílógrömm)

## Gagnaskipulag

### Upprunaleg skrá

Upphaflega gagnaskráin er á víðu formati (wide format) með:
- Línur fyrir hverja fisktegund og löndunarhöfn
- Dálkar fyrir hvern mánuð frá janúar 2010 til september 2025
- Multi-level headers þar sem ár eru á efri stigi og mánuðir á neðri stigi

**Dæmi um upphaflegt skipulag:**
```
                    2025                      2024
                    janúar  febrúar  mars    janúar  febrúar ...
Þorskur  Reykjavík  123456  234567   345678  456789  567890
         Akureyri   789012  890123   901234  012345  123456
```

### Hreinsuð skrá

Hreinsunarferlið umbreytir gögnunum í langt format (long format) sem hentar betur fyrir greiningar og sjónrænar framsetningar.

**Dálkar í hreinsaðri skrá:**

| Dálkur | Tegund | Lýsing |
|--------|--------|--------|
| `Dags` | Date | Dagsetning (fyrsti dagur mánaðar) í ISO formati (YYYY-MM-DD) |
| `Ár` | Integer | Ár (2010-2025) |
| `Mánuður` | String | Íslenskt nafn mánaðar (janúar, febrúar, mars, ...) |
| `Fisktegund` | String | Nafn fisktegundar (t.d. Þorskur, Ýsa) |
| `Löndunarhöfn` | String | Nafn hafnar þar sem afli var landaður |
| `Afli` | Integer | Magn landaðs afla í kílógrömmum (kg) |

## Hreinsunarferli

Hreinsunarferlið er útfært í skriptunni `scripts/hreinsa_gogn_v4.py` og felur í sér:

1. **Lestur á multi-level headers**: Greining á árslínum og mánaðarlínum
2. **Forward-fill á árum**: Árið 2025 gildir fyrir alla mánuði þar til næsta ár kemur
3. **Umbreyting í langt format**: Melt umbreyting frá víðu í langt format
4. **Hreinsun**:
   - Fjarlægja "Allar löndunartegundir" samantektarlínur
   - Umbreyta ".." í NA og fjarlægja
   - Fjarlægja færslur með núll afla
   - Tryggja að allar tölur séu rétt túlkaðar
5. **Dagsetningavinnsla**: Búa til dagsetningarreit út frá ári og mánaðarnúmeri
6. **Gæðaeftirlit**: Staðfesta að allar línur hafi gilt gildi

## Gagnagæði

### Þekkt vandamál

- **Tímabundin gögn**: Gögnin eru merkt sem bráðabirgðagögn
- **Vantar gagnapunktar**: Sum mánuðargögn vantar (merkt sem ".." í upprunalegri skrá)
- **Ójöfn skráning**: Ekki eru allar hafnir virkar öll árin

### Gæðavísar

Við hreinsun eru eftirfarandi atriði skoðuð:
- Núllgildi í afla (valid en fjarlægð úr hreinsaðri skrá)
- Neikvæð gildi (ættu ekki að koma fyrir)
- Vantar fisktegund eða löndunarhöfn (fjarlægt)
- Dagsetningar utan sviðs (fjarlægt)

## Notkun

### Hreinsun gagna

```bash
# Hreinsa fullt gagnasafn
python scripts/hreinsa_gogn_v4.py

# Hreinsa sample gagnasafn (fyrir prófanir)
python scripts/hreinsa_gogn_v4.py --sample
```

### Könnun gagna

```bash
# Skoða tölfræði fyrir fullt gagnasafn
python scripts/explore_afli_data.py

# Skoða sample gagnasafn
python scripts/explore_afli_data.py --sample
```

### Lestur í Python

```python
import pandas as pd

# Lesa hreinsaða skrá
df = pd.read_csv('data/processed/afli_hreinsad.csv',
                  parse_dates=['Dags'])

# Grunnupplýsingar
print(df.info())
print(df.head())

# Greining eftir tegund
species_summary = df.groupby('Fisktegund')['Afli'].sum()
print(species_summary)
```

### Lestur í R

```r
library(tidyverse)

# Lesa hreinsaða skrá
df <- read_csv('data/processed/afli_hreinsad.csv') %>%
  mutate(Dags = as.Date(Dags))

# Grunnupplýsingar
summary(df)

# Greining eftir tegund
species_summary <- df %>%
  group_by(Fisktegund) %>%
  summarise(Heildarafli = sum(Afli))
```

## Lykilfisktegund

Gagnasafnið inniheldur helst gögn um:
- **Þorskur** (Gadus morhua) - Atlantic Cod
- **Ýsa** (Melanogrammus aeglefinus) - Haddock

Þessar tvær tegundir eru meðal mikilvægustu nytjastofna Íslands og eru hluti af bolfiskstofnum við landið.

## Löndunarhafnir

Gögnin ná yfir allar helstu fiskveiðihafnir á Íslandi, þar á meðal en ekki takmarkað við:

**Stærstu hafnir** (eftir heildarmagni):
- Reykjavík
- Akureyri
- Grindavík
- Ísafjörður
- Neskaupstaður
- Dalvík
- Hafnarfjörður

Alls eru gögn frá **70+ höfnum** um allt land.

## Tímabilsgreining

### Árstíðabundin mynstur

Veiðimynstur sýnir skýra árstíðabundna breytileika:
- **Vetramánuðir** (jan-mar): Hámark í þorskveiðum vegna hrygningar
- **Sumarmánuðir** (jún-ágúst): Minni veiðar, sumarfriður fyrir suma stofna
- **Haustmánuðir** (sep-nóv): Aukning í veiðum eftir sumarfríið

### Langtímaþróun

Tímabilið 2010-2025 nær yfir:
- Bata þorskstofns eftir lágmark í kringum 2000
- Innleiðingu nýrra veiðistjórnunarreglna
- COVID-19 áhrif (2020-2021)
- Loftslagsbreytingar og áhrif þeirra á veiðistofna
- Loðnubrest og áhrif á fæðuframboð þorsks (2024-2025)

## Tengsl við rannsóknarframsetninguna

Þetta gagnasafn er notað til að sýna fram á:

1. **Vistkerfisbreytingar**: Hvernig afli hefur breyst með hlýnandi sjó
2. **Efnahagsleg mynstur**: Breytileiki eftir höfnum sýnir verðmætasköpun
3. **Áhrif ytri þátta**: Brexit, stríð og markaðsbreytingar
4. **Gagnadrifin stjórnun**: Hvernig rauntímagögn geta bætt ákvarðanatöku

## Höfundaréttur og notkunarleyfi

**Eigandi**: Fiskistofa / Hagstofa Íslands
**Höfundaréttur**: © Hagstofa Íslands

Gögnin eru bráðabirgðagögn. Nánari gögn um aflamagn og kvótastöðu einstakra skipa má finna á [www.fiskistofa.is](https://www.fiskistofa.is)

## Tilvísanir og tenglar

- **Fiskistofa**: https://www.fiskistofa.is
- **Hagstofa Íslands - Sjávarútvegur**: https://hagstofa.is/utgafur/frettasafn/sjavarutvegur/
- **Hafrannsóknastofnun**: https://www.hafogvatn.is

## Tengdar skrár

- `data/raw/Afli_eftir_fisktegundum_FULL_CSV.csv` - Upprunaleg gögn
- `data/processed/afli_hreinsad.csv` - Hreinsuð gögn (langt format)
- `data/processed/afli_stats.txt` - Tölfræðisamantekt
- `scripts/hreinsa_gogn_v4.py` - Hreinsunarskript
- `scripts/explore_afli_data.py` - Könnunarskript

## Samantekt fyrir rannsóknir

### Helstu tölfræðilegar mælingar

Könnunarskriptin reikna:
- Heildarafla eftir tegundum og tíma
- Meðalafla og miðgildi
- Staðalfrávik og dreifingu
- Árstíðabundin mynstur
- Landfræðilega dreifingu (eftir höfnum)
- Þróun yfir tíma (trend analysis)

### Mögulegar greiningar

Gögnin henta vel fyrir:
- **Tímaraðagreiningar** (time series analysis)
- **Árstíðaleiðréttingu** (seasonal decomposition)
- **Landfræðilega kortlagningu** (geographic mapping)
- **Samanburðargreiningar** milli hafna/tegunda
- **Spálíkön** (forecasting) fyrir framtíðarveiðar
- **Áhrifagreiningar** á ytri þætti (COVID, Brexit, etc.)

---

*Skjal síðast uppfært: 2025-11-04*
*Útgáfa: 1.0*
