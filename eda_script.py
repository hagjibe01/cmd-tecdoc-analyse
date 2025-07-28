import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import xml.etree.ElementTree as ET


# EDA function with additional output as CSV and PNG
def perform_eda(file_path, file_label):
    print(f"\n--- EDA for {file_label} ---")

    # Output directory preparation
    output_dir = f"eda_output/{file_label.replace(' ', '_')}"
    os.makedirs(output_dir, exist_ok=True)

    try:
        df = pd.read_csv(file_path, encoding='utf-8', sep=None, engine='python', nrows=100000)
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
        # Visualization: Top 10 columns with missing values (in %)
        missing_pct = df.isnull().mean().sort_values(ascending=False) * 100
        top_missing_pct = missing_pct[missing_pct > 0].head(10)

        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_missing_pct.values, y=top_missing_pct.index, palette="Blues_d")
        plt.xlabel("Percentage of missing values (%)")
        plt.title(f"Top 10 fields with highest missing value percentages ({file_label})")
        plt.xlim(0, 100)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/top_missing_percentage_{file_label}.png")
        plt.close()

           # 7. Boxplot of selected numerical columns
    """ Lieferant MAHLE
    boxplot_columns = [
        "gross_amount",
        "net_amount",
        "recom_retail_amount",
        "recom_garage_amount",
        "core_amount",
        "packaging_dimension_length",
        "packaging_dimension_width",
        "packaging_dimension_height",
        "packaging_weight",
        "packaging_volume"
    ]"""
    """ Lieferant TMD"""
    boxplot_columns_TMD = [
    "gross_amount",
    "net_amount",
    "recom_retail_amount",
    "recom_garage_amount",
    "packaging_dimension_length",
    "packaging_dimension_width",
    "packaging_dimension_height",
    "packaging_weight",
    "packaging_volume"
    ]


    # Filter only columns that exist in the DataFrame and have more than 10 non-empty values
    valid_columns = [col for col in boxplot_columns_TMD if col in df.columns and df[col].notnull().sum() > 10]

    if valid_columns:
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df[valid_columns], orient="h", showfliers=False)  # without outliers
        plt.title(f"Boxplot of selected numerical fields ({file_label})")
        plt.tight_layout()
        plt.savefig(f"{output_dir}/boxplot_{file_label}.png")
        plt.close()
        print(f"Boxplot saved at: {output_dir}/boxplot_{file_label}.png")
    else:
        print("No suitable columns available for boxplot.")

# perform_eda("cmd_daten.csv", "CMD data")
perform_eda("tmd_001000106869000000000065516001_data_2025-07-15-09-42-29-416.csv", "TecCMD_BusinessCloud_Daten_TMD-02")
