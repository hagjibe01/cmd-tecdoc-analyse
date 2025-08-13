#!/usr/bin/env python3
"""
Deterministische Matching-Algorithmen
Optimierte, modulare Implementierung aller exakten Matching-Methoden
"""

from typing import List, Dict, Set, Tuple
import pandas as pd
from collections import defaultdict
import time

from ..utils.core import clean_str, get_numeric_values, normalize_values, Config

# =============================================================================
# DETERMINISTISCHE MATCHING-METHODEN
# =============================================================================

class DeterministicMatcher:
    """Zentrale Klasse für deterministische Matching-Algorithmen"""
    
    def __init__(self):
        self.methods = {
            'Exakt': self.exact_match,
            'Substring': self.substring_match,
            'Prefix': self.prefix_match,
            'Suffix': self.suffix_match,
            'Numerisch_Exakt': self.numeric_exact_match,
            'Längenbasiert': self.length_based_match
        }
    
    def exact_match(self, tecdoc_values: List, target_values: List) -> Tuple[int, List[str]]:
        """Exaktes String-Matching mit verschiedenen Normalisierungsstrategien"""
        matches = 0
        examples = []
        
        try:
            # Strategie 1: Direkte exakte Übereinstimmung
            tecdoc_clean = set(clean_str(val) for val in tecdoc_values if clean_str(val))
            target_clean = set(clean_str(val) for val in target_values if clean_str(val))
            direct_matches = tecdoc_clean & target_clean
            
            if direct_matches:
                matches += len(direct_matches)
                examples.extend([f"Direkt: '{m}'" for m in list(direct_matches)[:2]])
            
            # Strategie 2: Numerische Normalisierung
            tecdoc_numeric = get_numeric_values(tecdoc_values)
            target_numeric = get_numeric_values(target_values)
            numeric_matches = tecdoc_numeric & target_numeric
            
            if numeric_matches:
                matches += len(numeric_matches)
                examples.extend([f"Numerisch: {m}" for m in list(numeric_matches)[:2]])
            
            # Strategie 3: Ohne Punkte/Bindestriche
            tecdoc_normalized = normalize_values(tecdoc_values)
            target_normalized = normalize_values(target_values)
            normalized_matches = tecdoc_normalized & target_normalized
            
            if normalized_matches:
                matches += len(normalized_matches)
                examples.extend([f"Normalisiert: '{m}'" for m in list(normalized_matches)[:2]])
            
        except Exception as e:
            print(f"⚠️ Fehler bei exact_match: {e}")
        
        return matches, examples[:5]
    
    def substring_match(self, tecdoc_values: List, target_values: List) -> Tuple[int, List[str]]:
        """Substring-Matching (TecDoc-Wert als Teilstring im Target)"""
        matches = 0
        examples = []
        
        try:
            # Bereite Daten vor
            tecdoc_clean = [clean_str(val) for val in tecdoc_values if clean_str(val) and len(clean_str(val)) >= Config.MIN_STRING_LENGTH]
            target_clean = [clean_str(val) for val in target_values if clean_str(val) and len(clean_str(val)) >= Config.MIN_STRING_LENGTH]
            
            # Finde Substring-Matches
            for tec_val in tecdoc_clean:
                for target_val in target_clean:
                    if tec_val in target_val and tec_val != target_val:  # Substring, aber nicht identisch
                        matches += 1
                        if len(examples) < 5:
                            examples.append(f"'{tec_val}' ↔ '{target_val}'")
                        break  # Ein Match pro TecDoc-Wert
            
        except Exception as e:
            print(f"⚠️ Fehler bei substring_match: {e}")
        
        return matches, examples
    
    def prefix_match(self, tecdoc_values: List, target_values: List, 
                    length: int = None) -> Tuple[int, List[str]]:
        """Prefix-Matching (gleicher Anfang)"""
        if length is None:
            length = Config.PREFIX_SUFFIX_LENGTH
            
        matches = 0
        examples = []
        
        try:
            # Bereite Präfixe vor
            tecdoc_prefixes = set()
            target_prefixes = set()
            
            for val in tecdoc_values:
                clean_val = clean_str(val)
                if len(clean_val) >= length:
                    tecdoc_prefixes.add(clean_val[:length])
            
            for val in target_values:
                clean_val = clean_str(val)
                if len(clean_val) >= length:
                    target_prefixes.add(clean_val[:length])
            
            # Finde gemeinsame Präfixe
            common_prefixes = tecdoc_prefixes & target_prefixes
            matches = len(common_prefixes)
            examples = list(common_prefixes)[:5]
            
        except Exception as e:
            print(f"⚠️ Fehler bei prefix_match: {e}")
        
        return matches, examples
    
    def suffix_match(self, tecdoc_values: List, target_values: List,
                    length: int = None) -> Tuple[int, List[str]]:
        """Suffix-Matching (gleiches Ende)"""
        if length is None:
            length = Config.PREFIX_SUFFIX_LENGTH
            
        matches = 0
        examples = []
        
        try:
            # Bereite Suffixe vor
            tecdoc_suffixes = set()
            target_suffixes = set()
            
            for val in tecdoc_values:
                clean_val = clean_str(val)
                if len(clean_val) >= length:
                    tecdoc_suffixes.add(clean_val[-length:])
            
            for val in target_values:
                clean_val = clean_str(val)
                if len(clean_val) >= length:
                    target_suffixes.add(clean_val[-length:])
            
            # Finde gemeinsame Suffixe
            common_suffixes = tecdoc_suffixes & target_suffixes
            matches = len(common_suffixes)
            examples = list(common_suffixes)[:5]
            
        except Exception as e:
            print(f"⚠️ Fehler bei suffix_match: {e}")
        
        return matches, examples
    
    def numeric_exact_match(self, tecdoc_values: List, target_values: List) -> Tuple[int, List[str]]:
        """Exaktes numerisches Matching"""
        matches = 0
        examples = []
        
        try:
            tecdoc_numeric = get_numeric_values(tecdoc_values)
            target_numeric = get_numeric_values(target_values)
            
            common_numbers = tecdoc_numeric & target_numeric
            matches = len(common_numbers)
            examples = [str(num) for num in list(common_numbers)[:5]]
            
        except Exception as e:
            print(f"⚠️ Fehler bei numeric_exact_match: {e}")
        
        return matches, examples
    
    def length_based_match(self, tecdoc_values: List, target_values: List) -> Tuple[int, List[str]]:
        """Längenbasiertes Matching (gleiche String-Länge)"""
        matches = 0
        examples = []
        
        try:
            # Gruppiere nach Längen
            tecdoc_lengths = defaultdict(list)
            target_lengths = defaultdict(list)
            
            for val in tecdoc_values:
                clean_val = clean_str(val)
                if clean_val:
                    tecdoc_lengths[len(clean_val)].append(clean_val)
            
            for val in target_values:
                clean_val = clean_str(val)
                if clean_val:
                    target_lengths[len(clean_val)].append(clean_val)
            
            # Finde gemeinsame Längen
            for length in tecdoc_lengths:
                if length in target_lengths:
                    matches += min(len(tecdoc_lengths[length]), len(target_lengths[length]))
                    if len(examples) < 5:
                        examples.append(str(length))
            
        except Exception as e:
            print(f"⚠️ Fehler bei length_based_match: {e}")
        
        return matches, examples
    
    def run_all_methods(self, tecdoc_values: List, target_values: List) -> Dict[str, Tuple[int, List[str]]]:
        """Führe alle deterministischen Methoden aus"""
        results = {}
        
        for method_name, method_func in self.methods.items():
            try:
                matches, examples = method_func(tecdoc_values, target_values)
                results[method_name] = (matches, examples)
            except Exception as e:
                print(f"⚠️ Fehler bei {method_name}: {e}")
                results[method_name] = (0, [])
        
        return results

