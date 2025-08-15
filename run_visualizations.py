#!/usr/bin/env python3
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
