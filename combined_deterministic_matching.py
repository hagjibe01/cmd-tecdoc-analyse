import pandas as pd
import os

TMD_FILE = "tmd_001000106869000000000065516001_data_2025-07-15-09-42-29-416.csv"
TECDOC_FILE = "200_Article_Table.csv"
OUTPUT_DIR = "matching_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Hilfsfunktion zur Bereinigung von Strings
def clean_str(s):
    return str(s).strip().upper() if pd.notna(s) else ""

def exact_one_to_one_matching(tmd_df, tecdoc_df, tmd_col, tecdoc_col):
    tmd_df = tmd_df.copy()
    tecdoc_df = tecdoc_df.copy()
    # Prüfe Anteil nicht-leerer Werte
    tmd_nonempty = tmd_df[tmd_col].notna() & (tmd_df[tmd_col].astype(str).str.strip() != "")
    tecdoc_nonempty = tecdoc_df[tecdoc_col].notna() & (tecdoc_df[tecdoc_col].astype(str).str.strip() != "")
    tmd_ratio = tmd_nonempty.sum() / len(tmd_df) if len(tmd_df) > 0 else 0
    tecdoc_ratio = tecdoc_nonempty.sum() / len(tecdoc_df) if len(tecdoc_df) > 0 else 0
    if tmd_ratio < 0.01 or tecdoc_ratio < 0.01:
        print(f"[Übersprungen: Zu viele leere Werte] {tmd_col} <-> {tecdoc_col} (TMD: {tmd_ratio:.2%}, TecDoc: {tecdoc_ratio:.2%})")
        return pd.DataFrame()
    tmd_df['clean'] = tmd_df[tmd_col].apply(clean_str)
    tecdoc_df['clean'] = tecdoc_df[tecdoc_col].apply(clean_str)
    merged = pd.merge(tmd_df, tecdoc_df, on='clean', suffixes=('_tmd', '_tecdoc'))
    return merged

def exact_two_column_matching(tmd_df, tecdoc_df, tmd_col1, tmd_col2, tecdoc_col1, tecdoc_col2):
    tmd_df = tmd_df.copy()
    tecdoc_df = tecdoc_df.copy()
    # Prüfe Anteil nicht-leerer Werte für beide Spalten
    tmd_nonempty = (tmd_df[tmd_col1].notna() & (tmd_df[tmd_col1].astype(str).str.strip() != "")) & \
                  (tmd_df[tmd_col2].notna() & (tmd_df[tmd_col2].astype(str).str.strip() != ""))
    tecdoc_nonempty = (tecdoc_df[tecdoc_col1].notna() & (tecdoc_df[tecdoc_col1].astype(str).str.strip() != "")) & \
                     (tecdoc_df[tecdoc_col2].notna() & (tecdoc_df[tecdoc_col2].astype(str).str.strip() != ""))
    tmd_ratio = tmd_nonempty.sum() / len(tmd_df) if len(tmd_df) > 0 else 0
    tecdoc_ratio = tecdoc_nonempty.sum() / len(tecdoc_df) if len(tecdoc_df) > 0 else 0
    if tmd_ratio < 0.01 or tecdoc_ratio < 0.01:
        print(f"[Übersprungen: Zu viele leere Werte] {tmd_col1}+{tmd_col2} <-> {tecdoc_col1}+{tecdoc_col2} (TMD: {tmd_ratio:.2%}, TecDoc: {tecdoc_ratio:.2%})")
        return pd.DataFrame()
    tmd_df['key'] = tmd_df[tmd_col1].apply(clean_str) + "_" + tmd_df[tmd_col2].apply(clean_str)
    tecdoc_df['key'] = tecdoc_df[tecdoc_col1].apply(clean_str) + "_" + tecdoc_df[tecdoc_col2].apply(clean_str)
    merged = pd.merge(tmd_df, tecdoc_df, on='key', suffixes=('_tmd', '_tecdoc'))
    return merged
