#!/usr/bin/env python3
"""
Fuzzy/Probabilistische Matching-Algorithmen
Optimierte, modulare Implementierung aller Fuzzy-Matching-Methoden
"""

from typing import List, Dict, Set, Tuple
import pandas as pd
import numpy as np
from difflib import SequenceMatcher
try:
    from jellyfish import jaro_winkler_similarity
    JELLYFISH_AVAILABLE = True
except ImportError:
    JELLYFISH_AVAILABLE = False
    print("⚠️ Jellyfish nicht verfügbar. Jaro-Winkler wird übersprungen.")

from ..utils.core import clean_str, get_numeric_values, Config

# =============================================================================
# FUZZY MATCHING-METHODEN
# =============================================================================

class FuzzyMatcher:
    """Zentrale Klasse für Fuzzy/Probabilistische Matching-Algorithmen"""
    
    def __init__(self, similarity_threshold: float = None):
        self.threshold = similarity_threshold or Config.SIMILARITY_THRESHOLD
        
        self.methods = {
            'Levenshtein': self.levenshtein_match,
            'Numerisch_Toleranz': self.numeric_tolerance_match,
            'Teilstring_Fuzzy': self.fuzzy_substring_match,
            'Längen_Toleranz': self.length_tolerance_match
        }
        
        # Jaro-Winkler nur wenn verfügbar
        if JELLYFISH_AVAILABLE:
            self.methods['Jaro_Winkler'] = self.jaro_winkler_match
    
    def levenshtein_match(self, tecdoc_values: List, target_values: List) -> Tuple[int, List[str]]:
        """Levenshtein-basiertes Fuzzy Matching"""
        matches = 0
        examples = []
        
        try:
            # Bereite Daten vor
            tecdoc_clean = [clean_str(val) for val in tecdoc_values 
                           if clean_str(val) and len(clean_str(val)) >= Config.MIN_STRING_LENGTH]
            target_clean = [clean_str(val) for val in target_values 
                           if clean_str(val) and len(clean_str(val)) >= Config.MIN_STRING_LENGTH]
            
            # Berechne Ähnlichkeiten
            for tec_val in tecdoc_clean:
                best_similarity = 0
                best_match = None
                
                for target_val in target_clean:
                    similarity = SequenceMatcher(None, tec_val, target_val).ratio()
                    if similarity > best_similarity and similarity >= self.threshold:
                        best_similarity = similarity
                        best_match = target_val
                
                if best_match:
                    matches += 1
                    if len(examples) < 5:
                        examples.append(f"'{tec_val}' ↔ '{best_match}' ({best_similarity:.2f})")
            
        except Exception as e:
            print(f"⚠️ Fehler bei levenshtein_match: {e}")
        
        return matches, examples
    
    def jaro_winkler_match(self, tecdoc_values: List, target_values: List) -> Tuple[int, List[str]]:
        """Jaro-Winkler Similarity Matching"""
        if not JELLYFISH_AVAILABLE:
            return 0, []
        
        matches = 0
        examples = []
        
        try:
            # Bereite Daten vor
            tecdoc_clean = [clean_str(val) for val in tecdoc_values 
                           if clean_str(val) and len(clean_str(val)) >= Config.MIN_STRING_LENGTH]
            target_clean = [clean_str(val) for val in target_values 
                           if clean_str(val) and len(clean_str(val)) >= Config.MIN_STRING_LENGTH]
            
            # Berechne Jaro-Winkler Ähnlichkeiten
            for tec_val in tecdoc_clean:
                best_similarity = 0
                best_match = None
                
                for target_val in target_clean:
                    similarity = jaro_winkler_similarity(tec_val, target_val)
                    if similarity > best_similarity and similarity >= self.threshold:
                        best_similarity = similarity
                        best_match = target_val
                
                if best_match:
                    matches += 1
                    if len(examples) < 5:
                        examples.append(f"'{tec_val}' ↔ '{best_match}' ({best_similarity:.2f})")
            
        except Exception as e:
            print(f"⚠️ Fehler bei jaro_winkler_match: {e}")
        
        return matches, examples
    
    def numeric_tolerance_match(self, tecdoc_values: List, target_values: List,
                              tolerance_percent: float = 5.0) -> Tuple[int, List[str]]:
        """Numerisches Matching mit Toleranz"""
        matches = 0
        examples = []
        
        try:
            # Extrahiere numerische Werte
            tecdoc_numeric = []
            target_numeric = []
            
            for val in tecdoc_values:
                try:
                    num_val = float(clean_str(val))
                    if not np.isnan(num_val):
                        tecdoc_numeric.append(num_val)
                except:
                    continue
            
            for val in target_values:
                try:
                    num_val = float(clean_str(val))
                    if not np.isnan(num_val):
                        target_numeric.append(num_val)
                except:
                    continue
            
            # Finde Matches mit Toleranz
            for tec_num in tecdoc_numeric:
                for target_num in target_numeric:
                    if tec_num == 0 or target_num == 0:
                        continue
                    
                    # Berechne prozentuale Abweichung
                    diff_percent = abs((tec_num - target_num) / tec_num) * 100
                    
                    if diff_percent <= tolerance_percent:
                        matches += 1
                        if len(examples) < 5:
                            examples.append(f"{tec_num} ↔ {target_num} ({diff_percent:.1f}%)")
                        break  # Ein Match pro TecDoc-Wert
            
        except Exception as e:
            print(f"⚠️ Fehler bei numeric_tolerance_match: {e}")
        
        return matches, examples
    
    def fuzzy_substring_match(self, tecdoc_values: List, target_values: List,
                            min_length: int = 4) -> Tuple[int, List[str]]:
        """Fuzzy Substring-Matching"""
        matches = 0
        examples = []
        
        try:
            # Bereite Daten vor
            tecdoc_clean = [clean_str(val) for val in tecdoc_values 
                           if clean_str(val) and len(clean_str(val)) >= min_length]
            target_clean = [clean_str(val) for val in target_values 
                           if clean_str(val) and len(clean_str(val)) >= min_length]
            
            # Finde Fuzzy-Substrings
            for tec_val in tecdoc_clean:
                best_similarity = 0
                best_match = None
                
                for target_val in target_clean:
                    # Prüfe alle möglichen Substrings
                    for i in range(len(target_val) - min_length + 1):
                        substring = target_val[i:i + len(tec_val)]
                        if len(substring) >= min_length:
                            similarity = SequenceMatcher(None, tec_val, substring).ratio()
                            if similarity > best_similarity and similarity >= self.threshold:
                                best_similarity = similarity
                                best_match = f"{tec_val} in {target_val}"
                
                if best_match:
                    matches += 1
                    if len(examples) < 5:
                        examples.append(f"{best_match} ({best_similarity:.2f})")
            
        except Exception as e:
            print(f"⚠️ Fehler bei fuzzy_substring_match: {e}")
        
        return matches, examples
    
    def length_tolerance_match(self, tecdoc_values: List, target_values: List,
                             max_diff: int = 2) -> Tuple[int, List[str]]:
        """Längen-Toleranz Matching (ähnliche Längen)"""
        matches = 0
        examples = []
        
        try:
            # Gruppiere nach ähnlichen Längen
            from collections import defaultdict
            
            tecdoc_by_length = defaultdict(list)
            target_by_length = defaultdict(list)
            
            for val in tecdoc_values:
                clean_val = clean_str(val)
                if clean_val:
                    tecdoc_by_length[len(clean_val)].append(clean_val)
            
            for val in target_values:
                clean_val = clean_str(val)
                if clean_val:
                    target_by_length[len(clean_val)].append(clean_val)
            
            # Finde Matches mit Längen-Toleranz
            for tec_length, tec_vals in tecdoc_by_length.items():
                for target_length in range(max(1, tec_length - max_diff), 
                                         tec_length + max_diff + 1):
                    if target_length in target_by_length:
                        potential_matches = min(len(tec_vals), len(target_by_length[target_length]))
                        matches += potential_matches
                        
                        if len(examples) < 5 and potential_matches > 0:
                            examples.append(f"Länge {tec_length} ↔ {target_length}")
            
        except Exception as e:
            print(f"⚠️ Fehler bei length_tolerance_match: {e}")
        
        return matches, examples
    
    def run_all_methods(self, tecdoc_values: List, target_values: List) -> Dict[str, Tuple[int, List[str]]]:
        """Führe alle Fuzzy-Methoden aus"""
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
# FUZZY MATCHING-PIPELINE
# =============================================================================

