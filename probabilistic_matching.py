import pandas as pd
import xml.etree.ElementTree as ET
from rapidfuzz import process, fuzz
import os

# --- Dateipfade ---
cmd_xml_path = "MAT-684500001-20250712112631.xml"
tecdoc_csv_path = "200_Article_Table.csv"
output_dir = "matching_output"
os.makedirs(output_dir, exist_ok=True)

# --- XML CMD-Daten einlesen ---
tree = ET.parse(cmd_xml_path)
root = tree.getroot()
ns = {'ns': root.tag.split('}')[0].strip('{')}

cmd_data = []
for article in root.findall('.//ns:Article', ns):
    supplier_pt_no_el = article.find('ns:SupplierPtNo', ns)
    brand_el = article.find('ns:Brand', ns)
    trade_no_el = article.find('.//ns:TradeNo', ns)
    supplier_pt_no = supplier_pt_no_el.text.strip() if supplier_pt_no_el is not None else ''
    brand = brand_el.text.strip() if brand_el is not None else ''
    trade_no = trade_no_el.text.strip() if trade_no_el is not None else ''
    cmd_data.append({
        'supplier_pt_no': supplier_pt_no,
        'brand': brand,
        'trade_no': trade_no
    })
cmd_df = pd.DataFrame(cmd_data)

# --- Spalten-Bereinigung ---
def clean_column(col):
    return col.astype(str).str.upper().str.replace(r'\W+', '', regex=True)

cmd_df['supplier_pt_no_clean'] = clean_column(cmd_df['supplier_pt_no'])
cmd_df['trade_no_clean'] = clean_column(cmd_df['trade_no'])

# --- TecDoc CSV einlesen (nur relevante Spalten, auf 10.000 Zeilen begrenzt) ---
tecdoc_df = pd.read_csv(tecdoc_csv_path, dtype=str, nrows=10000)
tecdoc_df['artno_clean'] = clean_column(tecdoc_df['artno'])

# --- Probalibistisches Matching (Fuzzy, Score als Wahrscheinlichkeit) ---
def probabilistic_match(cmd_series, tecdoc_series, threshold=70):
    matches = []
    tecdoc_list = tecdoc_series.dropna().unique().tolist()
    for cmd_val in cmd_series.dropna().unique():
        result = process.extract(cmd_val, tecdoc_list, scorer=fuzz.ratio, limit=3)
        for match_val, score, _ in result:
            if score >= threshold:
                matches.append({
                    'cmd_value': cmd_val,
                    'tecdoc_match': match_val,
                    'probability': score / 100.0
                })
    return pd.DataFrame(matches)

"""
Matching für verschiedene Spalten durchführen und Ergebnisse speichern
"""
# TradeNo <-> artno
prob_matches_trade = probabilistic_match(cmd_df['trade_no_clean'], tecdoc_df['artno_clean'], threshold=70)
prob_matches_trade.to_csv(f"{output_dir}/probabilistic_trade_no_matches.csv", index=False)
print(f"Probalibistische Matches TradeNo-artno gespeichert: {len(prob_matches_trade)}")
if not prob_matches_trade.empty:
    print("Beispiel TradeNo-artno:")
    print(prob_matches_trade.head())
else:
    print("Keine probabilistischen Matches für TradeNo-artno gefunden.")

# SupplierPtNo <-> artno
prob_matches_supplier = probabilistic_match(cmd_df['supplier_pt_no_clean'], tecdoc_df['artno_clean'], threshold=70)
prob_matches_supplier.to_csv(f"{output_dir}/probabilistic_supplierptno_matches.csv", index=False)
print(f"Probalibistische Matches SupplierPtNo-artno gespeichert: {len(prob_matches_supplier)}")
if not prob_matches_supplier.empty:
    print("Beispiel SupplierPtNo-artno:")
    print(prob_matches_supplier.head())
else:
    print("Keine probabilistischen Matches für SupplierPtNo-artno gefunden.")

# Brand <-> brandno (sofern vorhanden)
if 'brandno' in tecdoc_df.columns:
    tecdoc_df['brandno_clean'] = clean_column(tecdoc_df['brandno'])
    prob_matches_brand = probabilistic_match(cmd_df['brand'].astype(str).str.upper().str.replace(r'\W+', '', regex=True), tecdoc_df['brandno_clean'], threshold=70)
    prob_matches_brand.to_csv(f"{output_dir}/probabilistic_brand_matches.csv", index=False)
    print(f"Probalibistische Matches Brand-brandno gespeichert: {len(prob_matches_brand)}")
    if not prob_matches_brand.empty:
        print("Beispiel Brand-brandno:")
        print(prob_matches_brand.head())
    else:
        print("Keine probabilistischen Matches für Brand-brandno gefunden.")
"""Diese Datei wurde entfernt. Alle deterministischen Matchings sind jetzt in match.py enthalten."""
