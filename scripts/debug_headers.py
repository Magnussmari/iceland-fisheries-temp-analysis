import pandas as pd

# Read the sample file to debug the header structure
input_file = 'data/sampledata/Afli_eftir_fisktegundum_FULL_CSV_Sample.csv'

print("=" * 80)
print("DEBUGGING HEADER STRUCTURE")
print("=" * 80)

# Read with multi-level headers
df = pd.read_csv(
    input_file,
    sep=';',
    skiprows=3,
    header=[0, 1],
    na_values='..',
)

print(f"\nDataFrame shape: {df.shape}")
print(f"\nFirst 10 column tuples:")
for i, col in enumerate(df.columns[:10]):
    print(f"  {i}: {col}")

print(f"\nColumns 10-20:")
for i, col in enumerate(df.columns[10:20], 10):
    print(f"  {i}: {col}")

print(f"\nLast 10 columns:")
for i, col in enumerate(df.columns[-10:], len(df.columns)-10):
    print(f"  {i}: {col}")

# Show the actual data structure
print(f"\nFirst few rows of data:")
print(df.head(3))
