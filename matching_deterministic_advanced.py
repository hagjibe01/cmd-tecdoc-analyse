import pandas as pd
import xml.etree.ElementTree as ET
import os

TECDOC_FILE = "200_Article_Table.csv"
CMD_XML_FILE = "MAT-684500001-20250712112631.xml"
OUTPUT_DIR = "matching_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_str(s):
    """Standardisiert Strings für Vergleiche"""
    if not pd.notna(s) or s == 'nan':
        return ""
    s = str(s).strip().upper()
    s = ''.join(c for c in s if c.isalnum())
    s = s.lstrip("0")
    return s

def normalize_str(s):
    """Normalisiert Strings (entfernt Sonderzeichen, Bindestriche, Punkte)"""
    if not pd.notna(s) or s == 'nan':
        return ""
    s = str(s).strip().upper()
    # Entferne alle Sonderzeichen außer Buchstaben und Zahlen
    s = ''.join(c for c in s if c.isalnum())
    return s

def get_prefix(s, length=5):
    """Gibt die ersten N Zeichen zurück"""
    s = normalize_str(s)
    return s[:length] if len(s) >= length else s

def get_suffix(s, length=5):
    """Gibt die letzten N Zeichen zurück"""
    s = normalize_str(s)
    return s[-length:] if len(s) >= length else s

def extract_xml_values(xml_path, tag_name):
    """Extrahiert alle Werte für einen bestimmten Tag aus der XML"""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        values = []
        for elem in root.iter():
            if elem.tag.endswith(tag_name):
                if elem.text:
                    values.append(elem.text)
        return values
    except Exception as e:
        print(f"Fehler beim Extrahieren von {tag_name}: {e}")
        return []

