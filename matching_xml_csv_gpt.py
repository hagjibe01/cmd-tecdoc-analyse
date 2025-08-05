import pandas as pd
import xml.etree.ElementTree as ET
from rapidfuzz import fuzz, process
import matplotlib.pyplot as plt
import os

# ----- Datei-Pfade -----
cmd_xml_path = "MAT-684500001-20250712112631.xml"
tecdoc_csv_path = "200_Article_Table.csv"

# ----- Matching Output Ordner -----
os.makedirs("matching_output", exist_ok=True)

# ----- XML CMD-Daten einlesen -----
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

# ----- Spalten-Bereinigung -----
def clean_column(col):
    return col.astype(str).str.upper().str.replace(r'\W+', '', regex=True)

cmd_df['supplier_pt_no_clean'] = clean_column(cmd_df['supplier_pt_no'])
cmd_df['trade_no_clean'] = clean_column(cmd_df['trade_no'])

# Debug: Prüfen, ob CSV Trennzeichen stimmt
with open(tecdoc_csv_path, 'r', encoding='utf-8') as f:
    first_line = f.readline()
    print(f"🔍 Erste Zeile in TecDoc CSV: {first_line}")

# ----- TecDoc CSV chunkweise einlesen & bereinigen -----
chunksize = 100000
matches_deterministic = []
tecdoc_chunks = []

first_chunk = True  # Nur für erstes Chunk-Spalten-Print

for chunk in pd.read_csv(tecdoc_csv_path, chunksize=chunksize, sep=',', dtype=str):
    if first_chunk:
        print("Aktuelle Spalten:", chunk.columns.tolist())
        first_chunk = False

    chunk['artno_clean'] = clean_column(chunk['artno'])
    tecdoc_chunks.append(chunk[['artno_clean']])

    # Deterministisches Matching: Trade Number ↔ artno
    match_trade = pd.merge(cmd_df, chunk, left_on='trade_no_clean', right_on='artno_clean')
    if not match_trade.empty:
        matches_deterministic.append(match_trade)

# ----- Deterministische Ergebnisse zusammenführen -----
if matches_deterministic:
    result_deterministic_df = pd.concat(matches_deterministic, ignore_index=True)
    result_deterministic_df.to_csv("matching_output/deterministic_matches.csv", index=False)
else:
    print("❌ Keine deterministischen Matches gefunden.")
    result_deterministic_df = pd.DataFrame()

# ----- Fuzzy Matching vorbereiten -----
tecdoc_df = pd.concat(tecdoc_chunks).drop_duplicates().reset_index(drop=True)

# ----- Prefix-Fuzzy Matching Funktion -----
def fuzzy_match_prefix(cmd_series, tecdoc_series, threshold=80, prefix_length=4):
    matches = []
    tecdoc_series_list = tecdoc_series.tolist()

    for cmd_val in cmd_series.unique():
        prefix = cmd_val[:prefix_length]  # nur erste X Zeichen
        candidates = [val for val in tecdoc_series_list if val.startswith(prefix)]

        if not candidates:
            continue

        match, score, _ = process.extractOne(cmd_val, candidates, scorer=fuzz.ratio)
        if score >= threshold:
            matches.append({'cmd_value': cmd_val, 'tecdoc_match': match, 'similarity': score})

    return pd.DataFrame(matches)

# ----- Fuzzy Matching durchführen -----
fuzzy_matches_df = fuzzy_match_prefix(cmd_df['trade_no_clean'], tecdoc_df['artno_clean'], threshold=80, prefix_length=4)
fuzzy_matches_df.to_csv("matching_output/fuzzy_matched_trade_no.csv", index=False)

# ----- Visualisierung -----
total_unique_trade_numbers = cmd_df['trade_no_clean'].nunique()
unique_deterministic_matches = result_deterministic_df['trade_no_clean'].nunique() if not result_deterministic_df.empty else 0
unique_fuzzy_matches = fuzzy_matches_df['cmd_value'].nunique()

plt.figure(figsize=(8, 5))
plt.bar(['Deterministic Match', 'Fuzzy Match', 'Unmatched'], [
    unique_deterministic_matches,
    unique_fuzzy_matches,
    total_unique_trade_numbers - max(unique_deterministic_matches, unique_fuzzy_matches)
])
plt.ylabel('Anzahl eindeutiger Artikel')
plt.title(f'Matching-Übersicht (Total: {total_unique_trade_numbers} eindeutige Artikel)')
plt.tight_layout()
plt.savefig("matching_output/matching_overview.png")
plt.show()

# ----- Summary Print -----
print(f"🔍 Eindeutige Trade Numbers in CMD: {total_unique_trade_numbers}")
print(f"✅ Eindeutige deterministische Matches: {unique_deterministic_matches}")
print(f"✅ Eindeutige Fuzzy Matches (>=80%): {unique_fuzzy_matches}")
