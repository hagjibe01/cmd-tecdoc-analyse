import pandas as pd
from rapidfuzz import fuzz, process
from rapidfuzz.distance import Levenshtein, JaroWinkler


tmd_df = pd.read_csv("tmd_001000106869000000000065516001_data_2025-07-15-09-42-29-416.csv", dtype=str)
tecdoc_df = pd.read_csv("400_Article_Linkage.csv", dtype=str)

# Fuzzy Matching auf artno, refno, genartno zwischen zwei DataFrames
def fuzzy_match_columns(df_a, df_b, col_a, col_b, method="levenshtein", threshold=90, top_n=1):
    """
    Führt Fuzzy Matching auf zwei Spalten aus zwei DataFrames durch.
    Gibt die besten Matches pro Wert aus df_a zurück.
    method: "levenshtein" oder "jaro"
    """
    if method == "levenshtein":
        scorer = Levenshtein.normalized_similarity
    elif method == "jaro":
        scorer = JaroWinkler.normalized_similarity
    else:
        raise ValueError("Unbekannte Methode")
    results = []
    values_b = df_b[col_b].dropna().astype(str).unique().tolist()
    for val_a in df_a[col_a].dropna().astype(str).unique():
        matches = process.extract(val_a, values_b, scorer=scorer, limit=top_n)
        for match in matches:
            if match[1] >= threshold:
                results.append({
                    "value_a": val_a,
                    "value_b": match[0],
                    "score": match[1]
                })
    return pd.DataFrame(results)

# Beispiel: Anwendung auf artno, refno, genartno
if __name__ == "__main__":
    # Dummy-Daten
    df_a = pd.DataFrame({
        "artno": ["ABC123", "DEF456", "GHI789"],
        "refno": ["REF1", "REF2", "REF3"],
        "genartno": ["1", "2", "3"]
    })
    df_b = pd.DataFrame({
        "artno": ["ABC124", "DEF457", "GHI789", "XYZ000"],
        "refno": ["REF1A", "REF2B", "REF3", "REFX"],
        "genartno": ["1", "2", "4", "5"]
    })
    print("Fuzzy Matching artno (Levenshtein):")
    print(fuzzy_match_columns(df_a, df_b, "artno", "artno", method="levenshtein", threshold=90))
    print("Fuzzy Matching refno (Jaro-Winkler):")
    print(fuzzy_match_columns(df_a, df_b, "refno", "refno", method="jaro", threshold=90))
    print("Fuzzy Matching genartno (Levenshtein):")
    print(fuzzy_match_columns(df_a, df_b, "genartno", "genartno", method="levenshtein", threshold=90))

def fuzzy_match_levenshtein(list_a, list_b, threshold=90):
    """
    Fuzzy Matching mit Levenshtein-Distanz. Gibt Paare mit Score >= threshold zurück.
    """
    matches = []
    for a in list_a:
        best = process.extractOne(a, list_b, scorer=Levenshtein.normalized_similarity)
        if best and best[1] >= threshold:
            matches.append((a, best[0], best[1]))
    return matches

def fuzzy_match_jaro_winkler(list_a, list_b, threshold=90):
    """
    Fuzzy Matching mit Jaro-Winkler-Metrik. Gibt Paare mit Score >= threshold zurück.
    """
    matches = []
    for a in list_a:
        best = process.extractOne(a, list_b, scorer=JaroWinkler.normalized_similarity)
        if best and best[1] >= threshold:
            matches.append((a, best[0], best[1]))
    return matches

# Beispiel: Anwendung auf zwei Listen
if __name__ == "__main__":
    list_a = ["ABC123", "DEF456", "GHI789"]
    list_b = ["ABC124", "DEF457", "GHI789", "XYZ000"]
    print("Levenshtein-Matches:")
    print(fuzzy_match_levenshtein(list_a, list_b, threshold=90))
    print("Jaro-Winkler-Matches:")
    print(fuzzy_match_jaro_winkler(list_a, list_b, threshold=90))