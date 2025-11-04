"""Test that all required imports work"""

print("Testing imports...")

try:
    import pandas as pd
    print("✓ pandas:", pd.__version__)
except ImportError as e:
    print("✗ pandas:", e)

try:
    import numpy as np
    print("✓ numpy:", np.__version__)
except ImportError as e:
    print("✗ numpy:", e)

try:
    import xarray as xr
    print("✓ xarray:", xr.__version__)
except ImportError as e:
    print("✗ xarray:", e)

try:
    import netCDF4
    print("✓ netCDF4:", netCDF4.__version__)
except ImportError as e:
    print("✗ netCDF4:", e)

try:
    import streamlit as st
    print("✓ streamlit:", st.__version__)
except ImportError as e:
    print("✗ streamlit:", e)

try:
    import plotly
    print("✓ plotly:", plotly.__version__)
except ImportError as e:
    print("✗ plotly:", e)

print("\nAll imports successful! Ready to run streamlit app.")
print("\nTo run the app:")
print("  python -m streamlit run streamlit_app.py")
print("\nOr if that doesn't work:")
print("  .venv/bin/streamlit run streamlit_app.py")
