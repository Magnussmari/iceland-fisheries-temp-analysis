# Multi-Year Ocean Data Download - Full Documentation

## Download Initiated

**Date**: 2025-11-04 14:30
**Status**: In progress ⏳
**Expected Duration**: 1-3 hours

---

## What's Being Downloaded

### Dataset Information

**Product**: GLOBAL_MULTIYEAR_PHY_001_030
**Name**: Global Ocean Physics Reanalysis (GLORYS12v1)
**Provider**: Copernicus Marine Service
**Dataset ID**: `cmems_mod_glo_phy_my_0.083deg_P1D-m`

### Time Coverage

- **Start date**: 2010-01-01
- **End date**: 2025-09-16 (latest available as of download date)
- **Total days**: ~5,738 days
- **Temporal resolution**: Daily mean values
- **Update frequency**: Monthly

### Spatial Coverage

**Region**: Iceland waters
- **Latitude**: 63°N to 67°N
- **Longitude**: -25°E to -13°E (or 25°W to 13°W)
- **Depth range**: 0m to 50m (surface and subsurface)
- **Spatial resolution**: ~9 km (0.083°)

**Grid dimensions**:
- Latitude points: ~50
- Longitude points: ~145
- Depth levels: ~10
- Total grid points per day: ~72,500

### Variables Downloaded

| Variable | Full Name | Unit | Description |
|----------|-----------|------|-------------|
| `thetao` | Sea water potential temperature | °C | Temperature of seawater |
| `so` | Sea water salinity | PSU | Salt content (Practical Salinity Units) |
| `uo` | Eastward sea water velocity | m/s | Ocean current - east component |
| `vo` | Northward sea water velocity | m/s | Ocean current - north component |
| `zos` | Sea surface height above geoid | m | Sea level anomaly |

---

## File Details

### Output Location

```
data/raw/Copernicus/fetched/
└── copernicus_iceland_ocean_20100101_20250916.nc
```

### Expected File Size

- **NetCDF (compressed)**: ~2-4 GB
- **After spatial aggregation to daily averages**: ~2-3 MB CSV
- **Compression level**: 6 (balance between size and speed)

### Data Dimensions

```
Dimensions:
  - time: 5,738 days (2010-01-01 to 2025-09-16)
  - latitude: ~50 points
  - longitude: ~145 points
  - depth: ~10 levels

Total data points: 5,738 × 50 × 145 × 10 × 5 variables ≈ 208 million values
```

---

## Why This Data?

### Alignment with Catch Data

Your catch data (`afli_hreinsad_FULL.csv`) covers:
- **Period**: 2010-2025
- **Records**: 19,276 catch records
- **Temporal resolution**: Monthly aggregates
- **Species**: Multiple (þorskur, ýsa, etc.)

This ocean data provides:
- ✅ **Same time period** (2010-2025)
- ✅ **Daily resolution** (can aggregate to monthly)
- ✅ **Physical ocean conditions** during fishing
- ✅ **Perfect temporal overlap** for analysis

### Research Questions This Enables

1. **Climate Impact Analysis**
   - Ocean warming trends 2010-2025
   - Correlation with catch decline
   - Seasonal patterns

2. **Spatial Analysis**
   - Match fishing locations with ocean conditions
   - Identify optimal temperature ranges
   - Track shifting fishing grounds

3. **Predictive Modeling**
   - Train models on historical data
   - Predict catch from ocean conditions
   - Validate with recent years

4. **Ecosystem Changes**
   - Loðna migration patterns
   - Spawning condition suitability
   - Stock distribution shifts

---

## Data Processing Pipeline

### Step 1: Download (Current - 1-3 hours)
```bash
python scripts/fetch_copernicus_data.py custom
# Input: 2010-01-01 to 2025-09-16
```

### Step 2: Explore NetCDF Structure
```bash
python scripts/explore_netcdf.py
```

### Step 3: Spatial Aggregation

Create daily averages for Iceland region:

```python
import xarray as xr
import pandas as pd

# Load data
ds = xr.open_dataset('data/raw/Copernicus/fetched/copernicus_iceland_ocean_20100101_20250916.nc')

# Spatial average for each day
daily_avg = ds.mean(dim=['latitude', 'longitude', 'depth'])

# Convert to DataFrame
df = daily_avg.to_dataframe().reset_index()

# Save as CSV
df.to_csv('data/processed/oceantemp/Ocean_temp_2010_2025_DAILY.csv', index=False)
```

**Result**: ~5,738 rows × 6 columns (time + 5 variables)

