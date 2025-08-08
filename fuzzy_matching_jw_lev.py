import pandas as pd
import os
from rapidfuzz import fuzz, process
from rapidfuzz.distance import JaroWinkler

TMD_FILE = "tmd_001000106869000000000065516001_data_2025-07-15-09-42-29-416.csv"
TECDOC_FILE = "200_Article_Table.csv"
OUTPUT_DIR = "matching_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Hilfsfunktion zur Bereinigung von Strings
import re
def clean_str(s):
    if not pd.notna(s):
        return ""
    s = str(s).strip().upper()
    s = re.sub(r"[^A-Z0-9]", "", s)  # Nur Buchstaben/Zahlen behalten
    s = s.lstrip("0")  # Führende Nullen entfernen
    return s

def fuzzy_match_column(tmd_df, tecdoc_df, tmd_col, tecdoc_col, method="jaro", threshold=90, top_n=1):
    tmd_series = tmd_df[tmd_col].dropna().astype(str).apply(clean_str).unique()
    tecdoc_series = tecdoc_df[tecdoc_col].dropna().astype(str).apply(clean_str).unique()
    matches = []
    if method == "levenshtein":
        scorer = fuzz.WRatio
    elif method == "jaro":
        scorer = JaroWinkler.similarity
    else:
        scorer = fuzz.WRatio
    for tmd_val in tmd_series:
        if not tmd_val:
            continue
        results = process.extract(
            tmd_val, tecdoc_series, scorer=scorer, limit=top_n
        )
        for match_val, score, _ in results:
            if score >= threshold:
                matches.append({
                    f"{tmd_col}": tmd_val,
                    f"{tecdoc_col}": match_val,
                    "score": score
                })
    return pd.DataFrame(matches)

if __name__ == "__main__":
    tmd_df = pd.read_csv(TMD_FILE, dtype=str, sep=None, engine='python')
    tecdoc_df = pd.read_csv(TECDOC_FILE, dtype=str, nrows=100000, sep=None, engine='python')

    # Beispiel: Fuzzy Matching article_number <-> artno mit Jaro-Winkler
    print("\nFuzzy Matching: article_number <-> artno (Jaro-Winkler)")
    result_jaro = fuzzy_match_column(tmd_df, tecdoc_df, "article_number", "artno", method="jaro", threshold=90)
    print(f"Gefundene Fuzzy-Matches (Jaro-Winkler): {len(result_jaro)}")
    result_jaro.to_csv(f"{OUTPUT_DIR}/fuzzy_match_article_number_artno_jaro.csv", index=False)

    # Beispiel: Fuzzy Matching trade_number <-> artno mit Levenshtein
    print("\nFuzzy Matching: trade_number <-> artno (Levenshtein)")
    result_lev = fuzzy_match_column(tmd_df, tecdoc_df, "trade_number", "artno", method="levenshtein", threshold=90)
    print(f"Gefundene Fuzzy-Matches (Levenshtein): {len(result_lev)}")
    result_lev.to_csv(f"{OUTPUT_DIR}/fuzzy_match_trade_number_artno_lev.csv", index=False)

    print("\nFuzzy Matching abgeschlossen.")
