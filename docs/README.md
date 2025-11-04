# Documentation Index

Welcome to the Sjávarútvegs DataDemo documentation!

## Quick Start

New to the project? Start here:

1. 📖 **[Main README](../README.md)** - Project overview and structure
2. 🛠️ **[Setup Guide](setup/copernicus_setup.md)** - Environment setup and data download
3. 🚀 **[Quick Start Guide](setup/quick_start_guide.md)** - Get up and running quickly

---

## Documentation Structure

### 📁 Setup Guides (`setup/`)

Step-by-step instructions for setting up the project:

- **[copernicus_setup.md](setup/copernicus_setup.md)** - Copernicus Marine API setup
- **[quick_start_guide.md](setup/quick_start_guide.md)** - Fast project setup

### 📁 Data Documentation (`data/`)

Detailed information about datasets:

- **[afli_eftir_fisktegundum.md](afli_eftir_fisktegundum.md)** - Catch data description
- **[copernicus_data.md](copernicus_data.md)** - Sample ocean data documentation
- **[ocean_data_complete.md](data/ocean_data_complete.md)** - Full multi-year ocean dataset
- **[data_structure_guide.md](data/data_structure_guide.md)** - Understanding data formats
- **[fetch_guide.md](data/fetch_guide.md)** - Fetching multi-year data from Copernicus
- **[copernicus_api_guide.md](copernicus_api_guide.md)** - Complete API documentation

### 📁 Analysis Documentation (`analysis/`)

Guides for data processing and analysis:

- **[processing_workflow.md](analysis/processing_workflow.md)** - Step-by-step processing guide
- **Comparison analysis** - (see `data/processed/comparison/README.md`)

### 📁 Archived Documentation (`archived/`)

Older documentation kept for reference:

- Old setup and processing guides from development
- Download progress tracking files
- Superseded documentation

---

## Data Processing Workflow

### 1. Data Cleaning
```bash
# Clean raw catch data
python scripts/01_data_cleaning/hreinsa_gogn_v4.py

# Explore cleaned data
python scripts/01_data_cleaning/explore_afli_data.py
```

### 2. Data Fetching
```bash
# Fetch ocean data from Copernicus Marine
python scripts/02_data_fetching/fetch_copernicus_data.py

# Explore NetCDF structure
python scripts/02_data_fetching/explore_netcdf.py
```

### 3. Data Processing
```bash
# Aggregate spatially (NetCDF → Daily CSV)
python scripts/03_data_processing/aggregate_ocean_spatial.py

# Aggregate temporally (Daily → Monthly CSV)
python scripts/03_data_processing/aggregate_ocean_monthly.py

# Create comparison datasets
python scripts/03_data_processing/prepare_comparison_datasets.py
```

### 4. Visualization & Analysis
```bash
# Launch Streamlit app
streamlit run src/streamlit_app.py

# Or use Jupyter notebooks
jupyter lab notebooks/
```

---

## Project Structure

```
Sjavarutvegs_DataDemo/
├── README.md                  # Main project overview
├── CLAUDE.md                  # AI assistant instructions
├── requirements.txt           # Python dependencies
│
├── docs/                      # All documentation (you are here!)
│   ├── README.md              # This file
│   ├── setup/                 # Setup guides
│   ├── data/                  # Data documentation
│   ├── analysis/              # Analysis guides
│   └── archived/              # Old documentation
│
├── data/                      # All data files
│   ├── raw/                   # Original data
│   ├── processed/             # Cleaned/transformed data
│   └── outputs/               # Analysis outputs
│
├── scripts/                   # Data processing scripts
│   ├── 01_data_cleaning/      # Cleaning scripts
│   ├── 02_data_fetching/      # Fetching scripts
│   ├── 03_data_processing/    # Processing scripts
│   └── utils/                 # Shared utilities
│
├── notebooks/                 # Jupyter notebooks
├── src/                       # Application code
│   ├── streamlit_app.py       # Main Streamlit app
│   └── components/            # App components
└── tests/                     # Unit tests
```

---

## Key Datasets

### Catch Data (Afli eftir fisktegundum)

- **Source**: Icelandic fisheries data
- **Period**: 2010-2025 (16 years)
- **Resolution**: Monthly aggregates by species and port
- **Records**: 19,276 catch records
- **Total catch**: ~4.6 billion kg

**Location**: `data/processed/afli_eftir_fisktegundum/afli_hreinsad_FULL.csv`

### Ocean Data (Copernicus Marine)

- **Source**: GLORYS12v1 (Global Ocean Physics Reanalysis)
- **Period**: 2010-01-01 to 2025-09-30
- **Resolution**: Daily, ~9km spatial
- **Region**: Iceland waters (63-67°N, 25-13°W)
- **Variables**: Temperature, salinity, currents, sea surface height

**Locations**:
- Raw NetCDF: `data/raw/Copernicus/fetched/copernicus_iceland_ocean_20100101_20250930.nc`
- Daily CSV: `data/processed/oceantemp/Ocean_temp_*_DAILY.csv` (after processing)
- Monthly CSV: `data/processed/oceantemp/Ocean_temp_*_MONTHLY.csv` (after processing)

---

## Research Questions

This project enables analysis of:

1. **Climate Impact**
   - Ocean warming trends 2010-2025
   - Correlation with catch decline
   - Species-specific responses

2. **Seasonal Patterns**
   - Optimal fishing temperatures
   - Spawning season conditions
   - Migration patterns

3. **Long-term Trends**
   - Climate change signals
   - Tipping points
   - Future forecasts

4. **Species Analysis**
   - Þorskur (cod) responses
   - Ýsa (haddock) preferences
   - Loðna (capelin) collapse

---

## Getting Help

### Documentation Issues

If documentation is unclear or outdated:
1. Check the [archived/](archived/) folder for older versions
2. Consult the main [README.md](../README.md)
3. Look at script docstrings for implementation details

### Data Issues

For data-related questions:
- See [data/](data/) folder documentation
- Check `data/processed/comparison/README.md` for comparison datasets
- Review processing workflow in [analysis/processing_workflow.md](analysis/processing_workflow.md)

### Technical Issues

For code or setup issues:
- Review [setup/](setup/) guides
- Check script documentation in `scripts/`
- Verify Python environment with `pip list`

---

## Contributing

When adding new documentation:

1. **Setup guides** → `docs/setup/`
2. **Data descriptions** → `docs/data/`
3. **Analysis guides** → `docs/analysis/`
4. **Update this index** when adding major docs

---

## Version History

- **2025-11-04**: Project reorganization - documentation structure created
- **2025-11-04**: Multi-year ocean data downloaded (2010-2025)
- **2025-11-04**: Initial project setup with catch and sample ocean data

---

*Last updated: 2025-11-04*
*Documentation structure v1.0*
