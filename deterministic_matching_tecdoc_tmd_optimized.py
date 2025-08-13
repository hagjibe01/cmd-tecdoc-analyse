import pandas as pd
import os
import re
import time
from typing import Dict, Any

def clean_str(value):
    """Bereinigt String-Werte für Vergleiche"""
    if pd.isna(value) or value == '' or str(value).lower() == 'nan':
        return ''
    return str(value).strip().upper()

def normalize_str(value):
    """Normalisiert Strings (entfernt Sonderzeichen, etc.)"""
    if pd.isna(value) or value == '':
        return ''
    # Entferne Sonderzeichen, behalte nur Alphanumerisch
    normalized = re.sub(r'[^A-Z0-9]', '', str(value).upper())
    return normalized

def load_cmd_data():
    """Lädt CMD TMD Daten"""
    try:
        print("📁 Lade CMD TMD Daten...")
        # WICHTIG: CMD verwendet Semikolon als Trennzeichen!
        df = pd.read_csv(
            'tmd_001000106869000000000065516001_data_2025-07-15-09-42-29-416.csv',
            encoding='utf-8',
            low_memory=False,
            dtype=str,
            sep=';',  # Semikolon statt Komma!
            on_bad_lines='skip'
        )
        
        print(f"ℹ️  Spaltenanzahl: {len(df.columns)}")
        print(f"ℹ️  Erste 5 Spalten: {list(df.columns[:5])}")
        
        # Bereinige wichtige Spalten
        important_cols = ['article_number', 'brand', 'tec_doc_article_number', 
                         'article_description_de', 'article_description_en']
        
        for col in important_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.upper()
        
        print(f"✅ CMD Daten geladen: {len(df):,} Zeilen, {len(df.columns)} Spalten")
        return df
        
    except Exception as e:
        print(f"❌ Fehler beim Laden der CMD Daten: {e}")
        return None

# Matching-Methoden
def exact_match(tec_series, cmd_series, tec_col, cmd_col):
    """Exakte String-Übereinstimmung"""
    tec_values = set(clean_str(val) for val in tec_series[tec_col] if clean_str(val))
    cmd_values = set(clean_str(val) for val in cmd_series[cmd_col] if clean_str(val))
    return len(tec_values.intersection(cmd_values))

def normalized_match(tec_series, cmd_series, tec_col, cmd_col):
    """Normalisierte Übereinstimmung"""
    tec_values = set(normalize_str(val) for val in tec_series[tec_col] if normalize_str(val))
    cmd_values = set(normalize_str(val) for val in cmd_series[cmd_col] if normalize_str(val))
    return len(tec_values.intersection(cmd_values))

def substring_match(tec_series, cmd_series, tec_col, cmd_col):
    """Substring-Matching"""
    matches = 0
    tec_values = [clean_str(val) for val in tec_series[tec_col] if clean_str(val)]
    cmd_values = [clean_str(val) for val in cmd_series[cmd_col] if clean_str(val)]
    
    for tec_val in tec_values:
        if len(tec_val) >= 3:  # Mindestlänge für Substring
            for cmd_val in cmd_values:
                if tec_val in cmd_val or cmd_val in tec_val:
                    matches += 1
                    break
    return matches

def prefix_match(tec_series, cmd_series, tec_col, cmd_col, prefix_length=5):
    """Prefix-Matching"""
    tec_prefixes = set(clean_str(val)[:prefix_length] for val in tec_series[tec_col] 
                      if len(clean_str(val)) >= prefix_length)
    cmd_prefixes = set(clean_str(val)[:prefix_length] for val in cmd_series[cmd_col] 
                      if len(clean_str(val)) >= prefix_length)
    return len(tec_prefixes.intersection(cmd_prefixes))

def numeric_match(tec_series, cmd_series, tec_col, cmd_col):
    """Numerische Übereinstimmung"""
    matches = 0
    try:
        tec_numeric = pd.to_numeric(tec_series[tec_col], errors='coerce').dropna()
        cmd_numeric = pd.to_numeric(cmd_series[cmd_col], errors='coerce').dropna()
        
        tec_values = set(tec_numeric.values)
        cmd_values = set(cmd_numeric.values)
        return len(tec_values.intersection(cmd_values))
    except:
        return 0

