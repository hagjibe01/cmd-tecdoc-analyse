#!/usr/bin/env python3
"""
TecDoc-CMD Deterministische Matching-Analyse
Optimiertes Hauptskript für deterministisches Matching
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
from src.matching.deterministic import run_deterministic_matching
from src.visualization.charts import create_all_visualizations

def main():
    """Hauptfunktion für deterministische Matching-Analyse"""
    
    print("🎯 TECDOC-CMD DETERMINISTISCHE MATCHING-ANALYSE")
    print("=" * 60)
    
    # Setup
    setup_environment()
    start_time = time.time()
    
    try:
        # 1. Lade TecDoc-Daten
        print("\n📂 Lade TecDoc-Daten...")
        tecdoc_data = load_tecdoc_data(sample_mode=True)
        
        # 2. CSV-Matching
        print("\n🔍 DETERMINISTISCHE CSV-ANALYSE")
        print("-" * 40)
        
        try:
            cmd_csv_data = load_cmd_csv_data()
            csv_target_columns = ['article_number', 'tec_doc_article_number', 'trade_number']
            
            csv_results = run_deterministic_matching(
                tecdoc_data=tecdoc_data,
                target_data=cmd_csv_data,
                target_columns=csv_target_columns,
                sample_mode=True
            )
            
            if not csv_results.empty:
                # Speichere Ergebnisse
                csv_file = save_results_table(csv_results, "deterministic_csv_results.csv")
                print_summary_stats(csv_results, "CSV-Matching Ergebnisse")
                
                # Erstelle Visualisierungen
                vis_dir = Config.VIS_DIR / "csv_analysis"
                create_all_visualizations(csv_results, vis_dir, "CSV - ")
            
        except Exception as e:
            print(f"⚠️ CSV-Analyse fehlgeschlagen: {e}")
        
        # 3. XML-Matching
        print("\n🔍 DETERMINISTISCHE XML-ANALYSE")
        print("-" * 40)
        
        try:
            xml_data = extract_xml_values()
            xml_target_tags = ['SupplierPtNo', 'TradeNo', 'Brand']
            
            xml_results = run_deterministic_matching(
                tecdoc_data=tecdoc_data,
                target_data=xml_data,
                target_columns=xml_target_tags,
                sample_mode=True
            )
            
            if not xml_results.empty:
                # Speichere Ergebnisse
                xml_file = save_results_table(xml_results, "deterministic_xml_results.csv")
                print_summary_stats(xml_results, "XML-Matching Ergebnisse")
                
                # Erstelle Visualisierungen
                vis_dir = Config.VIS_DIR / "xml_analysis"
                create_all_visualizations(xml_results, vis_dir, "XML - ")
            
        except Exception as e:
            print(f"⚠️ XML-Analyse fehlgeschlagen: {e}")
        
        # 4. Finale Zusammenfassung
        elapsed_time = time.time() - start_time
        print(f"\n🎉 ANALYSE ABGESCHLOSSEN!")
        print(f"⏱️  Gesamtlaufzeit: {elapsed_time:.1f}s")
        print(f"📁 Ergebnisse in: {Config.RESULTS_DIR}")
        
    except Exception as e:
        print(f"❌ Kritischer Fehler: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