# =============================================================================
# MATCHING-PIPELINE
# =============================================================================

def run_deterministic_matching(tecdoc_data: pd.DataFrame, 
                              target_data: pd.DataFrame,
                              target_columns: List[str],
                              tecdoc_columns: List[str] = None,
                              sample_mode: bool = True) -> pd.DataFrame:
    """
    Führe deterministische Matching-Analyse durch
    
    Args:
        tecdoc_data: TecDoc DataFrame
        target_data: Target DataFrame (CMD CSV oder XML-Dict)
        target_columns: Zu matchende Spalten/Tags
        tecdoc_columns: TecDoc-Spalten (None = alle)
        sample_mode: Reduzierte Analyse
    
    Returns:
        DataFrame mit Matching-Ergebnissen
    """
    print("🔍 DETERMINISTISCHE MATCHING-ANALYSE")
    print("=" * 50)
    
    matcher = DeterministicMatcher()
    results = []
    
    # TecDoc-Spalten bestimmen
    if tecdoc_columns is None:
        tecdoc_columns = ['artno', 'brandno', 'batchsize1', 'batchsize2']
    
    # XML-Daten behandeln
    if isinstance(target_data, dict):
        print("📊 XML-Daten erkannt")
        return _run_xml_matching(tecdoc_data, target_data, target_columns, 
                               tecdoc_columns, matcher, sample_mode)
    
    # CSV-Daten behandeln
    print("📊 CSV-Daten erkannt")
    return _run_csv_matching(tecdoc_data, target_data, target_columns,
                           tecdoc_columns, matcher, sample_mode)