# Erweiterte Spalten-Mappings basierend auf den verfügbaren Daten
column_mappings = {
    # === ARTIKEL-IDENTIFIKATION ===
    'artno': ['article_number', 'tec_doc_article_number', 'alternative_article_number', 
              'predecessor_article_number', 'successor_article_number', 'trade_number', 
              'oe_number', 'buyer_article_number', 'ean', 'packaging_ean', 'packaging_upc'],
    
    # === BRAND/HERSTELLER ===
    'brandno': ['brand', 'alternative_brand', 'predecessor_brand', 'successor_brand'],
    
    # === SYSTEM-IDs ===
    'tableno': ['tec_doc_data_supplier_number'],
    
    # === NUMERISCHE FELDER - MENGEN ===
    'batchsize1': ['min_order_qty', 'max_order_qty', 'packaging_qty_per_uom', 
                   'sales_uom_lot_size', 'sales_uom_lot_size_2', 'sales_uom_lot_size_3',
                   'sales_uom_base_uom_per_uom', 'sales_uom_base_uom_per_uom_2'],
    
    # === NUMERISCHE FELDER - DIMENSIONEN/GEWICHT ===
    'batchsize2': ['packaging_weight', 'packaging_volume', 'packaging_dimension_length', 
                   'packaging_dimension_width', 'packaging_dimension_height', 'net_amount', 
                   'gross_amount', 'wholesale_amount', 'core_amount'],
}

def fuzzy_numeric_match(tec_series, cmd_series, tec_col, cmd_col, tolerance=0.1):
    """Numerisches Matching mit Toleranz"""
    matches = 0
    try:
        tec_numeric = pd.to_numeric(tec_series[tec_col], errors='coerce').dropna()
        cmd_numeric = pd.to_numeric(cmd_series[cmd_col], errors='coerce').dropna()
        
        for tec_val in tec_numeric.values:
            # Finde CMD-Werte innerhalb der Toleranz
            tolerance_range = abs(tec_val * tolerance)
            matching_cmd = cmd_numeric[
                (cmd_numeric >= tec_val - tolerance_range) & 
                (cmd_numeric <= tec_val + tolerance_range)
            ]
            if len(matching_cmd) > 0:
                matches += 1
        return matches
    except:
        return 0

def length_based_match(tec_series, cmd_series, tec_col, cmd_col):
    """Matching basierend auf String-Länge"""
    tec_lengths = set(len(clean_str(val)) for val in tec_series[tec_col] if clean_str(val))
    cmd_lengths = set(len(clean_str(val)) for val in cmd_series[cmd_col] if clean_str(val))
    return len(tec_lengths.intersection(cmd_lengths))

def collect_match_examples(tec_chunk, cmd_df, tec_col, cmd_col, method_func, max_examples=3):
    """Sammelt konkrete Beispiele für erfolgreiche Matches"""
    examples = []
    
    if method_func == exact_match:
        tec_values = [clean_str(val) for val in tec_chunk[tec_col] if clean_str(val)]
        cmd_values = [clean_str(val) for val in cmd_df[cmd_col] if clean_str(val)]
        
        for tec_val in tec_values[:50]:  # Nur erste 50 prüfen für Performance
            if tec_val in cmd_values:
                examples.append(f"{tec_val}")
                if len(examples) >= max_examples:
                    break
                    
    elif method_func == substring_match:
        tec_values = [clean_str(val) for val in tec_chunk[tec_col] if len(clean_str(val)) >= 3]
        cmd_values = [clean_str(val) for val in cmd_df[cmd_col] if clean_str(val)]
        
        for tec_val in tec_values[:30]:  # Weniger für Performance
            for cmd_val in cmd_values[:100]:
                if tec_val in cmd_val or cmd_val in tec_val:
                    examples.append(f"{tec_val} ↔ {cmd_val}")
                    break
            if len(examples) >= max_examples:
                break
                
    elif method_func == prefix_match:
        tec_prefixes = [(clean_str(val), clean_str(val)[:5]) for val in tec_chunk[tec_col] 
                       if len(clean_str(val)) >= 5]
        cmd_prefixes = [(clean_str(val), clean_str(val)[:5]) for val in cmd_df[cmd_col] 
                       if len(clean_str(val)) >= 5]
        
        for tec_full, tec_prefix in tec_prefixes[:30]:
            for cmd_full, cmd_prefix in cmd_prefixes[:100]:
                if tec_prefix == cmd_prefix:
                    examples.append(f"{tec_full} ↔ {cmd_full} (Prefix: {tec_prefix})")
                    break
            if len(examples) >= max_examples:
                break
                
    elif method_func == suffix_match:
        tec_suffixes = [(clean_str(val), clean_str(val)[-3:]) for val in tec_chunk[tec_col] 
                       if len(clean_str(val)) >= 3]
        cmd_suffixes = [(clean_str(val), clean_str(val)[-3:]) for val in cmd_df[cmd_col] 
                       if len(clean_str(val)) >= 3]
        
        for tec_full, tec_suffix in tec_suffixes[:30]:
            for cmd_full, cmd_suffix in cmd_suffixes[:100]:
                if tec_suffix == cmd_suffix:
                    examples.append(f"{tec_full} ↔ {cmd_full} (Suffix: {tec_suffix})")
                    break
            if len(examples) >= max_examples:
                break
                
    elif method_func == numeric_match:
        try:
            tec_numeric = pd.to_numeric(tec_chunk[tec_col], errors='coerce').dropna()
            cmd_numeric = pd.to_numeric(cmd_df[cmd_col], errors='coerce').dropna()
            
            tec_values = set(tec_numeric.values)
            cmd_values = set(cmd_numeric.values)
            intersection = tec_values.intersection(cmd_values)
            
            for val in list(intersection)[:max_examples]:
                examples.append(f"{val}")
        except:
            pass
    
    return examples

