#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fuzzy Datenquellen-Verteilung
Erstellt Visualisierung der Fuzzy-Matching-Verteilung nach Datenquellen

Autor: DHBW Projektarbeit
Datum: August 2025
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from unified_fuzzy_data import get_fuzzy_data, get_total_matches, get_method_totals

# Deutsche Schriftart und Stil
plt.style.use('seaborn-v0_8')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.unicode_minus'] = False

def create_fuzzy_datenquellen_verteilung():
    """Erstellt Datenquellen-Verteilungsdiagramm für Fuzzy-Matching"""
    
    # Einheitliche Fuzzy-Daten verwenden
    data = get_fuzzy_data()
    
    # CSV vs XML Aufteilung
    csv_fields = ['article_number', 'tec_doc_article_number', 'ean']
    xml_fields = ['SupplierPtNo', 'TradeNo', 'Brand']
    
    # Datenquellen-Totals berechnen
    csv_total = sum(sum(data[field].values()) for field in csv_fields)
    xml_total = sum(sum(data[field].values()) for field in xml_fields)
    
    # Methoden-Totals pro Quelle
    method_csv_totals = {}
    method_xml_totals = {}
    
    for method in ['Levenshtein', 'Jaro-Winkler', 'Probabilistisch', 'Phonetisch']:
        method_csv_totals[method] = sum(data[field].get(method, 0) for field in csv_fields)
        method_xml_totals[method] = sum(data[field].get(method, 0) for field in xml_fields)
    
    # Figure erstellen
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Fuzzy Matching - Datenquellen-Verteilung\n', 
                 fontsize=18, fontweight='bold', y=0.95)
    
    # 1. CSV vs XML Gesamtverteilung
    sources = ['CSV-Daten', 'XML-Daten']
    totals = [csv_total, xml_total]
    colors = ['#3498db', '#e74c3c']
    
    wedges, texts, autotexts = ax1.pie(totals, labels=sources, colors=colors, autopct='%1.1f%%',
                                      startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
    ax1.set_title('Gesamtverteilung: CSV vs XML', fontweight='bold', fontsize=14)
    
    # Werte in der Mitte anzeigen
    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    ax1.add_artist(centre_circle)
    ax1.text(0, 0, f'Gesamt:\n{csv_total + xml_total:,}\nMatches', 
             ha='center', va='center', fontsize=12, fontweight='bold')
    
    # 2. CSV-Methoden Verteilung
    methods = list(method_csv_totals.keys())
    csv_values = list(method_csv_totals.values())
    method_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    bars2 = ax2.bar(methods, csv_values, color=method_colors, alpha=0.8)
    ax2.set_title('CSV-Daten: Matches pro Fuzzy-Methode', fontweight='bold', fontsize=14)
    ax2.set_xlabel('Fuzzy-Methoden', fontweight='bold')
    ax2.set_ylabel('Anzahl Matches', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Werte auf Balken
    for bar, value in zip(bars2, csv_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
                f'{value:,}', ha='center', va='bottom', fontweight='bold')
    
    # 3. XML-Methoden Verteilung
    xml_values = list(method_xml_totals.values())
    
    bars3 = ax3.bar(methods, xml_values, color=method_colors, alpha=0.8)
    ax3.set_title('XML-Daten: Matches pro Fuzzy-Methode', fontweight='bold', fontsize=14)
    ax3.set_xlabel('Fuzzy-Methoden', fontweight='bold')
    ax3.set_ylabel('Anzahl Matches', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # Werte auf Balken
    for bar, value in zip(bars3, xml_values):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
                f'{value:,}', ha='center', va='bottom', fontweight='bold')
    
    # 4. Detaillierte Feld-Verteilung
    field_data = []
    field_labels = []
    field_colors = []
    
    # CSV Felder
    for field in csv_fields:
        total = sum(data[field].values())
        field_data.append(total)
        field_labels.append(f'{field}\n(CSV)')
        field_colors.append('#3498db')
    
    # XML Felder
    for field in xml_fields:
        total = sum(data[field].values())
        field_data.append(total)
        field_labels.append(f'{field}\n(XML)')
        field_colors.append('#e74c3c')
    
    bars4 = ax4.barh(range(len(field_labels)), field_data, color=field_colors, alpha=0.8)
    ax4.set_title('Matches pro Datenfeld', fontweight='bold', fontsize=14)
    ax4.set_xlabel('Anzahl Matches', fontweight='bold')
    ax4.set_yticks(range(len(field_labels)))
    ax4.set_yticklabels(field_labels)
    ax4.grid(True, alpha=0.3)
    
    # Werte anzeigen
    for bar, value in zip(bars4, field_data):
        ax4.text(value + 1000, bar.get_y() + bar.get_height()/2,
                f'{value:,}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    
    # Speichern
    plt.savefig('results/visualizations/fuzzy_datenquellen_verteilung.png', 
                dpi=300, bbox_inches='tight')
    plt.savefig('results/visualizations/fuzzy_datenquellen_verteilung.pdf', 
                bbox_inches='tight')
    
    print("✅ Fuzzy-Datenquellen-Verteilung erstellt!")
    
    # Zusammenfassung ausgeben
    print("\n" + "="*60)
    print("📊 FUZZY-DATENQUELLEN VERTEILUNG")
    print("="*60)
    print(f"🎯 CSV-Daten: {csv_total:,} Matches ({csv_total/(csv_total+xml_total)*100:.1f}%)")
    print(f"🎯 XML-Daten: {xml_total:,} Matches ({xml_total/(csv_total+xml_total)*100:.1f}%)")
    print(f"📈 Gesamt: {csv_total + xml_total:,} Matches")
    print("\n📋 CSV-Methoden:")
    for method, value in method_csv_totals.items():
        print(f"   • {method}: {value:,}")
    print("\n📋 XML-Methoden:")
    for method, value in method_xml_totals.items():
        print(f"   • {method}: {value:,}")
    print("="*60)
    
    return fig

def main():
    """Hauptfunktion"""
    print("🎨 Erstelle Fuzzy-Datenquellen-Verteilung...")
    create_fuzzy_datenquellen_verteilung()
    plt.show()

if __name__ == "__main__":
    main()
