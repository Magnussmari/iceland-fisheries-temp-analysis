# Fetching Multi-Year Ocean Data from Copernicus

## Problem

Current ocean data only covers **6 weeks** (Feb 7 - Mar 21, 2018).

Your catch data spans **16 years** (2010-2025).

**You need years of ocean measurements, not just months!**

---

## Solution: Fetch from Copernicus Marine API

### Step 1: Setup (5 minutes - ONE TIME ONLY)

#### A. Create FREE Copernicus account

1. Go to: https://data.marine.copernicus.eu/register
2. Fill in: Email, Password, Name
3. Check email and confirm

#### B. Configure credentials

```bash
copernicusmarine login
```

Enter your username and password when prompted.

**That's it!** Now you can download years of data.

---

## Step 2: Choose Your Approach

### Option A: Full Dataset (RECOMMENDED but SLOW)

Fetch **ALL years** (2010-2025) at once:

```bash
python scripts/fetch_copernicus_data.py
# Choose: 2 (Full)
```

**⚠️ WARNING:**
- Will take **1-3 hours** (depending on connection)
- File size: **~2-4 GB**
- Make sure you have disk space and stable internet

**What you get:**
- Daily ocean data for entire catch period
- Perfect alignment with catch data
- Ready for long-term trend analysis

---

### Option B: Year by Year (SAFER)

Fetch one year at a time to avoid timeouts:

```bash
python scripts/fetch_copernicus_data.py custom
```

Then enter dates like:
- 2010-01-01 to 2010-12-31
- 2011-01-01 to 2011-12-31
- etc.

**Pros:**
- More reliable (smaller chunks)
- Can stop/resume
- Easier to verify each year

**Cons:**
- Need to run 16 times
- Need to merge files afterward

---

### Option C: Recent Years Only (FAST)

Start with just recent years that are most relevant:

```bash
python scripts/fetch_copernicus_data.py custom
# Enter: 2018-01-01 to 2025-09-30
```

**Best for:**
- Quick analysis
- Presentation demos
- Recent climate impacts

**Time:** ~15-30 minutes
**Size:** ~500 MB - 1 GB

---

## Step 3: What Gets Downloaded

### Data Product

**GLOBAL_MULTIYEAR_PHY_001_030**
- Global Ocean Physics Reanalysis (GLORYS12v1)
- 1993 - present (updated monthly)
- Daily mean values
- ~9 km resolution (0.083°)

### Variables

For Iceland waters (63-67°N, 25-13°W, 0-50m depth):

| Variable | Description | Unit |
|----------|-------------|------|
| `thetao` | Sea water temperature | °C |
| `so` | Sea water salinity | PSU |
| `uo` | Eastward current velocity | m/s |
| `vo` | Northward current velocity | m/s |
| `zos` | Sea surface height | m |

### File Size Estimates

| Period | Days | Approx Size |
|--------|------|-------------|
| 1 month | 30 | 8-15 MB |
| 1 year | 365 | 100-200 MB |
| 5 years | 1,825 | 500 MB - 1 GB |
| 16 years (2010-2025) | 5,844 | 2-4 GB |

---

## Step 4: Monitor Progress

### While downloading you'll see:

```
⏳ Sæki gögn frá Copernicus Marine...
  (Þetta getur tekið nokkrar mínútur...)

Downloading: [=====>           ] 45% - 234/520 MB
```

**Tips:**
- Don't close terminal
- Keep computer awake
- Use stable internet (not mobile hotspot)
- If it fails, just run again - it will resume

---

## Step 5: After Download

### Automatic Processing

