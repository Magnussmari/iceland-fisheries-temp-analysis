# Project Reorganization Plan

## Current Issues

1. **Root directory cluttered** with 12+ markdown files
2. **Documentation scattered** - some in docs/, most in root
3. **Large CSV files** taking up space (2GB from 2018 test)
4. **No clear structure** for data science workflow

---

## New Structure (Best Practices)

```
Sjavarutvegs_DataDemo/
├── README.md                          # Main project overview
├── CLAUDE.md                          # AI assistant instructions
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore patterns
│
├── docs/                              # All documentation
│   ├── README.md                      # Documentation index
│   ├── setup/                         # Setup guides
│   │   ├── copernicus_setup.md
│   │   ├── environment_setup.md
│   │   └── data_download.md
│   ├── data/                          # Data documentation
│   │   ├── afli_eftir_fisktegundum.md
│   │   ├── copernicus_ocean_data.md
│   │   └── data_processing.md
│   ├── analysis/                      # Analysis documentation
│   │   ├── comparison_analysis.md
│   │   └── visualization_guide.md
│   └── archived/                      # Old/superseded docs
│       ├── DATA_PROCESSING_COMPLETE.md
│       └── SETUP_COMPLETE.md
│
├── data/                              # All data files
│   ├── raw/                           # Original, immutable data
│   │   ├── Afli_eftir_fisktegundum/
│   │   │   ├── Afli_eftir_fisktegundum_Sample.csv
│   │   │   └── Afli_eftir_fisktegundum_FULL_CSV.csv
│   │   └── Copernicus/
│   │       ├── fetched/
│   │       │   └── copernicus_iceland_ocean_20100101_20250930.nc
│   │       └── documentation/
│   │           └── *.pdf
│   ├── processed/                     # Cleaned, transformed data
│   │   ├── afli_eftir_fisktegundum/
│   │   │   ├── afli_hreinsad_SAMPLE.csv
│   │   │   └── afli_hreinsad_FULL.csv
│   │   ├── oceantemp/
│   │   │   ├── ocean_temp_DAILY.csv
│   │   │   └── ocean_temp_MONTHLY.csv
│   │   └── comparison/
│   │       ├── README.md
│   │       └── *.csv
│   └── outputs/                       # Analysis outputs
│       ├── figures/
│       ├── tables/
│       └── reports/
│
├── scripts/                           # Data processing scripts
│   ├── 01_data_cleaning/
│   │   ├── hreinsa_gogn_v4.py
│   │   └── explore_afli_data.py
│   ├── 02_data_fetching/
│   │   ├── fetch_copernicus_data.py
│   │   └── explore_netcdf.py
│   ├── 03_data_processing/
│   │   ├── aggregate_ocean_spatial.py
│   │   ├── aggregate_ocean_monthly.py
│   │   └── prepare_comparison_datasets.py
│   └── utils/
│       └── (shared utility functions)
│
├── notebooks/                         # Jupyter notebooks for analysis
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_ocean_catch_comparison.ipynb
│   └── 03_climate_impact_analysis.ipynb
│
├── src/                               # Application source code
│   ├── __init__.py
│   ├── streamlit_app.py
│   └── components/
│       ├── catch_visualizations.py
│       └── ocean_visualizations.py
│
└── tests/                             # Unit tests
    ├── test_data_processing.py
    └── test_aggregations.py
```

---

## Actions to Take

### 1. Documentation Reorganization

**Move to docs/setup/**:
- COPERNICUS_SETUP.md → docs/setup/copernicus_setup.md
- QUICK_START_MULTI_YEAR.md → docs/setup/data_download_guide.md

**Move to docs/data/**:
- MULTI_YEAR_OCEAN_DATA.md → docs/data/copernicus_ocean_data.md
- DATA_CLARIFICATION.md → docs/data/data_structure_explanation.md
- FETCH_MULTI_YEAR_DATA.md → docs/data/fetch_multi_year_guide.md

**Move to docs/analysis/**:
- AFTER_DOWNLOAD_COMPLETE.md → docs/analysis/processing_workflow.md

**Move to docs/archived/**:
- DATA_PROCESSING_COMPLETE.md
- SETUP_COMPLETE.md
- DOWNLOAD_IN_PROGRESS.md
- README_OCEAN_DATA_DOWNLOAD.md

**Keep in root**:
- README.md (main overview)
- CLAUDE.md (AI instructions)

### 2. Data Cleanup

**Delete unnecessary files**:
- `data/raw/Copernicus/fetched/copernicus_iceland_ocean_20180101_20181231.csv` (2GB test file - we have NetCDF)

**Organize NetCDF**:
- Keep: `copernicus_iceland_ocean_20100101_20250930.nc` (1.7GB - our main dataset)

### 3. Scripts Reorganization

**Create numbered folders**:
- `scripts/01_data_cleaning/` - Data cleaning scripts
- `scripts/02_data_fetching/` - API and data fetching
- `scripts/03_data_processing/` - Aggregation and comparison

**Move scripts accordingly**:
- hreinsa_gogn_*.py → 01_data_cleaning/
- fetch_*, explore_netcdf.py → 02_data_fetching/
- aggregate_*, prepare_comparison_*.py → 03_data_processing/

### 4. Create Notebooks Folder

- Create notebooks/ for exploratory analysis
- Move heavy analysis out of streamlit

### 5. Streamlit App Refactoring

- Move streamlit_app.py to src/
- Break into components
- Cleaner imports

---

## Benefits

✅ **Clear separation** of concerns (docs, data, code, outputs)
✅ **Numbered scripts** show processing order
✅ **Easy navigation** for new contributors
✅ **Standard structure** familiar to data scientists
✅ **Scalable** for future additions
✅ **Clean root** directory - only essentials

---

## Implementation Order

1. ✅ Create new folder structure
2. ✅ Move documentation files
3. ✅ Move and organize scripts
4. ✅ Delete unnecessary data files
5. ✅ Update import paths in scripts
6. ✅ Create docs/README.md (documentation index)
7. ✅ Update main README.md
8. ✅ Test that everything still works

---

*Created: 2025-11-04 14:40*
