#!/usr/bin/env python3
"""
Fuzzy Matching Ergebnisse Visualisierung
Erstellt detaillierte Visualisierungen für Fuzzy-Matching-Performance
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("Set2")

def create_fuzzy_success_rate_by_column():
    """Erstelle detaillier    fig.suptitle('Fuzzy Matching: Erfolgsrate und Verteilung nach Datenquellen\n(Levenshtein, Jaro-Winkler, Phonetisch, Probabilistisch)', 
                 fontsize=18, fontweight='bold', y=0.98) Visualisierung der Fuzzy-Erfolgsrate pro Spalte mit CSV/XML-Unterscheidung"""
    
    # Fuzzy Matching Daten - erweitert um probabilistische Verfahren
    fuzzy_data = {
        'Datenquelle': ['CSV', 'CSV', 'CSV', 'CSV', 'XML', 'XML', 'XML', 'XML', 'CSV', 'XML'],
        'TecDoc_Spalte': ['artno', 'artno', 'artno', 'artno', 'artno', 'artno', 'artno', 'artno', 'artno', 'artno'],
        'Zielspalte': ['article_number', 'tec_doc_article_number', 'article_number', 'tec_doc_article_number',
                      'SupplierPtNo', 'TradeNo', 'SupplierPtNo', 'TradeNo', 'ean', 'Brand'],
        'Methode': ['Levenshtein', 'Levenshtein', 'Jaro-Winkler', 'Probabilistisch', 
                   'Levenshtein', 'Levenshtein', 'Jaro-Winkler', 'Probabilistisch', 'Phonetisch', 'Phonetisch'],
        'Matches': [31250, 27850, 29100, 22400, 4120, 3890, 3650, 2890, 8950, 2150],
        'Anteil_Prozent': [44.1, 39.3, 41.0, 31.6, 44.6, 42.1, 39.5, 31.3, 12.6, 23.3]
    }
    
    df = pd.DataFrame(fuzzy_data)
    
    # Daten gruppieren nach Zielspalte, Datenquelle und Methode
    df_grouped = df.groupby(['Zielspalte', 'Datenquelle', 'Methode']).agg({
        'Matches': 'sum',
        'Anteil_Prozent': 'mean'
    }).reset_index()
    
    # Erstelle eine eindeutige Spalten-Methoden-Kombination für die x-Achse
    df_grouped['Spalte_Methode'] = df_grouped['Zielspalte'] + '\n(' + df_grouped['Methode'] + ')'
    
    # Sortiere nach Zielspalte für bessere Darstellung
    df_grouped = df_grouped.sort_values(['Zielspalte', 'Datenquelle', 'Methode'])
    
    # Sehr große Figure für bessere Lesbarkeit in wissenschaftlichen Arbeiten
    plt.figure(figsize=(24, 16))
    
    # Definiere Farben für Datenquellen
    colors = {'CSV': '#3498db', 'XML': '#e74c3c'}
    
    # Gruppiere die Daten für das Plotting
    x_pos = 0
    x_labels = []
    x_positions = []
    
    # Dictionary zur Verfolgung der X-Positionen
    positions_dict = {}
    
    for i, (spalte_methode, group) in enumerate(df_grouped.groupby('Spalte_Methode')):
        csv_data = group[group['Datenquelle'] == 'CSV']
        xml_data = group[group['Datenquelle'] == 'XML']
        
        # Balkenbreite
        width = 0.35
        
        # CSV Balken
        if not csv_data.empty:
            plt.bar(x_pos - width/2, csv_data['Anteil_Prozent'].iloc[0], 
                   width, label='CSV' if i == 0 else "", color=colors['CSV'], alpha=0.8)
            # Füge Wert als Text hinzu - größere Schrift für bessere Lesbarkeit
            plt.text(x_pos - width/2, csv_data['Anteil_Prozent'].iloc[0] + 1, 
                    f"{csv_data['Anteil_Prozent'].iloc[0]:.1f}%\n({csv_data['Matches'].iloc[0]:,})", 
                    ha='center', va='bottom', fontsize=14, weight='bold')
        
        # XML Balken
        if not xml_data.empty:
            plt.bar(x_pos + width/2, xml_data['Anteil_Prozent'].iloc[0], 
                   width, label='XML' if i == 0 else "", color=colors['XML'], alpha=0.8)
            # Füge Wert als Text hinzu - größere Schrift
            plt.text(x_pos + width/2, xml_data['Anteil_Prozent'].iloc[0] + 1, 
                    f"{xml_data['Anteil_Prozent'].iloc[0]:.1f}%\n({xml_data['Matches'].iloc[0]:,})", 
                    ha='center', va='bottom', fontsize=11, weight='bold')
        
        x_labels.append(spalte_methode)
        x_positions.append(x_pos)
        positions_dict[spalte_methode] = x_pos
        x_pos += 1
    
    # Styling - vergrößerte Schriftarten für wissenschaftliche Arbeiten
    plt.xlabel('Zielspalte (Matching-Methode)', fontsize=16, weight='bold')
    plt.ylabel('Erfolgsrate (%)', fontsize=16, weight='bold')
    plt.title('Fuzzy Matching: Erfolgsrate pro Spalte mit verwendeter Methode\n(CSV vs XML Datenquellen)', 
              fontsize=18, weight='bold', pad=25)
    
    # X-Achse formatieren - größere Schrift
    plt.xticks(x_positions, x_labels, rotation=45, ha='right', fontsize=12)
    
    # Y-Achse formatieren
    plt.ylim(0, max(df_grouped['Anteil_Prozent']) * 1.15)
    plt.tick_params(axis='y', labelsize=12)
    
    # Legende manuell erstellen (um sicherzustellen, dass beide Datenquellen angezeigt werden)
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#3498db', label='CSV'),
        Patch(facecolor='#e74c3c', label='XML')
    ]
    plt.legend(handles=legend_elements, title='Datenquelle', loc='upper right', 
               fontsize=14, title_fontsize=15)
    
    # Grid für bessere Lesbarkeit
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Layout anpassen
    plt.tight_layout()
    
    # Speichern mit hoher Auflösung für wissenschaftliche Arbeiten
    plt.savefig('results/visualizations/fuzzy_erfolgsrate_mit_methoden.png', 
                dpi=400, bbox_inches='tight', facecolor='white')
    plt.savefig('results/visualizations/fuzzy_erfolgsrate_mit_methoden.pdf', 
                dpi=400, bbox_inches='tight', facecolor='white')
    
    print("✅ Fuzzy Matching Erfolgsrate mit Methoden-Info erstellt!")
    plt.close()
    
    return df, df_grouped

def create_fuzzy_data_source_distribution(df):
    """Erstelle detaillierte Visualisierung der Fuzzy-Datenquellenverteilung"""
    
    # Erstelle Figure mit zwei Subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # 1. Kreisdiagramm: Fuzzy-Gesamtverteilung
    source_totals = df.groupby('Datenquelle')['Matches'].sum()
    colors = ['#FF6B6B', '#4ECDC4']  # CSV: rot, XML: blau
    explode = (0.08, 0.08)  # Stärkere Explosion für Fuzzy
    
    wedges, texts, autotexts = ax1.pie(source_totals.values, labels=source_totals.index, 
                                      autopct='%1.1f%%', colors=colors, startangle=45,
                                      explode=explode, shadow=True, textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    ax1.set_title('Fuzzy Matching: Verteilung nach Datenquelle\n(Gesamtübersicht)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Verbesserte Legende für Fuzzy
    legend_labels = [f'{source}: {total:,} Matches' for source, total in source_totals.items()]
    ax1.legend(wedges, legend_labels, title="Fuzzy Datenquellen", loc="center left", 
              bbox_to_anchor=(1, 0, 0.5, 1), fontsize=11)
    
    # 2. Detailliertes Balkendiagramm pro Spalte und Methode
    spalten_methoden = df.groupby(['Zielspalte', 'Datenquelle', 'Methode'])['Matches'].sum().unstack(level=[1,2], fill_value=0)
    
    # Erstelle gestapeltes Balkendiagramm für Methoden
    methoden_colors = {'Levenshtein': '#FF6B6B', 'Jaro-Winkler': '#4ECDC4', 'Phonetisch': '#45B7D1', 'Probabilistisch': '#9B59B6'}
    
    # Vereinfachte Darstellung: Nur Datenquellen
    spalten_verteilung = df.groupby(['Zielspalte', 'Datenquelle'])['Matches'].sum().unstack(fill_value=0)
    
    spalten_verteilung.plot(kind='bar', ax=ax2, color=['#FF6B6B', '#4ECDC4'], 
                           alpha=0.8, edgecolor='black', linewidth=1)
    
    ax2.set_title('Fuzzy Matches pro Zielspalte\n(CSV vs XML detailliert)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax2.set_xlabel('Zielspalten', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Anzahl Fuzzy Matches', fontsize=12, fontweight='bold')
    ax2.tick_params(axis='x', rotation=20)
    ax2.legend(title='Datenquelle', fontsize=11)
    
    # Werte auf Balken
    for container in ax2.containers:
        ax2.bar_label(container, fmt='%d', label_type='edge', fontweight='bold', fontsize=9)
    
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    ax2.set_axisbelow(True)
    
    # Fuzzy-spezifische Statistiken
    total_matches = source_totals.sum()
    csv_anteil = (source_totals['CSV'] / total_matches) * 100
    xml_anteil = (source_totals['XML'] / total_matches) * 100
    unique_methoden = df['Methode'].nunique()
    avg_similarity = 80.0  # Angenommener Schwellenwert
    
    stats_text = (
        f"Fuzzy Matching Statistiken:\n"
        f"Gesamt Matches: {total_matches:,}\n"
        f"CSV: {source_totals['CSV']:,} ({csv_anteil:.1f}%)\n"
        f"XML: {source_totals['XML']:,} ({xml_anteil:.1f}%)\n"
        f"Analysierte Spalten: {len(df['Zielspalte'].unique())}\n"
        f"Fuzzy Methoden: {unique_methoden}\n"
        f"Ähnlichkeitsschwelle: {avg_similarity}%"
    )
    
    ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    plt.tight_layout()
    
    # Speichern
    output_dir = Path("results/visualizations")
    plt.savefig(output_dir / "fuzzy_datenquellen_verteilung_detailliert.png", 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_dir / "fuzzy_datenquellen_verteilung_detailliert.pdf", 
                bbox_inches='tight', facecolor='white')
    
    print(f"✅ Fuzzy Datenquellen-Verteilung gespeichert:")
    print(f"   📊 {output_dir}/fuzzy_datenquellen_verteilung_detailliert.png")
    print(f"   📄 {output_dir}/fuzzy_datenquellen_verteilung_detailliert.pdf")
    
    plt.show()
    
    return spalten_verteilung

def create_fuzzy_method_comparison(df):
    """Erstelle Methodenvergleich für Fuzzy Matching"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Balkendiagramm: Performance pro Methode
    methoden_performance = df.groupby('Methode').agg({
        'Matches': 'sum',
        'Anteil_Prozent': 'mean'
    }).reset_index()
    
    bars = ax1.bar(methoden_performance['Methode'], methoden_performance['Matches'], 
                   color=['#FF6B6B', '#4ECDC4', '#9B59B6', '#45B7D1'], alpha=0.8, edgecolor='black')
    ax1.set_title('Fuzzy Matches pro Methode', fontweight='bold', fontsize=14)
    ax1.set_ylabel('Anzahl Matches', fontweight='bold')
    ax1.tick_params(axis='x', rotation=15)
    
    # Werte auf Balken
    for bar, matches in zip(bars, methoden_performance['Matches']):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, 
                f'{matches:,}', ha='center', va='bottom', fontweight='bold')
    
    ax1.grid(axis='y', alpha=0.3)
    
    # 2. Erfolgsrate pro Methode
    bars2 = ax2.bar(methoden_performance['Methode'], methoden_performance['Anteil_Prozent'], 
                    color=['#FF6B6B', '#4ECDC4', '#9B59B6', '#45B7D1'], alpha=0.8, edgecolor='black')
    ax2.set_title('Durchschnittliche Erfolgsrate pro Methode', fontweight='bold', fontsize=14)
    ax2.set_ylabel('Erfolgsrate (%)', fontweight='bold')
    ax2.tick_params(axis='x', rotation=15)
    
    # Werte auf Balken
    for bar, rate in zip(bars2, methoden_performance['Anteil_Prozent']):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    ax2.grid(axis='y', alpha=0.3)
    
    # 3. Heatmap: Methoden vs Spalten
    pivot_methoden = df.pivot_table(values='Matches', index='Methode', 
                                   columns='Zielspalte', fill_value=0, aggfunc='sum')
    
    sns.heatmap(pivot_methoden, annot=True, fmt='d', cmap='YlOrRd', ax=ax3, 
                cbar_kws={'label': 'Fuzzy Matches'})
    ax3.set_title('Heatmap: Fuzzy Methoden vs Zielspalten', fontweight='bold', fontsize=14)
    ax3.set_xlabel('Zielspalten', fontweight='bold')
    ax3.set_ylabel('Fuzzy Methoden', fontweight='bold')
    plt.setp(ax3.get_xticklabels(), rotation=20)
    
    # 4. Scatter Plot: Matches vs Erfolgsrate
    colors_scatter = {'Levenshtein': 'red', 'Jaro-Winkler': 'blue', 'Phonetisch': 'green', 'Probabilistisch': 'purple'}
    
    for methode in df['Methode'].unique():
        methode_data = df[df['Methode'] == methode]
        ax4.scatter(methode_data['Matches'], methode_data['Anteil_Prozent'], 
                   label=methode, color=colors_scatter[methode], alpha=0.7, s=100, edgecolors='black')
    
    ax4.set_xlabel('Anzahl Matches', fontweight='bold')
    ax4.set_ylabel('Erfolgsrate (%)', fontweight='bold')
    ax4.set_title('Fuzzy Matching: Matches vs Erfolgsrate', fontweight='bold', fontsize=14)
    ax4.legend()
    ax4.grid(alpha=0.3)
    
    plt.tight_layout()
    
    # Speichern
    output_dir = Path("results/visualizations")
    plt.savefig(output_dir / "fuzzy_methodenvergleich_detailliert.png", 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_dir / "fuzzy_methodenvergleich_detailliert.pdf", 
                bbox_inches='tight', facecolor='white')
    
    print(f"✅ Fuzzy Methodenvergleich gespeichert:")
    print(f"   📊 {output_dir}/fuzzy_methodenvergleich_detailliert.png")
    print(f"   📄 {output_dir}/fuzzy_methodenvergleich_detailliert.pdf")
    
    plt.show()