import pandas as pd
import xml.etree.ElementTree as ET
import os
import itertools

TECDOC_FILE = "200_Article_Table.csv"
CMD_XML_FILE = "MAT-684500001-20250712112631.xml"
OUTPUT_DIR = "matching_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_str(s):
    if not pd.notna(s):
        return ""
    s = str(s).strip().upper()
    s = ''.join(c for c in s if c.isalnum())
    s = s.lstrip("0")
    return s

def extract_xml_values(xml_path, tag_name):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    values = []
    for elem in root.iter():
        if elem.tag.endswith(tag_name):
            if elem.text:
                values.append(elem.text)
    return values

def main():
    # TecDoc laden
    tecdoc_df = pd.read_csv(TECDOC_FILE, dtype=str, sep=None, engine='python')
    tecdoc_df = tecdoc_df.fillna("")

    # XML-Felder extrahieren
    supplierptno = extract_xml_values(CMD_XML_FILE, 'SupplierPtNo')
    tradeno = extract_xml_values(CMD_XML_FILE, 'TradeNo')
    # ggf. weitere Felder ergänzen

    # Kombinierte Felder für Matching
    xml_combos = list(itertools.product(supplierptno, tradeno))
    xml_combo_df = pd.DataFrame(xml_combos, columns=['SupplierPtNo', 'TradeNo'])
    xml_combo_df['clean_supplierptno'] = xml_combo_df['SupplierPtNo'].apply(clean_str)
    xml_combo_df['clean_tradeno'] = xml_combo_df['TradeNo'].apply(clean_str)
    xml_combo_df['combo_key'] = xml_combo_df['clean_supplierptno'] + "_" + xml_combo_df['clean_tradeno']

    # TecDoc-Kombis bauen (nur Spalten, die existieren)
    tecdoc_cols = tecdoc_df.columns
    # Kombi: artno + brandno
    if 'artno' in tecdoc_cols and 'brandno' in tecdoc_cols:
        tecdoc_df['clean_artno'] = tecdoc_df['artno'].apply(clean_str)
        tecdoc_df['clean_brandno'] = tecdoc_df['brandno'].apply(clean_str)
        tecdoc_df['combo_key'] = tecdoc_df['clean_artno'] + "_" + tecdoc_df['clean_brandno']
        merged = pd.merge(xml_combo_df, tecdoc_df, on='combo_key', suffixes=('_xml', '_tecdoc'))
        print(f"Kombiniertes Matching SupplierPtNo+TradeNo <-> artno+brandno: {len(merged)} Matches")
        merged.to_csv(f"{OUTPUT_DIR}/combined_match_supplierptno_tradeno_artno_brandno.csv", index=False)
    else:
        print("Spalten 'artno' und/oder 'brandno' nicht in TecDoc gefunden – Kombi-Matching übersprungen.")

    # Kombi: artno + datasupplier_id
    if 'artno' in tecdoc_cols and 'datasupplier_id' in tecdoc_cols:
        tecdoc_df['clean_datasupplier_id'] = tecdoc_df['datasupplier_id'].apply(clean_str)
        tecdoc_df['combo_key2'] = tecdoc_df['clean_artno'] + "_" + tecdoc_df['clean_datasupplier_id']
        merged2 = pd.merge(xml_combo_df, tecdoc_df, left_on='combo_key', right_on='combo_key2', suffixes=('_xml', '_tecdoc'))
        print(f"Kombiniertes Matching SupplierPtNo+TradeNo <-> artno+datasupplier_id: {len(merged2)} Matches")
        merged2.to_csv(f"{OUTPUT_DIR}/combined_match_supplierptno_tradeno_artno_datasupplierid.csv", index=False)
    else:
        print("Spalten 'artno' und/oder 'datasupplier_id' nicht in TecDoc gefunden – Kombi-Matching übersprungen.")

if __name__ == "__main__":
    main()