# Globales Dictionary für Beispiele
match_examples = {}

def suffix_match(tec_series, cmd_series, tec_col, cmd_col, suffix_length=3):
    """Suffix-Matching (Ende der Strings)"""
    tec_suffixes = set(clean_str(val)[-suffix_length:] for val in tec_series[tec_col] 
                      if len(clean_str(val)) >= suffix_length)
    cmd_suffixes = set(clean_str(val)[-suffix_length:] for val in cmd_series[cmd_col] 
                      if len(clean_str(val)) >= suffix_length)
    return len(tec_suffixes.intersection(cmd_suffixes))

# Erweiterte Matching-Methoden
matching_methods = {
    'Exakt': exact_match,
    'Normalisiert': normalized_match,
    'Teilstring': substring_match,
    'Prefix_5': prefix_match,
    'Numerisch': numeric_match,
    'Numerisch_Toleranz': fuzzy_numeric_match,
    'Suffix_3': suffix_match,
    'Längen_Match': length_based_match
}

def print_summary(results, chunk_count, test_mode=False):
    """Druckt Zusammenfassung der Ergebnisse"""
    print("\n" + "="*80)
    print("MATCHING-ZUSAMMENFASSUNG")
    print("="*80)
    
    if test_mode:
        print(f"🧪 TEST-MODUS: {chunk_count} Chunks verarbeitet (Teilmenge der Daten)")
        print("Hochrechnung auf Gesamtdaten:")
        total_chunks_estimate = 114  # Geschätzt basierend auf 40GB / 350MB pro Chunk
        extrapolation_factor = total_chunks_estimate / chunk_count if chunk_count > 0 else 1
    
    total_matches = 0
    
    for method_name, method_results in results.items():
        method_total = sum(method_results.values())
        total_matches += method_total
        
        if method_total > 0:
            print(f"\n🎯 {method_name.upper()}:")
            for pair, matches in method_results.items():
                if matches > 0:
                    if test_mode:
                        estimated = int(matches * extrapolation_factor)
                        print(f"  {pair}: {matches:,} (Hochrechnung: ~{estimated:,})")
                    else:
                        print(f"  {pair}: {matches:,}")
        else:
            print(f"\n❌ {method_name.upper()}: Keine Matches")
    
    print(f"\n📊 GESAMT:")
    print(f"  Gefundene Matches: {total_matches:,}")
    
    if test_mode and total_matches > 0:
        estimated_total = int(total_matches * extrapolation_factor)
        print(f"  Hochrechnung Gesamtdaten: ~{estimated_total:,}")
    
    print(f"  Verarbeitete Chunks: {chunk_count}")
    print(f"  Methoden getestet: {len(matching_methods)}")
    print(f"  Spaltenpaare getestet: {sum(len(cols) for cols in column_mappings.values())}")
    
    # NEUE SEKTION: Beispieldatensätze anzeigen
    print(f"\n" + "="*80)
    print("BEISPIELDATENSÄTZE FÜR ERFOLGREICHE MATCHES")
    print("="*80)
    
    if match_examples:
        for example_key, examples in match_examples.items():
            if examples:  # Nur wenn Beispiele vorhanden
                method, pair = example_key.split(": ", 1)
                print(f"\n🔍 {method.upper()}: {pair}")
                for i, example in enumerate(examples[:3], 1):  # Max 3 Beispiele
                    print(f"  {i}. {example}")
    else:
        print("❌ Keine Beispieldaten gesammelt")

