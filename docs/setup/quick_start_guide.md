# Quick Start: Fetch Multi-Year Ocean Data

**Status**: System ready ✅ `copernicusmarine` installed

**Goal**: Get 2010-2025 ocean data to match your 16-year catch dataset

---

## Step 1: Copernicus Account (5 minutes, ONE TIME)

### If you DON'T have an account yet:

1. Go to: https://data.marine.copernicus.eu/register
2. Fill in: Email, Password, Name
3. Check email and confirm

### Configure credentials:

```bash
copernicusmarine login
```

Enter your username and password when prompted.

---

## Step 2: Choose Your Strategy

### RECOMMENDED: Start with 1 Year Test

This proves everything works before committing to the full download:

```bash
python scripts/fetch_copernicus_data.py custom
```

When prompted, enter:
- Start date: `2018-01-01`
- End date: `2018-12-31`

**Time**: 5-15 minutes
**Size**: ~100-200 MB
**Result**: Full year 2018 with all seasons

---

### After Test Succeeds: Fetch Multiple Years

#### Option A: Recent Years (2018-2025) - FAST
```bash
python scripts/fetch_copernicus_data.py custom
```
Enter:
- Start: `2018-01-01`
- End: `2025-09-30`

**Time**: 20-40 minutes
**Size**: ~500 MB - 1 GB
**Gets you**: 7 years of recent data

#### Option B: Full Period (2010-2025) - COMPLETE
```bash
python scripts/fetch_copernicus_data.py custom
```
Enter:
- Start: `2010-01-01`
- End: `2025-09-30`

**Time**: 1-3 hours
**Size**: 2-4 GB
**Gets you**: Complete 16-year overlap with catch data

---

## Step 3: After Download Completes

The script will automatically:
1. ✅ Download NetCDF file to `data/raw/Copernicus/fetched/`
2. ✅ Convert to CSV (you'll be asked)
3. ✅ Show statistics

Then run:

```bash
# Update comparison datasets with multi-year ocean data
python scripts/prepare_comparison_datasets.py

# Open Streamlit to explore
streamlit run streamlit_app.py
```

---

## What You'll Get

### With 2018 only (test):
- ✅ Full seasonal cycle (winter → spring → summer → fall)
- ✅ 365 daily measurements
- ✅ Proof of concept for your presentation
- ✅ ~100 MB file

### With 2018-2025 (recent):
- ✅ 7 years of data
- ✅ Recent climate trends
- ✅ ~2,555 daily measurements
- ✅ Good overlap with recent catch data
- ✅ Faster download

### With 2010-2025 (full):
- ✅ Complete 16-year period
- ✅ Perfect alignment with ALL catch data
- ✅ ~5,844 daily measurements
- ✅ Long-term climate analysis
- ✅ Publication-ready dataset

---

## Troubleshooting

### "Authentication failed"
```bash
copernicusmarine login
# Re-enter your credentials
```

### Download is slow
- Try during off-peak hours (evening EU time)
- Use year-by-year approach
- Check internet connection

### Out of disk space
```bash
df -h .
# Check you have enough free space:
# 1 year = ~200 MB
# 7 years = ~1 GB
# 16 years = ~4 GB
```

### Download interrupted
Just run the command again. You'll need to restart that chunk (Copernicus API doesn't support resume).

---

## My Recommendation

**For your presentation:**

1. **NOW (15 min)**: Fetch 2018 only
   - Quick test
   - Full seasonal cycle
   - Enough for demo

2. **TONIGHT (overnight)**: Fetch 2010-2025
   - Complete dataset
   - Run overnight or while you're away
   - Full analysis capability

This way you have something to work with immediately, while the complete dataset downloads in the background.

---

## Expected Results

### Current State:
- ❌ 6 weeks ocean data (Feb-Mar 2018)
- ❌ 16 years catch data (2010-2025)
- ❌ Minimal overlap for analysis

### After 2018 Fetch:
- ✅ 1 year ocean data (365 days)
- ✅ Seasonal patterns visible
- ✅ Proof of concept ready

### After 2010-2025 Fetch:
- ✅ 16 years ocean data (~5,844 days)
- ✅ Perfect temporal alignment
- ✅ Long-term trend analysis
- ✅ Climate impact correlation
- ✅ Predictive modeling capability
- ✅ Publication-quality dataset

---

## Commands Summary

```bash
# 1. Login (one time)
copernicusmarine login

# 2. Test with 2018
python scripts/fetch_copernicus_data.py custom
# Enter: 2018-01-01 to 2018-12-31

# 3. If successful, fetch full period
python scripts/fetch_copernicus_data.py custom
# Enter: 2010-01-01 to 2025-09-30

# 4. Process comparison
python scripts/prepare_comparison_datasets.py

# 5. Visualize
streamlit run streamlit_app.py
```

---

**Ready to start?** Run `copernicusmarine login` first! 🚀

---

*Created: 2025-11-04*
*All systems ready - just need your Copernicus credentials*
