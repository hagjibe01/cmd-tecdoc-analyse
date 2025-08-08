import pandas as pd
import xml.etree.ElementTree as ET
import os

TECDOC_FILE = "200_Article_Table.csv"
CMD_XML_FILE = "MAT-684500001-20250712112631.xml"
OUTPUT_DIR = "matching_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Passe diese Spaltennamen ggf. an deine Datenstruktur an
TECDOC_COL = "artno"
CMD_COL = "article_number"

def clean_str(s):
    if not pd.notna(s):
        return ""
    s = str(s).strip().upper()
    s = ''.join(c for c in s if c.isalnum())
    s = s.lstrip("0")
    return s


# Extraktionsfunktionen für verschiedene Felder aus der XML
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
    tecdoc_df[TECDOC_COL] = tecdoc_df[TECDOC_COL].astype(str)
    tecdoc_df['clean_artno'] = tecdoc_df[TECDOC_COL].apply(clean_str)

    # --- Erweiterung: Brute-Force-Matching gegen alle TecDoc-Spalten ---
    # Felder aus XML
    supplierptno = extract_xml_values(CMD_XML_FILE, 'SupplierPtNo')
    tradeno = extract_xml_values(CMD_XML_FILE, 'TradeNo')
    df_supplierptno = pd.DataFrame({'SupplierPtNo': supplierptno})
    df_supplierptno['clean_supplierptno'] = df_supplierptno['SupplierPtNo'].apply(clean_str)
    df_tradeno = pd.DataFrame({'TradeNo': tradeno})
    df_tradeno['clean_tradeno'] = df_tradeno['TradeNo'].apply(clean_str)

    # Liste der TecDoc-Spalten (ohne Index und berechnete Spalten)
    ignore_cols = {'clean_artno', 'clean_commodity_code', 'clean_ean'}
    tecdoc_cols = [col for col in tecdoc_df.columns if col not in ignore_cols]

    # SupplierPtNo gegen alle TecDoc-Spalten
    for col in tecdoc_cols:
        tecdoc_df[f'clean_{col}'] = tecdoc_df[col].apply(clean_str)
        merged = pd.merge(df_supplierptno, tecdoc_df, left_on='clean_supplierptno', right_on=f'clean_{col}', how='inner', suffixes=('_xml', '_tecdoc'))
        if len(merged) > 0:
            print(f"SupplierPtNo <-> {col}: {len(merged)} Matches (alle Spalten)")
            merged.to_csv(f"{OUTPUT_DIR}/deterministic_match_supplierptno_{col}.csv", index=False)

    # TradeNo gegen alle TecDoc-Spalten
    for col in tecdoc_cols:
        tecdoc_df[f'clean_{col}'] = tecdoc_df[col].apply(clean_str)
        merged = pd.merge(df_tradeno, tecdoc_df, left_on='clean_tradeno', right_on=f'clean_{col}', how='inner', suffixes=('_xml', '_tecdoc'))
        if len(merged) > 0:
            print(f"TradeNo <-> {col}: {len(merged)} Matches (alle Spalten)")
            merged.to_csv(f"{OUTPUT_DIR}/deterministic_match_tradeno_{col}.csv", index=False)
    # TecDoc laden
    tecdoc_df = pd.read_csv(TECDOC_FILE, dtype=str, sep=None, engine='python')
    tecdoc_df[TECDOC_COL] = tecdoc_df[TECDOC_COL].astype(str)
    tecdoc_df['clean_artno'] = tecdoc_df[TECDOC_COL].apply(clean_str)


    # CMD XML laden
    # Debug: Zeige die ersten 20 Tag-Namen und Beispielwerte aus der XML
    import xml.etree.ElementTree as ET
    tree = ET.parse(CMD_XML_FILE)
    root = tree.getroot()
    #print("Erste 20 Tags und Werte aus der XML:")
    count = 0
    for elem in root.iter():
        #print(f"Tag: {elem.tag}, Wert: {elem.text}")
        count += 1
        if count >= 20:
            break


    # 1. SupplierPtNo <-> artno
    supplierptno = extract_xml_values(CMD_XML_FILE, 'SupplierPtNo')
    df_supplierptno = pd.DataFrame({'SupplierPtNo': supplierptno})
    df_supplierptno['clean_supplierptno'] = df_supplierptno['SupplierPtNo'].apply(clean_str)
    merged1 = pd.merge(df_supplierptno, tecdoc_df, left_on='clean_supplierptno', right_on='clean_artno', how='inner', suffixes=('_xml', '_tecdoc'))
    print(f"SupplierPtNo <-> artno: {len(merged1)} Matches")
    merged1.to_csv(f"{OUTPUT_DIR}/deterministic_match_supplierptno_artno.csv", index=False)

    # 2. TradeNo <-> artno
    tradeno = extract_xml_values(CMD_XML_FILE, 'TradeNo')
    df_tradeno = pd.DataFrame({'TradeNo': tradeno})
    df_tradeno['clean_tradeno'] = df_tradeno['TradeNo'].apply(clean_str)
    merged2 = pd.merge(df_tradeno, tecdoc_df, left_on='clean_tradeno', right_on='clean_artno', how='inner', suffixes=('_xml', '_tecdoc'))
    print(f"TradeNo <-> artno: {len(merged2)} Matches")
    merged2.to_csv(f"{OUTPUT_DIR}/deterministic_match_tradeno_artno.csv", index=False)

    # 3. CommodityCode <-> commodity_code (falls vorhanden)
    if 'commodity_code' in tecdoc_df.columns:
        commoditycode = extract_xml_values(CMD_XML_FILE, 'CommodityCode')
        df_commoditycode = pd.DataFrame({'CommodityCode': commoditycode})
        df_commoditycode['clean_commoditycode'] = df_commoditycode['CommodityCode'].apply(clean_str)
        tecdoc_df['clean_commodity_code'] = tecdoc_df['commodity_code'].apply(clean_str)
        merged3 = pd.merge(df_commoditycode, tecdoc_df, left_on='clean_commoditycode', right_on='clean_commodity_code', how='inner', suffixes=('_xml', '_tecdoc'))
        print(f"CommodityCode <-> commodity_code: {len(merged3)} Matches")
        merged3.to_csv(f"{OUTPUT_DIR}/deterministic_match_commoditycode.csv", index=False)
    else:
        print("Spalte 'commodity_code' in TecDoc nicht gefunden – CommodityCode-Matching übersprungen.")

    # 4. EAN/GTIN <-> ean (falls vorhanden)
    if 'ean' in tecdoc_df.columns:
        eans = extract_xml_values(CMD_XML_FILE, 'EAN')
        gtins = extract_xml_values(CMD_XML_FILE, 'GTIN')
        all_eans = eans + gtins
        df_ean = pd.DataFrame({'EAN_GTIN': all_eans})
        df_ean['clean_ean'] = df_ean['EAN_GTIN'].apply(clean_str)
        tecdoc_df['clean_ean'] = tecdoc_df['ean'].apply(clean_str)
        merged4 = pd.merge(df_ean, tecdoc_df, left_on='clean_ean', right_on='clean_ean', how='inner', suffixes=('_xml', '_tecdoc'))
        print(f"EAN/GTIN <-> ean: {len(merged4)} Matches")
        merged4.to_csv(f"{OUTPUT_DIR}/deterministic_match_ean.csv", index=False)
    else:
        print("Spalte 'ean' in TecDoc nicht gefunden – EAN/GTIN-Matching übersprungen.")

if __name__ == "__main__":
    main()
