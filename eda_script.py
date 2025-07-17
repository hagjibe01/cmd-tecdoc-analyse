# Exploratory Data Analysis (EDA) using Pandas, Matplotlib, and Seaborn

import pandas as pd
import matplotlib.pyplot as plt  # For plotting graphs
import seaborn as sns  # For better-looking statistical visualizations

# Function to perform EDA on a given CSV file
def perform_eda(file_path, file_label):
    print(f"\n--- EDA for {file_label} ---")

    # 1. Load the CSV file
    try:
        # Try reading the file with automatic delimiter detection (e.g., ',' or ';')
        df = pd.read_csv(file_path, encoding='utf-8', sep=None, engine='python')
    except Exception as e:
        print(f"Error while reading the file {file_path}: {e}")
        return

    # 2. Display column names and their data types
    print("\nColumns and data types:")
    print(df.dtypes)

    # 3. Check for missing values in each column
    print("\nMissing values per column:")
    print(df.isnull().sum())

    # 4. Count of unique values per column (useful for detecting identifiers)
    print("\nNumber of unique values per column:")
    print(df.nunique())

    # 5. Identify fully duplicated rows
    num_duplicates = df.duplicated().sum()
    print(f"\nNumber of fully duplicated rows: {num_duplicates}")

    # 6. Basic statistical description of numerical fields
    print("\nDescriptive statistics for numerical fields:")
    print(df.describe())

    # 7. Visualize missing values (only if any columns contain NaNs)
    missing = df.isnull().sum()
    missing = missing[missing > 0]  # Only keep columns with missing values
    if not missing.empty:
        plt.figure(figsize=(10, 4))
        sns.barplot(x=missing.index, y=missing.values)
        plt.title(f"Missing Values per Column ({file_label})")
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
        plt.tight_layout()
        plt.show()  # Display the plot

# Sample CSV file names (update with actual file paths if needed)
cmd_file = "cmd_daten.csv"         # CMD master data file
tecdoc_file = "tecdoc_daten.csv"   # TecDoc catalog data file

# Run EDA on both datasets
perform_eda(cmd_file, "CMD Data")
perform_eda(tecdoc_file, "TecDoc Data")
