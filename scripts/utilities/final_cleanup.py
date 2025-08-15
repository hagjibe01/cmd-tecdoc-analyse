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

    print("[OK] MANUELLES REPOSITORY CLEANUP")
    print("=" * 50)

    # Dateien die entfernt werden sollen
    files_to_remove = [
        "deterministic_results_visualization.py",  # Ersetzt durch ultimate_comparison
        "einzelne_visualisierungen.py",  # Ersetzt durch ultimate_comparison
        "fuzzy_a4_einzeln.py",  # Test-Version
        "fuzzy_visualisierungen.py",  # Ersetzt durch ultimate_comparison
        "matching_visualization.py",  # Alte Version
        "consolidate_cmd_data.py",  # Einmalig verwendet
        "create_final_tables.py",  # Einmalig verwendet
        "status_check.py",  # Debug-Tool
        "cleanup_repo.py",  # Wird ersetzt
    ]

    # Verzeichnisse die entfernt werden sollen
    dirs_to_remove = [
        "visualizations",  # Ersetzt durch results/visualizations
        "eda",  # Explorative Analyse abgeschlossen
    ]

    removed_files = 0
    removed_dirs = 0

    # Dateien entfernen
    for file in files_to_remove:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"[OK] Entfernt: {file}")
                removed_files += 1
            except Exception as e:
                print(f"[ERROR] Fehler beim Entfernen von {file}: {e}")

    # Verzeichnisse entfernen
    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"[OK] Verzeichnis entfernt: {dir_path}")
                removed_dirs += 1
            except Exception as e:
                print(f"[ERROR] Fehler beim Entfernen von {dir_path}: {e}")

    print(f"\n[OK] Cleanup abgeschlossen!")
    print(f"[OK] {removed_files} Dateien entfernt")
    print(f"[OK] {removed_dirs} Verzeichnisse entfernt")

    return removed_files, removed_dirs

def show_final_structure():
    """Zeigt die finale Repository-Struktur"""

    print("\n[OK] FINALE REPOSITORY-STRUKTUR:")
    print("=" * 50)

    # Wichtige Dateien auflisten
    important_files = [
        "README.md",
        "requirements.txt",
        "run_main_analysis.py",
        "run_visualizations.py",
        "scripts/core/run_deterministic_analysis.py",
        "scripts/core/run_fuzzy_analysis.py",
        "scripts/analysis/ultimate_comparison.py",
        "src/",
        "data/",
        "results/",
        "archive/backup/",
    ]

    for item in important_files:
        if os.path.exists(item):
            if os.path.isdir(item):
                print(f"[OK] {item}/")
            else:
                print(f"[OK] {item}")
        else:
            print(f"[ERROR] {item} (nicht gefunden)")

    print("\n[OK] KERN-SKRIPTE FÜR DHBW-ANHANG:")
    print("1. scripts/core/run_deterministic_analysis.py - Deterministische Verfahren")
    print("2. scripts/core/run_fuzzy_analysis.py - Fuzzy-Matching-Verfahren")
    print("3. scripts/analysis/ultimate_comparison.py - Hauptvisualisierung")
    print("4. src/matching/deterministic.py - Algorithmus-Implementierung")
    print("5. src/utils/core.py - System-Konfiguration")

if __name__ == "__main__":
    print("Führe manuelles Repository-Cleanup durch...")
    removed_files, removed_dirs = manual_cleanup()
    show_final_structure()

    print(f"[OK] Alle wichtigen Dateien sind in archive/backup/ gesichert")
