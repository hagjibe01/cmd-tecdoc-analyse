#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fuzzy Erfolgsrate A4-Optimiert
A4-Hochformat Visualisierung mit Erfolgsraten pro Stapel und verwendeten Methoden (einheitliche Werte)

Autor: DHBW Projektarbeit
Datum: August 2025
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from unified_fuzzy_data import get_fuzzy_data

# Deutsche Schriftart und A4-optimiert
plt.style.use('seaborn-v0_8')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.unicode_minus'] = False

def create_fuzzy_erfolgsrate_a4_optimiert():
    """Erstellt Balkendiagramm wie im Referenzbild mit CSV/XML Farbkodierung"""
    
    # Einheitliche Fuzzy-Daten verwenden
    data = get_fuzzy_data()
    total_records = 70000  # Für Prozentberechnung
    
    # Erfolgsraten für alle Felder berechnen
    all_results = []
    
    # CSV Felder
    csv_fields = ['article_number', 'tec_doc_article_number', 'ean']
    for field in csv_fields:
        for method, matches in data[field].items():
            success_rate = (matches / total_records) * 100
            all_results.append({
                'Label': f"{field}\n({method})",
                'Erfolgsrate_%': success_rate,
                'Matches': matches,
                'Quelle': 'CSV'
            })
    
    # XML Felder
    xml_fields = ['SupplierPtNo', 'TradeNo', 'Brand']
    for field in xml_fields:
        for method, matches in data[field].items():
            success_rate = (matches / total_records) * 100
            all_results.append({
                'Label': f"{field}\n({method})",
                'Erfolgsrate_%': success_rate,
                'Matches': matches,
                'Quelle': 'XML'
            })
    
    df = pd.DataFrame(all_results)
    
    # Figure noch größer für 30% Skalierung - muss sehr groß sein
    fig, ax = plt.subplots(1, 1, figsize=(20, 16))  # Sehr groß: 20x16 für 30% Skalierung
    fig.suptitle('Fuzzy Matching: Erfolgsrate pro Spalte mit verwendeter Methode\n(CSV vs XML Datenquellen)', 
                 fontsize=24, fontweight='bold', y=0.96)  # Sehr große Schrift
    
    # Nach Erfolgsrate sortieren
    df_sorted = df.sort_values('Erfolgsrate_%', ascending=True)
    
    # Schönere Farben mit Gradient-Effekt
    csv_color = '#2E86AB'  # Dunkleres Blau
    xml_color = '#A23B72'  # Dunkleres Rot/Magenta
    colors = [csv_color if row['Quelle'] == 'CSV' else xml_color 
              for _, row in df_sorted.iterrows()]
    
    # Horizontale Balken mit größerem Styling für Skalierung
    bars = ax.barh(range(len(df_sorted)), df_sorted['Erfolgsrate_%'], 
                   color=colors, alpha=0.85, height=0.85,  # Noch höhere Balken
                   edgecolor='white', linewidth=1.5)  # Dickere Ränder
    
    # Y-Achse Labels sehr groß für Skalierung
    labels = [label.replace('\n', ' + ') for label in df_sorted['Label']]
    ax.set_yticks(range(len(df_sorted)))
    ax.set_yticklabels(labels, fontsize=16)  # Sehr große Schrift für 30% Skalierung
    ax.set_xlabel('Erfolgsrate (%)', fontweight='bold', fontsize=18)  # Sehr große Schrift
    
    # Dickeres Grid für bessere Sichtbarkeit bei Skalierung
    ax.grid(True, alpha=0.3, axis='x', linestyle='--', linewidth=1.2)
    ax.set_axisbelow(True)
    
    # X-Achse begrenzen für bessere Proportionen und Text-Platz
    max_rate = max(df_sorted['Erfolgsrate_%'])
    ax.set_xlim(0, max_rate * 1.25)  # Mehr Platz für Text (25% statt 15%)
    
    # Kompaktere Werte-Anzeige mit besserer Positionierung
    for i, (bar, rate, matches) in enumerate(zip(bars, df_sorted['Erfolgsrate_%'], 
                                                 df_sorted['Matches'])):
        # Dynamische Text-Position: bei hohen Werten links vom Balken
        if rate > max_rate * 0.7:  # Wenn Balken sehr lang ist
            text_x = rate - 1
            ha_align = 'right'
        else:
            text_x = rate + 0.8
            ha_align = 'left'
            
        ax.text(text_x, bar.get_y() + bar.get_height()/2,
                f'{rate:.1f}%', ha=ha_align, va='center', 
                fontsize=14, fontweight='bold', color='black')  # Noch größere Schrift für 30% Skalierung
    
    # Legende sehr groß für Skalierung
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=csv_color, alpha=0.85, label='CSV-Daten'),
                      Patch(facecolor=xml_color, alpha=0.85, label='XML-Daten')]
    legend = ax.legend(handles=legend_elements, title='Datenquelle', 
                       loc='upper right', fontsize=16, title_fontsize=16,  # Sehr große Schrift
                       frameon=True, fancybox=True, shadow=True)
    # Rahmen der Legende dicker machen
    legend.get_frame().set_edgecolor('black')
    legend.get_frame().set_linewidth(1.5)
    
    # Entferne überflüssige Spines für cleanen Look - dickere Linien für Skalierung
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1.5)
    
    # Layout mit mehr Platz für große Schriften
    plt.tight_layout(rect=[0, 0, 1, 0.94])  # Noch mehr Platz oben
    
    # Speichern
    plt.savefig('results/visualizations/fuzzy_erfolgsrate_a4_optimiert.png', 
                dpi=300, bbox_inches='tight')
    plt.savefig('results/visualizations/fuzzy_erfolgsrate_a4_optimiert.pdf', 
                bbox_inches='tight')
    
    print("✅ Fuzzy-Erfolgsraten mit CSV/XML Farbkodierung erstellt!")
    
    # Statistiken
    best_result = df_sorted.iloc[-1]  # Letzter ist der beste (aufsteigend sortiert)
    total_matches = df['Matches'].sum()
    
    print("\n" + "="*70)
    print("📊 FUZZY-ERFOLGSRATEN (CSV/XML FARBKODIERT)")
    print("="*70)
    print(f"🎯 Gesamte Matches: {total_matches:,}")
    print(f"🏆 Beste Leistung: {best_result['Label'].replace(chr(10), ' + ')}")
    print(f"    └─ {best_result['Erfolgsrate_%']:.1f}% ({best_result['Matches']:,} Matches)")
    print(f"📊 Zeigt alle {len(df)} Feld-Methoden-Kombinationen")
    print("="*70)
    
    return fig

def main():
    """Hauptfunktion"""
    print("🎨 Erstelle skalierungsoptimierte Fuzzy-Erfolgsraten-Visualisierung (30% lesbar)...")
    create_fuzzy_erfolgsrate_a4_optimiert()
    plt.show()

if __name__ == "__main__":
    main()
