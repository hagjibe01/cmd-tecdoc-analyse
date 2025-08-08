import pandas as pd
import os
import jellyfish

TMD_FILE = "tmd_001000106869000000000065516001_data_2025-07-15-09-42-29-416.csv"
TECDOC_FILE = "200_Article_Table.csv"
OUTPUT_DIR = "matching_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_str(s):
    if not pd.notna(s):
        return ""
    s = str(s).strip().upper()
    s = ''.join(c for c in s if c.isalnum())
    s = s.lstrip("0")
    return s

def soundex_match(tmd_df, tecdoc_df, tmd_col, tecdoc_col):
    tmd_df = tmd_df.copy()
    tecdoc_df = tecdoc_df.copy()
    tmd_df['soundex'] = tmd_df[tmd_col].apply(clean_str).apply(jellyfish.soundex)
    tecdoc_df['soundex'] = tecdoc_df[tecdoc_col].apply(clean_str).apply(jellyfish.soundex)

    # Diagnostics: print unique soundex counts and overlaps
    tmd_soundex_set = set(tmd_df['soundex'].unique())
    tecdoc_soundex_set = set(tecdoc_df['soundex'].unique())
    overlap = tmd_soundex_set & tecdoc_soundex_set
    print(f"TMD unique Soundex codes: {len(tmd_soundex_set)}")
    print(f"TecDoc unique Soundex codes: {len(tecdoc_soundex_set)}")
    print(f"Gemeinsame Soundex-Codes: {len(overlap)}")
    if overlap:
        print(f"Beispiel gemeinsame Soundex-Codes: {list(overlap)[:5]}")
    print(f"Beispiel TMD Soundex: {list(tmd_soundex_set)[:5]}")
    print(f"Beispiel TecDoc Soundex: {list(tecdoc_soundex_set)[:5]}")

    # Build a lookup dictionary for tecdoc rows by soundex
    tecdoc_soundex_dict = {}
    for idx, row in tecdoc_df.iterrows():
        sx = row['soundex']
        tecdoc_soundex_dict.setdefault(sx, []).append(row)

    # For each TMD row, find matches in TecDoc with the same soundex AND exact cleaned value
    matches = []
    for _, tmd_row in tmd_df.iterrows():
        sx = tmd_row['soundex']
        tmd_clean = clean_str(tmd_row[tmd_col])
        if sx in tecdoc_soundex_dict:
            for tecdoc_row in tecdoc_soundex_dict[sx]:
                tecdoc_clean = clean_str(tecdoc_row[tecdoc_col])
                if tmd_clean == tecdoc_clean:
                    match = {}
                    for col in tmd_df.columns:
                        match[f"{col}_tmd"] = tmd_row[col]
                    for col in tecdoc_df.columns:
                        match[f"{col}_tecdoc"] = tecdoc_row[col]
                    matches.append(match)
    if matches:
        return pd.DataFrame(matches)
    else:
        return pd.DataFrame()

if __name__ == "__main__":
    tmd_df = pd.read_csv(TMD_FILE, dtype=str, sep=None, engine='python')
    tecdoc_df = pd.read_csv(TECDOC_FILE, dtype=str, nrows=100000, sep=None, engine='python')

    # Beispiel: Soundex-Matching article_number <-> artno
    print("\nSoundex Matching: article_number <-> artno")
    result_soundex = soundex_match(tmd_df, tecdoc_df, "article_number", "artno")
    print(f"Gefundene Soundex-Matches: {len(result_soundex)}")
    result_soundex.to_csv(f"{OUTPUT_DIR}/soundex_match_article_number_artno.csv", index=False)

    print("\nPhonetic Matching abgeschlossen.")
