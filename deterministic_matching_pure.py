#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REIN DETERMINISTISCHE MATCHING-VERFAHREN
TecDoc vs CMD TMD - Nur regelbasierte, exakte Algorithmen
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
VISUALIZATION_DIR = "visualizations/deterministic_matching"
os.makedirs(VISUALIZATION_DIR, exist_ok=True)

def exact_match(tec_series, cmd_series, tec_col, cmd_col):
    """Exaktes String-Matching (Case-Insensitive)"""
    matches = 0
    try:
        tec_clean = tec_series[tec_col].astype(str).str.strip().str.upper()
        cmd_clean = cmd_series[cmd_col].astype(str).str.strip().str.upper()
        
        # Intersection für Performance
        common_values = set(tec_clean.dropna().unique()) & set(cmd_clean.dropna().unique())
        
        for value in common_values:
            tec_count = (tec_clean == value).sum()
            cmd_count = (cmd_clean == value).sum()
            matches += min(tec_count, cmd_count)
        return matches
    except:
        return 0

def substring_match(tec_series, cmd_series, tec_col, cmd_col):
    """Substring-Matching (TecDoc in CMD enthalten)"""
    matches = 0
    try:
        tec_values = tec_series[tec_col].astype(str).str.strip().str.upper().dropna()
        cmd_values = cmd_series[cmd_col].astype(str).str.strip().str.upper().dropna()
        
        for tec_val in tec_values.unique():
            if len(tec_val) >= 3:  # Mindestlänge für sinnvolle Substrings
                matching_cmd = cmd_values[cmd_values.str.contains(tec_val, na=False, regex=False)]
                if len(matching_cmd) > 0:
                    matches += 1
        return matches
    except:
        return 0

def prefix_match(tec_series, cmd_series, tec_col, cmd_col, min_length=3):
    """Prefix-Matching (gleicher Anfang)"""
    matches = 0
    try:
        tec_values = tec_series[tec_col].astype(str).str.strip().str.upper().dropna()
        cmd_values = cmd_series[cmd_col].astype(str).str.strip().str.upper().dropna()
        
        for tec_val in tec_values.unique():
            if len(tec_val) >= min_length:
                prefix = tec_val[:min_length]
                matching_cmd = cmd_values[cmd_values.str.startswith(prefix, na=False)]
                if len(matching_cmd) > 0:
                    matches += 1
        return matches
    except:
        return 0

def suffix_match(tec_series, cmd_series, tec_col, cmd_col, min_length=3):
    """Suffix-Matching (gleiches Ende)"""
    matches = 0
    try:
        tec_values = tec_series[tec_col].astype(str).str.strip().str.upper().dropna()
        cmd_values = cmd_series[cmd_col].astype(str).str.strip().str.upper().dropna()
        
        for tec_val in tec_values.unique():
            if len(tec_val) >= min_length:
                suffix = tec_val[-min_length:]
                matching_cmd = cmd_values[cmd_values.str.endswith(suffix, na=False)]
                if len(matching_cmd) > 0:
                    matches += 1
        return matches
    except:
        return 0

def numeric_exact_match(tec_series, cmd_series, tec_col, cmd_col):
    """Exaktes numerisches Matching (ohne Toleranz!)"""
    matches = 0
    try:
        tec_numeric = pd.to_numeric(tec_series[tec_col], errors='coerce').dropna()
        cmd_numeric = pd.to_numeric(cmd_series[cmd_col], errors='coerce').dropna()
        
        # Exakte Übereinstimmung
        common_values = set(tec_numeric.unique()) & set(cmd_numeric.unique())
        
        for value in common_values:
            tec_count = (tec_numeric == value).sum()
            cmd_count = (cmd_numeric == value).sum()
            matches += min(tec_count, cmd_count)
        return matches
    except:
        return 0

def length_based_match(tec_series, cmd_series, tec_col, cmd_col):
    """Längenbasiertes Matching (gleiche String-Länge)"""
    matches = 0
    try:
        tec_lengths = tec_series[tec_col].astype(str).str.len().dropna()
        cmd_lengths = cmd_series[cmd_col].astype(str).str.len().dropna()
        
        common_lengths = set(tec_lengths.unique()) & set(cmd_lengths.unique())
        
        for length in common_lengths:
            if length > 2:  # Nur sinnvolle Längen
                tec_count = (tec_lengths == length).sum()
                cmd_count = (cmd_lengths == length).sum()
                matches += min(tec_count, cmd_count)
        return matches
    except:
        return 0

