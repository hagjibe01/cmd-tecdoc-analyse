#!/usr/bin/env python3
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
