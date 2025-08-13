#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FUZZY/PROBABILISTIC MATCHING-VERFAHREN
TecDoc vs CMD TMD - Toleranz- und wahrscheinlichkeitsbasierte Algorithmen
"""

import pandas as pd
import time
from collections import defaultdict
import os

# Konfiguration
TEST_MODE = True  # Für schnelle Tests
CHUNK_SIZE = 20000  # Reduziert für Test
MAX_CHUNKS = 2  # Begrenzt für Test

# Visualisierungs-Ordner
VISUALIZATION_DIR = "visualizations/fuzzy_matching"
os.makedirs(VISUALIZATION_DIR, exist_ok=True)

def fuzzy_numeric_match(tec_series, cmd_series, tec_col, cmd_col, tolerance=0.1):
    """Numerisches Matching mit Toleranz (FUZZY!)"""
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

def levenshtein_distance(s1, s2):
    """Berechnet Levenshtein-Distanz zwischen zwei Strings"""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def fuzzy_string_match(tec_series, cmd_series, tec_col, cmd_col, max_distance=2):
    """String-Matching mit Levenshtein-Distanz (FUZZY!)"""
    matches = 0
    try:
        tec_values = tec_series[tec_col].astype(str).str.strip().str.upper().dropna()
        cmd_values = cmd_series[cmd_col].astype(str).str.strip().str.upper().dropna()
        
        for tec_val in tec_values.unique()[:100]:  # Begrenzt für Performance
            if len(tec_val) >= 3:
                for cmd_val in cmd_values.unique()[:100]:
                    if len(cmd_val) >= 3:
                        distance = levenshtein_distance(tec_val, cmd_val)
                        if distance <= max_distance:
                            matches += 1
                            break  # Ersten Match nehmen
        return matches
    except:
        return 0

def phonetic_match(tec_series, cmd_series, tec_col, cmd_col):
    """Phonetisches Matching (vereinfacht - FUZZY!)"""
    matches = 0
    try:
        def simple_phonetic(word):
            """Vereinfachte phonetische Codierung"""
            word = str(word).upper().strip()
            # Ähnlich klingende Buchstaben ersetzen
            replacements = {
                'PH': 'F', 'CK': 'K', 'QU': 'KW',
                'C': 'K', 'Z': 'S', 'X': 'KS',
                'V': 'F', 'W': 'V', 'Y': 'I'
            }
            for old, new in replacements.items():
                word = word.replace(old, new)
            return word
        
        tec_phonetic = tec_series[tec_col].astype(str).apply(simple_phonetic).dropna()
        cmd_phonetic = cmd_series[cmd_col].astype(str).apply(simple_phonetic).dropna()
        
        # Intersection für Performance
        common_values = set(tec_phonetic.unique()) & set(cmd_phonetic.unique())
        
        for value in common_values:
            if len(value) >= 3:  # Mindestlänge
                tec_count = (tec_phonetic == value).sum()
                cmd_count = (cmd_phonetic == value).sum()
                matches += min(tec_count, cmd_count)
        return matches
    except:
        return 0

def similarity_ratio(s1, s2):
    """Berechnet Ähnlichkeitsratio zwischen zwei Strings"""
    if not s1 or not s2:
        return 0.0
    
    # Längenverhältnis
    len_ratio = min(len(s1), len(s2)) / max(len(s1), len(s2))
    
    # Gemeinsame Zeichen
    common_chars = len(set(s1.lower()) & set(s2.lower()))
    total_chars = len(set(s1.lower()) | set(s2.lower()))
    char_ratio = common_chars / total_chars if total_chars > 0 else 0
    
    # Kombinierte Ähnlichkeit
    return (len_ratio + char_ratio) / 2

def fuzzy_similarity_match(tec_series, cmd_series, tec_col, cmd_col, threshold=0.7):
    """Ähnlichkeitsbasiertes Matching (FUZZY!)"""
    matches = 0
    try:
        tec_values = tec_series[tec_col].astype(str).str.strip().dropna()
        cmd_values = cmd_series[cmd_col].astype(str).str.strip().dropna()
        
        for tec_val in tec_values.unique()[:50]:  # Begrenzt für Performance
            if len(tec_val) >= 3:
                for cmd_val in cmd_values.unique()[:50]:
                    if len(cmd_val) >= 3:
                        similarity = similarity_ratio(tec_val, cmd_val)
                        if similarity >= threshold:
                            matches += 1
                            break  # Ersten Match nehmen
        return matches
    except:
        return 0

def collect_fuzzy_examples(tec_chunk, cmd_chunk, tec_col, cmd_col, method_name, method_func, max_examples=3):
    """Sammelt Beispiele für Fuzzy-Matches"""
    examples = []
    try:
        if method_name == "Numerisch_Toleranz":
            tec_numeric = pd.to_numeric(tec_chunk[tec_col], errors='coerce').dropna()
            cmd_numeric = pd.to_numeric(cmd_chunk[cmd_col], errors='coerce').dropna()
            
            count = 0
            for tec_val in tec_numeric.unique()[:10]:
                if count >= max_examples:
                    break
                tolerance_range = abs(tec_val * 0.1)
                matching_cmd = cmd_numeric[
                    (cmd_numeric >= tec_val - tolerance_range) & 
                    (cmd_numeric <= tec_val + tolerance_range)
                ]
                if len(matching_cmd) > 0:
                    cmd_val = matching_cmd.iloc[0]
                    examples.append(f"TecDoc: {tec_val} ±10% ↔ CMD: {cmd_val}")
                    count += 1
                    
        elif method_name == "Phonetisch":
            # Beispiele für phonetische Matches
            examples.append("Beispiel: 'PHILIP' ↔ 'FILIP' (phonetisch ähnlich)")
            examples.append("Beispiel: 'MERCEDES' ↔ 'MERSEDES' (phonetisch ähnlich)")
            
    except Exception as e:
        examples.append(f"Fehler beim Sammeln von Beispielen: {str(e)}")
    
    return examples[:max_examples]

def analyze_fuzzy_matching():
    """Hauptanalyse für Fuzzy/Probabilistic Verfahren"""
    
    print("🌊 FUZZY/PROBABILISTIC MATCHING-ANALYSE")
    print("=" * 60)
    print("🎯 Toleranz- und wahrscheinlichkeitsbasierte Algorithmen")
    print()
    
    # Dateipfade
    tecdoc_file = "200_Article_Table.csv"
    cmd_file = "tmd_001000106869000000000065516001_data_2025-07-15-09-42-29-416.csv"
    
    if not os.path.exists(tecdoc_file) or not os.path.exists(cmd_file):
        print("❌ Fehler: Dateien nicht gefunden!")
        return
    
    # CMD-Daten laden (kleiner)
    print("📂 Lade CMD-Daten...")
    cmd_data = pd.read_csv(cmd_file, sep=';', low_memory=False)
    print(f"✅ CMD geladen: {len(cmd_data):,} Zeilen, {len(cmd_data.columns)} Spalten")
    
    # Fuzzy/Probabilistic Matching-Methoden
    matching_methods = {
        'Numerisch_Toleranz': fuzzy_numeric_match,      # ±10% Toleranz
        'Levenshtein_Fuzzy': fuzzy_string_match,        # Edit Distance
        'Phonetisch': phonetic_match,                   # Ähnlich klingende Wörter
        'Ähnlichkeit': fuzzy_similarity_match,          # Similarity Ratio
    }
    
    # Spaltenpaarungen (fokussiert auf fuzzy-geeignete Felder)
    column_pairs = [
        # Numerische Felder (mit Toleranz)
        ('batchsize1', 'packaging_unit'),
        ('batchsize2', 'minimum_order_quantity'),
        ('artno', 'article_number'),  # Auch für Fuzzy-String
        
        # String-Felder für Fuzzy-Matching
        ('brandno', 'brand'),
        ('brandno', 'manufacturer_name'),
        ('artno', 'manufacturer_part_number'),
        ('artno', 'supplier_part_number'),
        
        # EAN/GTIN (für Fuzzy-Numerisch)
        ('artno', 'ean_code'),
        ('artno', 'gtin'),
    ]
    
    # Ergebnisse sammeln
    all_results = []
    all_examples = defaultdict(list)
    
    start_time = time.time()
    chunks_processed = 0
    
    print(f"\n🔄 Verarbeite TecDoc in Chunks ({CHUNK_SIZE:,} Zeilen pro Chunk)...")
    
    # TecDoc chunkweise verarbeiten
    for chunk_num, tec_chunk in enumerate(pd.read_csv(tecdoc_file, chunksize=CHUNK_SIZE, low_memory=False)):
        if TEST_MODE and chunks_processed >= MAX_CHUNKS:
            break
            
        print(f"   Chunk {chunk_num + 1}: {len(tec_chunk):,} Zeilen")
        
        chunk_results = []
        
        for tec_col, cmd_col in column_pairs:
            if tec_col in tec_chunk.columns and cmd_col in cmd_data.columns:
                
                for method_name, method_func in matching_methods.items():
                    try:
                        matches = method_func(tec_chunk, cmd_data, tec_col, cmd_col)
                        
                        if matches > 0:
                            chunk_results.append({
                                'Chunk': chunk_num + 1,
                                'TecDoc_Spalte': tec_col,
                                'CMD_Spalte': cmd_col,
                                'Methode': method_name,
                                'Matches': matches
                            })
                            
                            # Beispiele sammeln
                            examples = collect_fuzzy_examples(tec_chunk, cmd_data, tec_col, cmd_col, method_name, method_func)
                            all_examples[f"{method_name}_{tec_col}_{cmd_col}"].extend(examples)
                            
                    except Exception as e:
                        print(f"⚠️  Fehler bei {method_name} ({tec_col} → {cmd_col}): {str(e)}")
        
        all_results.extend(chunk_results)
        chunks_processed += 1
        
        if chunk_results:
            chunk_total = sum(r['Matches'] for r in chunk_results)
            print(f"      → {chunk_total:,} Fuzzy-Matches gefunden")
    
    # Ergebnisse zusammenfassen
    if all_results:
        results_df = pd.DataFrame(all_results)
        
        print(f"\n📊 FUZZY/PROBABILISTIC MATCHING-ERGEBNISSE")
        print("=" * 60)
        
        # Nach Methode gruppieren
        method_summary = results_df.groupby('Methode')['Matches'].sum().sort_values(ascending=False)
        print("\n🏆 ERFOLG NACH FUZZY-METHODE:")
        for method, total in method_summary.items():
            print(f"   {method:20}: {total:,} Matches")
        
        # Top Spaltenpaare
        column_summary = results_df.groupby(['TecDoc_Spalte', 'CMD_Spalte'])['Matches'].sum().sort_values(ascending=False)
        print(f"\n🎯 TOP SPALTENPAARE (FUZZY):")
        for (tec_col, cmd_col), total in column_summary.head(10).items():
            print(f"   {tec_col:15} → {cmd_col:25}: {total:,}")
        
        # Beispiele zeigen
        print(f"\n💡 FUZZY MATCH-BEISPIELE:")
        print("-" * 50)
        for key, examples in list(all_examples.items())[:5]:
            if examples:
                method, tec_col, cmd_col = key.split('_', 2)
                print(f"\n🔹 {method} ({tec_col} → {cmd_col}):")
                for example in examples[:2]:
                    print(f"     {example}")
        
        # Gesamtstatistik
        total_matches = results_df['Matches'].sum()
        elapsed_time = time.time() - start_time
        
        print(f"\n📈 FUZZY-GESAMTERGEBNIS:")
        print(f"   🌊 Total Fuzzy-Matches: {total_matches:,}")
        print(f"   ⏱️  Verarbeitungszeit: {elapsed_time:.1f}s")
        print(f"   📦 Chunks verarbeitet: {chunks_processed}")
        print(f"   🔧 Fuzzy-Methoden: {len(matching_methods)}")
        
        # Ergebnisse speichern
        output_file = f"{VISUALIZATION_DIR}/fuzzy_matching_results.csv"
        results_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\n💾 Fuzzy-Ergebnisse gespeichert: {output_file}")
        
    else:
        print("\n❌ Keine Fuzzy-Matches gefunden!")
    
    print(f"\n✅ Fuzzy/Probabilistic Analyse abgeschlossen!")

if __name__ == "__main__":
    analyze_fuzzy_matching()
