import matplotlib.pyplot as plt
def plot_matching_rate(match_counts, total_counts, labels, output_path):
    rates = [m / t * 100 if t > 0 else 0 for m, t in zip(match_counts, total_counts)]
    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, rates, color='skyblue')
    plt.ylabel('Matchingquote (%)')
    plt.ylim(0, 100)
    plt.title('Matchingquote der deterministischen Ansätze')
    for bar, rate in zip(bars, rates):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{rate:.1f}%', ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

import pandas as pd
import os


TMD_FILE = "tmd_001000106869000000000065516001_data_2025-07-15-09-42-29-416.csv"
TECDOC_FILE = "200_Article_Table.csv"
OUTPUT_DIR = "matching_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_str(s):
    return str(s).strip().upper() if pd.notna(s) else ""

def exact_one_to_one_matching(tmd_path, tecdoc_path, tmd_col, tecdoc_col, output_path, nrows_tecdoc=100000):
    print(f"\n[Deterministisches 1:1-Matching] {tmd_col} <-> {tecdoc_col}")
    tmd_df = pd.read_csv(tmd_path, dtype=str, sep=None, engine='python')
    tecdoc_df = pd.read_csv(tecdoc_path, dtype=str, nrows=nrows_tecdoc, sep=None, engine='python')
    tmd_df['clean'] = tmd_df[tmd_col].apply(clean_str)
    tecdoc_df['clean'] = tecdoc_df[tecdoc_col].apply(clean_str)
    merged = pd.merge(tmd_df, tecdoc_df, on='clean', suffixes=('_tmd', '_tecdoc'))
    print(f"Gefundene exakte Matches: {len(merged)}")
    merged.to_csv(output_path, index=False)
    print(f"Ergebnis gespeichert unter: {output_path}")

def exact_two_column_matching(tmd_path, tecdoc_path, tmd_col1, tmd_col2, tecdoc_col1, tecdoc_col2, output_path, nrows_tecdoc=100000):
    print(f"\n[Deterministisches 2-Spalten-Matching] {tmd_col1}+{tmd_col2} <-> {tecdoc_col1}+{tecdoc_col2}")
    tmd_df = pd.read_csv(tmd_path, dtype=str, sep=None, engine='python')
    tecdoc_df = pd.read_csv(tecdoc_path, dtype=str, nrows=nrows_tecdoc, sep=None, engine='python')
    tmd_df['key'] = tmd_df[tmd_col1].apply(clean_str) + "_" + tmd_df[tmd_col2].apply(clean_str)
    tecdoc_df['key'] = tecdoc_df[tecdoc_col1].apply(clean_str) + "_" + tecdoc_df[tecdoc_col2].apply(clean_str)
    merged = pd.merge(tmd_df, tecdoc_df, on='key', suffixes=('_tmd', '_tecdoc'))
    print(f"Gefundene 2-Spalten-Matches: {len(merged)}")
    merged.to_csv(output_path, index=False)
    print(f"Ergebnis gespeichert unter: {output_path}")




if __name__ == "__main__":

    # 1:1-Matching auf tec_doc_article_number <-> artno
    out1 = f"{OUTPUT_DIR}/exact_match_tmd_tecdoc200.csv"
    exact_one_to_one_matching(
        tmd_path=TMD_FILE,
        tecdoc_path=TECDOC_FILE,
        tmd_col="tec_doc_article_number",
        tecdoc_col="artno",
        output_path=out1
    )

    # 1:1-Matching auf trade_number <-> artno
    out2 = f"{OUTPUT_DIR}/exact_match_tmd_trade_tecdoc200.csv"
    exact_one_to_one_matching(
        tmd_path=TMD_FILE,
        tecdoc_path=TECDOC_FILE,
        tmd_col="trade_number",
        tecdoc_col="artno",
        output_path=out2
    )

    # 1:1-Matching auf article_number <-> artno
    out3 = f"{OUTPUT_DIR}/exact_match_tmd_articlenumber_tecdoc200.csv"
    exact_one_to_one_matching(
        tmd_path=TMD_FILE,
        tecdoc_path=TECDOC_FILE,
        tmd_col="article_number",
        tecdoc_col="artno",
        output_path=out3
    )

    # 1:1-Matching auf commodity_code <-> commodity_code (sofern beide vorhanden)
    if 'commodity_code' in pd.read_csv(TMD_FILE, nrows=1).columns and 'commodity_code' in pd.read_csv(TECDOC_FILE, nrows=1).columns:
        out4 = f"{OUTPUT_DIR}/exact_match_tmd_commoditycode_tecdoc200.csv"
        exact_one_to_one_matching(
            tmd_path=TMD_FILE,
            tecdoc_path=TECDOC_FILE,
            tmd_col="commodity_code",
            tecdoc_col="commodity_code",
            output_path=out4
        )

    # 1:1-Matching auf generic_article_no <-> genartno (sofern beide vorhanden)
    if 'generic_article_no' in pd.read_csv(TMD_FILE, nrows=1).columns and 'genartno' in pd.read_csv(TECDOC_FILE, nrows=1).columns:
        out5 = f"{OUTPUT_DIR}/exact_match_tmd_genericarticleno_tecdoc200.csv"
        exact_one_to_one_matching(
            tmd_path=TMD_FILE,
            tecdoc_path=TECDOC_FILE,
            tmd_col="generic_article_no",
            tecdoc_col="genartno",
            output_path=out5
        )

    # 1:1-Matching auf brand <-> brandno (sofern beide vorhanden)
    if 'brand' in pd.read_csv(TMD_FILE, nrows=1).columns and 'brandno' in pd.read_csv(TECDOC_FILE, nrows=1).columns:
        out6 = f"{OUTPUT_DIR}/exact_match_tmd_brand_tecdoc200.csv"
        exact_one_to_one_matching(
            tmd_path=TMD_FILE,
            tecdoc_path=TECDOC_FILE,
            tmd_col="brand",
            tecdoc_col="brandno",
            output_path=out6
        )

    # Diagramm: Matchingquote für alle Ansätze
    match_counts = []
    total_counts = []
    labels = [
        'tec_doc_article_number-artno',
        'trade_number-artno',
        'article_number+supplier_number-artno+datasupplier_id'
    ]
    # Lade die Output-Dateien und berechne die Quoten
    # Ansatz 1
    try:
        df1 = pd.read_csv(out1)
        match_counts.append(len(df1))
        total_counts.append(df1['tec_doc_article_number'].nunique())
    except Exception:
        match_counts.append(0)
        total_counts.append(1)
    # Ansatz 2
    try:
        df2 = pd.read_csv(out2)
        match_counts.append(len(df2))
        total_counts.append(df2['trade_number'].nunique())
    except Exception:
        match_counts.append(0)
        total_counts.append(1)
    # Ansatz 3
    try:
        df3 = pd.read_csv(out3)
        match_counts.append(len(df3))
        total_counts.append(df3['article_number'].nunique())
    except Exception:
        match_counts.append(0)
        total_counts.append(1)

    plot_matching_rate(match_counts, total_counts, labels, f"{OUTPUT_DIR}/deterministic_matching_rate.png")
    print(f"Diagramm gespeichert unter: {OUTPUT_DIR}/deterministic_matching_rate.png")

