import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Visualisierungs-Ordner für TecDoc XML-Analysen
VISUALIZATION_DIR = "visualizations/tecdoc_xml_analysis"
os.makedirs(VISUALIZATION_DIR, exist_ok=True)

# Ergebnisse aus dem Matching-Skript
matching_results = {
    "Exakt: artno <-> SupplierPtNo": 20,
    "Exakt: brandno <-> Brand": 0,
    "Exakt: batchsize1 <-> MinOrderQuantity": 0,
    "Exakt: batchsize2 <-> MaxOrderQuantity": 0,
    "Exakt: batchsize1 <-> GrossWeight": 4672,
    "Exakt: batchsize2 <-> Volume": 4672,
    "Normalisiert: artno <-> SupplierPtNo": 0,
    "Normalisiert: brandno <-> Brand": 0,
    "Teilstring: artno <-> SupplierPtNo": 15496,
    "Teilstring: artno <-> ArticleDescription_DE": 0,
    "Teilstring: artno <-> ArticleDescription_EN": 0,
    "Prefix_5: artno <-> SupplierPtNo": 128,
    "Prefix_5: brandno <-> Brand": 0
}

def create_matching_visualizations():
    """Erstellt verschiedene Visualisierungen der Matching-Ergebnisse"""
    
    # Set style
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # Erstelle Figure mit Subplots
    fig = plt.figure(figsize=(20, 15))
    
    # 1. Balkendiagramm aller Matches
    ax1 = plt.subplot(2, 3, 1)
    methods = []
    pairs = []
    values = []
    
    for key, value in matching_results.items():
        if value > 0:  # Nur nicht-null Werte
            method, pair = key.split(": ", 1)
            methods.append(method)
            pairs.append(pair)
            values.append(value)
    
    # Farben für verschiedene Methoden
    colors = {'Exakt': '#e74c3c', 'Teilstring': '#3498db', 'Prefix_5': '#2ecc71', 'Normalisiert': '#f39c12'}
    bar_colors = [colors.get(method, '#95a5a6') for method in methods]
    
    bars = ax1.bar(range(len(values)), values, color=bar_colors)
    ax1.set_xlabel('Matching-Paare')
    ax1.set_ylabel('Anzahl Matches')
    ax1.set_title('Matching-Ergebnisse nach Verfahren und Spaltenpaaren')
    ax1.set_xticks(range(len(pairs)))
    ax1.set_xticklabels([p.replace(' <-> ', '\n↔\n') for p in pairs], rotation=45, ha='right')
    ax1.set_yscale('log')  # Logarithmische Skala wegen großer Unterschiede
    
    # Werte auf Balken anzeigen
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:,}', ha='center', va='bottom', fontsize=8)
    
    # 2. Pie Chart nach Methoden
    ax2 = plt.subplot(2, 3, 2)
    method_totals = {}
    for key, value in matching_results.items():
        method = key.split(": ")[0]
        method_totals[method] = method_totals.get(method, 0) + value
    
    # Nur Methoden mit Matches
    method_totals = {k: v for k, v in method_totals.items() if v > 0}
    
    wedges, texts, autotexts = ax2.pie(method_totals.values(), 
                                      labels=method_totals.keys(),
                                      autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*sum(method_totals.values())):,})',
                                      startangle=90)
    ax2.set_title('Verteilung der Matches nach Verfahren')
    
    # 3. Heatmap der Spaltenpaare
    ax3 = plt.subplot(2, 3, 3)
    
    # Erstelle Matrix für Heatmap
    tec_cols = ['artno', 'brandno', 'batchsize1', 'batchsize2']
    cmd_cols = ['SupplierPtNo', 'Brand', 'MinOrderQuantity', 'MaxOrderQuantity', 'GrossWeight', 'Volume', 'ArticleDescription_DE', 'ArticleDescription_EN']
    
    heatmap_data = np.zeros((len(tec_cols), len(cmd_cols)))
    
    for key, value in matching_results.items():
        if value > 0:
            _, pair = key.split(": ", 1)
            tec_col, cmd_col = pair.split(" <-> ")
            if tec_col in tec_cols and cmd_col in cmd_cols:
                i = tec_cols.index(tec_col)
                j = cmd_cols.index(cmd_col)
                heatmap_data[i, j] = max(heatmap_data[i, j], value)
    
    # Log-transformierte Werte für bessere Visualisierung
    heatmap_data_log = np.log10(heatmap_data + 1)
    
    sns.heatmap(heatmap_data_log, 
                xticklabels=[col.replace('_', '\n') for col in cmd_cols],
                yticklabels=tec_cols,
                annot=heatmap_data.astype(int), 
                fmt='d',
                cmap='YlOrRd',
                ax=ax3,
                cbar_kws={'label': 'log10(Matches + 1)'})
    ax3.set_title('Heatmap: TecDoc ↔ CMD Spalten-Matches')
    ax3.set_xlabel('CMD Spalten')
    ax3.set_ylabel('TecDoc Spalten')
    
    # 4. Balkendiagramm Top-Performer
    ax4 = plt.subplot(2, 3, 4)
    top_pairs = sorted([(k, v) for k, v in matching_results.items() if v > 0], 
                      key=lambda x: x[1], reverse=True)[:8]
    
    top_labels = [pair[0].replace(': ', '\n').replace(' <-> ', '\n↔\n') for pair in top_pairs]
    top_values = [pair[1] for pair in top_pairs]
    
    bars = ax4.barh(range(len(top_values)), top_values, 
                   color=plt.cm.viridis(np.linspace(0, 1, len(top_values))))
    ax4.set_yticks(range(len(top_labels)))
    ax4.set_yticklabels(top_labels, fontsize=9)
    ax4.set_xlabel('Anzahl Matches')
    ax4.set_title('Top Matching-Paare')
    ax4.set_xscale('log')
    
    # Werte anzeigen
    for i, (bar, value) in enumerate(zip(bars, top_values)):
        width = bar.get_width()
        ax4.text(width, bar.get_y() + bar.get_height()/2.,
                f'{value:,}', ha='left', va='center', fontsize=8)
    
    # 5. Erfolgsrate nach Verfahren
    ax5 = plt.subplot(2, 3, 5)
    
    method_stats = {}
    for key, value in matching_results.items():
        method = key.split(": ")[0]
        if method not in method_stats:
            method_stats[method] = {'total_pairs': 0, 'successful_pairs': 0, 'total_matches': 0}
        method_stats[method]['total_pairs'] += 1
        if value > 0:
            method_stats[method]['successful_pairs'] += 1
        method_stats[method]['total_matches'] += value
    
    methods = list(method_stats.keys())
    success_rates = [method_stats[m]['successful_pairs'] / method_stats[m]['total_pairs'] * 100 
                    for m in methods]
    
    bars = ax5.bar(methods, success_rates, color=['#e74c3c', '#f39c12', '#3498db', '#2ecc71'])
    ax5.set_ylabel('Erfolgsrate (%)')
    ax5.set_title('Erfolgsrate der Matching-Verfahren\n(% der Spaltenpaare mit Matches)')
    ax5.set_ylim(0, 100)
    
    # Werte anzeigen
    for bar, rate in zip(bars, success_rates):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{rate:.1f}%', ha='center', va='bottom')
    
    # 6. Textuelle Zusammenfassung
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')
    
    total_matches = sum(matching_results.values())
    hochrechnung = total_matches * 114  # Faktor aus dem Skript
    
    summary_text = f"""
MATCHING-ZUSAMMENFASSUNG

📊 Getestete Daten:
• 350.000 TecDoc-Zeilen (7 Chunks)
• 4 verschiedene Verfahren
• 13 Spaltenpaare getestet

🎯 Ergebnisse:
• Gesamt: {total_matches:,} Matches
• Hochrechnung: {hochrechnung:,} Matches
• Beste Methode: Teilstring ({sum(v for k, v in matching_results.items() if 'Teilstring' in k):,})
• Bestes Paar: artno ↔ SupplierPtNo

🚀 Top-Erkenntnisse:
• Teilstring-Matching sehr erfolgreich
• Numerische Werte matchen gut
• Brand-Matching schwierig
• Artikelnummern haben Potenzial
    """
    
    ax6.text(0.05, 0.95, summary_text, transform=ax6.transAxes, 
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(f'{VISUALIZATION_DIR}/matching_results_visualization.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Zusätzliche detaillierte Statistiken
    print("\n" + "="*80)
    print("DETAILLIERTE STATISTIKEN")
    print("="*80)
    
    for method in method_stats:
        stats = method_stats[method]
        print(f"\n{method.upper()}:")
        print(f"  Getestete Paare: {stats['total_pairs']}")
        print(f"  Erfolgreiche Paare: {stats['successful_pairs']}")
        print(f"  Erfolgsrate: {stats['successful_pairs']/stats['total_pairs']*100:.1f}%")
        print(f"  Gesamt Matches: {stats['total_matches']:,}")
        if stats['successful_pairs'] > 0:
            print(f"  Ø Matches pro erfolgreichem Paar: {stats['total_matches']/stats['successful_pairs']:.0f}")

if __name__ == "__main__":
    create_matching_visualizations()
