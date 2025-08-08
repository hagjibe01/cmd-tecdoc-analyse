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
    # Diese Funktion bleibt für Einzelwert-Extraktion erhalten
    tree = ET.parse(xml_path)
    root = tree.getroot()
    values = []
    for elem in root.iter():
        if elem.tag.endswith(tag_name):
            if elem.text:
                values.append(elem.text)
    return values

# Extrahiere echte Paare (SupplierPtNo, TradeNo) pro Artikel aus der XML
def extract_xml_pairs(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    pairs = []
    # Annahme: Jeder <Article> Block enthält die Felder
    for article in root.iter():
        if article.tag.endswith('Article'):
            supplier = None
            trade = None
            for child in article:
                if child.tag.endswith('SupplierPtNo'):
                    supplier = child.text
                if child.tag.endswith('TradeNo'):
                    trade = child.text
            if supplier and trade:
                pairs.append((supplier, trade))
    return pairs

def main():
    # TecDoc laden
    tecdoc_df = pd.read_csv(TECDOC_FILE, dtype=str, sep=None, engine='python')
    tecdoc_df = tecdoc_df.fillna("")

    # Echte Paare extrahieren
    xml_pairs = extract_xml_pairs(CMD_XML_FILE)
    xml_combo_df = pd.DataFrame(xml_pairs, columns=['SupplierPtNo', 'TradeNo'])
    xml_combo_df['clean_supplierptno'] = xml_combo_df['SupplierPtNo'].apply(clean_str)
    xml_combo_df['clean_tradeno'] = xml_combo_df['TradeNo'].apply(clean_str)
    xml_combo_df['combo_key'] = xml_combo_df['clean_supplierptno'] + "_" + xml_combo_df['clean_tradeno']


    # Liste der wichtigsten TecDoc-Spalten für Kombis
    main_cols = ['artno', 'brandno', 'datasupplier_id', 'oe', 'supno', 'gtin', 'ean']
    tecdoc_cols = [col for col in main_cols if col in tecdoc_df.columns]

    # Alle 2er-Kombinationen der TecDoc-Spalten testen
    from itertools import combinations
    for col1, col2 in combinations(tecdoc_cols, 2):
        tecdoc_df[f'clean_{col1}'] = tecdoc_df[col1].apply(clean_str)
        tecdoc_df[f'clean_{col2}'] = tecdoc_df[col2].apply(clean_str)
        tecdoc_df['combo_key'] = tecdoc_df[f'clean_{col1}'] + "_" + tecdoc_df[f'clean_{col2}']
        merged = pd.merge(xml_combo_df, tecdoc_df, on='combo_key', suffixes=('_xml', '_tecdoc'))
        if len(merged) > 0:
            print(f"Kombiniertes Matching SupplierPtNo+TradeNo <-> {col1}+{col2}: {len(merged)} Matches")
            merged.to_csv(f"{OUTPUT_DIR}/combined_match_supplierptno_tradeno_{col1}_{col2}.csv", index=False)
        else:
            print(f"Kombiniertes Matching SupplierPtNo+TradeNo <-> {col1}+{col2}: 0 Matches")

if __name__ == "__main__":
    main()
