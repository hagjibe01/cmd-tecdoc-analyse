
import pandas as pd

def exact_one_to_one_matching(tmd_path, tecdoc_path, tmd_col, tecdoc_col, output_path):
    """
    Führt ein deterministisches 1:1-Matching (exakter Merge) zwischen zwei CSV-Dateien durch.
    tmd_col: Spaltenname in TMD-Datei
    tecdoc_col: Spaltenname in TecDoc-Datei
    output_path: Speicherort für Ergebnis-CSV
    """
    print(f"\n[Deterministisches Matching] Lese {tmd_path} und {tecdoc_path} ...")
    tmd_df = pd.read_csv(tmd_path, dtype=str, sep=None, engine='python')
    tecdoc_df = pd.read_csv(tecdoc_path, dtype=str, sep=None, engine='python')
    # Clean
    tmd_df['clean'] = tmd_df[tmd_col].astype(str).str.strip().str.upper()
    tecdoc_df['clean'] = tecdoc_df[tecdoc_col].astype(str).str.strip().str.upper()
    # Merge
    merged = pd.merge(tmd_df, tecdoc_df, on='clean', suffixes=('_tmd', '_tecdoc'))
    print(f"Gefundene exakte Matches: {len(merged)}")
    merged.to_csv(output_path, index=False)
    print(f"Ergebnis gespeichert unter: {output_path}")

# --- Parameter ---
TMD_FILE = "tmd_001000106869000000000065516001_data_2025-07-15-09-42-29-416.csv"
TABLES = {
    "120": "120_Vehicle_Types.csv",
    "200": "200_Article_Table.csv",
    "203": "203_Reference _Numbers.csv",
    "209": "209_GTIN.csv",
    "210": "210_Article_Criteria.csv",
    "213": "213_Article_Criteria.csv",
    "400": "400_Article_Linkage.csv"
}

def ean_one_to_one_matching(tmd_path, tecdoc_path, tmd_col, tecdoc_col, output_path):
    """
    Führt ein deterministisches 1:1-Matching (exakter Merge) auf Basis der EAN durch.
    tmd_col: Spaltenname in TMD-Datei (z.B. 'ean')
    tecdoc_col: Spaltenname in TecDoc-Datei (z.B. 'ean')
    output_path: Speicherort für Ergebnis-CSV
    """
    print(f"\n[EAN-Matching] Lese {tmd_path} und {tecdoc_path} ...")
    tmd_df = pd.read_csv(tmd_path, dtype=str, sep=None, engine='python')
    tecdoc_df = pd.read_csv(tecdoc_path, dtype=str, sep=None, engine='python')
    if tmd_col not in tmd_df.columns:
        print(f"Spalte '{tmd_col}' nicht in TMD-Datei gefunden!")
        return
    if tecdoc_col not in tecdoc_df.columns:
        print(f"Spalte '{tecdoc_col}' nicht in TecDoc-Datei gefunden!")
        return
    # TMD: EAN als String, nur Ziffern, führende Nullen auffüllen
    tmd_df['ean_clean'] = tmd_df[tmd_col].astype(str).str.replace(r'\D', '', regex=True).str.zfill(13)
    def gtin_to_str(val):
        try:
            if pd.isna(val) or str(val).strip() == '':
                return ''
            if 'E' in str(val).upper():
                return str(int(float(val))).zfill(13)
            return str(int(float(val))).zfill(13)
        except Exception:
            return str(val).strip()
    tecdoc_df['ean_clean'] = tecdoc_df[tecdoc_col].apply(gtin_to_str)
    # Filter: Nur echte, nicht-leere, nicht-Null EAN/GTIN
    tmd_df = tmd_df[(tmd_df['ean_clean'] != '') & (tmd_df['ean_clean'] != '0'*13)]
    tecdoc_df = tecdoc_df[(tecdoc_df['ean_clean'] != '') & (tecdoc_df['ean_clean'] != '0'*13)]
    print("\nErste 10 bereinigte EANs aus TMD:")
    print(tmd_df['ean_clean'].drop_duplicates().head(10).to_list())
    print("\nErste 10 bereinigte GTINs aus TecDoc:")
    print(tecdoc_df['ean_clean'].drop_duplicates().head(10).to_list())
    merged = pd.merge(tmd_df, tecdoc_df, left_on='ean_clean', right_on='ean_clean', suffixes=('_tmd', '_tecdoc'))
    print(f"Gefundene EAN-Matches: {len(merged)}")
    merged.to_csv(output_path, index=False)
    print(f"Ergebnis gespeichert unter: {output_path}")



# Matching-Aufrufe ans Dateiende in einen Main-Block verschieben
def exact_two_column_matching(tmd_path, tecdoc_path, tmd_col1, tmd_col2, tecdoc_col1, tecdoc_col2, output_path):
    print(f"\n[Deterministisches 2-Spalten-Matching] Lese {tmd_path} und {tecdoc_path} ...")
    tmd_df = pd.read_csv(tmd_path, dtype=str, sep=None, engine='python')
    tecdoc_df = pd.read_csv(tecdoc_path, dtype=str, sep=None, engine='python')
    tmd_df['key'] = tmd_df[tmd_col1].astype(str).str.strip().str.upper() + "_" + tmd_df[tmd_col2].astype(str).str.strip().str.upper()
    tecdoc_df['key'] = tecdoc_df[tecdoc_col1].astype(str).str.strip().str.upper() + "_" + tecdoc_df[tecdoc_col2].astype(str).str.strip().str.upper()
    merged = pd.merge(tmd_df, tecdoc_df, on='key', suffixes=('_tmd', '_tecdoc'))
    print(f"Gefundene 2-Spalten-Matches: {len(merged)}")
    merged.to_csv(output_path, index=False)
    print(f"Ergebnis gespeichert unter: {output_path}")

if __name__ == "__main__":
    # Beispielaufruf für exaktes Matching TMD <-> Tabelle 200 (Artikelnummer)
    exact_one_to_one_matching(
        tmd_path=TMD_FILE,
        tecdoc_path=TABLES["200"],
        tmd_col="tec_doc_article_number",
        tecdoc_col="artno",
        output_path="matching_output/exact_match_tmd_tecdoc200.csv"
    )

    # Matching auf Kombination: article_number + datasupplier_id
    exact_two_column_matching(
        tmd_path=TMD_FILE,
        tecdoc_path=TABLES["200"],
        tmd_col1="article_number",
        tmd_col2="tec_doc_data_supplier_number",
        tecdoc_col1="artno",
        tecdoc_col2="datasupplier_id",
        output_path="matching_output/exact_match_tmd_tecdoc200_2col.csv"
    )

    # --- Auskommentiert: EAN-Matching ---
    # ean_one_to_one_matching(
    #     tmd_path=TMD_FILE,
    #     tecdoc_path=TABLES["209"],
    #     tmd_col="ean",
    #     tecdoc_col="gtin",
    #     output_path="matching_output/ean_match_tmd_tecdoc209.csv"
    # )

    # Matching auf trade_number (TMD) gegen artno (TecDoc 200)
    exact_one_to_one_matching(
        tmd_path=TMD_FILE,
        tecdoc_path=TABLES["200"],
        tmd_col="trade_number",
        tecdoc_col="artno",
        output_path="matching_output/exact_match_tmd_trade_tecdoc200.csv"
    )