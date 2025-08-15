#!/usr/bin/env python3
"""
Repository Cleanup Script für DHBW Projektarbeit
Organisiert und bereinigt das Repository systematisch
"""

import os
import shutil
import glob
from pathlib import Path

def create_directory_structure():
    """Erstellt die saubere Verzeichnisstruktur"""

    base_dirs = [
    'scripts/core', # Hauptskripte
    'scripts/analysis', # Analyse-Skripte
    'scripts/visualization', # Visualisierung-Skripte
    'scripts/utilities', # Hilfsskripte
    'data/input', # Eingangsdaten (bereits vorhanden)
    'data/output', # Ausgangsdaten (bereits vorhanden)
    'results/tables', # Tabellen-Ergebnisse (bereits vorhanden)
    'results/visualizations', # Visualisierungen (bereits vorhanden)
    'archive/backup', # Archiv für alte Dateien
    'docs' # Dokumentation
    ]

    for directory in base_dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"[OK] Verzeichnis erstellt/geprüft: {directory}")

def cleanup_pycache():
    """Entfernt alle __pycache__ Verzeichnisse"""

    pycache_dirs = glob.glob('**/__pycache__', recursive=True)
    for cache_dir in pycache_dirs:
        try:
            shutil.rmtree(cache_dir)
            print(f"[OK] Entfernt: {cache_dir}")
            except Exception as e:
                print(f"[WARNING] Fehler beim Entfernen von {cache_dir}: {e}")

