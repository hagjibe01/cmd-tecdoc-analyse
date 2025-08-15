#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Separate Method Visualizations
Erstellt zwei getrennte, klare Visualisierungen für deterministische und Fuzzy-Methoden

Autor: DHBW Projektarbeit
Datum: August 2025
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle

# Deutsche Schriftart und Stil
plt.style.use('seaborn-v0_8')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.unicode_minus'] = False

def create_deterministic_overview():
 """Erstellt ein einziges, klares Diagramm für deterministische Methoden"""

 # Deterministische Daten - alle Felder kombiniert
 all_fields_data = {
 'article_number': {'Substring': 15221, 'Suffix': 4890, 'Prefix': 3567, 'Exact': 2543},
 'tec_doc_article_number': {'Substring': 12001, 'Suffix': 5234, 'Prefix': 3766, 'Exact': 2000},
 'ean': {'Substring': 3890, 'Suffix': 1567, 'Prefix': 1433, 'Exact': 0},
 'manufacturer_number': {'Substring': 1200, 'Suffix': 562, 'Prefix': 200, 'Exact': 0},
 'SupplierPtNo': {'Substring': 2622, 'Suffix': 1200, 'Prefix': 600, 'Exact': 200},
 'TradeNo': {'Substring': 1822, 'Suffix': 700, 'Prefix': 400, 'Exact': 100},
 'Brand': {'Substring': 584, 'Suffix': 200, 'Prefix': 150, 'Exact': 50}
 }

 # Figure erstellen - nur ein Diagramm
 fig, ax = plt.subplots(1, 1, figsize=(12, 8))
 fig.suptitle('Deterministische Matching-Methoden - Übersicht\n', 
 fontsize=16, fontweight='bold', y=0.95)

 # Heatmap für alle Felder
 df = pd.DataFrame(all_fields_data).T
 sns.heatmap(df, annot=True, fmt='d', cmap='Blues', ax=ax, 
 cbar_kws={'label': 'Anzahl Matches'})
 ax.set_title('Matches pro Feld und Methode', fontweight='bold', fontsize=14)
 ax.set_xlabel('Deterministische Methoden', fontweight='bold')
 ax.set_ylabel('Datenfelder', fontweight='bold')

 plt.tight_layout()

 # Speichern
 plt.savefig('results/visualizations/deterministic_methods_overview.png', 
 dpi=300, bbox_inches='tight')
 plt.savefig('results/visualizations/deterministic_methods_overview.pdf', 
 bbox_inches='tight')

 print("[OK] Deterministische Methoden-Übersicht erstellt!")
 return fig

def create_fuzzy_overview():
 """Erstellt ein einziges, klares Diagramm für Fuzzy-Methoden"""

 # Fuzzy Daten - alle Felder kombiniert (aus unified_fuzzy_data.py)
 all_fields_data = {
 'article_number': {'Levenshtein': 31250, 'Jaro-Winkler': 29100, 'Probabilistisch': 22400, 'Phonetisch': 8950},
 'tec_doc_article_number': {'Levenshtein': 27850, 'Jaro-Winkler': 24200, 'Probabilistisch': 18650, 'Phonetisch': 7200},
 'ean': {'Levenshtein': 6850, 'Jaro-Winkler': 4200, 'Probabilistisch': 2100, 'Phonetisch': 950},
 'SupplierPtNo': {'Levenshtein': 4120, 'Jaro-Winkler': 3650, 'Probabilistisch': 2200, 'Phonetisch': 850},
 'TradeNo': {'Levenshtein': 3890, 'Jaro-Winkler': 3200, 'Probabilistisch': 2890, 'Phonetisch': 750},
 'Brand': {'Levenshtein': 2150, 'Jaro-Winkler': 1650, 'Probabilistisch': 980, 'Phonetisch': 450}
 }

 # Figure erstellen - nur ein Diagramm
 fig, ax = plt.subplots(1, 1, figsize=(12, 8))
 fig.suptitle('Fuzzy Matching-Methoden - Übersicht\n', 
 fontsize=16, fontweight='bold', y=0.95)

 # Heatmap für alle Felder
 df = pd.DataFrame(all_fields_data).T
 sns.heatmap(df, annot=True, fmt='d', cmap='Reds', ax=ax,
 cbar_kws={'label': 'Anzahl Matches'})
 ax.set_title('Matches pro Feld und Methode', fontweight='bold', fontsize=14)
 ax.set_xlabel('Fuzzy-Methoden', fontweight='bold')
 ax.set_ylabel('Datenfelder', fontweight='bold')

 plt.tight_layout()

 # Speichern
 plt.savefig('results/visualizations/fuzzy_methods_overview.png', 
 dpi=300, bbox_inches='tight')
 plt.savefig('results/visualizations/fuzzy_methods_overview.pdf', 
 bbox_inches='tight')

 print("[OK] Fuzzy Methoden-Übersicht erstellt!")
 return fig

def main():
 """Hauptfunktion zum Erstellen beider Übersichten"""
 print(" Erstelle getrennte Methoden-Übersichten...")

 # Deterministische Übersicht
 det_fig = create_deterministic_overview()

 # Fuzzy Übersicht 
 fuzzy_fig = create_fuzzy_overview()

 print("\n" + "="*60)
 print(" EINFACHE METHODEN-ÜBERSICHTEN ERSTELLT")
 print("="*60)
 print(" DETERMINISTISCH:")
 print(" • Ein Heatmap-Diagramm für alle Felder")
 print(" • Gesamt: 66,702 Matches über 4 Methoden")
 print(" • Beste Methode: Substring")
 print()
 print(" FUZZY:")
 print(" • Ein Heatmap-Diagramm für alle Felder") 
 print(" • Gesamt: 210,480 Matches über 4 Methoden")
 print(" • Beste Methode: Levenshtein")
 print()
 print(" Dateien gespeichert:")
 print(" • deterministic_methods_overview.png/pdf")
 print(" • fuzzy_methods_overview.png/pdf")
 print("="*60)

 plt.show()

if __name__ == "__main__":
 main()
