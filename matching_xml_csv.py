
import pandas as pd
from rapidfuzz import process
from rapidfuzz.distance import Levenshtein, JaroWinkler
import xml.etree.ElementTree as ET

def fuzzy_match_columns(df_a, df_b, col_a, col_b, method="levenshtein", threshold=85, top_n=1):
    if method == "levenshtein":
        scorer = Levenshtein.normalized_similarity
    elif method == "jaro":
        scorer = JaroWinkler.normalized_similarity
    else:
        raise ValueError("Unbekannte Methode")
    results = []
    values_b = df_b[col_b].dropna().astype(str).unique().tolist()
    for val_a in df_a[col_a].dropna().astype(str).unique():
        matches = process.extract(val_a, values_b, scorer=scorer, limit=top_n)
        for match in matches:
            if match[1] >= threshold:
                results.append({
                    "value_a": val_a,
                    "value_b": match[0],
                    "score": match[1]
                })
    return pd.DataFrame(results)

# === XML parsen und DataFrame bauen ===
def parse_cmd_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    ns = {'ns': root.tag.split('}')[0].strip('{')}  # Namespace extrahieren
    articles = []
    for art in root.findall('.//ns:Article', ns):
        entry = {}
        entry['SupplierPtNo'] = art.findtext('ns:SupplierPtNo', default='', namespaces=ns)
        entry['Brand'] = art.findtext('ns:Brand', default='', namespaces=ns)
        entry['SalesCountry'] = art.findtext('ns:SalesCountry', default='', namespaces=ns)
        entry['CommodityCode'] = art.findtext('ns:CommodityCode', default='', namespaces=ns)
        entry['ExchangePart'] = art.findtext('ns:ExchangePart', default='', namespaces=ns)
        # Beschreibung DE/EN
        desc_de = art.find('.//ns:ArticleDescription[@Language="DE"]', ns)
        desc_en = art.find('.//ns:ArticleDescription[@Language="EN"]', ns)
        entry['ArticleDescription_DE'] = desc_de.text if desc_de is not None else ''
        entry['ArticleDescription_EN'] = desc_en.text if desc_en is not None else ''
        articles.append(entry)
    return pd.DataFrame(articles)

# === Dateipfade anpassen ===
cmd_path = "MAT-684500001-20250712112631.xml"
tecdoc_path = "400_Article_Linkage.csv"

# CMD-XML parsen
cmd_df = parse_cmd_xml(cmd_path)
# TecDoc: Nur die ersten 10.000 Zeilen laden
tecdoc_df = pd.read_csv(tecdoc_path, dtype=str, nrows=10000)


# Fuzzy Matching SupplierPtNo <-> artno
result_artno = fuzzy_match_columns(cmd_df, tecdoc_df, "SupplierPtNo", "artno", method="levenshtein", threshold=85)
print("Fuzzy Matching SupplierPtNo <-> artno:")
print(result_artno)

# Fuzzy Matching Brand <-> brandno
result_brand = fuzzy_match_columns(cmd_df, tecdoc_df, "Brand", "brandno", method="levenshtein", threshold=85)
print("Fuzzy Matching Brand <-> brandno:")
print(result_brand)

# Fuzzy Matching CommodityCode <-> genartno
if "CommodityCode" in cmd_df.columns and "genartno" in tecdoc_df.columns:
    result_genartno = fuzzy_match_columns(cmd_df, tecdoc_df, "CommodityCode", "genartno", method="levenshtein", threshold=85)
    print("Fuzzy Matching CommodityCode <-> genartno:")
    print(result_genartno)
     
# Deterministisches Matching SupplierPtNo <-> artno
cmd_df["SupplierPtNo_clean"] = cmd_df["SupplierPtNo"].astype(str).str.replace(".", "").str.strip().str.upper()
tecdoc_df["artno_clean"] = tecdoc_df["artno"].astype(str).str.replace(".", "").str.strip().str.upper()
deterministic_artno = pd.merge(cmd_df, tecdoc_df, left_on="SupplierPtNo_clean", right_on="artno_clean", how="inner")
print("Deterministisches Matching SupplierPtNo <-> artno:")
print(deterministic_artno[["SupplierPtNo", "artno", "Brand", "brandno"]] if not deterministic_artno.empty else "Keine Matches")

# Deterministisches Matching Brand <-> brandno
cmd_df["Brand_clean"] = cmd_df["Brand"].astype(str).str.strip().str.upper()
tecdoc_df["brandno_clean"] = tecdoc_df["brandno"].astype(str).str.strip().str.upper()
deterministic_brand = pd.merge(cmd_df, tecdoc_df, left_on="Brand_clean", right_on="brandno_clean", how="inner")
print("Deterministisches Matching Brand <-> brandno:")
print(deterministic_brand[["Brand", "brandno", "SupplierPtNo", "artno"]] if not deterministic_brand.empty else "Keine Matches")