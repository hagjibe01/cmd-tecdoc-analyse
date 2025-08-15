#!/usr/bin/env python3
"""
TecDoc-CMD Fuzzy-Matching-Analyse
Optimiertes Hauptskript für Fuzzy/Probabilistisches Matching
"""

import sys
import time
from pathlib import Path

# Füge src-Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.core import (
    setup_environment, load_tecdoc_data, load_cmd_csv_data, 
    extract_xml_values, save_results_table, print_summary_stats, Config
)
from src.matching.fuzzy import run_fuzzy_matching
from src.visualization.charts import create_all_visualizations

def main():
    """Hauptfunktion für Fuzzy-Matching-Analyse"""
    
    print("🎯 TECDOC-CMD FUZZY-MATCHING-ANALYSE")
    print("=" * 60)
    
    # Setup
    setup_environment()
    start_time = time.time()
    
    try:
        # 1. Lade TecDoc-Daten (reduziert für Fuzzy)
        print("\n📂 Lade TecDoc-Daten (Sample-Modus)...")
        tecdoc_data = load_tecdoc_data(sample_mode=True)
        
        # 2. CSV-Fuzzy-Matching
        print("\n🔍 FUZZY CSV-ANALYSE")
        print("-" * 40)
        
        try:
            cmd_csv_data = load_cmd_csv_data()
            csv_target_columns = ['article_number', 'tec_doc_article_number']  # Reduziert für Fuzzy
            
            csv_results = run_fuzzy_matching(
                tecdoc_data=tecdoc_data,
                target_data=cmd_csv_data,
                target_columns=csv_target_columns,
                tecdoc_columns=['artno'],  # Nur artno für Fuzzy
                similarity_threshold=0.8,
                sample_mode=True
            )
            
            if not csv_results.empty:
                # Speichere Ergebnisse
                csv_file = save_results_table(csv_results, "fuzzy_csv_results.csv")
                print_summary_stats(csv_results, "CSV-Fuzzy-Matching Ergebnisse")
                
                # Erstelle Visualisierungen
                vis_dir = Config.VIS_DIR / "fuzzy_csv_analysis"
                create_all_visualizations(csv_results, vis_dir, "Fuzzy CSV - ")
            
        except Exception as e:
            print(f"⚠️ CSV-Fuzzy-Analyse fehlgeschlagen: {e}")
        
        # 3. XML-Fuzzy-Matching
        print("\n🔍 FUZZY XML-ANALYSE")
        print("-" * 40)
        
        try:
            xml_data = extract_xml_values()
            xml_target_tags = ['SupplierPtNo', 'TradeNo']  # Reduziert für Fuzzy
            
            xml_results = run_fuzzy_matching(
                tecdoc_data=tecdoc_data,
                target_data=xml_data,
                target_columns=xml_target_tags,
                tecdoc_columns=['artno'],  # Nur artno für Fuzzy
                similarity_threshold=0.8,
                sample_mode=True
            )
            
            if not xml_results.empty:
                # Speichere Ergebnisse
                xml_file = save_results_table(xml_results, "fuzzy_xml_results.csv")
                print_summary_stats(xml_results, "XML-Fuzzy-Matching Ergebnisse")
                
                # Erstelle Visualisierungen
                vis_dir = Config.VIS_DIR / "fuzzy_xml_analysis"
                create_all_visualizations(xml_results, vis_dir, "Fuzzy XML - ")
            
        except Exception as e:
            print(f"⚠️ XML-Fuzzy-Analyse fehlgeschlagen: {e}")
        
        # 4. Finale Zusammenfassung
        elapsed_time = time.time() - start_time
        print(f"\n🎉 FUZZY-ANALYSE ABGESCHLOSSEN!")
        print(f"⏱️  Gesamtlaufzeit: {elapsed_time:.1f}s")
        print(f"📁 Ergebnisse in: {Config.RESULTS_DIR}")
        print(f"💡 Hinweis: Fuzzy-Matching ist rechenintensiv - Sample-Modus verwendet")
        
    except Exception as e:
        print(f"❌ Kritischer Fehler: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