def organize_scripts():
    """Organisiert Python-Skripte in passende Verzeichnisse"""

    script_organization = {
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

    for target_dir, scripts in script_organization.items():
        for script in scripts:
            if os.path.exists(script):
                try:
                    shutil.move(script, os.path.join(target_dir, script))
                    print(f"[OK] Verschoben: {script} → {target_dir}")
                    except Exception as e:
                        print(f"[WARNING] Fehler beim Verschieben von {script}: {e}")

def archive_backup_content():
    """Archiviert den Inhalt des backup_old_scripts Ordners"""

    if os.path.exists('backup_old_scripts'):
        try:
 # Kopiere gesamten Backup-Ordner ins Archiv
            if os.path.exists('archive/backup/backup_old_scripts'):
                shutil.rmtree('archive/backup/backup_old_scripts')

                shutil.copytree('backup_old_scripts', 'archive/backup/backup_old_scripts')
                print("[OK] Backup-Ordner ins Archiv kopiert")

 # Entferne Original-Backup-Ordner
                shutil.rmtree('backup_old_scripts')
                print("[OK] Original backup_old_scripts entfernt")

                except Exception as e:
                    print(f"[WARNING] Fehler beim Archivieren: {e}")

def create_main_scripts():
    """Erstellt Haupt-Ausführungsskripte"""

 # Main Analysis Script
    main_analysis = '''#!/usr/bin/env python3
    """
    Haupt-Analyseskript für DHBW Projektarbeit
    Führt komplette Datenanalyse durch
    """

    import sys
    import os
    sys.path.append('scripts/core')
    sys.path.append('scripts/analysis')

def run_deterministic_analysis():
    """Führt deterministische Analyse durch"""
    try:
        from run_deterministic_analysis import main as det_main
        print(" Starte deterministische Analyse...")
        det_main()
        print("[OK] Deterministische Analyse abgeschlossen")
        except Exception as e:
            print(f"[ERROR] Fehler bei deterministischer Analyse: {e}")

def run_fuzzy_analysis():
    """Führt Fuzzy-Analyse durch"""
    try:
        from run_fuzzy_analysis import main as fuzzy_main
        print(" Starte Fuzzy-Analyse...")
        fuzzy_main()
        print("[OK] Fuzzy-Analyse abgeschlossen")
        except Exception as e:
            print(f"[ERROR] Fehler bei Fuzzy-Analyse: {e}")

def create_final_tables():
    """Erstellt finale Tabellen"""
    try:
        from create_final_tables import main as table_main
        print(" Erstelle finale Tabellen...")
        table_main()
        print("[OK] Finale Tabellen erstellt")
        except Exception as e:
            print(f"[ERROR] Fehler beim Erstellen der Tabellen: {e}")

            if __name__ == "__main__":
                print(" DHBW Projektarbeit - Hauptanalyse")
                print("=" * 50)

                run_deterministic_analysis()
                run_fuzzy_analysis()
                create_final_tables()

                print("=" * 50)
                print("[OK] Alle Analysen abgeschlossen!")
                '''

                with open('run_main_analysis.py', 'w', encoding='utf-8') as f:
                    f.write(main_analysis)
                    print("[OK] Erstellt: run_main_analysis.py")

 # Visualization Script
                    main_viz = '''#!/usr/bin/env python3
                    """
                    Haupt-Visualisierungsskript für DHBW Projektarbeit
                    Erstellt alle benötigten Visualisierungen
                    """

                    import sys
                    import os
                    sys.path.append('scripts/visualization')
                    sys.path.append('scripts/core')

def create_all_visualizations():
    """Erstellt alle Visualisierungen"""

    visualizations = [
    ('deterministic_results_visualization', 'Deterministische Ergebnisse'),
    ('fuzzy_visualisierungen', 'Fuzzy-Matching Übersicht'),
    ('fuzzy_erfolgsrate_a4_optimiert', 'A4-optimierte Erfolgsraten'),
    ('einzelne_visualisierungen', 'Einzelne Visualisierungen'),
    ('separate_method_visualizations', 'Methoden-spezifische Visualisierungen')
    ]

    for script_name, description in visualizations:
        try:
            module = __import__(script_name)
            if hasattr(module, 'main'):
                print(f" Erstelle: {description}")
                module.main()
                print(f"[OK] {description} erstellt")
                else:
                    print(f"[WARNING] Kein main() in {script_name}")
                    except Exception as e:
                        print(f"[ERROR] Fehler bei {description}: {e}")

                        if __name__ == "__main__":
                            print(" DHBW Projektarbeit - Visualisierungen")
                            print("=" * 50)

                            create_all_visualizations()

                            print("=" * 50)
                            print("[OK] Alle Visualisierungen erstellt!")
                            '''

                            with open('run_visualizations.py', 'w', encoding='utf-8') as f:
                                f.write(main_viz)
                                print("[OK] Erstellt: run_visualizations.py")

def update_gitignore():
    """Aktualisiert .gitignore für bessere Repository-Hygiene"""

    gitignore_content = '''# Python
    __pycache__/
    *.py[cod]
    *$py.class
    *.so
    .Python
    build/
    develop-eggs/
    dist/
    downloads/
    eggs/
    .eggs/
    lib/
    lib64/
    parts/
    sdist/
    var/
    wheels/
    share/python-wheels/
    *.egg-info/
    .installed.cfg
    *.egg
    MANIFEST

# PyInstaller
    *.manifest
    *.spec

# Unit test / coverage reports
    htmlcov/
    .tox/
    .nox/
    .coverage
    .coverage.*
    .cache
    nosetests.xml
    coverage.xml
    *.cover
    *.py,cover
    .hypothesis/
    .pytest_cache/
    cover/

# Jupyter Notebook
    .ipynb_checkpoints

# pyenv
    .python-version

# VS Code
    .vscode/
    *.code-workspace

# Data files (große Dateien)
    *.csv
    *.xlsx
    *.xml
    data/input/*
    !data/input/.gitkeep
    data/output/*
    !data/output/.gitkeep

# Temporary files
    *.tmp
    *.temp
    *.log

# OS
    .DS_Store
    Thumbs.db

# Archive (außer README)
    archive/
    !archive/README.md
    '''

    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
        print("[OK] .gitignore aktualisiert")

def create_readme():
    """Erstellt eine übersichtliche README.md"""

    readme_content = '''# CMD-TecDoc Datenanalyse - DHBW Projektarbeit

## Überblick
    Analyse und Matching von Fahrzeugteile-Daten zwischen CMD und TecDoc Datenquellen.

## Projektstruktur

### scripts/
    - **core/**: Kernfunktionalität und Hauptanalyse-Skripte
    - **analysis/**: Datenanalyse und Tabellenerstellung
    - **visualization/**: Alle Visualisierungsskripte
    - **utilities/**: Hilfsskripte und Utilities

### data/
    - **input/**: Eingangsdaten (CSV/XML Dateien)
    - **output/**: Verarbeitete Ausgangsdaten

### results/
    - **tables/**: Ergebnis-Tabellen (CSV/TXT)
    - **visualizations/**: Generierte Diagramme und Plots

### docs/
    - Dokumentation und Berichte

## Schnellstart

### Komplette Analyse ausführen:
    ```bash
    python run_main_analysis.py
    ```

### Nur Visualisierungen erstellen:
    ```bash
    python run_visualizations.py
    ```

### Einzelne Komponenten:
    ```bash
# Deterministische Analyse
    python scripts/core/run_deterministic_analysis.py

# Fuzzy-Matching Analyse 
    python scripts/core/run_fuzzy_analysis.py

# Spezifische Visualisierung
    python scripts/visualization/fuzzy_erfolgsrate_a4_optimiert.py
    ```

## Matching-Methoden

### Deterministische Methoden:
    - Exact Match
    - Substring Match
    - Prefix/Suffix Match
    - Numeric Exact Match
    - Length-based Match

### Fuzzy-Methoden:
    - Levenshtein Distance
    - Jaro-Winkler
    - Probabilistic Matching
    - Phonetic Matching

## Datenquellen
    - **CMD Business Cloud**: CSV-Format
    - **CMD Platform**: XML-Format
    - **TecDoc**: XML-Referenzdaten

## Abhängigkeiten
    ```bash
    pip install -r requirements.txt
    ```

## Projektergebnisse
    - **70.000** Datensätze analysiert
    - **66.702** deterministische Matches gefunden
    - **210.480** Fuzzy-Matches identifiziert
    - Multiple Visualisierungen für akademische Präsentation

## Autor
    DHBW Projektarbeit - Datenanalyse und Matching-Algorithmen
    '''

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
        print("[OK] README.md aktualisiert")

def create_gitkeep_files():
    """Erstellt .gitkeep Dateien für leere wichtige Verzeichnisse"""

    gitkeep_dirs = [
    'data/input',
    'data/output',
    'results/tables',
    'results/visualizations',
    'docs'
    ]

    for directory in gitkeep_dirs:
        gitkeep_path = os.path.join(directory, '.gitkeep')
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w') as f:
                f.write('')
                print(f"[OK] Erstellt: {gitkeep_path}")

def main():
    """Hauptfunktion für Repository-Cleanup"""

    print(" Repository Cleanup gestartet")
    print("=" * 50)

 # 1. Verzeichnisstruktur erstellen
    print("\n1. Erstelle saubere Verzeichnisstruktur...")
    create_directory_structure()

 # 2. Cache-Dateien entfernen
    print("\n2. Entferne Cache-Dateien...")
    cleanup_pycache()

 # 3. Skripte organisieren
    print("\n3. Organisiere Python-Skripte...")
    organize_scripts()

 # 4. Backup archivieren
    print("\n4. Archiviere Backup-Dateien...")
    archive_backup_content()

 # 5. Haupt-Skripte erstellen
    print("\n5. Erstelle Haupt-Ausführungsskripte...")
    create_main_scripts()

 # 6. .gitignore aktualisieren
    print("\n6. Aktualisiere .gitignore...")
    update_gitignore()

 # 7. README erstellen
    print("\n7. Erstelle neue README.md...")
    create_readme()

 # 8. .gitkeep Dateien erstellen
    print("\n8. Erstelle .gitkeep Dateien...")
    create_gitkeep_files()

    print("\n" + "=" * 50)
    print("[OK] Repository-Cleanup abgeschlossen!")
    print("\nNeue Struktur:")
    print(" scripts/ - Alle Python-Skripte organisiert")
    print(" data/ - Ein- und Ausgangsdaten")
    print(" results/ - Analyseergebnisse")
    print(" archive/ - Archivierte Backup-Dateien")
    print(" docs/ - Dokumentation")
    print(" run_main_analysis.py - Hauptanalyse ausführen")
    print(" run_visualizations.py - Alle Visualisierungen")
    print(" README.md - Projektdokumentation")

    if __name__ == "__main__":
        main()
