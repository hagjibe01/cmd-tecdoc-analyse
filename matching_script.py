import pandas as pd
import matplotlib.pyplot as plt
import os

# ========== MATCHING AUF GENERIC ARTICLE NO ==========
def match_by_generic_article(cmd_df, tecdoc_file, output_path="matching_output/match_genart.csv", chunksize=100_000):
    """
    Führt Matching basierend auf generic_article_no durch.
    Speichert die Ergebnisse als CSV-Datei.
    """
    def clean_column(col):
        return col.astype(str).str.strip().str.upper()

    # CMD-Felder bereinigen
    if 'generic_article_no' not in cmd_df.columns:
        print("Spalte 'generic_article_no' nicht in CMD-Datei gefunden.")
        return pd.DataFrame()
    cmd_df['genart_clean'] = clean_column(cmd_df['generic_article_no'])

    match_list = []

    rows_processed = 0
    for i, chunk in enumerate(pd.read_csv(tecdoc_file, dtype=str, chunksize=chunksize), 1):
        if i == 1:
            print("Spalten im TecDoc-Chunk:", chunk.columns.tolist())
            print("CMD genart_clean Beispiele:", cmd_df['genart_clean'].dropna().unique()[:5])
            chunk['genart_clean'] = clean_column(chunk['genartno'])
            print("TecDoc genart_clean Beispiele:", chunk['genart_clean'].dropna().unique()[:5])
        else:
            chunk['genart_clean'] = clean_column(chunk['genartno'])
        match_chunk = pd.merge(cmd_df, chunk, left_on='genart_clean', right_on='genart_clean', suffixes=('_cmd', '_tecdoc'))
        print(f"GenArt-Matches in Chunk: {len(match_chunk)}")
        match_list.append(match_chunk)
        rows_processed += len(chunk)
        if rows_processed >= 100_000:
            print(f"Abbruch nach {rows_processed} Zeilen (Testmodus)")
            break

    if match_list:
        all_matches = pd.concat(match_list, ignore_index=True)
        spalten = ['generic_article_no', 'article_number', 'brand', 'artno', 'brandno']
        vorhandene = [s for s in spalten if s in all_matches.columns]
        reduced = all_matches[vorhandene]
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        reduced.to_csv(output_path, index=False)
        print(f"\nGesamt-Matches GenArt: {len(reduced)} gespeichert in: {output_path}")
        return reduced
    else:
        print("Keine Matches für generic_article_no gefunden.")
        return pd.DataFrame()


# Eingabedateien
cmd_file = "tmd_001000106869000000000065516001_data_2025-07-15-09-42-29-416.csv"
tecdoc_file = "400_Article_Linkage.csv"

# Ordner für Ausgaben
output_dir = "matching_output"
os.makedirs(output_dir, exist_ok=True)

# CMD-Daten laden
cmd_df = pd.read_csv(cmd_file, dtype=str, sep=None, engine='python')
print("CMD-Daten geladen")



# Jetzt ist cmd_df definiert, daher kann die Funktion aufgerufen werden
match_by_generic_article(cmd_df, tecdoc_file)

# Hilfsfunktion zur Spaltenbereinigung
def clean_column(col):
    return col.astype(str).str.strip().str.upper()

# Bereinigung der TecDoc-Artikelnummer
cmd_df['tec_doc_article_number_clean'] = clean_column(cmd_df['tec_doc_article_number'])

# ========== MATCHING AUF TECDOC-NR ==========
"""match_tecdoc_nr_list = []
chunksize = 100_000

for chunk in pd.read_csv(tecdoc_file, dtype=str, chunksize=chunksize):
    chunk['artno_clean'] = clean_column(chunk['artno'])

    match_tecdoc = pd.merge(
        cmd_df,
        chunk,
        left_on='tec_doc_article_number_clean',
        right_on='artno_clean',
        suffixes=('_cmd', '_tecdoc')
    )

    print(f"Chunk-Matches (TecDoc-Nr): {len(match_tecdoc)}")
    match_tecdoc_nr_list.append(match_tecdoc)

# Ergebnisse konsolidieren
if match_tecdoc_nr_list:
    all_tecdoc_matches = pd.concat(match_tecdoc_nr_list, ignore_index=True)

    wichtige_spalten = ['tec_doc_article_number', 'article_description_de', 'ean']
    vorhandene_spalten = [s for s in wichtige_spalten if s in all_tecdoc_matches.columns]
    reduced_df = all_tecdoc_matches[vorhandene_spalten]

    reduced_df = reduced_df[reduced_df['tec_doc_article_number'].notna()]
    reduced_df['ean'] = "'" + reduced_df['ean'].astype(str)

    reduced_df.to_csv(f"{output_dir}/match_tecdoc_kompakt.csv", index=False)

    # Metriken
    total_cmd_rows = len(cmd_df)
    unique_cmd = cmd_df['tec_doc_article_number'].nunique()
    unique_matches = all_tecdoc_matches['tec_doc_article_number'].nunique()
    pct_tecdoc = unique_matches / unique_cmd * 100

    # Ausgabe
    print("\n--- TecDoc-Nr-Matching-Ergebnisse ---")
    print(f"Eindeutige CMD-Artikelnummern: {unique_cmd}")
    print(f"Eindeutige Matches: {unique_matches}")
    print(f"Matching-Quote: {pct_tecdoc:.2f}%")
#else:
    print("Keine TecDoc-Nr-Matches gefunden.")
    """

