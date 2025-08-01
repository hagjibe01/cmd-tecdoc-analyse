import pandas as pd

# CMD-Datei einlesen
cmd_df = pd.read_csv("tmd_001000106869000000000065516001_data_2025-07-15-09-42-29-416.csv", sep=";", dtype=str)

# TecDoc Datei (200_Article_Table.csv) korrekt einlesen: Komma als Trennzeichen!
tecdoc_df = pd.read_csv("200_Article_Table.csv", sep=",", dtype=str)

# Spalten bereinigen (Anführungszeichen entfernen)
tecdoc_df.columns = tecdoc_df.columns.str.replace('"', '').str.strip()

# Check
print("✅ CMD Spalten:", cmd_df.columns.tolist())
print("✅ TecDoc Spalten:", tecdoc_df.columns.tolist())

# Cleanups für Matching
cmd_df['article_number_clean'] = cmd_df['article_number'].astype(str).str.upper().str.replace(r'\W+', '', regex=True)
cmd_df['datasupplier_id_clean'] = cmd_df['tec_doc_data_supplier_number'].astype(str).str.strip()

tecdoc_df['article_number_clean'] = tecdoc_df['artno'].astype(str).str.upper().str.replace(r'\W+', '', regex=True)
tecdoc_df['datasupplier_id_clean'] = tecdoc_df['datasupplier_id'].astype(str).str.strip()

# Debug-Ausgaben
print("\n🔍 Beispiel Datasupplier-ID CMD:", cmd_df['datasupplier_id_clean'].value_counts().head())
print("🔍 Beispiel Datasupplier-ID TecDoc:", tecdoc_df['datasupplier_id_clean'].value_counts().head())

# Matching auf Artikelnummer + Datenlieferant
matched = pd.merge(
    cmd_df,
    tecdoc_df,
    on=['article_number_clean', 'datasupplier_id_clean'],
    how='inner'
)

print(f"\n✅ Gefundene Matches: {len(matched)}")

# Ergebnis speichern
matched.to_csv("matching_output/match_article_datasupplier.csv", index=False)
print("📂 Ergebnis gespeichert: matching_output/match_article_datasupplier.csv")