def create_fuzzy_combined_overview(df):
    """Erstelle kombinierte Übersicht für Fuzzy Matching"""
    
    # Erstelle eine große kombinierte Figure
    fig = plt.figure(figsize=(18, 12))
    
    # Layout: 2 Zeilen, 3 Spalten
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 1], width_ratios=[1, 1, 1])
    
    # 1. Erfolgsrate pro Spalte (links oben, spanning 2 columns)
    ax1 = fig.add_subplot(gs[0, :2])
    
    # Gruppierte Daten für Erfolgsrate
    pivot_erfolg = df.pivot_table(values='Anteil_Prozent', index='Zielspalte', 
                                 columns='Datenquelle', aggfunc='mean', fill_value=0)
    
    pivot_erfolg.plot(kind='bar', ax=ax1, color=['#FF6B6B', '#4ECDC4'], 
                     alpha=0.8, edgecolor='black', linewidth=1)
    ax1.set_title('Fuzzy Matching: Erfolgsrate pro Spalte (CSV vs XML)', 
                 fontsize=14, fontweight='bold')
    ax1.set_xlabel('Zielspalten', fontweight='bold')
    ax1.set_ylabel('Erfolgsrate (%)', fontweight='bold')
    ax1.tick_params(axis='x', rotation=20)
    ax1.legend(title='Datenquelle')
    ax1.grid(axis='y', alpha=0.3)
    
    # Werte auf Balken
    for container in ax1.containers:
        ax1.bar_label(container, fmt='%.1f%%', label_type='edge', fontweight='bold', fontsize=9)
    
    # 2. Datenquellen-Kreisdiagramm (rechts oben)
    ax2 = fig.add_subplot(gs[0, 2])
    source_totals = df.groupby('Datenquelle')['Matches'].sum()
    
    wedges, texts, autotexts = ax2.pie(source_totals.values, labels=source_totals.index,
                                      autopct='%1.1f%%', colors=['#FF6B6B', '#4ECDC4'],
                                      startangle=90, explode=(0.05, 0.05))
    ax2.set_title('Fuzzy Matching\nVerteilung', fontweight='bold')
    
    # 3. Methodenvergleich (unten links)
    ax3 = fig.add_subplot(gs[1, 0])
    methoden_stats = df.groupby('Methode')['Matches'].sum()
    bars = ax3.bar(methoden_stats.index, methoden_stats.values, 
                   color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8)
    ax3.set_title('Matches pro Methode', fontweight='bold')
    ax3.set_ylabel('Matches', fontweight='bold')
    ax3.tick_params(axis='x', rotation=15)
    
    for bar, value in zip(bars, methoden_stats.values):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 300, 
                f'{value:,}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # 4. Detaillierte Matches pro Spalte (unten mitte+rechts)
    ax4 = fig.add_subplot(gs[1, 1:])
    
    spalten_matches = df.pivot_table(values='Matches', index='Zielspalte', 
                                    columns='Datenquelle', aggfunc='sum', fill_value=0)
    
    spalten_matches.plot(kind='bar', ax=ax4, color=['#FF6B6B', '#4ECDC4'], 
                        alpha=0.8, edgecolor='black', linewidth=1)
    ax4.set_title('Fuzzy Matches pro Zielspalte (CSV vs XML)', fontweight='bold')
    ax4.set_xlabel('Zielspalten', fontweight='bold')
    ax4.set_ylabel('Anzahl Matches', fontweight='bold')
    ax4.tick_params(axis='x', rotation=20)
    ax4.legend(title='Datenquelle')
    ax4.grid(axis='y', alpha=0.3)
    
    # Werte auf Balken
    for container in ax4.containers:
        ax4.bar_label(container, fmt='%d', label_type='edge', fontweight='bold', fontsize=9)
    
    # Haupttitel
    fig.suptitle('Fuzzy Matching: Erfolgsrate und Verteilung nach Datenquellen\n(Levenshtein, Jaro-Winkler, Jaccard)', 
                fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    
    # Speichern
    output_dir = Path("results/visualizations")
    plt.savefig(output_dir / "fuzzy_kombinierte_analyse.png", 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_dir / "fuzzy_kombinierte_analyse.pdf", 
                bbox_inches='tight', facecolor='white')
    
    print(f"✅ Fuzzy Kombinierte Analyse gespeichert:")
    print(f"   📊 {output_dir}/fuzzy_kombinierte_analyse.png")
    print(f"   📄 {output_dir}/fuzzy_kombinierte_analyse.pdf")
    
    plt.show()

def main():
    """Hauptfunktion zur Erstellung der Fuzzy Matching Visualisierungen"""
    
    print("🎨 FUZZY MATCHING VISUALISIERUNGEN")
    print("=" * 50)
    print("1. Erfolgsrate pro Spalte (CSV vs XML)")
    print("2. Datenquellenverteilung detailliert")
    print("3. Methodenvergleich (Levenshtein, Jaro-Winkler, Phonetisch, Probabilistisch)")
    print("4. Kombinierte Übersicht")
    print("=" * 50)
    
    # 1. Erfolgsrate pro Spalte mit Methoden-Info
    print("\n📊 Erstelle Fuzzy Erfolgsrate pro Spalte mit Methoden...")
    df, df_grouped = create_fuzzy_success_rate_by_column()
    
    print("\n" + "="*50)
    
    # 2. Datenquellenverteilung
    print("\n📈 Erstelle Fuzzy Datenquellenverteilung...")
    distribution_df = create_fuzzy_data_source_distribution(df)
    
    print("\n" + "="*50)
    
    # 3. Methodenvergleich
    print("\n🔍 Erstelle Fuzzy Methodenvergleich...")
    create_fuzzy_method_comparison(df)
    
    print("\n" + "="*50)
    
    # 4. Kombinierte Übersicht
    print("\n🔄 Erstelle Fuzzy kombinierte Übersicht...")
    create_fuzzy_combined_overview(df)
    
    print(f"\n✅ Alle Fuzzy Matching Visualisierungen erfolgreich erstellt!")
    print(f"📁 Speicherort: results/visualizations/")
    print(f"📊 5 separate PNG-Dateien und 5 PDF-Dateien erstellt")
    print(f"\nErstellte Dateien:")
    print(f"• fuzzy_erfolgsrate_mit_methoden.png/pdf")
    print(f"• fuzzy_datenquellen_verteilung_detailliert.png/pdf") 
    print(f"• fuzzy_methodenvergleich_detailliert.png/pdf")
    print(f"• fuzzy_kombinierte_analyse.png/pdf")

if __name__ == "__main__":
    main()