def run_fuzzy_matching(tecdoc_data: pd.DataFrame, 
                      target_data: pd.DataFrame,
                      target_columns: List[str],
                      tecdoc_columns: List[str] = None,
                      similarity_threshold: float = None,
                      sample_mode: bool = True) -> pd.DataFrame:
    """
    Führe Fuzzy-Matching-Analyse durch
    
    Args:
        tecdoc_data: TecDoc DataFrame
        target_data: Target DataFrame (CMD CSV oder XML-Dict)
        target_columns: Zu matchende Spalten/Tags
        tecdoc_columns: TecDoc-Spalten (None = alle)
        similarity_threshold: Ähnlichkeitsschwelle
        sample_mode: Reduzierte Analyse
    
    Returns:
        DataFrame mit Fuzzy-Matching-Ergebnissen
    """
    print("🔍 FUZZY-MATCHING-ANALYSE")
    print("=" * 50)
    
    matcher = FuzzyMatcher(similarity_threshold)
    results = []
    
    # TecDoc-Spalten bestimmen
    if tecdoc_columns is None:
        tecdoc_columns = ['artno', 'brandno']  # Reduziert für Fuzzy
    
    # XML-Daten behandeln
    if isinstance(target_data, dict):
        print("📊 XML-Daten erkannt")
        return _run_xml_fuzzy_matching(tecdoc_data, target_data, target_columns, 
                                      tecdoc_columns, matcher, sample_mode)
    
    # CSV-Daten behandeln
    print("📊 CSV-Daten erkannt")
    return _run_csv_fuzzy_matching(tecdoc_data, target_data, target_columns,
                                  tecdoc_columns, matcher, sample_mode)