The script will:
1. ✅ Download NetCDF file
2. ✅ Convert to CSV (optional - you'll be asked)
3. ✅ Show statistics

### Files Created

```
data/raw/Copernicus/fetched/
└── copernicus_iceland_ocean_20100101_20251001.nc  # NetCDF (compressed)
└── copernicus_iceland_ocean_20100101_20251001.csv # CSV (larger, easy to use)
```

### Next: Create Comparison

Once downloaded, re-run comparison:

```bash
# Update script to use new multi-year ocean data
python scripts/prepare_comparison_datasets.py
```

This will create properly aligned datasets with **years** of overlap!

---

## Troubleshooting

### "Authentication failed"

```bash
copernicusmarine login
# Re-enter credentials
```

### "Dataset not available"

The dataset exists from 1993-present. Make sure your dates are in this range.

### Slow download / Timeout

**Solutions:**
1. Fetch smaller chunks (year by year)
2. Try during off-peak hours (evening/night EU time)
3. Check internet connection
4. Increase compression: add `netcdf_compression_level=9` in script

### Out of disk space

Check space needed:
```bash
df -h .  # Current directory free space
```

For 16 years, need ~4-5 GB free (2-4 GB data + processing space).

### Download interrupted

Just run the script again. Unfortunately, Copernicus API doesn't support resume, so you'll need to restart that chunk.

**Pro tip:** Use year-by-year approach to minimize loss if interrupted.

---

## Alternative: Use Existing Global Datasets

If Copernicus is too slow, you can also use:

### 1. ERA5 Reanalysis (via Copernicus Climate Data Store)
- Different service: https://cds.climate.copernicus.eu/
- Atmospheric + ocean surface data
- Faster download
- Different API

### 2. NOAA OISST
- Sea surface temperature only
- Daily, 0.25° resolution
- Free, no account needed
- Available via OPeNDAP

### 3. Hafrannsóknastofnun
- Local Icelandic measurements
- May have gaps
- Contact: https://www.hafogvatn.is/

---

## Recommended Strategy

**For your presentation (BEST approach):**

### Phase 1: Quick Demo (NOW - 30 min)
```bash
python scripts/fetch_copernicus_data.py custom
# 2018-01-01 to 2018-12-31
```

This gives you:
- 1 full year of data
- Fast download
- Enough for demo/proof of concept
- Shows seasonal patterns

### Phase 2: Extended Analysis (LATER - overnight)
```bash
python scripts/fetch_copernicus_data.py custom
# 2010-01-01 to 2025-09-30
```

Run overnight or when you can wait.

This gives you:
- Full 16-year period
- Complete comparison with catch data
- Publication-quality analysis
- Long-term climate trends

---

## Expected Results

### With Multi-Year Data You Can:

1. **Seasonal Analysis**
   - Compare summer vs winter conditions
   - Match with spawning seasons
   - Identify optimal temperature ranges

2. **Long-term Trends**
   - Ocean warming over 2010-2025
   - Correlation with catch decline
   - Climate change impacts

3. **Predictive Models**
   - Train ML models on historical data
   - Predict catch from ocean conditions
   - Validate with recent years

4. **Spatial Analysis**
   - Map fishing areas with temperature
   - Identify shifting patterns (loðna migration)
   - Compare different fishing grounds

---

## Summary

**Current situation:**
- ❌ Only 6 weeks of ocean data (Feb-Mar 2018)
- ❌ Can't do meaningful trend analysis
- ❌ Very limited overlap with catch data

**After fetching multi-year data:**
- ✅ 16 years of daily ocean data (2010-2025)
- ✅ ~5,844 data points
- ✅ Perfect alignment with catch data
- ✅ Can analyze climate impacts
- ✅ Can build predictive models
- ✅ Publication-ready analysis

---

## Quick Start Commands

```bash
# 1. Setup (one time)
pip install copernicusmarine
copernicusmarine login

# 2. Fetch data
python scripts/fetch_copernicus_data.py custom

# 3. Enter dates
#    Start: 2010-01-01
#    End:   2025-09-30

# 4. Wait... (1-3 hours for full period)

# 5. Process comparison
python scripts/prepare_comparison_datasets.py

# 6. Analyze!
streamlit run streamlit_app.py
```

---

**Ready to start?**

Choose your option:
- **Quick (30 min)**: Fetch 2018 only
- **Full (overnight)**: Fetch 2010-2025
- **Safer (few hours)**: Fetch year-by-year

Then your presentation will have real multi-year ocean vs catch analysis! 🌊📊

---

*Last updated: 2025-11-04*
