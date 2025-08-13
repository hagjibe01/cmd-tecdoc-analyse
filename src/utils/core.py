#!/usr/bin/env python3
"""
Core Utilities für TecDoc-CMD Matching Analyse
Zentrale Hilfsfunktionen und Konfiguration
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional, Union
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# KONFIGURATION
# =============================================================================

class Config:
    """Zentrale Konfiguration für das Matching-System"""
    
    # Verzeichnisse
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    INPUT_DIR = DATA_DIR / "input"
    OUTPUT_DIR = DATA_DIR / "output"
    RESULTS_DIR = PROJECT_ROOT / "results"
    TABLES_DIR = RESULTS_DIR / "tables"
    VIS_DIR = RESULTS_DIR / "visualizations"
    
    # TecDoc Daten
    TECDOC_FILE = "200_Article_Table.csv"
    CHUNK_SIZE = 10000
    SAMPLE_CHUNKS = 5  # Für Test-Modus
    
    # CMD Daten
    CMD_CSV_FILES = ["cmd_daten.csv"]
    CMD_XML_DIR = "cmd_platform_data"
    
    # Matching Parameter
    MIN_STRING_LENGTH = 3
    PREFIX_SUFFIX_LENGTH = 5
    SIMILARITY_THRESHOLD = 0.8
    
    @classmethod
    def ensure_directories(cls):
        """Stelle sicher, dass alle Verzeichnisse existieren"""
        for dir_path in [cls.DATA_DIR, cls.INPUT_DIR, cls.OUTPUT_DIR, 
                        cls.RESULTS_DIR, cls.TABLES_DIR, cls.VIS_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)

# =============================================================================
# DATEN-UTILITIES
# =============================================================================

def clean_str(value) -> str:
    """Reinige und normalisiere String-Werte"""
    if pd.isna(value):
        return ""
    return str(value).strip().upper()

def load_tecdoc_data(chunk_size: int = Config.CHUNK_SIZE, 
                    sample_mode: bool = True) -> pd.DataFrame:
    """
    Lade TecDoc-Daten chunkweise
    
    Args:
        chunk_size: Größe der Chunks
        sample_mode: Nur erste N Chunks laden
    
    Returns:
        DataFrame mit TecDoc-Daten
    """
    file_path = Config.INPUT_DIR / Config.TECDOC_FILE
    
    if not file_path.exists():
        # Fallback zum alten Standort
        file_path = Config.PROJECT_ROOT / Config.TECDOC_FILE
    
    if not file_path.exists():
        raise FileNotFoundError(f"TecDoc-Datei nicht gefunden: {Config.TECDOC_FILE}")
    
    print(f"📂 Lade TecDoc-Daten: {file_path}")
    
    if sample_mode:
        # Nur erste Chunks für Tests
        chunks = []
        for i, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
            chunks.append(chunk)
            if i >= Config.SAMPLE_CHUNKS - 1:
                break
        data = pd.concat(chunks, ignore_index=True)
        print(f"📊 Sample-Modus: {len(data):,} Zeilen aus {len(chunks)} Chunks geladen")
    else:
        # Vollständige Datei
        data = pd.read_csv(file_path)
        print(f"📊 Vollständige Datei: {len(data):,} Zeilen geladen")
    
    return data

def load_cmd_csv_data() -> pd.DataFrame:
    """Lade CMD CSV-Daten"""
    csv_files = []
    
    for filename in Config.CMD_CSV_FILES:
        file_path = Config.INPUT_DIR / filename
        if not file_path.exists():
            file_path = Config.PROJECT_ROOT / filename
        
        if file_path.exists():
            csv_files.append(file_path)
    
    if not csv_files:
        raise FileNotFoundError("Keine CMD CSV-Dateien gefunden")
    
    # Lade alle CSV-Dateien
    dataframes = []
    for file_path in csv_files:
        print(f"📂 Lade CMD CSV: {file_path}")
        df = pd.read_csv(file_path)
        dataframes.append(df)
    
    # Kombiniere alle DataFrames
    combined_data = pd.concat(dataframes, ignore_index=True)
    print(f"📊 CMD CSV geladen: {len(combined_data):,} Zeilen")
    
    return combined_data

def extract_xml_values(xml_dir: str = None) -> Dict[str, List]:
    """Extrahiere Werte aus XML-Dateien"""
    import xml.etree.ElementTree as ET
    
    if xml_dir is None:
        xml_dir = Config.INPUT_DIR / Config.CMD_XML_DIR
        if not xml_dir.exists():
            xml_dir = Config.PROJECT_ROOT / Config.CMD_XML_DIR
    
    if not Path(xml_dir).exists():
        raise FileNotFoundError(f"XML-Verzeichnis nicht gefunden: {xml_dir}")
    
    xml_data = {}
    xml_files = list(Path(xml_dir).glob("*.xml"))
    
    print(f"🔍 Extrahiere XML-Werte aus {len(xml_files)} Dateien...")
    
    # Relevante XML-Tags
    target_tags = [
        'SupplierPtNo', 'TradeNo', 'ArticleDescription_DE', 'ArticleDescription_EN',
        'Brand', 'MinOrderQuantity', 'MaxOrderQuantity', 'GrossWeight', 'Volume', 'CategoryID'
    ]
    
    for tag in target_tags:
        xml_data[tag] = []
    
    for xml_file in xml_files:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Extrahiere Werte für jeden Tag
            for tag in target_tags:
                elements = root.findall(f".//{tag}")
                for elem in elements:
                    if elem.text and elem.text.strip():
                        xml_data[tag].append(elem.text.strip())
        
        except Exception as e:
            print(f"⚠️ Fehler beim Parsen von {xml_file}: {e}")
    
    # Entferne Duplikate und konvertiere zu Sets
    for tag in target_tags:
        xml_data[tag] = list(set(xml_data[tag]))
        print(f"   {tag}: {len(xml_data[tag]):,} Werte gefunden")
    
    return xml_data

# =============================================================================
# MATCHING-UTILITIES
# =============================================================================

def get_numeric_values(values: List) -> Set[int]:
    """Extrahiere numerische Werte aus einer Liste"""
    numeric_set = set()
    for val in values:
        clean_val = clean_str(val)
        if clean_val.isdigit():
            numeric_set.add(int(clean_val))
    return numeric_set

def normalize_values(values: List, remove_punct: bool = True) -> Set[str]:
    """Normalisiere Werte (ohne Punkte/Bindestriche)"""
    normalized = set()
    for val in values:
        if remove_punct:
            normalized_val = str(val).replace('.', '').replace('-', '').replace(' ', '').upper().strip()
        else:
            normalized_val = clean_str(val)
        
        if normalized_val and len(normalized_val) >= Config.MIN_STRING_LENGTH:
            normalized.add(normalized_val)
    
    return normalized

# =============================================================================
# ERGEBNIS-UTILITIES
# =============================================================================

def save_results_table(df: pd.DataFrame, filename: str, 
                      results_dir: str = None) -> str:
    """Speichere Ergebnistabelle"""
    if results_dir is None:
        results_dir = Config.TABLES_DIR
    
    Path(results_dir).mkdir(parents=True, exist_ok=True)
    file_path = Path(results_dir) / filename
    
    df.to_csv(file_path, index=False)
    print(f"💾 Ergebnisse gespeichert: {file_path}")
    
    return str(file_path)

def load_results_table(filename: str, results_dir: str = None) -> pd.DataFrame:
    """Lade Ergebnistabelle"""
    if results_dir is None:
        results_dir = Config.TABLES_DIR
    
    file_path = Path(results_dir) / filename
    
    if not file_path.exists():
        raise FileNotFoundError(f"Ergebnisdatei nicht gefunden: {file_path}")
    
    return pd.read_csv(file_path)

def print_summary_stats(df: pd.DataFrame, title: str = "Zusammenfassung"):
    """Drucke Zusammenfassungsstatistiken"""
    print(f"\n📊 {title.upper()}")
    print("=" * 60)
    print(f"📈 Gesamtzeilen: {len(df):,}")
    
    if 'Matches' in df.columns:
        print(f"🎯 Gesamtmatches: {df['Matches'].sum():,}")
        print(f"💫 Durchschnitt: {df['Matches'].mean():.1f}")
        print(f"📊 Median: {df['Matches'].median():.1f}")
    
    if 'Methode' in df.columns:
        print(f"🔧 Methoden: {df['Methode'].nunique()}")
        top_method = df.groupby('Methode')['Matches'].sum().idxmax()
        print(f"🏆 Top-Methode: {top_method}")

# =============================================================================
# MAIN UTILITIES
# =============================================================================

def setup_environment():
    """Setup der Arbeitsumgebung"""
    print("🔧 Setup Arbeitsumgebung...")
    Config.ensure_directories()
    print("✅ Verzeichnisse erstellt")

if __name__ == "__main__":
    # Test der Utilities
    setup_environment()
    print("🧪 Core Utils erfolgreich geladen!")