def _run_csv_fuzzy_matching(tecdoc_data: pd.DataFrame, cmd_data: pd.DataFrame,
                           cmd_columns: List[str], tecdoc_columns: List[str],
                           matcher: FuzzyMatcher, sample_mode: bool) -> pd.DataFrame:
    """CSV-basiertes Fuzzy-Matching"""
    results = []
    chunk_size = Config.CHUNK_SIZE
    
    # Reduzierte Chunk-Anzahl für Fuzzy (rechenintensiv)
    max_chunks = 2 if sample_mode else len(tecdoc_data) // chunk_size + 1
    
    for chunk_num in range(max_chunks):
        start_idx = chunk_num * chunk_size
        end_idx = min(start_idx + chunk_size, len(tecdoc_data))
        tecdoc_chunk = tecdoc_data.iloc[start_idx:end_idx]
        
        print(f"🔄 Fuzzy Chunk {chunk_num + 1}/{max_chunks}: {len(tecdoc_chunk)} Zeilen")
        
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
                
                # Alle Fuzzy-Methoden ausführen
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

def _run_xml_fuzzy_matching(tecdoc_data: pd.DataFrame, xml_data: Dict,
                           xml_tags: List[str], tecdoc_columns: List[str],
                           matcher: FuzzyMatcher, sample_mode: bool) -> pd.DataFrame:
    """XML-basiertes Fuzzy-Matching"""
    results = []
    chunk_size = Config.CHUNK_SIZE
    
    # Reduzierte Chunk-Anzahl für Fuzzy
    max_chunks = 2 if sample_mode else len(tecdoc_data) // chunk_size + 1
    
    for chunk_num in range(max_chunks):
        start_idx = chunk_num * chunk_size
        end_idx = min(start_idx + chunk_size, len(tecdoc_data))
        tecdoc_chunk = tecdoc_data.iloc[start_idx:end_idx]
        
        print(f"🔄 Fuzzy Chunk {chunk_num + 1}/{max_chunks}: {len(tecdoc_chunk)} Zeilen")
        
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
                
                # Alle Fuzzy-Methoden ausführen
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
