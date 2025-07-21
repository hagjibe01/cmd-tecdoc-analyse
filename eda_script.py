import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# EDA-Funktion mit zusätzlicher Ausgabe als CSV und PNG
def perform_eda(file_path, file_label):
    print(f"\n--- EDA for {file_label} ---")

    # Output-Ordner vorbereiten
    output_dir = f"eda_output/{file_label.replace(' ', '_')}"
    os.makedirs(output_dir, exist_ok=True)

    try:
        df = pd.read_csv(file_path, encoding='utf-8', sep=None, engine='python')
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return

    # 1. Column types
    column_types = pd.DataFrame(df.dtypes, columns=["DataType"])
    column_types.to_csv(f"{output_dir}/column_types.csv")

    print("\nColumns and data types:")
    print(column_types)

    # 2. Missing values
    missing_values = df.isnull().sum()
    missing_values = missing_values[missing_values > 0]
    missing_values_df = pd.DataFrame(missing_values, columns=["MissingValues"])
    missing_values_df.to_csv(f"{output_dir}/missing_values.csv")

    print("\nMissing values per column:")
    print(missing_values_df)

    # 3. Unique values
    unique_values = df.nunique()
    unique_values_df = pd.DataFrame(unique_values, columns=["UniqueValues"])
    unique_values_df.to_csv(f"{output_dir}/unique_values.csv")

    print("\nUnique values per column:")
    print(unique_values_df)

    # 4. Duplicate rows
    num_duplicates = df.duplicated().sum()
    with open(f"{output_dir}/duplicates.txt", "w") as f:
        f.write(f"Number of fully duplicated rows: {num_duplicates}\n")
    print(f"\nNumber of fully duplicated rows: {num_duplicates}")

    # 5. Summary statistics
    stats = df.describe(include='all')
    stats.to_csv(f"{output_dir}/summary_statistics.csv")
    print("\nSummary statistics for numerical fields:")
    print(stats)

    # 6. Plot missing values (if any)
    if not missing_values.empty:
        plt.figure(figsize=(10, 4))
        sns.barplot(x=missing_values.index, y=missing_values.values)
        plt.title(f"Missing Values per Column ({file_label})")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/missing_values_plot.png")
        plt.close()
        print(f"Missing values plot saved as PNG in {output_dir}")

# Beispielhafte Dateien (anpassen!)
#perform_eda("cmd_daten.csv", "CMD Daten")
perform_eda("203 - Reference Numbers.csv", "TecDoc Daten 203 ")
