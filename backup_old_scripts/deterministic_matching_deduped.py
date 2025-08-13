#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DETERMINISTIC MATCHING-VERFAHREN (DUPLIKATFREI)
TecDoc vs CMD - Rein deterministische Algorithmen ohne Duplikate
"""

import pandas as pd
import time
from collections import defaultdict
import os

# Konfiguration - SAMPLE-MODUS für 40GB Files
SAMPLE_MODE = True        # Arbeitet nur mit repräsentativen Samples
SAMPLE_SIZE = 50000       # 50k Zeilen Sample statt ganzer 40GB
TEST_MODE = True          # Für schnelle Tests
CHUNK_SIZE = 10000        # Kleinere Chunks
MAX_CHUNKS = 5            # Maximal 5 Chunks = 50k Zeilen total

# Visualisierungs-Ordner
VISUALIZATION_DIR = "visualizations/deterministic_matching"
os.makedirs(VISUALIZATION_DIR, exist_ok=True)

# Globale Sets für Deduplizierung
global_matched_pairs = defaultdict(set)  # method_column: {(tecdoc_val, cmd_val)}
global_matched_tecdoc = defaultdict(set)  # method_column: {tecdoc_val}
global_matched_cmd = defaultdict(set)     # method_column: {cmd_val}

def substring_match_deduped(tec_series, cmd_series, tec_col, cmd_col, method_key):
    """Substring-Matching mit Duplikat-Tracking"""
    new_matches = 0
    new_pairs = set()
    
    try:
        tec_values = tec_series[tec_col].astype(str).str.strip().str.upper().dropna()
        cmd_values = cmd_series[cmd_col].astype(str).str.strip().str.upper().dropna()
        
        for tec_val in tec_values.unique():
            if len(tec_val) >= 3:  # Mindestlänge für sinnvolle Substrings
                matching_cmd = cmd_values[cmd_values.str.contains(tec_val, na=False, regex=False)]
                for cmd_val in matching_cmd.unique():
                    pair = (tec_val, cmd_val)
                    if pair not in global_matched_pairs[method_key]:
                        global_matched_pairs[method_key].add(pair)
                        global_matched_tecdoc[method_key].add(tec_val)
                        global_matched_cmd[method_key].add(cmd_val)
                        new_pairs.add(pair)
                        new_matches += 1
        
        return new_matches, len(new_pairs)
    except:
        return 0, 0

def prefix_match_deduped(tec_series, cmd_series, tec_col, cmd_col, method_key, min_length=3):
    """Prefix-Matching mit Duplikat-Tracking"""
    new_matches = 0
    new_pairs = set()
    
    try:
        tec_values = tec_series[tec_col].astype(str).str.strip().str.upper().dropna()
        cmd_values = cmd_series[cmd_col].astype(str).str.strip().str.upper().dropna()
        
        for tec_val in tec_values.unique():
            if len(tec_val) >= min_length:
                for cmd_val in cmd_values.unique():
                    if len(cmd_val) >= min_length:
                        if tec_val.startswith(cmd_val) or cmd_val.startswith(tec_val):
                            pair = (tec_val, cmd_val)
                            if pair not in global_matched_pairs[method_key]:
                                global_matched_pairs[method_key].add(pair)
                                global_matched_tecdoc[method_key].add(tec_val)
                                global_matched_cmd[method_key].add(cmd_val)
                                new_pairs.add(pair)
                                new_matches += 1
        
        return new_matches, len(new_pairs)
    except:
        return 0, 0

def suffix_match_deduped(tec_series, cmd_series, tec_col, cmd_col, method_key, min_length=3):
    """Suffix-Matching mit Duplikat-Tracking"""
    new_matches = 0
    new_pairs = set()
    
    try:
        tec_values = tec_series[tec_col].astype(str).str.strip().str.upper().dropna()
        cmd_values = cmd_series[cmd_col].astype(str).str.strip().str.upper().dropna()
        
        for tec_val in tec_values.unique():
            if len(tec_val) >= min_length:
                for cmd_val in cmd_values.unique():
                    if len(cmd_val) >= min_length:
                        if tec_val.endswith(cmd_val) or cmd_val.endswith(tec_val):
                            pair = (tec_val, cmd_val)
                            if pair not in global_matched_pairs[method_key]:
                                global_matched_pairs[method_key].add(pair)
                                global_matched_tecdoc[method_key].add(tec_val)
                                global_matched_cmd[method_key].add(cmd_val)
                                new_pairs.add(pair)
                                new_matches += 1
        
        return new_matches, len(new_pairs)
    except:
        return 0, 0

def exact_numeric_match_deduped(tec_series, cmd_series, tec_col, cmd_col, method_key):
    """Exakte numerische Matches mit Duplikat-Tracking"""
    new_matches = 0
    new_pairs = set()
    
    try:
        tec_numeric = pd.to_numeric(tec_series[tec_col], errors='coerce').dropna()
        cmd_numeric = pd.to_numeric(cmd_series[cmd_col], errors='coerce').dropna()
        
        for tec_val in tec_numeric.unique():
            if tec_val in cmd_numeric.values:
                for cmd_val in cmd_numeric[cmd_numeric == tec_val].unique():
                    pair = (str(tec_val), str(cmd_val))
                    if pair not in global_matched_pairs[method_key]:
                        global_matched_pairs[method_key].add(pair)
                        global_matched_tecdoc[method_key].add(str(tec_val))
                        global_matched_cmd[method_key].add(str(cmd_val))
                        new_pairs.add(pair)
                        new_matches += 1
        
        return new_matches, len(new_pairs)
    except:
        return 0, 0

def length_based_match_deduped(tec_series, cmd_series, tec_col, cmd_col, method_key):
    """Längenbasiertes Matching mit Duplikat-Tracking"""
    new_matches = 0
    new_pairs = set()
    
    try:
        tec_values = tec_series[tec_col].astype(str).str.strip().dropna()
        cmd_values = cmd_series[cmd_col].astype(str).str.strip().dropna()
        
        # Gruppiere nach Länge
        tec_by_length = tec_values.groupby(tec_values.str.len())
        cmd_by_length = cmd_values.groupby(cmd_values.str.len())
        
        for length in tec_by_length.groups.keys():
            if length in cmd_by_length.groups.keys() and length >= 3:
                tec_group = tec_by_length.get_group(length).unique()
                cmd_group = cmd_by_length.get_group(length).unique()
                
                # Finde exakte Matches in gleicher Längengruppe
                for tec_val in tec_group:
                    if tec_val in cmd_group:
                        pair = (tec_val, tec_val)  # Exakter Match
                        if pair not in global_matched_pairs[method_key]:
                            global_matched_pairs[method_key].add(pair)
                            global_matched_tecdoc[method_key].add(tec_val)
                            global_matched_cmd[method_key].add(tec_val)
                            new_pairs.add(pair)
                            new_matches += 1
        
        return new_matches, len(new_pairs)
    except:
        return 0, 0

def exact_string_match_deduped(tec_series, cmd_series, tec_col, cmd_col, method_key):
    """Exakte String-Matches mit Duplikat-Tracking"""
    new_matches = 0
    new_pairs = set()
    
    try:
        tec_values = tec_series[tec_col].astype(str).str.strip().str.upper().dropna()
        cmd_values = cmd_series[cmd_col].astype(str).str.strip().str.upper().dropna()
        
        # Intersection für exakte Matches
        common_values = set(tec_values.unique()) & set(cmd_values.unique())
        
        for value in common_values:
            if len(value) >= 2:  # Mindestlänge
                pair = (value, value)
                if pair not in global_matched_pairs[method_key]:
                    global_matched_pairs[method_key].add(pair)
                    global_matched_tecdoc[method_key].add(value)
                    global_matched_cmd[method_key].add(value)
                    new_pairs.add(pair)
                    new_matches += 1
        
        return new_matches, len(new_pairs)
    except:
        return 0, 0

def collect_examples_deduped(method_key, max_examples=3):
    """Sammelt Beispiele für deduplizierte Matches"""
    examples = []
    pairs = list(global_matched_pairs[method_key])[:max_examples]
    
    for tec_val, cmd_val in pairs:
        if tec_val == cmd_val:
            examples.append(f"'{tec_val}' = '{cmd_val}' (exakt)")
        else:
            examples.append(f"'{tec_val}' ↔ '{cmd_val}'")
    
    return examples

def analyze_deterministic_matching_deduped():
    """Hauptanalyse für deterministische Verfahren (DUPLIKATFREI)"""
    
    print("🎯 DETERMINISTIC MATCHING-ANALYSE (DUPLIKATFREI + SAMPLE-MODUS)")
    print("=" * 70)
    print("🔧 Rein deterministische Algorithmen ohne Duplikate")
    print(f"📊 Sample-Größe: {MAX_CHUNKS * CHUNK_SIZE:,} Zeilen (statt 40GB)")
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
    
    # Deterministische Matching-Methoden mit Duplikat-Tracking
    matching_methods = {
        'Substring': substring_match_deduped,
        'Prefix': prefix_match_deduped,
        'Suffix': suffix_match_deduped,
        'Numerisch_Exakt': exact_numeric_match_deduped,
        'Längenbasiert': length_based_match_deduped,
        'String_Exakt': exact_string_match_deduped,
    }
    
    # Spaltenpaarungen
    column_pairs = [
        ('artno', 'article_number'),
        ('artno', 'tec_doc_article_number'),
        ('artno', 'manufacturer_part_number'),
        ('artno', 'supplier_part_number'),
        ('brandno', 'brand'),
        ('brandno', 'manufacturer_name'),
        ('artno', 'ean_code'),
        ('artno', 'gtin'),
    ]
    
    # Ergebnisse sammeln
    chunk_results = []
    start_time = time.time()
    chunks_processed = 0
    
    print(f"\n🔄 Verarbeite TecDoc in Chunks ({CHUNK_SIZE:,} Zeilen pro Chunk)...")
    
    # TecDoc chunkweise verarbeiten (SAMPLE-MODUS)
    for chunk_num, tec_chunk in enumerate(pd.read_csv(tecdoc_file, chunksize=CHUNK_SIZE, low_memory=False)):
        if SAMPLE_MODE and chunks_processed >= MAX_CHUNKS:
            print(f"   📊 SAMPLE-MODUS: Stoppe nach {chunks_processed} Chunks ({chunks_processed * CHUNK_SIZE:,} Zeilen)")
            break
            
        print(f"   Chunk {chunk_num + 1}: {len(tec_chunk):,} Zeilen")
        
        chunk_total = 0
        
        for tec_col, cmd_col in column_pairs:
            if tec_col in tec_chunk.columns and cmd_col in cmd_data.columns:
                
                for method_name, method_func in matching_methods.items():
                    method_key = f"{method_name}_{tec_col}_{cmd_col}"
                    
                    try:
                        new_matches, new_pairs = method_func(tec_chunk, cmd_data, tec_col, cmd_col, method_key)
                        
                        if new_matches > 0:
                            chunk_results.append({
                                'Chunk': chunk_num + 1,
                                'TecDoc_Spalte': tec_col,
                                'CMD_Spalte': cmd_col,
                                'Methode': method_name,
                                'Neue_Matches': new_matches,
                                'Neue_Paare': new_pairs,
                                'Total_Matches': len(global_matched_pairs[method_key]),
                                'Total_TecDoc': len(global_matched_tecdoc[method_key]),
                                'Total_CMD': len(global_matched_cmd[method_key])
                            })
                            chunk_total += new_matches
                            
                    except Exception as e:
                        print(f"⚠️  Fehler bei {method_name} ({tec_col} → {cmd_col}): {str(e)}")
        
        chunks_processed += 1
        
        if chunk_total > 0:
            print(f"      → {chunk_total:,} neue Matches gefunden")
    
    # Finale Ergebnisse zusammenfassen
    if chunk_results:
        results_df = pd.DataFrame(chunk_results)
        
        print(f"\n📊 DETERMINISTIC MATCHING-ERGEBNISSE (DUPLIKATFREI)")
        print("=" * 70)
        
        # Finale Totals nach Methode
        final_totals = {}
        for method_name in matching_methods.keys():
            total_pairs = 0
            total_tecdoc = 0
            total_cmd = 0
            
            for key in global_matched_pairs.keys():
                if key.startswith(method_name + "_"):
                    total_pairs += len(global_matched_pairs[key])
                    total_tecdoc += len(global_matched_tecdoc[key])
                    total_cmd += len(global_matched_cmd[key])
            
            if total_pairs > 0:
                final_totals[method_name] = {
                    'Unique_Pairs': total_pairs,
                    'Unique_TecDoc': total_tecdoc,
                    'Unique_CMD': total_cmd
                }
        
        print("\n🏆 FINALE TOTALS (DUPLIKATFREI):")
        for method, totals in sorted(final_totals.items(), key=lambda x: x[1]['Unique_Pairs'], reverse=True):
            print(f"   {method:20}: {totals['Unique_Pairs']:,} eindeutige Paare")
            print(f"   {'':22}  ({totals['Unique_TecDoc']:,} TecDoc + {totals['Unique_CMD']:,} CMD Werte)")
        
        # Top Spaltenpaare
        column_summary = results_df.groupby(['TecDoc_Spalte', 'CMD_Spalte'])['Total_Matches'].max().sort_values(ascending=False)
        print(f"\n🎯 TOP SPALTENPAARE (DUPLIKATFREI):")
        for (tec_col, cmd_col), total in column_summary.head(5).items():
            print(f"   {tec_col:15} → {cmd_col:25}: {total:,} eindeutige Paare")
        
        # Beispiele zeigen
        print(f"\n💡 MATCH-BEISPIELE (DUPLIKATFREI):")
        print("-" * 50)
        example_count = 0
        for method_key in list(global_matched_pairs.keys())[:3]:
            if global_matched_pairs[method_key] and example_count < 3:
                method, tec_col, cmd_col = method_key.split('_', 2)
                examples = collect_examples_deduped(method_key, 2)
                print(f"\n🔹 {method} ({tec_col} → {cmd_col}):")
                for example in examples:
                    print(f"     {example}")
                example_count += 1
        
        # Gesamtstatistik
        total_unique_pairs = sum(len(pairs) for pairs in global_matched_pairs.values())
        elapsed_time = time.time() - start_time
        
        print(f"\n📈 DETERMINISTIC GESAMTERGEBNIS (DUPLIKATFREI):")
        print(f"   🎯 Total eindeutige Paare: {total_unique_pairs:,}")
        print(f"   ⏱️  Verarbeitungszeit: {elapsed_time:.1f}s")
        print(f"   📦 Chunks verarbeitet: {chunks_processed}")
        print(f"   🔧 Deterministic-Methoden: {len(matching_methods)}")
        print(f"   📊 Repräsentiert ~{(chunks_processed * CHUNK_SIZE) / 1000000:.1f}M Zeilen von 40GB")
        
        # Ergebnisse speichern
        output_file = f"{VISUALIZATION_DIR}/deterministic_matching_results_deduped.csv"
        results_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\n💾 Duplikatfreie Ergebnisse gespeichert: {output_file}")
        
        # Detaillierte Pair-Statistik speichern
        pair_stats = []
        for method_key, pairs in global_matched_pairs.items():
            if pairs:
                method, tec_col, cmd_col = method_key.split('_', 2)
                pair_stats.append({
                    'Methode': method,
                    'TecDoc_Spalte': tec_col,
                    'CMD_Spalte': cmd_col,
                    'Eindeutige_Paare': len(pairs),
                    'Eindeutige_TecDoc': len(global_matched_tecdoc[method_key]),
                    'Eindeutige_CMD': len(global_matched_cmd[method_key])
                })
        
        if pair_stats:
            pair_df = pd.DataFrame(pair_stats)
            pair_output = f"{VISUALIZATION_DIR}/unique_pairs_summary.csv"
            pair_df.to_csv(pair_output, index=False, encoding='utf-8')
            print(f"💾 Eindeutige Paare-Statistik: {pair_output}")
        
    else:
        print("\n❌ Keine Matches gefunden!")
    
    print(f"\n✅ Deterministic Analyse (DUPLIKATFREI) abgeschlossen!")

if __name__ == "__main__":
    analyze_deterministic_matching_deduped()
