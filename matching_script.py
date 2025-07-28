import pandas as pd

# Eingabedateien
cmd_file = ""
tecdoc_file = "tecdoc_data.csv"

# Einlesen der Daten
cmd_df = pd.read_csv(cmd_file, dtype=str)
tecdoc_df = pd.read_csv(tecdoc_file, dtype=str)

# Vorverarbeitung (z.B. Leerzeichen entfernen, alles in Großbuchstaben)
def clean_column(col):
    return col.astype(str).str.strip().str.upper()

cmd_df['ean_clean'] = clean_column(cmd_df['ean'])
tecdoc_df['ean_clean'] = clean_column(tecdoc_df['ean'])

cmd_df['supplier_no_clean'] = clean_column(cmd_df['supplier_part_number'])
cmd_df['brand_clean'] = clean_column(cmd_df['brand'])

tecdoc_df['supplier_no_clean'] = clean_column(tecdoc_df['supplier_part_number'])
tecdoc_df['brand_clean'] = clean_column(tecdoc_df['brand'])

# 1. Deterministisches Matching über EAN
match_ean = pd.merge(cmd_df, tecdoc_df, on='ean_clean', suffixes=('_cmd', '_tecdoc'))

# 2. Matching über TecDoc-Nummer
match_tecdoc_nr = pd.merge(cmd_df, tecdoc_df, left_on='tec_doc_article_number', right_on='artno', suffixes=('_cmd', '_tecdoc'))

# 3. Kombination: Supplier Part Number + Brand
match_supplier_brand = pd.merge(
    cmd_df,
    tecdoc_df,
    on=['supplier_no_clean', 'brand_clean'],
    suffixes=('_cmd', '_tecdoc')
)

# Ergebnisse speichern
match_ean.to_csv("match_ean.csv", index=False)
match_tecdoc_nr.to_csv("match_tecdoc_nr.csv", index=False)
match_supplier_brand.to_csv("match_supplier_brand.csv", index=False)

# Zusammenfassung
print("Matches über EAN:", len(match_ean))
print("Matches über TecDoc-Nr:", len(match_tecdoc_nr))
print("Matches über Supplier Part Number + Brand:", len(match_supplier_brand))