def _run_csv_matching(tecdoc_data: pd.DataFrame, cmd_data: pd.DataFrame,
                     cmd_columns: List[str], tecdoc_columns: List[str],
                     matcher: DeterministicMatcher, sample_mode: bool) -> pd.DataFrame:
    """CSV-basiertes Matching"""
    results = []
    chunk_size = Config.CHUNK_SIZE
    
    # Processiere TecDoc chunkweise
    total_chunks = len(tecdoc_data) // chunk_size + 1
    if sample_mode:
        total_chunks = min(total_chunks, Config.SAMPLE_CHUNKS)
    
    for chunk_num in range(total_chunks):
        start_idx = chunk_num * chunk_size
        end_idx = min(start_idx + chunk_size, len(tecdoc_data))
        tecdoc_chunk = tecdoc_data.iloc[start_idx:end_idx]
        
        print(f"🔄 Chunk {chunk_num + 1}/{total_chunks}: {len(tecdoc_chunk)} Zeilen")
        
        for tecdoc_col in tecdoc_columns:
            if tecdoc_col not in tecdoc_chunk.columns:
                continue
                
            tecdoc_values = tecdoc_chunk[tecdoc_col].dropna().tolist()
            if not tecdoc_values:
                continue
            
            for cmd_col in cmd_columns:
                if cmd_col not in cmd_data.columns:
                    continue
                    
                cmd_values = cmd_data[cmd_col].dropna().tolist()
                if not cmd_values:
                    continue
                
                # Alle Matching-Methoden ausführen
                method_results = matcher.run_all_methods(tecdoc_values, cmd_values)
                
                for method_name, (matches, examples) in method_results.items():
                    results.append({
                        'Chunk': chunk_num + 1,
                        'TecDoc_Spalte': tecdoc_col,
                        'CMD_Spalte': cmd_col,
                        'Methode': method_name,
                        'Matches': matches,
                        'TecDoc_Anzahl': len(tecdoc_values),
                        'CMD_Anzahl': len(cmd_values)
                    })
    
    return pd.DataFrame(results)

def _run_xml_matching(tecdoc_data: pd.DataFrame, xml_data: Dict,
                     xml_tags: List[str], tecdoc_columns: List[str],
                     matcher: DeterministicMatcher, sample_mode: bool) -> pd.DataFrame:
    """XML-basiertes Matching"""
    results = []
    chunk_size = Config.CHUNK_SIZE
    
    # Processiere TecDoc chunkweise
    total_chunks = len(tecdoc_data) // chunk_size + 1
    if sample_mode:
        total_chunks = min(total_chunks, Config.SAMPLE_CHUNKS)
    
    for chunk_num in range(total_chunks):
        start_idx = chunk_num * chunk_size
        end_idx = min(start_idx + chunk_size, len(tecdoc_data))
        tecdoc_chunk = tecdoc_data.iloc[start_idx:end_idx]
        
        print(f"🔄 Chunk {chunk_num + 1}/{total_chunks}: {len(tecdoc_chunk)} Zeilen")
        
        for tecdoc_col in tecdoc_columns:
            if tecdoc_col not in tecdoc_chunk.columns:
                continue
                
            tecdoc_values = tecdoc_chunk[tecdoc_col].dropna().tolist()
            if not tecdoc_values:
                continue
            
            for xml_tag in xml_tags:
                xml_values = xml_data.get(xml_tag, [])
                if not xml_values:
                    continue
                
                # Alle Matching-Methoden ausführen
                method_results = matcher.run_all_methods(tecdoc_values, xml_values)
                
                for method_name, (matches, examples) in method_results.items():
                    results.append({
                        'Chunk': chunk_num + 1,
                        'TecDoc_Spalte': tecdoc_col,
                        'XML_Tag': xml_tag,
                        'Methode': method_name,
                        'Matches': matches,
                        'TecDoc_Anzahl': len(tecdoc_values),
                        'XML_Anzahl': len(xml_values)
                    })
    
    return pd.DataFrame(results)
