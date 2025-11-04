# Sjávarútvegs Data Demo - Icelandic Fisheries Data Visualization Project

## ✅ Project Status: Ready for Analysis!

**Ocean Data**: 2010-2025 downloaded (1.7GB NetCDF)
**Catch Data**: 2010-2025 cleaned and ready
**Next Step**: Run processing scripts to create analysis datasets

📖 **See [docs/README.md](docs/README.md) for complete documentation index**

---

## Project Overview

This project contains data demonstrations and visualizations supporting a presentation on the resilience and sustainability of the Icelandic fishing industry, with focus on using AI and data-driven decision making to address contemporary challenges.

## Presentation Theme

**"Burðarþol íslensks sjávarútvegs: Greining á samþættum áskorunum og framtíðarlausnum í ljósi kerfisbreytinga"**

(Resilience of Icelandic Fisheries: Analysis of Integrated Challenges and Future Solutions in Light of System Changes)

### Key Topics Covered

1. **Ecological Challenges**
   - Capelin (loðna) stock migration and collapse
   - Cod stock condition deterioration
   - Climate change impacts on marine ecosystems

2. **Economic Pressures**
   - Rising operational costs (energy, labor)
   - Fishing fees and taxation
   - Export market challenges (Russia sanctions, Brexit complications)

3. **Value Chain Issues**
   - Export of unprocessed fish
   - Value creation opportunities
   - Technology infrastructure dependencies

4. **Future Solutions**
   - Data-driven fisheries management
   - AI integration for:
     - Real-time catch quality optimization
     - Ecosystem monitoring
     - Value chain optimization
   - Integration of fishing vessel data, processing data, and ecosystem data

### Sub-presentation: "Valdefling sérfræðinga"

"Empowering Experts: Creating Value with AI Without Losing Trust"
- Addresses the dichotomy in AI discussions
- Focuses on avoiding responsibility fog and cognitive debt
- Practical implementation of AI in industry

## Project Structure

```
Sjavarutvegs_DataDemo/
├── README.md                          # This file - project overview
├── CLAUDE.md                          # AI assistant instructions
├── requirements.txt                   # Python dependencies
│
├── docs/                              # 📚 All documentation
│   ├── README.md                      # Documentation index (START HERE!)
│   ├── setup/                         # Setup guides
│   ├── data/                          # Data documentation
│   ├── analysis/                      # Analysis guides
│   └── archived/                      # Old documentation
│
├── data/                              # 💾 All data files
│   ├── raw/                           # Original, immutable data
│   │   ├── Afli_eftir_fisktegundum/  # Catch data
│   │   └── Copernicus/                # Ocean data (NetCDF)
│   ├── processed/                     # Cleaned, transformed data
│   │   ├── afli_eftir_fisktegundum/  # Cleaned catch data
│   │   ├── oceantemp/                 # Processed ocean data
│   │   └── comparison/                # Merged datasets
│   └── outputs/                       # Analysis outputs
│       ├── figures/                   # Plots and visualizations
│       ├── tables/                    # Summary tables
│       └── reports/                   # Analysis reports
│
├── scripts/                           # 🔧 Data processing scripts
│   ├── 01_data_cleaning/              # Clean raw data
│   ├── 02_data_fetching/              # Fetch from APIs
│   ├── 03_data_processing/            # Aggregate and compare
│   └── utils/                         # Shared utilities
│
├── notebooks/                         # 📓 Jupyter notebooks
│   └── (analysis notebooks here)
│
├── src/                               # 🚀 Application code
│   ├── streamlit_app.py               # Main Streamlit app
│   └── components/                    # App components
│
└── tests/                             # ✅ Unit tests
```

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Process Ocean Data

```bash
# Step 1: Aggregate spatially (NetCDF → Daily CSV, ~5-10 min)
python scripts/03_data_processing/aggregate_ocean_spatial.py

# Step 2: Aggregate temporally (Daily → Monthly CSV, ~1 min)
python scripts/03_data_processing/aggregate_ocean_monthly.py

# Step 3: Create comparison datasets (~2 min)
python scripts/03_data_processing/prepare_comparison_datasets.py
```

### 3. Launch Visualization

```bash
# Start Streamlit app
streamlit run src/streamlit_app.py
```

### 4. Or Use Jupyter Notebooks

```bash
# Launch Jupyter Lab
jupyter lab notebooks/
```

**Note**: Catch data is already cleaned and ready in `data/processed/afli_eftir_fisktegundum/`

---

## Data Sources Referenced

The presentation references multiple data silos that could be integrated:

1. **Fishing Vessel Data** (Trackwell/Hafsýn)
   - Location tracking
   - Catch data
   - Real-time operations

2. **Processing Data** (Marel systems, etc.)
   - Yield and quality metrics
   - Processing efficiency
   - Fish condition data

3. **Ecosystem Data** (Hafrannsóknastofnun/Marine Research Institute)
   - Stock assessments
   - Temperature data
   - Biological indicators

## Features

### 1. Interactive Streamlit Dashboard
Launch a comprehensive web-based visualization tool:
- **Catch Data Visualizations**: Time series, port analysis, species breakdown
- **Ocean Data Explorer**: NetCDF file analysis, temperature/wind data
- **Real-time Filtering**: Interactive controls for data exploration
- **Export Options**: Download processed data as CSV

### 2. Data Processing Scripts
- **Data Cleaning**: Convert wide-format CSV to long-format
- **Statistical Analysis**: Generate comprehensive statistics
- **NetCDF Exploration**: Extract and analyze oceanographic data

### 3. Comprehensive Documentation
- Dataset descriptions and metadata
- Data quality assessments
- Usage examples in Python and R
- Connection to presentation research

## Getting Started

### Prerequisites

- Python 3.9+
- Required Python packages (see `requirements.txt`)

### Installation

```bash
# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Quick Start

```bash
# 1. Clean catch data
python scripts/hreinsa_gogn_v4.py

# 2. Explore data
python scripts/explore_afli_data.py

# 3. Explore NetCDF ocean data
python scripts/explore_netcdf.py

# 4. Launch interactive Streamlit app
streamlit run streamlit_app.py
```

## Key References

- Hafrannsóknastofnun (Marine Research Institute): https://www.hafogvatn.is
- Hagstofa Íslands (Statistics Iceland): https://hagstofa.is
- Samtök fyrirtækja í sjávarútvegi (SFS): https://www.sfs.is

## Presentation Context

This project supports a discussion forum on:
> "Are we overestimating the resilience of Icelandic fisheries?"

The presentation argues that 21st-century resilience must be measured not in tons of catch, but in **adaptability** and **value creation per ton**, enabled by data integration and AI.

## License

This is an educational/presentation project.

## Contact

Magnus Smári - Presentation Project 2025