### Step 4: Temporal Aggregation to Monthly

Match catch data resolution:

```python
# Aggregate to monthly means
monthly = df.set_index('time').resample('MS').mean()

# Save
monthly.to_csv('data/processed/oceantemp/Ocean_temp_2010_2025_MONTHLY.csv')
```

**Result**: ~189 rows (months) × 5 variables

### Step 5: Merge with Catch Data

```bash
python scripts/prepare_comparison_datasets.py
```

Creates aligned datasets for analysis.

---

## Expected Results

### Current State (Before This Download)

❌ Ocean data: 6 weeks (Feb-Mar 2018)
❌ Catch data: 16 years (2010-2025)
❌ Overlap: Minimal (2 months only)
❌ Analysis capability: Very limited

### After This Download

✅ Ocean data: 15.75 years (~5,738 days)
✅ Catch data: 16 years (monthly)
✅ Overlap: Complete temporal coverage
✅ Analysis capability: Full long-term trends

---

## Data Quality Notes

### Model vs. Observations

This is **reanalysis data**, meaning:
- ✅ Combines observations with numerical models
- ✅ Spatially and temporally complete (no gaps)
- ✅ Quality controlled
- ✅ Best estimate of ocean state
- ⚠️ Not direct measurements
- ⚠️ Model uncertainty exists

### Validation

GLORYS12v1 is validated against:
- Satellite observations (SST, SSH)
- Argo floats (temperature, salinity)
- Ship measurements
- Mooring data

**Accuracy**: Generally within observational uncertainty for Iceland waters.

### Known Limitations

1. **Spatial resolution**: ~9 km may not capture small-scale features
2. **Depth limitation**: Focuses on 0-50m (surface layer)
3. **Coastal accuracy**: May be less accurate very close to shore
4. **Temporal lag**: Updates monthly, ~2-3 month delay

---

## Monitoring the Download

### Check Progress

```bash
# Method 1: Watch output
tail -f nohup.out  # If running in background

# Method 2: Check file size
watch -n 30 'ls -lh data/raw/Copernicus/fetched/'

# Method 3: Check process
ps aux | grep fetch_copernicus_data
```

### Progress Indicators

The download shows:
```
INFO - Starting download. Please wait...
  45%|████▌     | 2587/5738 [25:30<28:15,  1.86it/s]
```

- **Percentage**: Overall progress
- **Numbers**: Current day / Total days
- **Time**: Elapsed / Estimated remaining
- **Speed**: Days per second

### If Download Fails

**Common issues**:
1. Network timeout - just restart script, it will resume
2. Disk space - check `df -h .`
3. Authentication - run `copernicusmarine login` again

**To restart**:
```bash
python scripts/fetch_copernicus_data.py custom
# Enter same dates: 2010-01-01 to 2025-09-16
```

---

## After Download Completes

### Verification Steps

1. **Check file exists and size**:
```bash
ls -lh data/raw/Copernicus/fetched/copernicus_iceland_ocean_20100101_20250916.nc
# Expected: 2-4 GB
```

2. **Verify data structure**:
```bash
python scripts/explore_netcdf.py
```

3. **Check time coverage**:
```python
import xarray as xr
ds = xr.open_dataset('data/raw/Copernicus/fetched/copernicus_iceland_ocean_20100101_20250916.nc')
print(f"Start: {ds.time.values[0]}")
print(f"End: {ds.time.values[-1]}")
print(f"Days: {len(ds.time)}")
```

Expected output:
```
Start: 2010-01-01
End: 2025-09-16
Days: 5738
```

### Next Steps

1. ✅ Spatially aggregate to daily Iceland averages
2. ✅ Temporally aggregate to monthly for catch comparison
3. ✅ Update comparison datasets
4. ✅ Run analysis in Streamlit
5. ✅ Create visualizations for presentation

---

## Processing Scripts to Run

### 1. Create Daily Aggregated File

```bash
# Create script to aggregate spatially
python scripts/aggregate_ocean_spatial.py
```

This will create:
```
data/processed/oceantemp/Ocean_temp_2010_2025_DAILY.csv
- 5,738 rows (days)
- 6 columns (date + 5 variables)
- ~2-3 MB file size
```

### 2. Create Monthly Aggregated File

```bash
python scripts/aggregate_ocean_monthly.py
```

This will create:
```
data/processed/oceantemp/Ocean_temp_2010_2025_MONTHLY.csv
- ~189 rows (months)
- 6 columns (date + 5 variables)
- ~50 KB file size
```

### 3. Update Comparison Datasets

