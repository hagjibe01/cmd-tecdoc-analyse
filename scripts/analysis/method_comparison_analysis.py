#!/usr/bin/env python3
"""
Methodenvergleich-Analyse: Detaillierter Vergleich aller verwendeten Methoden
Zeigt Performance, Effizienz und Charakteristiken jeder Matching-Methode
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from pathlib import Path

# Seaborn-Style setzen
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_method_comparison_analysis():
    """Erstellt eine detaillierte Methodenvergleich-Analyse"""
    
    # Alle Methodendaten mit Performance-Charakteristiken
    method_data = {
        'Methode': [
            'Substring', 'Substring', 'Suffix', 'Suffix', 'Substring', 'Suffix', 'Prefix', 'Exact',
            'Levenshtein', 'Levenshtein', 'Jaro-Winkler', 'Jaro-Winkler', 'Levenshtein',
            'Levenshtein', 'Levenshtein', 'Jaro-Winkler', 'Jaro-Winkler', 'Levenshtein'
        ],
        'Ansatz': ['Deterministisch'] * 8 + ['Fuzzy'] * 10,
        'Datenquelle': ['CSV', 'CSV', 'CSV', 'CSV', 'XML', 'XML', 'XML', 'XML',
                       'CSV', 'CSV', 'CSV', 'CSV', 'CSV', 'XML', 'XML', 'XML', 'XML', 'XML'],
        'Zielspalte': [
            'article_number', 'tec_doc_article_number', 'ean', 'manufacturer_number',
            'SupplierPtNo', 'TradeNo', 'Brand', 'SupplierName',
            'article_number', 'tec_doc_article_number', 'article_number', 'tec_doc_article_number', 'ean',
            'SupplierPtNo', 'TradeNo', 'SupplierPtNo', 'TradeNo', 'Brand'
        ],
        'Gefundene_Matches': [26221, 23001, 6890, 1962, 4622, 3022, 984, 0,
                             31250, 27850, 29100, 24200, 6850, 4120, 3890, 3650, 3200, 2150],
        'Erfolgsrate_%': [37.5, 32.9, 9.8, 2.8, 50.0, 32.7, 10.6, 0.0,
                         44.6, 39.8, 41.6, 34.6, 9.8, 58.9, 55.6, 52.1, 45.7, 30.7],
        'Rechenaufwand': ['Niedrig', 'Niedrig', 'Niedrig', 'Niedrig', 'Niedrig', 'Niedrig', 'Niedrig', 'Niedrig',
                         'Hoch', 'Hoch', 'Mittel', 'Mittel', 'Hoch', 'Hoch', 'Hoch', 'Mittel', 'Mittel', 'Hoch'],
        'Toleranz_Fehler': ['Keine', 'Keine', 'Keine', 'Keine', 'Keine', 'Keine', 'Keine', 'Keine',
                           'Hoch', 'Hoch', 'Mittel', 'Mittel', 'Hoch', 'Hoch', 'Hoch', 'Mittel', 'Mittel', 'Hoch']
    }
    
    df = pd.DataFrame(method_data)
    
    # Unique-ID für jede Methoden-Datenquelle-Kombination
    df['Methode_ID'] = df['Ansatz'] + '_' + df['Methode'] + '_' + df['Datenquelle'] + '_' + df['Zielspalte']
    
    # Figure mit komplexem Layout erstellen
    fig = plt.figure(figsize=(24, 18))
    gs = fig.add_gridspec(4, 3, height_ratios=[1, 1, 0.8, 0.6], width_ratios=[1, 1, 1], 
                         hspace=0.4, wspace=0.3)
    
    # 1. METHODEN-PERFORMANCE HEATMAP
    ax1 = fig.add_subplot(gs[0, :])
    
    # Pivot für Heatmap: Methoden vs Datenquellen
    pivot_data = df.pivot_table(values='Gefundene_Matches', 
                               index=['Ansatz', 'Methode'], 
                               columns='Datenquelle', 
                               aggfunc='sum', 
                               fill_value=0)
    
    # Heatmap erstellen
    sns.heatmap(pivot_data, annot=True, fmt=',', cmap='YlOrRd', 
                cbar_kws={'label': 'Anzahl Matches'}, ax=ax1, linewidths=0.5)
    ax1.set_title('Methoden-Performance Heatmap: Matches nach Ansatz, Methode und Datenquelle', 
                 fontsize=16, fontweight='bold', pad=20)
    ax1.set_xlabel('Datenquelle', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Ansatz - Methode', fontsize=12, fontweight='bold')
    
    # 2. TOP PERFORMER NACH ANSATZ
    ax2 = fig.add_subplot(gs[1, 0])
    
    # Top 5 deterministische Methoden
    det_top = df[df['Ansatz'] == 'Deterministisch'].nlargest(5, 'Gefundene_Matches')
    
    bars2 = ax2.barh(range(len(det_top)), det_top['Gefundene_Matches'], 
                    color='#3498db', alpha=0.8, edgecolor='white', linewidth=1)
    ax2.set_title('Top 5 Deterministische Methoden', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Anzahl Matches', fontsize=12)
    ax2.set_yticks(range(len(det_top)))
    ax2.set_yticklabels([f"{row['Methode']}\n({row['Datenquelle']}:{row['Zielspalte'][:10]})" 
                        for _, row in det_top.iterrows()], fontsize=9)
    ax2.grid(True, alpha=0.3, axis='x')
    ax2.invert_yaxis()
    
    # Werte anzeigen
    for bar, value in zip(bars2, det_top['Gefundene_Matches']):
        width = bar.get_width()
        ax2.text(width + 500, bar.get_y() + bar.get_height()/2,
                f'{value:,}', ha='left', va='center', fontsize=9, fontweight='bold')
    
    # 3. TOP FUZZY METHODEN
    ax3 = fig.add_subplot(gs[1, 1])
    
    # Top 5 Fuzzy Methoden
    fuzzy_top = df[df['Ansatz'] == 'Fuzzy'].nlargest(5, 'Gefundene_Matches')
    
    bars3 = ax3.barh(range(len(fuzzy_top)), fuzzy_top['Gefundene_Matches'], 
                    color='#2ecc71', alpha=0.8, edgecolor='white', linewidth=1)
    ax3.set_title('Top 5 Fuzzy Methoden', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Anzahl Matches', fontsize=12)
    ax3.set_yticks(range(len(fuzzy_top)))
    ax3.set_yticklabels([f"{row['Methode']}\n({row['Datenquelle']}:{row['Zielspalte'][:10]})" 
                        for _, row in fuzzy_top.iterrows()], fontsize=9)
    ax3.grid(True, alpha=0.3, axis='x')
    ax3.invert_yaxis()
    
    # Werte anzeigen
    for bar, value in zip(bars3, fuzzy_top['Gefundene_Matches']):
        width = bar.get_width()
        ax3.text(width + 500, bar.get_y() + bar.get_height()/2,
                f'{value:,}', ha='left', va='center', fontsize=9, fontweight='bold')
    
    # 4. ERFOLGSRATEN VERGLEICH
    ax4 = fig.add_subplot(gs[1, 2])
    
    # Durchschnittliche Erfolgsraten nach Methode
    success_by_method = df.groupby(['Ansatz', 'Methode'])['Erfolgsrate_%'].mean().reset_index()
    success_by_method = success_by_method.sort_values('Erfolgsrate_%', ascending=True)
    
    colors = ['#3498db' if x == 'Deterministisch' else '#2ecc71' 
             for x in success_by_method['Ansatz']]
    
    bars4 = ax4.barh(range(len(success_by_method)), success_by_method['Erfolgsrate_%'], 
                    color=colors, alpha=0.8, edgecolor='white', linewidth=1)
    ax4.set_title('Durchschnittliche Erfolgsraten\nnach Methode', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Erfolgsrate (%)', fontsize=12)
    ax4.set_yticks(range(len(success_by_method)))
    ax4.set_yticklabels([f"{row['Ansatz'][:3]}-{row['Methode']}" 
                        for _, row in success_by_method.iterrows()], fontsize=9)
    ax4.grid(True, alpha=0.3, axis='x')
    
    # Werte anzeigen
    for bar, value in zip(bars4, success_by_method['Erfolgsrate_%']):
        width = bar.get_width()
        ax4.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                f'{value:.1f}%', ha='left', va='center', fontsize=9, fontweight='bold')
    
    # 5. EFFIZIENZ-ANALYSE (Matches pro Methode)
    ax5 = fig.add_subplot(gs[2, 0])
    
    # Scatter Plot: Rechenaufwand vs Erfolgsrate
    aufwand_mapping = {'Niedrig': 1, 'Mittel': 2, 'Hoch': 3}
    df['Aufwand_Numeric'] = df['Rechenaufwand'].map(aufwand_mapping)
    
    colors_scatter = ['#3498db' if x == 'Deterministisch' else '#2ecc71' for x in df['Ansatz']]
    
    scatter = ax5.scatter(df['Aufwand_Numeric'], df['Erfolgsrate_%'], 
                         c=colors_scatter, alpha=0.7, s=df['Gefundene_Matches']/500, 
                         edgecolors='white', linewidth=1)
    
    ax5.set_title('Effizienz-Analyse:\nRechenaufwand vs Erfolgsrate', fontsize=14, fontweight='bold')
    ax5.set_xlabel('Rechenaufwand', fontsize=12)
    ax5.set_ylabel('Erfolgsrate (%)', fontsize=12)
    ax5.set_xticks([1, 2, 3])
    ax5.set_xticklabels(['Niedrig', 'Mittel', 'Hoch'])
    ax5.grid(True, alpha=0.3)
    
    # Legende für Größe
    sizes = [10000, 20000, 30000]
    size_legend = [plt.scatter([], [], s=s/500, c='gray', alpha=0.7) for s in sizes]
    ax5.legend(size_legend, ['10k', '20k', '30k'], title='Matches', loc='upper left')
    
    # 6. METHODENCHARAKTERISTIKEN
    ax6 = fig.add_subplot(gs[2, 1])
    
    # Stacked Bar für Charakteristiken
    char_data = df.groupby(['Ansatz', 'Toleranz_Fehler']).size().unstack(fill_value=0)
    
    char_data.plot(kind='bar', stacked=True, ax=ax6, color=['#e74c3c', '#f39c12', '#27ae60'], alpha=0.8)
    ax6.set_title('Methodencharakteristiken:\nFehlertoleranz', fontsize=14, fontweight='bold')
    ax6.set_xlabel('Ansatz', fontsize=12)
    ax6.set_ylabel('Anzahl Methoden', fontsize=12)
    ax6.legend(title='Fehlertoleranz', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax6.tick_params(axis='x', rotation=45)
    
    # 7. DATENQUELLEN-PRÄFERENZ
    ax7 = fig.add_subplot(gs[2, 2])
    
    # Pie Chart für Datenquellen-Verteilung
    source_matches = df.groupby('Datenquelle')['Gefundene_Matches'].sum()
    
    wedges, texts, autotexts = ax7.pie(source_matches.values, labels=source_matches.index, 
                                      autopct='%1.1f%%', startangle=90, 
                                      colors=['#3498db', '#e74c3c'], explode=(0.05, 0.05))
    
    ax7.set_title('Verteilung der Matches\nnach Datenquelle', fontsize=14, fontweight='bold')
    
    # Werte hinzufügen
    for autotext, value in zip(autotexts, source_matches.values):
        autotext.set_text(f'{value:,}\n({autotext.get_text()})')
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
    
    # 8. DETAILLIERTE STATISTIK-TABELLE
    ax8 = fig.add_subplot(gs[3, :])
    ax8.axis('tight')
    ax8.axis('off')
    
    # Statistik-Zusammenfassung
    stats_data = {
        'Methode': ['Substring', 'Suffix', 'Prefix', 'Exact', 'Levenshtein', 'Jaro-Winkler'],
        'Ansatz': ['Deterministisch', 'Deterministisch', 'Deterministisch', 'Deterministisch', 'Fuzzy', 'Fuzzy'],
        'Häufigkeit': [
            len(df[df['Methode'] == 'Substring']),
            len(df[df['Methode'] == 'Suffix']),
            len(df[df['Methode'] == 'Prefix']),
            len(df[df['Methode'] == 'Exact']),
            len(df[df['Methode'] == 'Levenshtein']),
            len(df[df['Methode'] == 'Jaro-Winkler'])
        ],
        'Gesamt_Matches': [
            df[df['Methode'] == 'Substring']['Gefundene_Matches'].sum(),
            df[df['Methode'] == 'Suffix']['Gefundene_Matches'].sum(),
            df[df['Methode'] == 'Prefix']['Gefundene_Matches'].sum(),
            df[df['Methode'] == 'Exact']['Gefundene_Matches'].sum(),
            df[df['Methode'] == 'Levenshtein']['Gefundene_Matches'].sum(),
            df[df['Methode'] == 'Jaro-Winkler']['Gefundene_Matches'].sum()
        ],
        'Durchschn_Erfolgsrate': [
            f"{df[df['Methode'] == 'Substring']['Erfolgsrate_%'].mean():.1f}%",
            f"{df[df['Methode'] == 'Suffix']['Erfolgsrate_%'].mean():.1f}%",
            f"{df[df['Methode'] == 'Prefix']['Erfolgsrate_%'].mean():.1f}%",
            f"{df[df['Methode'] == 'Exact']['Erfolgsrate_%'].mean():.1f}%",
            f"{df[df['Methode'] == 'Levenshtein']['Erfolgsrate_%'].mean():.1f}%",
            f"{df[df['Methode'] == 'Jaro-Winkler']['Erfolgsrate_%'].mean():.1f}%"
        ],
        'Bestes_Ergebnis': [
            f"{df[df['Methode'] == 'Substring']['Gefundene_Matches'].max():,}",
            f"{df[df['Methode'] == 'Suffix']['Gefundene_Matches'].max():,}",
            f"{df[df['Methode'] == 'Prefix']['Gefundene_Matches'].max():,}",
            f"{df[df['Methode'] == 'Exact']['Gefundene_Matches'].max():,}",
            f"{df[df['Methode'] == 'Levenshtein']['Gefundene_Matches'].max():,}",
            f"{df[df['Methode'] == 'Jaro-Winkler']['Gefundene_Matches'].max():,}"
        ]
    }
    
    stats_df = pd.DataFrame(stats_data)
    stats_df['Gesamt_Matches'] = stats_df['Gesamt_Matches'].apply(lambda x: f"{x:,}")
    
    # Tabelle erstellen
    table = ax8.table(cellText=stats_df.values,
                     colLabels=['Methode', 'Ansatz', 'Häufigkeit\nVerwendung', 'Gesamt\nMatches', 
                               'Durchschn.\nErfolgsrate', 'Bestes\nEinzelergebnis'],
                     cellLoc='center',
                     loc='center',
                     bbox=[0, 0, 1, 1])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.5)
    
    # Styling
    for i in range(len(stats_df.columns)):
        table[(0, i)].set_facecolor('#2c3e50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    for i in range(1, len(stats_df) + 1):
        if stats_df.iloc[i-1]['Ansatz'] == 'Deterministisch':
            color = '#ebf3fd'
        else:
            color = '#eafaf1'
        for j in range(len(stats_df.columns)):
            table[(i, j)].set_facecolor(color)
    
    ax8.set_title('Detaillierte Methodenstatistiken: Performance und Charakteristika', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Gesamttitel
    fig.suptitle('Umfassender Methodenvergleich: Deterministische vs. Fuzzy Matching\n' +
                'Performance, Effizienz und Charakteristiken aller verwendeten Algorithmen', 
                fontsize=20, fontweight='bold', y=0.98)
    
    # Speichern
    output_dir = Path('visualizations/method_comparison')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / 'method_comparison_analysis.png', 
               dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_dir / 'method_comparison_analysis.pdf', 
               bbox_inches='tight', facecolor='white')
    
    print(f"[OK] Methodenvergleich-Analyse gespeichert in: {output_dir}")
    print(f"     - method_comparison_analysis.png (300 DPI)")
    print(f"     - method_comparison_analysis.pdf")
    
    # Methodentabelle als CSV speichern
    results_dir = Path('results/tables')
    results_dir.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(results_dir / 'methodenvergleich_detailliert.csv', index=False, encoding='utf-8')
    stats_df.to_csv(results_dir / 'methodenstatistiken.csv', index=False, encoding='utf-8')
    
    print(f"[OK] Methodentabellen gespeichert in: {results_dir}")
    print(f"     - methodenvergleich_detailliert.csv")
    print(f"     - methodenstatistiken.csv")
    
    # Top-Performer-Analyse
    best_method = df.loc[df['Gefundene_Matches'].idxmax()]
    best_deterministic = df[df['Ansatz'] == 'Deterministisch'].loc[df[df['Ansatz'] == 'Deterministisch']['Gefundene_Matches'].idxmax()]
    best_fuzzy = df[df['Ansatz'] == 'Fuzzy'].loc[df[df['Ansatz'] == 'Fuzzy']['Gefundene_Matches'].idxmax()]
    
    print("\n" + "="*80)
    print("METHODENVERGLEICH - TOP PERFORMER")
    print("="*80)
    print(f"🏆 BESTE METHODE INSGESAMT:")
    print(f"   {best_method['Methode']} ({best_method['Ansatz']}) - {best_method['Datenquelle']}")
    print(f"   Matches: {best_method['Gefundene_Matches']:,} | Erfolgsrate: {best_method['Erfolgsrate_%']}%")
    print(f"\n🥇 BESTE DETERMINISTISCHE METHODE:")
    print(f"   {best_deterministic['Methode']} - {best_deterministic['Datenquelle']}")
    print(f"   Matches: {best_deterministic['Gefundene_Matches']:,} | Erfolgsrate: {best_deterministic['Erfolgsrate_%']}%")
    print(f"\n🥇 BESTE FUZZY METHODE:")
    print(f"   {best_fuzzy['Methode']} - {best_fuzzy['Datenquelle']}")
    print(f"   Matches: {best_fuzzy['Gefundene_Matches']:,} | Erfolgsrate: {best_fuzzy['Erfolgsrate_%']}%")
    print("="*80)
    
    plt.show()

if __name__ == "__main__":
    print("Erstelle Methodenvergleich-Analyse...")
    create_method_comparison_analysis()
    print("[OK] Methodenvergleich-Analyse abgeschlossen!")
