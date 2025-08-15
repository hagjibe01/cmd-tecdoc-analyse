#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fuzzy Datenquellen-Verteilung Detailliert
Detaillierte Visualisierung mit Kreisdiagramm (wie original) aber mit einheitlichen Werten

Autor: DHBW Projektarbeit
Datum: August 2025
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from unified_fuzzy_data import get_fuzzy_data

# Deutsche Schriftart und Stil
plt.style.use('seaborn-v0_8')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.unicode_minus'] = False

def create_fuzzy_datenquellen_verteilung_detailliert():
 """Erstellt Kreisdiagramm für Fuzzy-Datenquellen-Verteilung mit Legende"""

 # Einheitliche Fuzzy-Daten verwenden
 data = get_fuzzy_data()

 # CSV vs XML Aufteilung
 csv_fields = ['article_number', 'tec_doc_article_number', 'ean']
 xml_fields = ['SupplierPtNo', 'TradeNo', 'Brand']

 # Datenquellen-Totals berechnen
 csv_total = sum(sum(data[field].values()) for field in csv_fields)
 xml_total = sum(sum(data[field].values()) for field in xml_fields)

 # Figure mit dem Design aus dem Bild
 fig, ax = plt.subplots(1, 1, figsize=(12, 8))
 fig.suptitle('Fuzzy Matching: Verteilung nach Datenquelle\n(Gesamtübersicht)', 
 fontsize=16, fontweight='bold', y=0.95)

 # Kreisdiagramm mit Schatten wie im Bild
 labels = ['CSV', 'XML']
 sizes = [csv_total, xml_total]
 colors = ['#ff6b6b', '#4ecdc4'] # Rot und Türkis wie im Bild
 explode = (0.05, 0.05) # Leichte Trennung

 wedges, texts, autotexts = ax.pie(sizes, labels=None, colors=colors, 
 autopct='%1.1f%%', startangle=45,
 explode=explode, shadow=True,
 textprops={'fontsize': 12, 'fontweight': 'bold'})

 # Legende rechts erstellen wie im Bild
 legend_labels = [f'CSV: {csv_total:,} Matches', f'XML: {xml_total:,} Matches']
 ax.legend(wedges, legend_labels, title="Fuzzy Datenquellen", 
 loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
 fontsize=11, title_fontsize=12)

 ax.set_title('') # Kein zusätzlicher Titel

 plt.tight_layout()

 # Speichern
 plt.savefig('results/visualizations/fuzzy_datenquellen_verteilung_detailliert.png', 
 dpi=300, bbox_inches='tight')
 plt.savefig('results/visualizations/fuzzy_datenquellen_verteilung_detailliert.pdf', 
 bbox_inches='tight')

 print("[OK] Fuzzy-Datenquellen-Verteilung mit Legende erstellt!")

 # Zusammenfassung ausgeben
 print("\n" + "="*70)
 print(" FUZZY-DATENQUELLEN VERTEILUNG (MIT LEGENDE)")
 print("="*70)
 print(f" CSV-Daten: {csv_total:,} Matches ({csv_total/(csv_total+xml_total)*100:.1f}%)")
 print(f" XML-Daten: {xml_total:,} Matches ({xml_total/(csv_total+xml_total)*100:.1f}%)")
 print(f" Gesamt: {csv_total + xml_total:,} Matches")
 print("="*70)

 return fig

def main():
 """Hauptfunktion"""
 print(" Erstelle Fuzzy-Datenquellen-Verteilung mit Legende wie im Referenzbild...")
 create_fuzzy_datenquellen_verteilung_detailliert()
 plt.show()

if __name__ == "__main__":
 main()