def main():
    print("Starte deterministische Matching-Verfahren zwischen TecDoc und CMD...")
    
    # Verschiedene deterministische Matching-Ansätze
    matching_methods = {
        "Exakt": {
            "pairs": [
                ("artno", "SupplierPtNo"),
                ("brandno", "Brand"),
                ("batchsize1", "MinOrderQuantity"),
                ("batchsize2", "MaxOrderQuantity"),
                ("batchsize1", "GrossWeight"),
                ("batchsize2", "Volume"),
            ],
            "prep_func": clean_str,
            "match_func": lambda a, b: a == b and len(a) > 0
        },
        "Normalisiert": {
            "pairs": [
                ("artno", "SupplierPtNo"),
                ("brandno", "Brand"),
            ],
            "prep_func": normalize_str,
            "match_func": lambda a, b: a == b and len(a) > 0
        },
        "Teilstring": {
            "pairs": [
                ("artno", "SupplierPtNo"),
                ("artno", "ArticleDescription_DE"),
                ("artno", "ArticleDescription_EN"),
            ],
            "prep_func": normalize_str,
            "match_func": lambda a, b: (a in b or b in a) if len(a) >= 3 and len(b) >= 3 else False
        },
        "Prefix_5": {
            "pairs": [
                ("artno", "SupplierPtNo"),
                ("brandno", "Brand"),
            ],
            "prep_func": lambda s: get_prefix(s, 5),
            "match_func": lambda a, b: a == b and len(a) >= 5
        }
    }
    
    # XML-Daten einlesen - sammle alle benötigten Spalten
    all_cmd_cols = set()
    for method_name, method_data in matching_methods.items():
        for tec_col, cmd_col in method_data["pairs"]:
            all_cmd_cols.add(cmd_col)
    
    print("Lade XML-Daten...")
    cmd_data = {}
    for cmd_col in all_cmd_cols:
        values = extract_xml_values(CMD_XML_FILE, cmd_col)
        cmd_data[cmd_col] = values
        print(f"XML {cmd_col}: {len(values)} Werte gefunden, erste 3: {values[:3]}")
    
    # CMD DataFrame erstellen
    cmd_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in cmd_data.items()]))
    print(f"CMD DataFrame erstellt: {len(cmd_df)} Zeilen")
    
    # TecDoc chunkweise verarbeiten (nur erste 6 Chunks für Testzwecke)
    chunk_size = 50_000  # Kleinere Chunks für bessere Performance
    max_chunks = 6  # Begrenzung für Tests
    chunk_num = 0
    
    # Dictionary für Ergebnisse aller Matching-Verfahren
    matching_results = {}
    for method_name, method_data in matching_methods.items():
        for tec_col, cmd_col in method_data["pairs"]:
            key = f"{method_name}: {tec_col} <-> {cmd_col}"
            matching_results[key] = 0
    
    print(f"Starte chunkweise Verarbeitung der TecDoc-Datei (maximal {max_chunks} Chunks für Tests)...")
    
    try:
        for chunk in pd.read_csv(TECDOC_FILE, dtype=str, sep=None, engine='python', chunksize=chunk_size):
            chunk_num += 1
            print(f"Verarbeite Chunk {chunk_num} ({len(chunk)} Zeilen)...")
            
            # Chunk vorbereiten
            chunk = chunk.astype(str)
            
            # Stoppe nach max_chunks für Testzwecke
            if chunk_num > max_chunks:
                print(f"Test-Limit von {max_chunks} Chunks erreicht, stoppe Verarbeitung...")
                break
            
            # Für jede Matching-Methode
            for method_name, method_data in matching_methods.items():
                prep_func = method_data["prep_func"]
                match_func = method_data["match_func"]
                
                for tec_col, cmd_col in method_data["pairs"]:
                    if tec_col not in chunk.columns:
                        if chunk_num == 1:
                            print(f"  Spalte {tec_col} nicht in TecDoc gefunden")
                        continue
                    if cmd_col not in cmd_df.columns:
                        if chunk_num == 1:
                            print(f"  Spalte {cmd_col} nicht in CMD gefunden")
                        continue
                    
                    # Daten vorbereiten mit der jeweiligen Prep-Funktion
                    tec_values = chunk[tec_col].apply(prep_func)
                    cmd_values = cmd_df[cmd_col].apply(prep_func)
                    
                    # Debug für ersten Chunk
                    if chunk_num == 1:
                        tec_sample = [v for v in tec_values.head(3).tolist() if v]
                        cmd_sample = [v for v in cmd_values.head(3).tolist() if v]
                        print(f"  {method_name} {tec_col}<->{cmd_col}: TecDoc={tec_sample}, CMD={cmd_sample}")
                    
                    # Nur nicht-leere Werte
                    tec_clean = tec_values[tec_values != ""]
                    cmd_clean = cmd_values[cmd_values != ""]
                    
                    if len(tec_clean) == 0 or len(cmd_clean) == 0:
                        continue
                    
                    # Matching durchführen
                    matches_count = 0
                    for tec_val in tec_clean:
                        for cmd_val in cmd_clean:
                            if match_func(tec_val, cmd_val):
                                matches_count += 1
                                break  # Ein Match pro TecDoc-Wert reicht
                    
                    if matches_count > 0:
                        key = f"{method_name}: {tec_col} <-> {cmd_col}"
                        matching_results[key] += matches_count
                        print(f"  {key}: {matches_count} neue Matches in Chunk {chunk_num}")
            
            # Fortschritt alle 20 Chunks
            if chunk_num % 20 == 0:
                total_matches = sum(matching_results.values())
                print(f"Fortschritt: {chunk_num} Chunks verarbeitet, {total_matches} Matches insgesamt")
    
    except Exception as e:
        print(f"Fehler beim Verarbeiten der TecDoc-Datei: {e}")
        return
    
    # Zusammenfassung aller Matching-Verfahren
    print(f"\n" + "="*80)
    print("ZUSAMMENFASSUNG - DETERMINISTISCHE MATCHING-ERGEBNISSE (TEST)")
    print("="*80)
    print(f"Verarbeitete Chunks: {chunk_num}")
    print(f"Verarbeitete TecDoc-Zeilen: {chunk_num * chunk_size:,}")
    print(f"Hochrechnung auf alle ~800 Chunks: x{800//chunk_num:.0f}")
    print("-"*80)
    
    total_matches = 0
    for method_name in matching_methods.keys():
        method_total = sum(count for key, count in matching_results.items() if key.startswith(method_name))
        print(f"\n{method_name.upper()} MATCHING:")
        for key, count in matching_results.items():
            if key.startswith(method_name):
                pair_name = key.replace(f"{method_name}: ", "")
                print(f"  {pair_name:<35}: {count:>8,} Matches")
        print(f"  {method_name} Gesamt{'':<22}: {method_total:>8,} Matches")
        total_matches += method_total
    
    print("-"*80)
    print(f"{'ALLE VERFAHREN GESAMT':<40}: {total_matches:>8,} Matches")
    print("="*80)

if __name__ == "__main__":
    main()