def main():
    """Hauptfunktion für das Matching"""
    print("TecDoc ↔ CMD TMD Deterministic Matching")
    print("=" * 60)
    
    # PERFORMANCE-OPTIMIERT: Test-Modus
    TEST_MODE = True
    MAX_CHUNKS = 2  # Reduziert auf 2 Chunks wegen mehr Tests
    CHUNK_SIZE = 20000  # Kleinere Chunks wegen mehr Spaltenpaare
    
    if TEST_MODE:
        print("🚀 ERWEITERTE ANALYSE: 2 Chunks, 8 Methoden, ~30 Spaltenpaare")
        print("   (Für vollständige Analyse TEST_MODE auf False setzen)")
    
    start_time = time.time()
    
    # Lade CMD TMD Daten (komplett)
    cmd_df = load_cmd_data()
    if cmd_df is None:
        return
    
    # Für Test-Modus: Reduziere CMD Daten stärker wegen mehr Tests
    if TEST_MODE and len(cmd_df) > 15000:
        cmd_df = cmd_df.head(15000)
        print(f"🧪 Test-Performance: Reduziert auf {len(cmd_df):,} CMD Zeilen")
    
    # Initialisiere Ergebnisse
    results = {}
    for method_name in matching_methods.keys():
        results[method_name] = {}
        for tec_col, cmd_cols in column_mappings.items():
            for cmd_col in cmd_cols:
                key = f"{tec_col} <-> {cmd_col}"
                results[method_name][key] = 0
    
    # Chunk-basierte Verarbeitung der TecDoc Daten
    print(f"\n📦 Starte TecDoc-Verarbeitung (Chunk-Größe: {CHUNK_SIZE:,})...")
    
    chunk_count = 0
    try:
        # TecDoc Chunk-Reader
        chunk_reader = pd.read_csv(
            '200_Article_Table.csv',
            chunksize=CHUNK_SIZE,
            low_memory=False,
            dtype=str
        )
        
        for chunk in chunk_reader:
            chunk_count += 1
            print(f"\n📊 Chunk {chunk_count}/{MAX_CHUNKS if TEST_MODE else '?'} ({len(chunk):,} Zeilen)")
            
            # Bereinige TecDoc Chunk
            for col in ['artno', 'brandno', 'batchsize1', 'batchsize2', 'tableno']:
                if col in chunk.columns:
                    chunk[col] = chunk[col].astype(str).str.strip().str.upper()
            
            # Matching für alle Methoden und Spaltenpaare
            for method_name, method_func in matching_methods.items():
                print(f"  🔍 {method_name}:", end=" ")
                method_matches = 0
                
                for tec_col, cmd_cols in column_mappings.items():
                    if tec_col in chunk.columns:
                        for cmd_col in cmd_cols:
                            if cmd_col in cmd_df.columns:
                                try:
                                    matches = method_func(chunk, cmd_df, tec_col, cmd_col)
                                    key = f"{tec_col} <-> {cmd_col}"
                                    results[method_name][key] += matches
                                    method_matches += matches
                                    
                                    # Sammle Beispiele für erfolgreiche Matches
                                    if matches > 0:
                                        example_key = f"{method_name}: {key}"
                                        if example_key not in match_examples:
                                            examples = collect_match_examples(chunk, cmd_df, tec_col, cmd_col, method_func)
                                            if examples:
                                                match_examples[example_key] = examples
                                        
                                        print(f"{tec_col}↔{cmd_col}({matches})", end=" ")
                                except Exception as e:
                                    print(f"Fehler bei {tec_col}↔{cmd_col}: {e}")
                
                if method_matches == 0:
                    print("keine Matches")
                else:
                    print(f"→ {method_matches:,} gesamt")
            
            # Test-Modus: Nur begrenzte Chunks
            if TEST_MODE and chunk_count >= MAX_CHUNKS:
                print(f"\n🧪 Test-Modus: Stoppe nach {MAX_CHUNKS} Chunks")
                break
            
            # Memory cleanup
            del chunk
            
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return
    
    elapsed_time = time.time() - start_time
    print(f"\n⏱️ Verarbeitung abgeschlossen in {elapsed_time:.1f} Sekunden")
    
    # Zeige Ergebnisse
    print_summary(results, chunk_count, TEST_MODE)

if __name__ == "__main__":
    main()
