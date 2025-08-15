#!/usr/bin/env python3
"""
Deterministische Matching Ergebnisse Visualisierung
Erstellt umfassende Visualisierungen der Matching-Performance basierend auf den tatsächlichen Ergebnissen
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_deterministic_results_visualization():
    """Erstelle Visualisierung der deterministischen Matching-Ergebnisse"""
    
    # Daten aus der bereitgestellten Tabelle
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
    
    # Erstelle umfassende Visualisierung
    fig = plt.figure(figsize=(20, 16))
    
    # 1. Balkendiagramm: Matches pro Spalten-Kombination (horizontal)
    ax1 = plt.subplot(2, 3, 1)
    df_sorted = df.sort_values('Matches', ascending=True)
    colors = ['#FF6B6B' if x == 'CSV' else '#4ECDC4' for x in df_sorted['Datenquelle']]
    
    bars = ax1.barh(range(len(df_sorted)), df_sorted['Matches'], color=colors)
    ax1.set_yticks(range(len(df_sorted)))
    ax1.set_yticklabels([f"{row['Zielspalte']}\n({row['Datenquelle']}-{row['Methode']})" 
                        for _, row in df_sorted.iterrows()], fontsize=10)
    ax1.set_xlabel('Anzahl Matches', fontsize=12, fontweight='bold')
    ax1.set_title('📊 Matches pro Spalten-Kombination', fontsize=14, fontweight='bold', pad=20)
    
    # Werte auf Balken hinzufügen
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax1.text(width + 300, bar.get_y() + bar.get_height()/2, 
                f'{int(width):,}', ha='left', va='center', fontweight='bold')
    
    ax1.grid(axis='x', alpha=0.3)
    
    # 2. Kreisdiagramm: Verteilung nach Datenquelle
    ax2 = plt.subplot(2, 3, 2)
    source_totals = df.groupby('Datenquelle')['Matches'].sum()
    colors_pie = ['#4ECDC4', '#FF6B6B']  # XML zuerst (blau), dann CSV (rot)
    explode = (0.05, 0.05)  # Leichte Explosion für bessere Sichtbarkeit
    
    wedges, texts, autotexts = ax2.pie(source_totals.values, labels=source_totals.index, 
                                      autopct='%1.1f%%', colors=colors_pie, startangle=90,
                                      explode=explode, shadow=True)
    ax2.set_title('📈 Verteilung nach Datenquelle', fontsize=14, fontweight='bold', pad=20)
    
    # Verbesserte Legende mit absoluten Zahlen
    legend_labels = [f'{source}: {total:,} Matches' for source, total in source_totals.items()]
    ax2.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    # 3. Heatmap: Methoden vs Zielspalten
    ax3 = plt.subplot(2, 3, 3)
    pivot_matches = df.pivot_table(values='Matches', index='Methode', 
                                  columns='Zielspalte', fill_value=0, aggfunc='sum')
    
    sns.heatmap(pivot_matches, annot=True, fmt='d', cmap='Reds', ax=ax3, 
                cbar_kws={'label': 'Anzahl Matches'})
    ax3.set_title('🔥 Heatmap: Methoden vs Zielspalten', fontsize=14, fontweight='bold', pad=20)
    ax3.set_xlabel('Zielspalten', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Matching-Methoden', fontsize=12, fontweight='bold')
    plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
    
    # 4. Balkendiagramm: Erfolgsrate in % pro Kombination
    ax4 = plt.subplot(2, 3, 4)
    df_sorted_pct = df.sort_values('Anteil_Prozent', ascending=True)
    colors_pct = ['#FF6B6B' if x == 'CSV' else '#4ECDC4' for x in df_sorted_pct['Datenquelle']]
    
    bars_pct = ax4.barh(range(len(df_sorted_pct)), df_sorted_pct['Anteil_Prozent'], color=colors_pct)
    ax4.set_yticks(range(len(df_sorted_pct)))
    ax4.set_yticklabels([f"{row['Zielspalte'][:15]}\n({row['Methode']})" 
                        for _, row in df_sorted_pct.iterrows()], fontsize=10)
    ax4.set_xlabel('Matching-Anteil (%)', fontsize=12, fontweight='bold')
    ax4.set_title('📊 Matching-Erfolgsrate (%)', fontsize=14, fontweight='bold', pad=20)
    
    # Prozent-Werte auf Balken
    for i, bar in enumerate(bars_pct):
        width = bar.get_width()
        ax4.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                f'{width:.1f}%', ha='left', va='center', fontweight='bold')
    
    ax4.grid(axis='x', alpha=0.3)
    ax4.set_xlim(0, max(df['Anteil_Prozent']) * 1.2)
    
    # 5. Kombiniertes Diagramm: Matches und Prozent
    ax5 = plt.subplot(2, 3, 5)
    x_pos = np.arange(len(df))
    
    # Verkürzte Labels für bessere Lesbarkeit
    combined_labels = [f"{row['Zielspalte'][:8]}\n{row['Datenquelle']}\n{row['Methode'][:6]}" 
                      for _, row in df.iterrows()]
    
    bars_combined = ax5.bar(x_pos, df['Matches'], color=colors, alpha=0.8, width=0.6)
    ax5.set_xticks(x_pos)
    ax5.set_xticklabels(combined_labels, fontsize=9, ha='center')
    ax5.set_ylabel('Anzahl Matches', fontsize=12, fontweight='bold')
    ax5.set_title('📈 Matches mit Erfolgsrate', fontsize=14, fontweight='bold', pad=20)
    
    # Sekundäre Y-Achse für Prozente
    ax5_twin = ax5.twinx()
    line = ax5_twin.plot(x_pos, df['Anteil_Prozent'], 'o-', color='darkred', 
                        linewidth=3, markersize=8, label='Erfolgsrate %')
    ax5_twin.set_ylabel('Matching-Anteil (%)', fontsize=12, fontweight='bold', color='darkred')
    ax5_twin.tick_params(axis='y', labelcolor='darkred')
    
    # Werte über Balken und Linien
    for i, (matches, pct) in enumerate(zip(df['Matches'], df['Anteil_Prozent'])):
        ax5.text(i, matches + 600, f'{matches:,}', ha='center', va='bottom', 
                fontweight='bold', fontsize=9)
        ax5_twin.text(i, pct + 1.5, f'{pct:.1f}%', ha='center', va='bottom', 
                     fontweight='bold', fontsize=9, color='darkred')
    
    ax5.grid(axis='y', alpha=0.3)
    
    # 6. Zusammenfassungstabelle
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('tight')
    ax6.axis('off')
    
    # Statistiken berechnen
    total_matches = df['Matches'].sum()
    avg_success_rate = df['Anteil_Prozent'].mean()
    best_combination = df.loc[df['Matches'].idxmax()]
    csv_total = df[df['Datenquelle'] == 'CSV']['Matches'].sum()
    xml_total = df[df['Datenquelle'] == 'XML']['Matches'].sum()
    
    # Zusammenfassungsdaten
    summary_data = [
        ['Gesamte Matches', f'{total_matches:,}'],
        ['Ø Erfolgsrate', f'{avg_success_rate:.1f}%'],
        ['Top Kombination', f"{best_combination['Zielspalte']} ({best_combination['Matches']:,})"],
        ['CSV Matches', f'{csv_total:,} ({csv_total/total_matches*100:.1f}%)'],
        ['XML Matches', f'{xml_total:,} ({xml_total/total_matches*100:.1f}%)'],
        ['Methoden', 'Substring (4x), Suffix (2x)'],
        ['Zielspalten', '4 verschiedene analysiert']
    ]
    
    # Erstelle Tabelle
    table = ax6.table(cellText=summary_data, 
                     colLabels=['Metrik', 'Wert'],
                     cellLoc='left',
                     loc='center',
                     colWidths=[0.5, 0.5])
    
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 2)
    
    # Styling der Tabelle
    for i in range(len(summary_data[0])):
        table[(0, i)].set_facecolor('#E8E8E8')
        table[(0, i)].set_text_props(weight='bold')
    
    # Alternating row colors
    for i in range(1, len(summary_data) + 1):
        if i % 2 == 0:
            for j in range(len(summary_data[0])):
                table[(i, j)].set_facecolor('#F5F5F5')
    
    ax6.set_title('📋 Ergebnis-Zusammenfassung', fontsize=14, fontweight='bold', pad=20)
    
    # Haupttitel für die gesamte Visualisierung
    fig.suptitle('🎯 TecDoc-CMD Deterministische Matching-Analyse\nSpalten-Performance und Matching-Erfolg im Detail', 
                fontsize=18, fontweight='bold', y=0.98)
    
    # Layout anpassen
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Speichern
    output_dir = Path("results/visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / "deterministic_matching_results_detailed.png", 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_dir / "deterministic_matching_results_detailed.pdf", 
                bbox_inches='tight', facecolor='white')
    
    print(f"✅ Detaillierte Visualisierung gespeichert:")
    print(f"   📊 {output_dir}/deterministic_matching_results_detailed.png")
    print(f"   📄 {output_dir}/deterministic_matching_results_detailed.pdf")
    
    plt.show()
    
    return df

def create_column_comparison_chart(df):
    """Erstelle spezielle Spalten-Vergleichsvisualisierung"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Gestapeltes Balkendiagramm: Methoden pro Spalte
    pivot_data = df.pivot_table(values='Matches', index='Zielspalte', 
                               columns='Methode', fill_value=0, aggfunc='sum')
    
    pivot_data.plot(kind='bar', stacked=True, ax=ax1, 
                   color=['#FF6B6B', '#4ECDC4'], alpha=0.8)
    ax1.set_title('📊 Matches pro Zielspalte (nach Methode)', fontweight='bold', fontsize=14)
    ax1.set_xlabel('Zielspalten', fontweight='bold')
    ax1.set_ylabel('Anzahl Matches', fontweight='bold')
    legend = ax1.legend(title='Matching-Methode')
    legend.get_title().set_fontweight('bold')
    ax1.tick_params(axis='x', rotation=45)
    
    # Werte auf gestapelten Balken
    for container in ax1.containers:
        ax1.bar_label(container, fmt='%d', label_type='center', fontweight='bold')
    
    # 2. Erfolgsrate pro Spalte (Durchschnitt bei mehreren Einträgen)
    column_stats = df.groupby('Zielspalte').agg({
        'Matches': 'sum',
        'Anteil_Prozent': 'mean'
    }).reset_index()
    
    bars = ax2.bar(column_stats['Zielspalte'], column_stats['Anteil_Prozent'], 
                   color=['#FF6B6B', '#FFD93D', '#6BCF7F', '#4ECDC4'], alpha=0.8)
    ax2.set_title('📈 Durchschnittliche Erfolgsrate pro Spalte', fontweight='bold', fontsize=14)
    ax2.set_xlabel('Zielspalten', fontweight='bold')
    ax2.set_ylabel('Erfolgsrate (%)', fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    
    # Werte über Balken
    for bar, value in zip(bars, column_stats['Anteil_Prozent']):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 3. Heatmap: Datenquelle vs Zielspalte
    pivot_source = df.pivot_table(values='Matches', index='Datenquelle', 
                                 columns='Zielspalte', fill_value=0, aggfunc='sum')
    
    sns.heatmap(pivot_source, annot=True, fmt='d', cmap='Oranges', ax=ax3, 
                cbar_kws={'label': 'Anzahl Matches'})
    ax3.set_title('🔥 Datenquelle vs Zielspalte', fontweight='bold', fontsize=14)
    ax3.set_xlabel('Zielspalten', fontweight='bold')
    ax3.set_ylabel('Datenquelle', fontweight='bold')
    plt.setp(ax3.get_xticklabels(), rotation=45)
    
    # 4. Bubble Chart: Matches vs Erfolgsrate
    scatter = ax4.scatter(df['Matches'], df['Anteil_Prozent'], 
                         s=[x/50 for x in df['Matches']],  # Bubble-Größe proportional zu Matches
                         c=['red' if x == 'CSV' else 'blue' for x in df['Datenquelle']], 
                         alpha=0.7, edgecolors='black', linewidth=2)
    
    ax4.set_xlabel('Anzahl Matches', fontweight='bold')
    ax4.set_ylabel('Erfolgsrate (%)', fontweight='bold')
    ax4.set_title('💫 Bubble Chart: Matches vs Erfolgsrate\n(Bubble-Größe = Matches)', 
                 fontweight='bold', fontsize=14)
    
    # Labels für jeden Punkt
    for i, row in df.iterrows():
        ax4.annotate(f"{row['Zielspalte'][:10]}\n({row['Methode']})", 
                    (row['Matches'], row['Anteil_Prozent']),
                    xytext=(8, 8), textcoords='offset points', fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8),
                    ha='center')
    
    # Legende für Datenquellen
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
                                 markersize=12, label='CSV-Daten'),
                      plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', 
                                markersize=12, label='XML-Daten')]
    ax4.legend(handles=legend_elements, loc='upper left')
    
    plt.tight_layout()
    
    # Speichern
    output_dir = Path("results/visualizations")
    plt.savefig(output_dir / "column_comparison_analysis.png", dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / "column_comparison_analysis.pdf", bbox_inches='tight')
    
    print(f"✅ Spalten-Vergleichsanalyse gespeichert:")
    print(f"   📊 {output_dir}/column_comparison_analysis.png")
    print(f"   📄 {output_dir}/column_comparison_analysis.pdf")
    
    plt.show()

def main():
    """Hauptfunktion zur Erstellung aller Visualisierungen"""
    
    print("🎨 DETERMINISTISCHE MATCHING ERGEBNISSE - VISUALISIERUNG")
    print("=" * 60)
    print("Basierend auf den tatsächlichen Matching-Ergebnissen:")
    print("• CSV: 58,074 Matches (Substring: 49,222 + Suffix: 8,852)")
    print("• XML: 7,628 Matches (Suffix: 6,065 + Substring: 1,563)")
    print("• Gesamt: 65,702 Matches über 4 Zielspalten")
    print("=" * 60)
    
    # Erstelle detaillierte Hauptvisualisierung
    df = create_deterministic_results_visualization()
    
    print("\n" + "="*60)
    
    # Erstelle Spalten-Vergleichsvisualisierung
    create_column_comparison_chart(df)
    
    print(f"\n✅ Alle Visualisierungen erfolgreich erstellt!")
    print(f"📁 Speicherort: results/visualizations/")
    print(f"📊 2 PNG-Dateien und 2 PDF-Dateien erstellt")

if __name__ == "__main__":
    main()