```bash
python scripts/prepare_comparison_datasets.py
```

This will create updated comparison files in:
```
data/processed/comparison/
├── ocean_catch_merged_2010_2025.csv
├── ocean_monthly_aggregated_2010_2025.csv
├── afli_monthly_aggregated_2010_2025.csv
└── README.md (updated)
```

---

## Data Usage Examples

### Python: Load and Explore

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load daily ocean data
ocean_daily = pd.read_csv('data/processed/oceantemp/Ocean_temp_2010_2025_DAILY.csv',
                          parse_dates=['time'])

# Basic statistics
print(ocean_daily.describe())

# Plot temperature trend
plt.figure(figsize=(15, 5))
plt.plot(ocean_daily['time'], ocean_daily['thetao'], linewidth=0.5)
plt.xlabel('Year')
plt.ylabel('Sea Temperature (°C)')
plt.title('Iceland Waters - Daily Temperature 2010-2025')
plt.grid(True)
plt.savefig('ocean_temp_trend_2010_2025.png', dpi=150)
plt.show()
```

### Python: Merge with Catch Data

```python
# Load catch data
catch = pd.read_csv('data/processed/afli_eftir_fisktegundum/afli_hreinsad_FULL.csv',
                   parse_dates=['Dags'])

# Load monthly ocean data
ocean_monthly = pd.read_csv('data/processed/oceantemp/Ocean_temp_2010_2025_MONTHLY.csv',
                           parse_dates=['time'])

# Rename for merge
ocean_monthly = ocean_monthly.rename(columns={'time': 'Dags'})

# Merge on month
merged = catch.merge(ocean_monthly, on='Dags', how='inner')

print(f"Merged dataset: {len(merged)} records")
print(f"Date range: {merged['Dags'].min()} to {merged['Dags'].max()}")

# Correlation analysis
correlation = merged[['Afli_heildar', 'thetao']].corr()
print(f"\nCorrelation catch vs temperature:\n{correlation}")
```

---

## Timeline Summary

| Time | Action | Status |
|------|--------|--------|
| 14:30 | Download started | ✅ In progress |
| ~16:00-17:00 | Download completes (estimated) | ⏳ Pending |
| +10 min | Verify NetCDF structure | ⏸️ Waiting |
| +20 min | Create spatial aggregation script | ⏸️ Waiting |
| +30 min | Create daily CSV file | ⏸️ Waiting |
| +35 min | Create monthly CSV file | ⏸️ Waiting |
| +40 min | Update comparison datasets | ⏸️ Waiting |
| +45 min | Run Streamlit analysis | ⏸️ Waiting |

**Total time to analysis-ready data**: ~3-4 hours from now

---

## Storage Requirements

### Disk Space Needed

```
Current:
  - Raw NetCDF downloading: ~2-4 GB

After processing:
  - Daily CSV: ~2-3 MB
  - Monthly CSV: ~50 KB
  - Comparison files: ~5-10 MB

Total: ~2.5-4 GB (mostly raw NetCDF)
```

### Cleanup Options

After processing, you can optionally:
```bash
# Keep only processed CSV files (saves ~2-4 GB)
rm data/raw/Copernicus/fetched/copernicus_iceland_ocean_20100101_20250916.nc

# Or compress for archival
gzip data/raw/Copernicus/fetched/copernicus_iceland_ocean_20100101_20250916.nc
```

---

## Citation

If you use this data in publications:

```
EU Copernicus Marine Service Information (CMEMS).
Marine Data Store (MDS).
doi: 10.48670/moi-00021

Product: GLOBAL_MULTIYEAR_PHY_001_030
Dataset: cmems_mod_glo_phy_my_0.083deg_P1D-m
Downloaded: 2025-11-04
```

---

## Support Resources

### Copernicus Marine Documentation
- Product page: https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030
- User manual: https://catalogue.marine.copernicus.eu/documents/PUM/CMEMS-GLO-PUM-001-030.pdf
- API docs: https://help.marine.copernicus.eu/

### Project Documentation
- API guide: `docs/copernicus_api_guide.md`
- Data clarification: `DATA_CLARIFICATION.md`
- Quick start: `QUICK_START_MULTI_YEAR.md`

---

## Download Status

**Check current status**:
```bash
# View background process output
# (Instructions will be provided when download completes)
```

**Estimated completion**: 2025-11-04 ~16:00-17:00

---

*Documentation created: 2025-11-04 14:31*
*Download initiated: 2025-11-04 14:30*
*Status: IN PROGRESS ⏳*