# ========== EAN-MATCHING ALS FUNKTION ==========

def perform_ean_matching(cmd_df, tecdoc_file):
    print("\n--- Starte EAN-Matching ---")
    cmd_df['ean_clean'] = clean_column(cmd_df['ean'])
    match_ean_list = []

    for chunk in pd.read_csv(tecdoc_file, dtype=str, chunksize=100000):
        ean_col = next((c for c in chunk.columns if c.lower() == 'ean'), None)
        if not ean_col:
            print("Spalte 'EAN' nicht gefunden.")
            return

        chunk['ean_clean'] = clean_column(chunk[ean_col])
        match_chunk = pd.merge(cmd_df, chunk, on='ean_clean', suffixes=('_cmd', '_tecdoc'))
        print(f"EAN-Matches in Chunk: {len(match_chunk)}")
        match_ean_list.append(match_chunk)

    if match_ean_list:
        all_ean_matches = pd.concat(match_ean_list, ignore_index=True)
        reduced = all_ean_matches[['ean', 'article_number', 'brand']].copy()
        reduced['ean'] = "'" + reduced['ean'].astype(str)
        reduced.to_csv(f"{output_dir}/match_ean_kompakt.csv", index=False)

        unique_cmd_eans = cmd_df['ean_clean'].nunique()
        unique_matches = all_ean_matches['ean_clean'].nunique()
        pct_match = unique_matches / unique_cmd_eans * 100

        print("\n--- EAN-Matching-Ergebnisse ---")
        print(f"Eindeutige CMD-EANs: {unique_cmd_eans}")
        print(f"Eindeutige gematchte EANs: {unique_matches}")
        print(f"EAN-Matching-Quote: {pct_match:.2f}%")
    else:
        print("Keine EAN-Matches gefunden.")

# ========== AUFRUF DER FUNKTION ==========

# perform_ean_matching(cmd_df, tecdoc_file)

# ========== MATCHING NACH SUPPLIER UND BRAND ==========
""""
def match_by_supplier_and_brand(cmd_df, tecdoc_file, output_path="matching_output/match_supplier_brand.csv", chunksize=100_000):
    
    Führt Matching basierend auf Supplier-Part-Number und Brand durch.
    Speichert die Ergebnisse als CSV-Datei.
    
    def clean_column(col):
        return col.astype(str).str.strip().str.upper()

    # CMD-Felder bereinigen
    cmd_df['supplier_no_clean'] = clean_column(cmd_df['article_number'])
    cmd_df['brand_clean'] = clean_column(cmd_df['brand'])

    match_list = []

    for chunk in pd.read_csv(tecdoc_file, dtype=str, chunksize=chunksize):
        chunk['artno_clean'] = clean_column(chunk['artno'])
        chunk['article_number_clean'] = clean_column(chunk['article_number'])

        match_chunk = pd.merge(
            cmd_df,
            chunk,
            left_on=['article_number_clean'],
            right_on=['artno_clean'],
            suffixes=('_cmd', '_tecdoc')
        )

        print(f"Chunk-Matches (Supplier+Brand): {len(match_chunk)}")
        match_list.append(match_chunk)

    # Alle Matches zusammenführen und speichern
    if match_list:
        all_matches = pd.concat(match_list, ignore_index=True)

        # Optional: Nur interessante Spalten behalten
        spalten = ['article_number', 'brand', 'artno', 'brandno']
        vorhandene = [s for s in spalten if s in all_matches.columns]
        reduced = all_matches[vorhandene]

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        reduced.to_csv(output_path, index=False)

        print(f"\nGesamt-Matches Supplier+Brand: {len(reduced)} gespeichert in: {output_path}")
        return reduced
    else:
        print("Keine Matches für Supplier + Brand gefunden.")
        return pd.DataFrame()

match_by_supplier_and_brand(cmd_df, tecdoc_file)

"""
# ========== VISUALISIERUNG DER MATCHING-ERGEBNISSE ==========
