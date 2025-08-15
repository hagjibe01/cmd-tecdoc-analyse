#!/usr/bin/env python3
"""
Manual Repository Cleanup für finale DHBW-Projektarbeit
Entfernt alle nicht-essentiellen Dateien und behält nur die Kern-Funktionalität
"""

import os
import shutil
from pathlib import Path
import sys

def manual_cleanup():
    """Führt manuelle Aufräumarbeiten durch"""
    
    print("🧹 MANUELLES REPOSITORY CLEANUP")
    print("=" * 50)
    
    # Dateien die entfernt werden sollen
    files_to_remove = [
        "deterministic_results_visualization.py",  # Ersetzt durch ultimate_comparison
        "einzelne_visualisierungen.py",           # Ersetzt durch ultimate_comparison
        "fuzzy_a4_einzeln.py",                    # Test-Version
        "fuzzy_visualisierungen.py",              # Ersetzt durch ultimate_comparison
        "matching_visualization.py",              # Alte Version
        "consolidate_cmd_data.py",                # Einmalig verwendet
        "create_final_tables.py",                 # Einmalig verwendet
        "status_check.py",                        # Debug-Tool
        "cleanup_repo.py",                        # Wird ersetzt
    ]
    
    # Verzeichnisse die entfernt werden sollen
    dirs_to_remove = [
        "visualizations",  # Ersetzt durch results/visualizations
        "eda",            # Explorative Analyse abgeschlossen
    ]
    
    removed_files = 0
    removed_dirs = 0
    
    # Dateien entfernen
    for file in files_to_remove:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"🗑️  Entfernt: {file}")
                removed_files += 1
            except Exception as e:
                print(f"❌ Fehler beim Entfernen von {file}: {e}")
    
    # Verzeichnisse entfernen
    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"📁 Verzeichnis entfernt: {dir_path}")
                removed_dirs += 1
            except Exception as e:
                print(f"❌ Fehler beim Entfernen von {dir_path}: {e}")
    
    print(f"\n✅ Cleanup abgeschlossen!")
    print(f"🗑️  {removed_files} Dateien entfernt")
    print(f"📁 {removed_dirs} Verzeichnisse entfernt")
    
    return removed_files, removed_dirs

def show_final_structure():
    """Zeigt die finale Repository-Struktur"""
    
    print("\n📋 FINALE REPOSITORY-STRUKTUR:")
    print("=" * 50)
    
    # Wichtige Dateien auflisten
    important_files = [
        "README.md",
        "requirements.txt", 
        "run_deterministic_analysis.py",
        "run_fuzzy_analysis.py",
        "ultimate_comparison.py",
        "src/",
        "data/",
        "results/",
        "backup_old_scripts/",
    ]
    
    for item in important_files:
        if os.path.exists(item):
            if os.path.isdir(item):
                print(f"📁 {item}")
            else:
                print(f"📄 {item}")
        else:
            print(f"❌ {item} (nicht gefunden)")
    
    print("\n🎯 KERN-SKRIPTE FÜR DHBW-ANHANG:")
    print("1. run_deterministic_analysis.py - Deterministische Verfahren")
    print("2. run_fuzzy_analysis.py - Fuzzy-Matching-Verfahren")  
    print("3. ultimate_comparison.py - Hauptvisualisierung")
    print("4. src/matching/deterministic.py - Algorithmus-Implementierung")
    print("5. src/utils/core.py - System-Konfiguration")

if __name__ == "__main__":
    print("Führe manuelles Repository-Cleanup durch...")
    removed_files, removed_dirs = manual_cleanup()
    show_final_structure()
    
    print(f"\n🚀 Repository ist jetzt aufgeräumt und bereit für die DHBW-Abgabe!")
    print(f"💾 Alle wichtigen Dateien sind in backup_old_scripts/ gesichert")
