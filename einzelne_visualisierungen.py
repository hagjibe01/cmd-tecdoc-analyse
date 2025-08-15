#!/usr/bin/env python3
"""
Einzelne detaillierte Visualisierungen für Spalten-Erfolgsrate und Datenquellenverteilung
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("Set2")

def create_success_rate_by_column():
    """Erstelle detaillierte Visualisierung der Erfolgsrate pro Spalte mit CSV/XML-Unterscheidung"""
    
    # Daten aus der Tabelle
    data = {
        'Datenquelle': ['CSV', 'CSV', 'CSV', 'XML', 'XML', 'XML'],
        'TecDoc_Spalte': ['artno', 'artno', 'artno', 'artno', 'artno', 'artno'],
        'Zielspalte': ['article_number', 'tec_doc_article_number', 'article_number', 
                      'SupplierPtNo', 'TradeNo', 'SupplierPtNo'],
        'Methode': ['Substring', 'Substring', 'Suffix', 'Suffix', 'Suffix', 'Substring'],
        'Matches': [26221, 23001, 8852, 3043, 3022, 1563],
        'Anteil_Prozent': [37.0, 32.4, 12.5, 32.9, 32.7, 16.9]
    }
    
    df = pd.DataFrame(data)
    
    # Erstelle Figure für Erfolgsrate pro Spalte
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Gruppiere Daten nach Spalte und Datenquelle
    spalten_data = []
    
    for spalte in df['Zielspalte'].unique():
        spalte_df = df[df['Zielspalte'] == spalte]
        
        csv_data = spalte_df[spalte_df['Datenquelle'] == 'CSV']
        xml_data = spalte_df[spalte_df['Datenquelle'] == 'XML']
        
        # CSV-Daten
        if not csv_data.empty:
            spalten_data.append({
                'Spalte': spalte,
                'Datenquelle': 'CSV',
                'Erfolgsrate': csv_data['Anteil_Prozent'].mean(),
                'Matches': csv_data['Matches'].sum(),
                'Methoden': ', '.join(csv_data['Methode'].unique())
            })
        
        # XML-Daten
        if not xml_data.empty:
            spalten_data.append({
                'Spalte': spalte,
                'Datenquelle': 'XML',
                'Erfolgsrate': xml_data['Anteil_Prozent'].mean(),
                'Matches': xml_data['Matches'].sum(),
                'Methoden': ', '.join(xml_data['Methode'].unique())
            })
    
    result_df = pd.DataFrame(spalten_data)
    
    # Erstelle gruppiertes Balkendiagramm
    spalten = result_df['Spalte'].unique()
    x_pos = np.arange(len(spalten))
    width = 0.35
    
    csv_data = []
    xml_data = []
    csv_matches = []
    xml_matches = []
    
    for spalte in spalten:
        csv_row = result_df[(result_df['Spalte'] == spalte) & (result_df['Datenquelle'] == 'CSV')]
        xml_row = result_df[(result_df['Spalte'] == spalte) & (result_df['Datenquelle'] == 'XML')]
        
        csv_erfolg = csv_row['Erfolgsrate'].iloc[0] if not csv_row.empty else 0
        xml_erfolg = xml_row['Erfolgsrate'].iloc[0] if not xml_row.empty else 0
        
        csv_match = csv_row['Matches'].iloc[0] if not csv_row.empty else 0
        xml_match = xml_row['Matches'].iloc[0] if not xml_row.empty else 0
        
        csv_data.append(csv_erfolg)
        xml_data.append(xml_erfolg)
        csv_matches.append(csv_match)
        xml_matches.append(xml_match)
    
    # Erstelle Balken
    bars1 = ax.bar(x_pos - width/2, csv_data, width, label='CSV-Daten', 
                   color='#FF6B6B', alpha=0.8, edgecolor='black', linewidth=1)
    bars2 = ax.bar(x_pos + width/2, xml_data, width, label='XML-Daten', 
                   color='#4ECDC4', alpha=0.8, edgecolor='black', linewidth=1)
    
    # Beschriftung
    ax.set_xlabel('Zielspalten', fontsize=14, fontweight='bold')
    ax.set_ylabel('Durchschnittliche Erfolgsrate (%)', fontsize=14, fontweight='bold')
    ax.set_title('Durchschnittliche Erfolgsrate pro Spalte\n(CSV vs XML Datenquellen)', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(spalten, rotation=15, ha='right')
    
    # Legende
    legend = ax.legend(loc='upper right', fontsize=12)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_alpha(0.9)
    
    # Werte auf Balken hinzufügen
    for i, (bar1, bar2, csv_val, xml_val, csv_match, xml_match) in enumerate(zip(bars1, bars2, csv_data, xml_data, csv_matches, xml_matches)):
        # CSV Balken
        if csv_val > 0:
            ax.text(bar1.get_x() + bar1.get_width()/2, bar1.get_height() + 0.5, 
                   f'{csv_val:.1f}%\n({csv_match:,})', ha='center', va='bottom', 
                   fontweight='bold', fontsize=10)
        
        # XML Balken  
        if xml_val > 0:
            ax.text(bar2.get_x() + bar2.get_width()/2, bar2.get_height() + 0.5, 
                   f'{xml_val:.1f}%\n({xml_match:,})', ha='center', va='bottom', 
                   fontweight='bold', fontsize=10)
    
    # Grid für bessere Lesbarkeit
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Y-Achse bis zum Maximum + Puffer
    max_val = max(max(csv_data), max(xml_data))
    ax.set_ylim(0, max_val * 1.15)
    
    # Zusätzliche Informationen als Text
    info_text = (
        f"Analysierte Daten:\n"
        f"• CSV Gesamt: {sum(csv_matches):,} Matches\n"
        f"• XML Gesamt: {sum(xml_matches):,} Matches\n"
        f"• Methoden: Substring, Suffix"
    )
    
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=10,
           verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    plt.tight_layout()
    
    # Speichern
    output_dir = Path("results/visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / "erfolgsrate_pro_spalte_detailliert.png", 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_dir / "erfolgsrate_pro_spalte_detailliert.pdf", 
                bbox_inches='tight', facecolor='white')
    
    print(f"✅ Erfolgsrate-Visualisierung gespeichert:")
    print(f"   📊 {output_dir}/erfolgsrate_pro_spalte_detailliert.png")
    print(f"   📄 {output_dir}/erfolgsrate_pro_spalte_detailliert.pdf")
    
    plt.show()
    
    return result_df

def create_data_source_distribution():
    """Erstelle detaillierte Visualisierung der Datenquellenverteilung"""
    
    # Daten für Verteilung
    data = {
        'Datenquelle': ['CSV', 'CSV', 'CSV', 'XML', 'XML', 'XML'],
        'Zielspalte': ['article_number', 'tec_doc_article_number', 'article_number', 
                      'SupplierPtNo', 'TradeNo', 'SupplierPtNo'],
        'Methode': ['Substring', 'Substring', 'Suffix', 'Suffix', 'Suffix', 'Substring'],
        'Matches': [26221, 23001, 8852, 3043, 3022, 1563],
        'Anteil_Prozent': [37.0, 32.4, 12.5, 32.9, 32.7, 16.9]
    }
    
    df = pd.DataFrame(data)
    
    # Erstelle Figure mit zwei Subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # 1. Kreisdiagramm: Gesamtverteilung
    source_totals = df.groupby('Datenquelle')['Matches'].sum()
    colors = ['#FF6B6B', '#4ECDC4']  # CSV: rot, XML: blau
    explode = (0.05, 0.05)  # Leichte Explosion
    
    wedges, texts, autotexts = ax1.pie(source_totals.values, labels=source_totals.index, 
                                      autopct='%1.1f%%', colors=colors, startangle=90,
                                      explode=explode, shadow=True, textprops={'fontsize': 12})
    
    ax1.set_title('Verteilung der Matches nach Datenquelle\n(Gesamtübersicht)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Zusätzliche Informationen zum Kreisdiagramm
    legend_labels = [f'{source}: {total:,} Matches' for source, total in source_totals.items()]
    ax1.legend(wedges, legend_labels, title="Datenquellen", loc="center left", 
              bbox_to_anchor=(1, 0, 0.5, 1), fontsize=11)
    
    # 2. Detailliertes Balkendiagramm pro Spalte
    spalten_verteilung = df.groupby(['Zielspalte', 'Datenquelle'])['Matches'].sum().unstack(fill_value=0)
    
    spalten_verteilung.plot(kind='bar', ax=ax2, color=['#FF6B6B', '#4ECDC4'], 
                           alpha=0.8, edgecolor='black', linewidth=1)
    
    ax2.set_title('Matches pro Zielspalte\n(CSV vs XML detailliert)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax2.set_xlabel('Zielspalten', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Anzahl Matches', fontsize=12, fontweight='bold')
    ax2.tick_params(axis='x', rotation=15)
    ax2.legend(title='Datenquelle', fontsize=11)
    
    # Werte auf Balken
    for container in ax2.containers:
        ax2.bar_label(container, fmt='%d', label_type='edge', fontweight='bold', fontsize=10)
    
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    ax2.set_axisbelow(True)
    
    # Statistiken als Textbox
    total_matches = source_totals.sum()
    csv_anteil = (source_totals['CSV'] / total_matches) * 100
    xml_anteil = (source_totals['XML'] / total_matches) * 100
    
    stats_text = (
        f"Statistiken:\n"
        f"Gesamt Matches: {total_matches:,}\n"
        f"CSV: {source_totals['CSV']:,} ({csv_anteil:.1f}%)\n"
        f"XML: {source_totals['XML']:,} ({xml_anteil:.1f}%)\n"
        f"Anzahl Spalten: {len(df['Zielspalte'].unique())}\n"
        f"Methoden: {len(df['Methode'].unique())}"
    )
    
    ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    
    # Speichern
    output_dir = Path("results/visualizations")
    plt.savefig(output_dir / "datenquellen_verteilung_detailliert.png", 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_dir / "datenquellen_verteilung_detailliert.pdf", 
                bbox_inches='tight', facecolor='white')
    
    print(f"✅ Datenquellen-Verteilung gespeichert:")
    print(f"   📊 {output_dir}/datenquellen_verteilung_detailliert.png")
    print(f"   📄 {output_dir}/datenquellen_verteilung_detailliert.pdf")
    
    plt.show()
    
    return spalten_verteilung

def create_combined_overview():
    """Erstelle eine kombinierte Übersicht beider Visualisierungen"""
    
    data = {
        'Datenquelle': ['CSV', 'CSV', 'CSV', 'XML', 'XML', 'XML'],
        'Zielspalte': ['article_number', 'tec_doc_article_number', 'article_number', 
                      'SupplierPtNo', 'TradeNo', 'SupplierPtNo'],
        'Methode': ['Substring', 'Substring', 'Suffix', 'Suffix', 'Suffix', 'Substring'],
        'Matches': [26221, 23001, 8852, 3043, 3022, 1563],
        'Anteil_Prozent': [37.0, 32.4, 12.5, 32.9, 32.7, 16.9]
    }
    
    df = pd.DataFrame(data)
    
    # Erstelle eine große kombinierte Figure
    fig = plt.figure(figsize=(18, 10))
    
    # Layout: 2 Zeilen, 3 Spalten
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 1], width_ratios=[1, 1, 1])
    
    # 1. Erfolgsrate pro Spalte (links oben, spanning 2 columns)
    ax1 = fig.add_subplot(gs[0, :2])
    
    # Gruppierte Daten für Erfolgsrate
    pivot_erfolg = df.pivot_table(values='Anteil_Prozent', index='Zielspalte', 
                                 columns='Datenquelle', aggfunc='mean', fill_value=0)
    
    pivot_erfolg.plot(kind='bar', ax=ax1, color=['#FF6B6B', '#4ECDC4'], 
                     alpha=0.8, edgecolor='black', linewidth=1)
    ax1.set_title('Durchschnittliche Erfolgsrate pro Spalte (CSV vs XML)', 
                 fontsize=14, fontweight='bold')
    ax1.set_xlabel('Zielspalten', fontweight='bold')
    ax1.set_ylabel('Erfolgsrate (%)', fontweight='bold')
    ax1.tick_params(axis='x', rotation=15)
    ax1.legend(title='Datenquelle')
    ax1.grid(axis='y', alpha=0.3)
    
    # Werte auf Balken
    for container in ax1.containers:
        ax1.bar_label(container, fmt='%.1f%%', label_type='edge', fontweight='bold')
    
    # 2. Datenquellen-Kreisdiagramm (rechts oben)
    ax2 = fig.add_subplot(gs[0, 2])
    source_totals = df.groupby('Datenquelle')['Matches'].sum()
    
    wedges, texts, autotexts = ax2.pie(source_totals.values, labels=source_totals.index,
                                      autopct='%1.1f%%', colors=['#FF6B6B', '#4ECDC4'],
                                      startangle=90, explode=(0.05, 0.05))
    ax2.set_title('Verteilung nach\nDatenquelle', fontweight='bold')
    
    # 3. Detaillierte Matches pro Spalte (unten, spanning all columns)
    ax3 = fig.add_subplot(gs[1, :])
    
    spalten_matches = df.pivot_table(values='Matches', index='Zielspalte', 
                                    columns='Datenquelle', aggfunc='sum', fill_value=0)
    
    spalten_matches.plot(kind='bar', ax=ax3, color=['#FF6B6B', '#4ECDC4'], 
                        alpha=0.8, edgecolor='black', linewidth=1)
    ax3.set_title('Anzahl Matches pro Zielspalte (CSV vs XML)', fontweight='bold', fontsize=14)
    ax3.set_xlabel('Zielspalten', fontweight='bold')
    ax3.set_ylabel('Anzahl Matches', fontweight='bold')
    ax3.tick_params(axis='x', rotation=15)
    ax3.legend(title='Datenquelle')
    ax3.grid(axis='y', alpha=0.3)
    
    # Werte auf Balken
    for container in ax3.containers:
        ax3.bar_label(container, fmt='%d', label_type='edge', fontweight='bold')
    
    # Haupttitel
    fig.suptitle('TecDoc-CMD Matching: Erfolgsrate und Verteilung nach Datenquellen', 
                fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    
    # Speichern
    output_dir = Path("results/visualizations")
    plt.savefig(output_dir / "kombinierte_spalten_datenquellen_analyse.png", 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_dir / "kombinierte_spalten_datenquellen_analyse.pdf", 
                bbox_inches='tight', facecolor='white')
    
    print(f"✅ Kombinierte Analyse gespeichert:")
    print(f"   📊 {output_dir}/kombinierte_spalten_datenquellen_analyse.png")
    print(f"   📄 {output_dir}/kombinierte_spalten_datenquellen_analyse.pdf")
    
    plt.show()

def main():
    """Hauptfunktion zur Erstellung der einzelnen detaillierten Visualisierungen"""
    
    print("🎨 EINZELNE DETAILLIERTE VISUALISIERUNGEN")
    print("=" * 50)
    print("1. Erfolgsrate pro Spalte (CSV vs XML)")
    print("2. Datenquellenverteilung detailliert")
    print("3. Kombinierte Übersicht")
    print("=" * 50)
    
    # 1. Erfolgsrate pro Spalte
    print("\n📊 Erstelle Erfolgsrate pro Spalte...")
    result_df = create_success_rate_by_column()
    
    print("\n" + "="*50)
    
    # 2. Datenquellenverteilung
    print("\n📈 Erstelle Datenquellenverteilung...")
    distribution_df = create_data_source_distribution()
    
    print("\n" + "="*50)
    
    # 3. Kombinierte Übersicht
    print("\n🔄 Erstelle kombinierte Übersicht...")
    create_combined_overview()
    
    print(f"\n✅ Alle einzelnen Visualisierungen erfolgreich erstellt!")
    print(f"📁 Speicherort: results/visualizations/")
    print(f"📊 3 separate PNG-Dateien und 3 PDF-Dateien erstellt")
    print(f"\nErstellte Dateien:")
    print(f"• erfolgsrate_pro_spalte_detailliert.png/pdf")
    print(f"• datenquellen_verteilung_detailliert.png/pdf") 
    print(f"• kombinierte_spalten_datenquellen_analyse.png/pdf")

if __name__ == "__main__":
    main()
