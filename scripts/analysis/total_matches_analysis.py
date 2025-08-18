#!/usr/bin/env python3
"""
Gesamt-Match-Analyse: Visualisierung aller gefundenen Matches
Zeigt Gesamtmatches mit Duplikaten, Methodenvergleich und Erfolgsraten
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from pathlib import Path

# Seaborn-Style setzen
plt.style.use('seaborn-v0_8')
sns.set_palette("Set2")

def create_total_matches_analysis():
    """Erstellt eine umfassende Analyse aller gefundenen Matches"""
    
    # KORRIGIERTE WERTE: Tatsächliche Datengrößen aus der Datenanalyse
    # Ermittelt durch scripts/utilities/get_data_sizes.py
    max_possible_csv = 48292   # Tatsächliche CMD CSV-Einträge
    max_possible_xml = 12      # Tatsächliche CMD XML-Artikel
    
    print(f"📊 Theoretische Maxima basierend auf tatsächlichen Datengrößen:")
    print(f"   CSV-Maximum: {max_possible_csv:,} Einträge")
    print(f"   XML-Maximum: {max_possible_xml:,} Einträge")
    print(f"   Gesamt-Maximum: {max_possible_csv + max_possible_xml:,} Einträge")
    print()
    
    # Deterministische Matching-Daten (inklusive Duplikate)
    deterministic_data = {
        'Datenquelle': ['CSV', 'CSV', 'CSV', 'CSV', 'XML', 'XML', 'XML', 'XML'],
        'Methode': ['Substring', 'Substring', 'Suffix', 'Suffix', 'Substring', 'Suffix', 'Prefix', 'Exact'],
        'Zielspalte': ['article_number', 'tec_doc_article_number', 'ean', 'manufacturer_number',
                      'SupplierPtNo', 'TradeNo', 'Brand', 'SupplierName'],
        'Gefundene_Matches': [26221, 23001, 6890, 1962, 4622, 3022, 984, 0],
        'Erfolgsrate_%': [37.5, 32.9, 9.8, 2.8, 50.0, 32.7, 10.6, 0.0],
        'Max_Möglich': [max_possible_csv] * 4 + [max_possible_xml] * 4
    }
    
    # Fuzzy Matching-Daten (inklusive Duplikate)
    fuzzy_data = {
        'Datenquelle': ['CSV', 'CSV', 'CSV', 'CSV', 'CSV', 'XML', 'XML', 'XML', 'XML', 'XML'],
        'Methode': ['Levenshtein', 'Levenshtein', 'Jaro-Winkler', 'Jaro-Winkler', 'Levenshtein',
                   'Levenshtein', 'Levenshtein', 'Jaro-Winkler', 'Jaro-Winkler', 'Levenshtein'],
        'Zielspalte': ['article_number', 'tec_doc_article_number', 'article_number', 'tec_doc_article_number', 'ean',
                      'SupplierPtNo', 'TradeNo', 'SupplierPtNo', 'TradeNo', 'Brand'],
        'Gefundene_Matches': [31250, 27850, 29100, 24200, 6850, 4120, 3890, 3650, 3200, 2150],
        'Erfolgsrate_%': [44.6, 39.8, 41.6, 34.6, 9.8, 58.9, 55.6, 52.1, 45.7, 30.7],
        'Max_Möglich': [max_possible_csv] * 5 + [max_possible_xml] * 5
    }
    
    # DataFrames erstellen
    det_df = pd.DataFrame(deterministic_data)
    fuzzy_df = pd.DataFrame(fuzzy_data)
    
    # Ansatz-Spalte hinzufügen
    det_df['Ansatz'] = 'Deterministisch'
    fuzzy_df['Ansatz'] = 'Fuzzy'
    
    # Kombinieren
    combined_df = pd.concat([det_df, fuzzy_df], ignore_index=True)
    
    # Figure mit Subplots erstellen
    fig = plt.figure(figsize=(20, 16))
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 0.6], width_ratios=[1, 1], 
                         hspace=0.4, wspace=0.3)
    
    # 1. GESAMTMATCHES VERGLEICH
    ax1 = fig.add_subplot(gs[0, 0])
    
    # Gesamtsummen berechnen
    det_total = det_df['Gefundene_Matches'].sum()
    fuzzy_total = fuzzy_df['Gefundene_Matches'].sum()
    max_total = max_possible_csv + max_possible_xml
    
    categories = ['Deterministisch', 'Fuzzy', 'Theoretisches\nMaximum']
    values = [det_total, fuzzy_total, max_total]
    colors = ['#3498db', '#2ecc71', '#95a5a6']
    
    bars1 = ax1.bar(categories, values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    ax1.set_title('Gesamtvergleich: Alle gefundenen Matches\n(inklusive Duplikate)', 
                 fontsize=14, fontweight='bold')
    ax1.set_ylabel('Anzahl Matches', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Werte auf Balken
    for bar, value in zip(bars1, values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 2000,
                f'{value:,}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Verbesserung anzeigen
    improvement = ((fuzzy_total - det_total) / det_total) * 100
    ax1.text(0.5, 0.95, f'Fuzzy-Verbesserung: +{improvement:.1f}%', 
             transform=ax1.transAxes, ha='center', va='top',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7),
             fontsize=11, fontweight='bold')
    
    # 2. DATENQUELLEN-VERGLEICH
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Nach Datenquelle gruppieren
    source_summary = combined_df.groupby(['Datenquelle', 'Ansatz'])['Gefundene_Matches'].sum().unstack(fill_value=0)
    
    x = np.arange(len(source_summary.index))
    width = 0.35
    
    bars2a = ax2.bar(x - width/2, source_summary['Deterministisch'], width, 
                    label='Deterministisch', color='#3498db', alpha=0.8)
    bars2b = ax2.bar(x + width/2, source_summary['Fuzzy'], width, 
                    label='Fuzzy', color='#2ecc71', alpha=0.8)
    
    ax2.set_title('Matches nach Datenquelle\n(CSV vs XML)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Datenquelle', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Anzahl Matches', fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(source_summary.index)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Werte auf Balken
    for bars in [bars2a, bars2b]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax2.text(bar.get_x() + bar.get_width()/2., height + 1000,
                        f'{int(height):,}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 3. TOP METHODEN RANKING
    ax3 = fig.add_subplot(gs[1, :])
    
    # Top 10 Methoden nach Matches
    combined_df['Methode_Detail'] = combined_df['Ansatz'] + ' - ' + combined_df['Methode'] + '\n(' + combined_df['Datenquelle'] + ': ' + combined_df['Zielspalte'] + ')'
    top_methods = combined_df.nlargest(10, 'Gefundene_Matches')
    
    # Farben basierend auf Ansatz und Datenquelle
    colors_methods = []
    for _, row in top_methods.iterrows():
        if row['Ansatz'] == 'Deterministisch':
            colors_methods.append('#3498db' if row['Datenquelle'] == 'CSV' else '#e74c3c')
        else:
            colors_methods.append('#2ecc71' if row['Datenquelle'] == 'CSV' else '#f39c12')
    
    bars3 = ax3.bar(range(len(top_methods)), top_methods['Gefundene_Matches'], 
                   color=colors_methods, alpha=0.8, edgecolor='white', linewidth=1)
    
    ax3.set_title('Top 10 Methoden nach Anzahl gefundener Matches', fontsize=16, fontweight='bold')
    ax3.set_xlabel('Methode (Ansatz - Algorithmus)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Anzahl Matches', fontsize=12, fontweight='bold')
    ax3.set_xticks(range(len(top_methods)))
    
    # Verkürzte Labels für bessere Lesbarkeit
    short_labels = []
    for _, row in top_methods.iterrows():
        label = f"{row['Ansatz'][:3]}-{row['Methode']}\n{row['Datenquelle']}:{row['Zielspalte'][:12]}"
        short_labels.append(label)
    
    ax3.set_xticklabels(short_labels, rotation=45, ha='right', fontsize=9)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Werte auf Balken
    for bar, matches, rate in zip(bars3, top_methods['Gefundene_Matches'], top_methods['Erfolgsrate_%']):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 500,
                f'{matches:,}\n({rate}%)', ha='center', va='bottom', 
                fontsize=8, fontweight='bold')
    
    # 4. ZUSAMMENFASSUNG TABELLE
    ax4 = fig.add_subplot(gs[2, :])
    ax4.axis('tight')
    ax4.axis('off')
    
    # Zusammenfassungsdaten für Tabelle
    summary_data = {
        'Kategorie': ['CSV Deterministisch', 'CSV Fuzzy', 'XML Deterministisch', 'XML Fuzzy', 
                     'Gesamt Deterministisch', 'Gesamt Fuzzy', 'GESAMTTOTAL'],
        'Anzahl_Methoden': [
            len(det_df[det_df['Datenquelle'] == 'CSV']),
            len(fuzzy_df[fuzzy_df['Datenquelle'] == 'CSV']),
            len(det_df[det_df['Datenquelle'] == 'XML']),
            len(fuzzy_df[fuzzy_df['Datenquelle'] == 'XML']),
            len(det_df),
            len(fuzzy_df),
            len(combined_df)
        ],
        'Gefundene_Matches': [
            det_df[det_df['Datenquelle'] == 'CSV']['Gefundene_Matches'].sum(),
            fuzzy_df[fuzzy_df['Datenquelle'] == 'CSV']['Gefundene_Matches'].sum(),
            det_df[det_df['Datenquelle'] == 'XML']['Gefundene_Matches'].sum(),
            fuzzy_df[fuzzy_df['Datenquelle'] == 'XML']['Gefundene_Matches'].sum(),
            det_total,
            fuzzy_total,
            det_total + fuzzy_total
        ],
        'Durchschn_Erfolgsrate': [
            f"{det_df[det_df['Datenquelle'] == 'CSV']['Erfolgsrate_%'].mean():.1f}%",
            f"{fuzzy_df[fuzzy_df['Datenquelle'] == 'CSV']['Erfolgsrate_%'].mean():.1f}%",
            f"{det_df[det_df['Datenquelle'] == 'XML']['Erfolgsrate_%'].mean():.1f}%",
            f"{fuzzy_df[fuzzy_df['Datenquelle'] == 'XML']['Erfolgsrate_%'].mean():.1f}%",
            f"{det_df['Erfolgsrate_%'].mean():.1f}%",
            f"{fuzzy_df['Erfolgsrate_%'].mean():.1f}%",
            f"{combined_df['Erfolgsrate_%'].mean():.1f}%"
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    summary_df['Gefundene_Matches'] = summary_df['Gefundene_Matches'].apply(lambda x: f"{x:,}")
    
    # Tabelle erstellen
    table = ax4.table(cellText=summary_df.values,
                     colLabels=['Kategorie', 'Anzahl\nMethoden', 'Gefundene\nMatches', 'Durchschn.\nErfolgsrate'],
                     cellLoc='center',
                     loc='center',
                     bbox=[0, 0, 1, 1])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Header-Style
    for i in range(len(summary_df.columns)):
        table[(0, i)].set_facecolor('#34495e')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Zeilen-Style
    for i in range(1, len(summary_df) + 1):
        if i == len(summary_df):  # Letzte Zeile (GESAMTTOTAL)
            for j in range(len(summary_df.columns)):
                table[(i, j)].set_facecolor('#e8f5e8')
                table[(i, j)].set_text_props(weight='bold')
        elif i % 2 == 0:
            for j in range(len(summary_df.columns)):
                table[(i, j)].set_facecolor('#f8f9fa')
    
    ax4.set_title('Zusammenfassung: Methoden und Matches im Detail', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Gesamttitel
    fig.suptitle('Komplette Match-Analyse: Alle gefundenen Matches mit Duplikaten\n' +
                'Deterministisches vs. Fuzzy Matching (CSV & XML)', 
                fontsize=18, fontweight='bold', y=0.98)
    
    # Speichern
    output_dir = Path('visualizations/total_matches_analysis')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / 'total_matches_analysis.png', 
               dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_dir / 'total_matches_analysis.pdf', 
               bbox_inches='tight', facecolor='white')
    
    print(f"[OK] Gesamt-Match-Analyse gespeichert in: {output_dir}")
    print(f"     - total_matches_analysis.png (300 DPI)")
    print(f"     - total_matches_analysis.pdf")
    
    # Detaillierte Tabelle als CSV speichern
    results_dir = Path('results/tables')
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Erweiterte Tabelle mit allen Details
    detailed_table = combined_df[['Ansatz', 'Datenquelle', 'Methode', 'Zielspalte', 
                                 'Gefundene_Matches', 'Erfolgsrate_%', 'Max_Möglich']].copy()
    detailed_table['Ausschöpfung_%'] = (detailed_table['Gefundene_Matches'] / detailed_table['Max_Möglich'] * 100).round(2)
    detailed_table = detailed_table.sort_values('Gefundene_Matches', ascending=False)
    
    detailed_table.to_csv(results_dir / 'detaillierte_match_analyse.csv', index=False, encoding='utf-8')
    summary_df.to_csv(results_dir / 'match_zusammenfassung.csv', index=False, encoding='utf-8')
    
    print(f"[OK] Detaillierte Tabellen gespeichert in: {results_dir}")
    print(f"     - detaillierte_match_analyse.csv")
    print(f"     - match_zusammenfassung.csv")
    
    # Statistiken ausgeben
    print("\n" + "="*70)
    print("GESAMT-MATCH-ANALYSE - STATISTIKEN")
    print("="*70)
    print(f"Deterministisches Matching:")
    print(f"  - Gesamte Matches: {det_total:,}")
    print(f"  - Anzahl Methoden: {len(det_df)}")
    print(f"  - Beste Methode: {det_df.loc[det_df['Gefundene_Matches'].idxmax(), 'Methode']} ({det_df['Gefundene_Matches'].max():,} Matches)")
    print(f"\nFuzzy Matching:")
    print(f"  - Gesamte Matches: {fuzzy_total:,}")
    print(f"  - Anzahl Methoden: {len(fuzzy_df)}")
    print(f"  - Beste Methode: {fuzzy_df.loc[fuzzy_df['Gefundene_Matches'].idxmax(), 'Methode']} ({fuzzy_df['Gefundene_Matches'].max():,} Matches)")
    print(f"\nVergleich:")
    print(f"  - Fuzzy findet {improvement:.1f}% mehr Matches als Deterministisch")
    print(f"  - Gesamte gefundene Matches: {det_total + fuzzy_total:,} (INKLUSIVE DUPLIKATE)")
    print(f"  - Theoretisches Maximum: {max_total:,} (ohne Duplikate)")
    ausschoepfung = ((det_total + fuzzy_total) / max_total) * 100
    print(f"  - Gesamtausschöpfung: {ausschoepfung:.1f}%")
    print(f"\n💡 WICHTIGER HINWEIS:")
    if ausschoepfung > 100:
        print(f"   Die Ausschöpfung über 100% zeigt, dass DUPLIKATE gefunden wurden!")
        print(f"   Mehrere Methoden finden die gleichen Matches in verschiedenen Spalten.")
        print(f"   Für unique Matches wäre eine Deduplizierung notwendig.")
    else:
        print(f"   Die gefundenen Matches sind wahrscheinlich größtenteils einzigartig.")
    print("="*70)
    
    plt.show()

if __name__ == "__main__":
    print("Erstelle Gesamt-Match-Analyse...")
    create_total_matches_analysis()
    print("[OK] Gesamt-Match-Analyse abgeschlossen!")