def collect_match_examples(tec_chunk, cmd_chunk, tec_col, cmd_col, method_name, method_func, max_examples=3):
    """Sammelt konkrete Beispiele für erfolgreiche Matches"""
    examples = []
    try:
        if method_name == "Exakt":
            tec_clean = tec_chunk[tec_col].astype(str).str.strip().str.upper()
            cmd_clean = cmd_chunk[cmd_col].astype(str).str.strip().str.upper()
            common_values = set(tec_clean.dropna().unique()) & set(cmd_clean.dropna().unique())
            
            for i, value in enumerate(list(common_values)[:max_examples]):
                tec_example = tec_chunk[tec_clean == value].iloc[0][tec_col] if (tec_clean == value).any() else value
                cmd_example = cmd_chunk[cmd_clean == value].iloc[0][cmd_col] if (cmd_clean == value).any() else value
                examples.append(f"TecDoc: '{tec_example}' ↔ CMD: '{cmd_example}'")
                
        elif method_name == "Substring":
            tec_values = tec_chunk[tec_col].astype(str).str.strip().str.upper().dropna()
            cmd_values = cmd_chunk[cmd_col].astype(str).str.strip().str.upper().dropna()
            
            count = 0
            for tec_val in tec_values.unique():
                if count >= max_examples:
                    break
                if len(tec_val) >= 3:
                    matching_cmd = cmd_values[cmd_values.str.contains(tec_val, na=False, regex=False)]
                    if len(matching_cmd) > 0:
                        examples.append(f"TecDoc: '{tec_val}' in CMD: '{matching_cmd.iloc[0]}'")
                        count += 1
                        
    except Exception as e:
        examples.append(f"Fehler beim Sammeln von Beispielen: {str(e)}")
    
    return examples[:max_examples]

def analyze_deterministic_matching():
    """Hauptanalyse für rein deterministische Verfahren"""
    
    print("🔍 REIN DETERMINISTISCHE MATCHING-ANALYSE")
    print("=" * 60)
    print("📊 Nur regelbasierte, exakte Algorithmen (ohne Toleranz/Fuzzy)")
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
    
    # Deterministische Matching-Methoden (OHNE fuzzy_numeric_match!)
    matching_methods = {
        'Exakt': exact_match,
        'Substring': substring_match, 
        'Prefix': prefix_match,
        'Suffix': suffix_match,
        'Numerisch_Exakt': numeric_exact_match,  # OHNE Toleranz!
        'Längenbasiert': length_based_match
    }
    
    # Spaltenpaarungen
    column_pairs = [
        # Artikel-Identifikatoren
        ('artno', 'article_number'),
        ('artno', 'tec_doc_article_number'),
        ('brandno', 'brand'),
        
        # Numerische Felder (exakt!)
        ('batchsize1', 'packaging_unit'),
        ('batchsize2', 'minimum_order_quantity'),
        
        # EAN/GTIN
        ('artno', 'ean_code'),
        ('artno', 'gtin'),
        
        # Weitere wichtige Felder
        ('artno', 'manufacturer_part_number'),
        ('artno', 'supplier_part_number'),
        ('brandno', 'manufacturer_name'),
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
                            examples = collect_match_examples(tec_chunk, cmd_data, tec_col, cmd_col, method_name, method_func)
                            all_examples[f"{method_name}_{tec_col}_{cmd_col}"].extend(examples)
                            
                    except Exception as e:
                        print(f"⚠️  Fehler bei {method_name} ({tec_col} → {cmd_col}): {str(e)}")
        
        all_results.extend(chunk_results)
        chunks_processed += 1
        
        if chunk_results:
            chunk_total = sum(r['Matches'] for r in chunk_results)
            print(f"      → {chunk_total:,} Matches gefunden")
    
    # Ergebnisse zusammenfassen
    if all_results:
        results_df = pd.DataFrame(all_results)
        
        print(f"\n📊 DETERMINISTISCHE MATCHING-ERGEBNISSE")
        print("=" * 60)
        
        # Nach Methode gruppieren
        method_summary = results_df.groupby('Methode')['Matches'].sum().sort_values(ascending=False)
        print("\n🏆 ERFOLG NACH METHODE:")
        for method, total in method_summary.items():
            print(f"   {method:20}: {total:,} Matches")
        
        # Top Spaltenpaare
        column_summary = results_df.groupby(['TecDoc_Spalte', 'CMD_Spalte'])['Matches'].sum().sort_values(ascending=False)
        print(f"\n🎯 TOP SPALTENPAARE:")
        for (tec_col, cmd_col), total in column_summary.head(10).items():
            print(f"   {tec_col:15} → {cmd_col:25}: {total:,}")
        
        # Beispiele zeigen
        print(f"\n💡 KONKRETE MATCH-BEISPIELE:")
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
        
        print(f"\n📈 GESAMTERGEBNIS:")
        print(f"   💫 Total Matches: {total_matches:,}")
        print(f"   ⏱️  Verarbeitungszeit: {elapsed_time:.1f}s")
        print(f"   📦 Chunks verarbeitet: {chunks_processed}")
        print(f"   🔧 Methoden getestet: {len(matching_methods)}")
        
        # Ergebnisse speichern
        output_file = f"{VISUALIZATION_DIR}/deterministic_matching_results_pure.csv"
        results_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\n💾 Ergebnisse gespeichert: {output_file}")
        
    else:
        print("\n❌ Keine Matches gefunden!")
    
    print(f"\n✅ Rein deterministische Analyse abgeschlossen!")

if __name__ == "__main__":
    analyze_deterministic_matching()
