#!/usr/bin/env python3
"""
Repository Status Check nach Cleanup
Überprüft die organisierte Struktur und erstellt einen Bericht
"""

import os
import glob
from pathlib import Path

def count_files_in_directory(directory, extension="*.py"):
    """Zählt Dateien in einem Verzeichnis"""
    if not os.path.exists(directory):
        return 0
    return len(glob.glob(os.path.join(directory, extension)))

def check_directory_structure():
    """Überprüft die Verzeichnisstruktur nach Cleanup"""
    
    print("📁 REPOSITORY STRUKTUR NACH CLEANUP")
    print("=" * 60)
    
    structure = {
        'scripts/core': 'Kernfunktionalität und Hauptanalyse',
        'scripts/analysis': 'Datenanalyse und Tabellenerstellung', 
        'scripts/visualization': 'Visualisierungsskripte',
        'scripts/utilities': 'Hilfsskripte und Tools',
        'data/input': 'Eingangsdaten',
        'data/output': 'Ausgangsdaten',
        'results/tables': 'Ergebnis-Tabellen',
        'results/visualizations': 'Generierte Visualisierungen',
        'archive/backup': 'Archivierte Backup-Dateien',
        'docs': 'Dokumentation'
    }
    
    for directory, description in structure.items():
        exists = "✅" if os.path.exists(directory) else "❌"
        py_files = count_files_in_directory(directory)
        py_info = f"({py_files} .py)" if py_files > 0 else ""
        
        print(f"{exists} {directory:<25} - {description} {py_info}")

def list_main_files():
    """Listet die Hauptdateien im Root-Verzeichnis"""
    
    print("\n📄 HAUPTDATEIEN IM ROOT-VERZEICHNIS")
    print("=" * 60)
    
    main_files = [
        'run_main_analysis.py',
        'run_visualizations.py', 
        'README.md',
        'requirements.txt',
        '.gitignore',
        'repository_cleanup.py'
    ]
    
    for file in main_files:
        exists = "✅" if os.path.exists(file) else "❌"
        print(f"{exists} {file}")

def check_python_scripts():
    """Überprüft die Organisation der Python-Skripte"""
    
    print("\n🐍 PYTHON-SKRIPTE ORGANISATION")
    print("=" * 60)
    
    script_categories = {
        'scripts/core': [
            'unified_fuzzy_data.py',
            'run_deterministic_analysis.py',
            'run_fuzzy_analysis.py'
        ],
        'scripts/analysis': [
            'consolidate_cmd_data.py',
            'comprehensive_matching_overview.py',
            'deterministic_results_table.py',
            'fuzzy_results_table.py',
            'create_final_tables.py',
            'ultimate_comparison.py'
        ],
        'scripts/visualization': [
            'deterministic_results_visualization.py',
            'fuzzy_visualisierungen.py',
            'fuzzy_erfolgsrate_a4_optimiert.py',
            'fuzzy_a4_einzeln.py',
            'fuzzy_datenquellen_verteilung.py',
            'fuzzy_datenquellen_verteilung_detailliert.py',
            'einzelne_visualisierungen.py',
            'matching_visualization.py',
            'separate_method_visualizations.py'
        ],
        'scripts/utilities': [
            'quick_calc.py',
            'status_check.py',
            'final_cleanup.py',
            'cleanup_repo.py'
        ]
    }
    
    for category, scripts in script_categories.items():
        print(f"\n📂 {category}:")
        for script in scripts:
            script_path = os.path.join(category, script)
            exists = "✅" if os.path.exists(script_path) else "❌"
            print(f"  {exists} {script}")

def check_cleanup_success():
    """Überprüft ob das Cleanup erfolgreich war"""
    
    print("\n🧹 CLEANUP ERFOLG-CHECK")
    print("=" * 60)
    
    # Prüfe ob __pycache__ Verzeichnisse entfernt wurden
    pycache_dirs = glob.glob('**/__pycache__', recursive=True)
    if not pycache_dirs:
        print("✅ Alle __pycache__ Verzeichnisse entfernt")
    else:
        print("❌ Noch vorhandene __pycache__ Verzeichnisse:")
        for cache_dir in pycache_dirs:
            print(f"  - {cache_dir}")
    
    # Prüfe ob backup_old_scripts entfernt wurde
    if not os.path.exists('backup_old_scripts'):
        print("✅ backup_old_scripts erfolgreich archiviert")
    else:
        print("❌ backup_old_scripts noch vorhanden")
    
    # Prüfe ob Archiv erstellt wurde
    if os.path.exists('archive/backup'):
        print("✅ Archiv-Verzeichnis erstellt")
    else:
        print("❌ Archiv-Verzeichnis fehlt")

def generate_project_statistics():
    """Generiert Projektstatistiken"""
    
    print("\n📊 PROJEKT-STATISTIKEN")
    print("=" * 60)
    
    # Zähle Python-Dateien in verschiedenen Kategorien
    core_scripts = count_files_in_directory('scripts/core')
    analysis_scripts = count_files_in_directory('scripts/analysis')
    viz_scripts = count_files_in_directory('scripts/visualization')
    util_scripts = count_files_in_directory('scripts/utilities')
    
    total_scripts = core_scripts + analysis_scripts + viz_scripts + util_scripts
    
    print(f"🐍 Gesamt Python-Skripte: {total_scripts}")
    print(f"  ├─ Core-Skripte: {core_scripts}")
    print(f"  ├─ Analyse-Skripte: {analysis_scripts}")
    print(f"  ├─ Visualisierung-Skripte: {viz_scripts}")
    print(f"  └─ Utility-Skripte: {util_scripts}")
    
    # Zähle Ergebnisdateien
    result_tables = count_files_in_directory('results/tables', '*.*')
    result_viz = count_files_in_directory('results/visualizations', '*.*')
    
    print(f"\n📊 Ergebnisdateien:")
    print(f"  ├─ Tabellen: {result_tables}")
    print(f"  └─ Visualisierungen: {result_viz}")

def main():
    """Hauptfunktion für Status-Check"""
    
    print("🔍 REPOSITORY STATUS CHECK")
    print("🕒 Nach Repository-Cleanup")
    print("=" * 60)
    
    check_directory_structure()
    list_main_files()
    check_python_scripts()
    check_cleanup_success()
    generate_project_statistics()
    
    print("\n" + "=" * 60)
    print("✅ STATUS-CHECK ABGESCHLOSSEN")
    print("\n🚀 Repository ist jetzt sauber organisiert!")
    print("📋 Nutzen Sie 'python run_main_analysis.py' für komplette Analyse")
    print("🎨 Nutzen Sie 'python run_visualizations.py' für alle Visualisierungen")

if __name__ == "__main__":
    main()
