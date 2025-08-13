import pandas as pd
import xml.etree.ElementTree as ET
import os

TECDOC_FILE = "200_Article_Table.csv"
CMD_XML_FILE = "MAT-684500001-20250712112631.xml"
OUTPUT_DIR = "matching_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Regelbasiertes Mapping: Liste von (TecDoc-Spalte, CMD-Spalte, Regel)
# Die Regel ist eine Funktion, die zwei Werte (tecdoc, cmd) vergleicht und True/False zurückgibt
mapping_rules = [
    ("artno", "SupplierPtNo", lambda t, c: t == c),
    ("brandno", "Brand", lambda t, c: str(t) == str(c)),
    ("CommodityCode", "CommodityCode", lambda t, c: t == c),
    ("BaseUOM", "BaseUOM", lambda t, c: t == c),
    ("MinOrderQuantity", "MinOrderQuantity", lambda t, c: t == c),
    ("MaxOrderQuantity", "MaxOrderQuantity", lambda t, c: t == c),
    ("GrossWeight", "GrossWeight", lambda t, c: abs(float(t)-float(c)) < 0.01 if t and c else False),
    ("Volume", "Volume", lambda t, c: abs(float(t)-float(c)) < 0.01 if t and c else False),
    ("ArticleDescription_DE", "ArticleDescription_DE", lambda t, c: t == c),
    ("ArticleDescription_EN", "ArticleDescription_EN", lambda t, c: t == c),
]

# Cleaning-Funktion
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
    # XML-Daten vorbereiten
    cmd_data = {}
    for _, cmd_col, _ in mapping_rules:
        cmd_data[cmd_col] = extract_xml_values(CMD_XML_FILE, cmd_col)
    # Debug: Zeige alle extrahierten Spaltennamen und die ersten 10 Werte jeder Spalte
    print("Extrahierte XML-Spalten und Beispielwerte:")
    for k, v in cmd_data.items():
        print(f"{k}: {v[:10]}")
    cmd_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in cmd_data.items()]))
    for col in cmd_df.columns:
        cmd_df[f'clean_{col.lower()}'] = cmd_df[col].apply(clean_str)

    # TecDoc iterativ einlesen (wegen Größe)
    chunk_size = 500_000
    match_count = 0
    first_chunk = True
    for chunk in pd.read_csv(TECDOC_FILE, dtype=str, sep=None, engine='python', chunksize=chunk_size):
        chunk = chunk.astype(str)
        for tec_col, cmd_col, rule in mapping_rules:
            if tec_col not in chunk.columns or f'clean_{cmd_col.lower()}' not in cmd_df.columns:
                continue
            chunk[f'clean_{tec_col.lower()}'] = chunk[tec_col].apply(clean_str)
            tec_vals = chunk[[tec_col, f'clean_{tec_col.lower()}']]
            cmd_vals = cmd_df[[cmd_col, f'clean_{cmd_col.lower()}']]
            # Debug-Ausgabe nach erstem Chunk für jede Spalte
            if first_chunk:
                print(f"--- Debug TecDoc {tec_col} ---")
                print("Erste 10 Clean-Werte:", tec_vals[f'clean_{tec_col.lower()}'].head(10).tolist())
                print("Nicht-leere Werte:", tec_vals[f'clean_{tec_col.lower()}'].replace('', pd.NA).dropna().shape[0])
                print(f"--- Debug CMD {cmd_col} ---")
                print("Erste 10 Clean-Werte:", cmd_vals[f'clean_{cmd_col.lower()}'].head(10).tolist())
                print("Nicht-leere Werte:", cmd_vals[f'clean_{cmd_col.lower()}'].replace('', pd.NA).dropna().shape[0])
            # Regelbasiertes Matching
            matches = []
            for idx, tec_row in tec_vals.iterrows():
                tec_val = tec_row[f'clean_{tec_col.lower()}']
                if tec_val == "":
                    continue
                found = cmd_vals[cmd_vals[f'clean_{cmd_col.lower()}'] != ""]
                for _, cmd_row in found.iterrows():
                    if rule(tec_val, cmd_row[f'clean_{cmd_col.lower()}']):
                        matches.append({
                            f'tec_{tec_col}': tec_row[tec_col],
                            f'cmd_{cmd_col}': cmd_row[cmd_col]
                        })
            if matches:
                match_count += len(matches)
                out_file = f"{OUTPUT_DIR}/regelbasiert_{tec_col.lower()}_{cmd_col.lower()}_matches.csv"
                pd.DataFrame(matches).to_csv(out_file, mode='a', header=not os.path.exists(out_file), index=False)
                print(f"{tec_col} <-> {cmd_col}: {len(matches)} neue Matches (Regel) im Chunk, insgesamt {match_count}")
        first_chunk = False

if __name__ == "__main__":
    main()
