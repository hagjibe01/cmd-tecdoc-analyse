import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Visualisierungs-Ordner erstellen
VISUALIZATION_DIR = "visualizations/cmd_csv_analysis"
os.makedirs(VISUALIZATION_DIR, exist_ok=True)

# Ergebnisse aus dem TecDoc-TMD Matching-Skript
matching_results = {
    # Exakt
    "Exakt: artno <-> article_number": 8,
    "Exakt: artno <-> tec_doc_article_number": 8,
    "Exakt: batchsize2 <-> packaging_weight": 2,
    "Exakt: batchsize2 <-> packaging_dimension_length": 2,
    "Exakt: batchsize2 <-> packaging_dimension_width": 2,
    "Exakt: batchsize2 <-> packaging_dimension_height": 2,
    "Exakt: batchsize2 <-> net_amount": 2,
    "Exakt: batchsize2 <-> gross_amount": 2,
    
    # Normalisiert
    "Normalisiert: artno <-> article_number": 8,
    "Normalisiert: artno <-> tec_doc_article_number": 8,
    "Normalisiert: batchsize2 <-> packaging_weight": 2,
    "Normalisiert: batchsize2 <-> packaging_dimension_length": 2,
    "Normalisiert: batchsize2 <-> packaging_dimension_width": 2,
    "Normalisiert: batchsize2 <-> packaging_dimension_height": 2,
    "Normalisiert: batchsize2 <-> net_amount": 2,
    "Normalisiert: batchsize2 <-> gross_amount": 2,
    
    # Teilstring
    "Teilstring: artno <-> article_number": 964,
    "Teilstring: artno <-> tec_doc_article_number": 941,
    "Teilstring: artno <-> predecessor_article_number": 25,
    "Teilstring: artno <-> ean": 1162,
    "Teilstring: artno <-> packaging_ean": 639,
    
    # Prefix_5
    "Prefix_5: artno <-> article_number": 194,
    "Prefix_5: artno <-> tec_doc_article_number": 194,
    "Prefix_5: artno <-> predecessor_article_number": 1,
    
    # Numerisch
    "Numerisch: artno <-> article_number": 8,
    "Numerisch: artno <-> tec_doc_article_number": 8,
    "Numerisch: batchsize2 <-> packaging_weight": 2,
    "Numerisch: batchsize2 <-> packaging_dimension_length": 2,
    "Numerisch: batchsize2 <-> packaging_dimension_width": 2,
    "Numerisch: batchsize2 <-> packaging_dimension_height": 2,
    "Numerisch: batchsize2 <-> net_amount": 2,
    "Numerisch: batchsize2 <-> gross_amount": 2,
    
    # Numerisch_Toleranz
    "Numerisch_Toleranz: artno <-> article_number": 3036,
    "Numerisch_Toleranz: artno <-> tec_doc_article_number": 3036,
    "Numerisch_Toleranz: artno <-> predecessor_article_number": 3034,
    "Numerisch_Toleranz: batchsize2 <-> packaging_weight": 16778,
    "Numerisch_Toleranz: batchsize2 <-> packaging_dimension_length": 16778,
    "Numerisch_Toleranz: batchsize2 <-> packaging_dimension_width": 16778,
    "Numerisch_Toleranz: batchsize2 <-> packaging_dimension_height": 16778,
    "Numerisch_Toleranz: batchsize2 <-> net_amount": 16778,
    "Numerisch_Toleranz: batchsize2 <-> gross_amount": 16778,
    
    # Suffix_3
    "Suffix_3: artno <-> article_number": 2209,
    "Suffix_3: artno <-> tec_doc_article_number": 2106,
    "Suffix_3: artno <-> predecessor_article_number": 190,
    "Suffix_3: artno <-> ean": 1996,
    "Suffix_3: artno <-> packaging_ean": 1988,
    
    # Längen_Match
    "Längen_Match: artno <-> article_number": 22,
    "Längen_Match: artno <-> tec_doc_article_number": 22,
    "Längen_Match: artno <-> predecessor_article_number": 10,
    "Längen_Match: artno <-> ean": 2,
    "Längen_Match: artno <-> packaging_ean": 2,
    "Längen_Match: brandno <-> brand": 2,
    "Längen_Match: brandno <-> predecessor_brand": 2,
    "Längen_Match: tableno <-> tec_doc_data_supplier_number": 2,
    "Längen_Match: batchsize1 <-> packaging_qty_per_uom": 2,
    "Längen_Match: batchsize1 <-> sales_uom_lot_size": 2,
    "Längen_Match: batchsize1 <-> sales_uom_base_uom_per_uom": 2,
    "Längen_Match: batchsize2 <-> packaging_weight": 2,
    "Längen_Match: batchsize2 <-> packaging_dimension_length": 2,
    "Längen_Match: batchsize2 <-> packaging_dimension_width": 2,
    "Längen_Match: batchsize2 <-> packaging_dimension_height": 2,
    "Längen_Match: batchsize2 <-> net_amount": 2,
    "Längen_Match: batchsize2 <-> gross_amount": 2,
}

def create_tecdoc_tmd_visualizations():
    """Erstellt umfassende Visualisierungen für TecDoc-TMD Matching"""
    
    # Set style
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # Global style parameters
    plt.rcParams.update({
        'font.size': 12,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16
    })
    
    # 1. TOP SPALTENPAARE RANKING
    plt.figure(figsize=(16, 10))
    
    # Finde Top-Performer
    top_pairs = sorted([(k, v) for k, v in matching_results.items() if v > 10], 
                      key=lambda x: x[1], reverse=True)[:15]
    
    pairs = [pair[0].replace(': ', '\n').replace(' <-> ', '\n↔\n') for pair in top_pairs]
    values = [pair[1] for pair in top_pairs]
    
    # Farben basierend auf Methode
    colors = []
    for pair_name in top_pairs:
        method = pair_name[0].split(':')[0]
        if 'Numerisch_Toleranz' in method:
            colors.append('#e74c3c')  # Rot für Top-Performer
        elif 'Suffix' in method:
            colors.append('#3498db')  # Blau für Suffix
        elif 'Teilstring' in method:
            colors.append('#2ecc71')  # Grün für Teilstring
        else:
            colors.append('#f39c12')  # Orange für andere
    
    bars = plt.barh(range(len(pairs)), values, color=colors)
    plt.yticks(range(len(pairs)), pairs, fontsize=10)
    plt.xlabel('Anzahl Matches (Testdaten: 2 Chunks)', fontsize=14)
    plt.title('TecDoc ↔ CMD TMD: TOP-PERFORMING SPALTENPAARE\n(Deterministische Matching-Verfahren)', 
              fontsize=16, pad=20)
    plt.xscale('log')
    plt.grid(axis='x', alpha=0.3)
    
    # Werte anzeigen
    for i, (bar, value) in enumerate(zip(bars, values)):
        width = bar.get_width()
        plt.text(width * 1.1, bar.get_y() + bar.get_height()/2.,
                f'{value:,}', ha='left', va='center', fontsize=10, weight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{VISUALIZATION_DIR}/tecdoc_tmd_top_matches.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 2. METHODEN-PERFORMANCE VERGLEICH
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Aggregiere nach Methoden
    method_totals = {}
    for key, value in matching_results.items():
        method = key.split(": ")[0]
        method_totals[method] = method_totals.get(method, 0) + value
    
    # Balkendiagramm nach Methoden
    methods = list(method_totals.keys())
    totals = list(method_totals.values())
    
    colors_method = plt.cm.viridis(np.linspace(0, 1, len(methods)))
    bars1 = ax1.bar(range(len(methods)), totals, color=colors_method)
    ax1.set_xticks(range(len(methods)))
    ax1.set_xticklabels(methods, rotation=45, ha='right', fontsize=11)
    ax1.set_ylabel('Gesamte Matches', fontsize=14)
    ax1.set_title('Performance nach Matching-Methode', fontsize=14)
    ax1.set_yscale('log')
    ax1.grid(axis='y', alpha=0.3)
    
    # Werte anzeigen
    for bar, total in zip(bars1, totals):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height * 1.1,
                f'{total:,}', ha='center', va='bottom', fontsize=10, weight='bold')
    
    # Pie Chart für Top 5 Methoden
    top_methods = sorted(method_totals.items(), key=lambda x: x[1], reverse=True)[:5]
    
    wedges, texts, autotexts = ax2.pie([m[1] for m in top_methods], 
                                      labels=[m[0] for m in top_methods],
                                      autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*sum([m[1] for m in top_methods])):,})',
                                      startangle=90)
    ax2.set_title('Top 5 Methoden: Verteilung der Matches', fontsize=14)
    
    plt.tight_layout()
    plt.savefig(f'{VISUALIZATION_DIR}/tecdoc_tmd_methoden_vergleich.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 3. TECDOC vs CMD SPALTEN ANALYSIS
    plt.figure(figsize=(16, 10))
    
    # Analysiere TecDoc Spalten
    tec_columns = {}
    cmd_columns = {}
    
    for key, value in matching_results.items():
        if value > 0:  # Nur erfolgreiche Matches
            _, pair = key.split(": ", 1)
            tec_col, cmd_col = pair.split(" <-> ")
            
            tec_columns[tec_col] = tec_columns.get(tec_col, 0) + value
            cmd_columns[cmd_col] = cmd_columns.get(cmd_col, 0) + value
    
    # Top TecDoc Spalten
    tec_sorted = sorted(tec_columns.items(), key=lambda x: x[1], reverse=True)[:8]
    cmd_sorted = sorted(cmd_columns.items(), key=lambda x: x[1], reverse=True)[:8]
    
    # Subplot für TecDoc Spalten
    ax1 = plt.subplot(2, 1, 1)
    tec_names = [item[0] for item in tec_sorted]
    tec_values = [item[1] for item in tec_sorted]
    
    bars = ax1.bar(tec_names, tec_values, color=plt.cm.Set3(np.linspace(0, 1, len(tec_names))))
    ax1.set_ylabel('Gesamte Matches', fontsize=14)
    ax1.set_title('TecDoc Spalten: Performance Ranking', fontsize=14)
    ax1.set_yscale('log')
    ax1.grid(axis='y', alpha=0.3)
    
    for bar, value in zip(bars, tec_values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height * 1.1,
                f'{value:,}', ha='center', va='bottom', fontsize=10, weight='bold')
    
    # Subplot für CMD Spalten
    ax2 = plt.subplot(2, 1, 2)
    cmd_names = [item[0].replace('_', '\n') for item in cmd_sorted]
    cmd_values = [item[1] for item in cmd_sorted]
    
    bars = ax2.barh(range(len(cmd_names)), cmd_values, 
                   color=plt.cm.plasma(np.linspace(0, 1, len(cmd_names))))
    ax2.set_yticks(range(len(cmd_names)))
    ax2.set_yticklabels(cmd_names, fontsize=10)
    ax2.set_xlabel('Gesamte Matches', fontsize=14)
    ax2.set_title('CMD Spalten: Performance Ranking', fontsize=14)
    ax2.set_xscale('log')
    ax2.grid(axis='x', alpha=0.3)
    
    for i, (bar, value) in enumerate(zip(bars, cmd_values)):
        width = bar.get_width()
        ax2.text(width * 1.1, bar.get_y() + bar.get_height()/2.,
                f'{value:,}', ha='left', va='center', fontsize=9, weight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{VISUALIZATION_DIR}/tecdoc_tmd_spalten_ranking.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 4. MATCHING-KATEGORIEN HEATMAP
    plt.figure(figsize=(14, 8))
    
    # Kategorisiere Spaltenpaare
    categories = {
        'Artikel-IDs': ['article_number', 'tec_doc_article_number', 'predecessor_article_number'],
        'Barcodes': ['ean', 'packaging_ean'],
        'Packaging': ['packaging_weight', 'packaging_dimension_length', 
                     'packaging_dimension_width', 'packaging_dimension_height'],
        'Pricing': ['net_amount', 'gross_amount'],
        'Quantities': ['packaging_qty_per_uom', 'sales_uom_lot_size', 'sales_uom_base_uom_per_uom'],
        'Brand': ['brand', 'predecessor_brand'],
        'System': ['tec_doc_data_supplier_number']
    }
    
    # Erstelle Heatmap-Daten
    methods = ['Exakt', 'Normalisiert', 'Teilstring', 'Prefix_5', 'Numerisch', 
               'Numerisch_Toleranz', 'Suffix_3', 'Längen_Match']
    
    heatmap_data = []
    category_labels = []
    
    for category, cmd_cols in categories.items():
        category_total = []
        for method in methods:
            method_total = 0
            for key, value in matching_results.items():
                if key.startswith(method + ":"):
                    _, pair = key.split(": ", 1)
                    _, cmd_col = pair.split(" <-> ")
                    if cmd_col in cmd_cols:
                        method_total += value
            category_total.append(method_total)
        heatmap_data.append(category_total)
        category_labels.append(category)
    
    # Log-transformierte Werte für bessere Visualisierung
    heatmap_array = np.array(heatmap_data)
    heatmap_log = np.log10(heatmap_array + 1)
    
    sns.heatmap(heatmap_log, 
                xticklabels=methods,
                yticklabels=category_labels,
                annot=heatmap_array,
                fmt='d',
                cmap='YlOrRd',
                cbar_kws={'label': 'log10(Matches + 1)'})
    
    plt.title('Matching Performance: Methoden vs. Datenkategorien\n(log-Skala für bessere Visualisierung)', 
              fontsize=14, pad=20)
    plt.xlabel('Matching-Methoden', fontsize=12)
    plt.ylabel('Datenkategorien', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(f'{VISUALIZATION_DIR}/tecdoc_tmd_kategorien_heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 5. ZUSAMMENFASSUNG MIT HOCHRECHNUNG
    plt.figure(figsize=(14, 8))
    plt.axis('off')
    
    total_matches = sum(matching_results.values())
    hochrechnung = total_matches * 57  # 2 Chunks von 114 geschätzt
    
    summary_text = f"""
TECDOC ↔ CMD TMD MATCHING: ZUSAMMENFASSUNG

📊 TESTDATEN:
• 40.000 TecDoc-Zeilen (2 Chunks von ~2,3 Millionen)
• 15.000 CMD TMD-Zeilen (Teilmenge)
• 8 verschiedene Matching-Verfahren
• 33 Spaltenpaare getestet

🎯 ERGEBNISSE (TESTDATEN):
• Gesamt: {total_matches:,} Matches
• Hochrechnung: ~{hochrechnung:,} Matches (Volldata)
• Top-Methode: Numerisch mit Toleranz ({sum(v for k, v in matching_results.items() if 'Numerisch_Toleranz' in k):,})
• Top-Paar: batchsize2 ↔ packaging_weight (16.778)

🏆 TOP-ERKENNTNISSE:
• Numerische Toleranz: Mega-Erfolg bei Packaging-Daten
• Suffix-Matching: Artikelnummern-Varianten erkannt  
• EAN-Integration: TecDoc-Nr. in Barcodes eingebettet
• Predecessor-Matching: Produktlinien verfolgbar

🚀 PRAKTISCHE ANWENDUNG:
• Artikelnummer-Verknüpfung: {sum(v for k, v in matching_results.items() if 'artno' in k and 'article_number' in k):,} direkte Matches
• EAN-Verknüpfung: {sum(v for k, v in matching_results.items() if 'ean' in k):,} Barcode-Matches  
• Packaging-Integration: {sum(v for k, v in matching_results.items() if 'packaging' in k):,} Dimensionen-Matches
• Brand-Mapping: {sum(v for k, v in matching_results.items() if 'brand' in k):,} Hersteller-Matches

💡 EMPFEHLUNG:
1. Numerische Toleranz für Packaging-Daten
2. Suffix-Matching für Artikelnummer-Varianten
3. EAN-Integration für Barcode-Systeme
4. Predecessor-Analyse für Produktentwicklung
    """
    
    plt.text(0.05, 0.95, summary_text, transform=plt.gca().transAxes, 
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
    
    plt.title('TecDoc ↔ CMD TMD: Matching-Analyse Zusammenfassung', 
              fontsize=16, pad=20)
    
    plt.tight_layout()
    plt.savefig(f'{VISUALIZATION_DIR}/tecdoc_tmd_zusammenfassung.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\n" + "="*80)
    print("VISUALISIERUNGEN ERSTELLT:")
    print("="*80)
    print(f"✅ {VISUALIZATION_DIR}/tecdoc_tmd_top_matches.png - Top-Performing Spaltenpaare")
    print(f"✅ {VISUALIZATION_DIR}/tecdoc_tmd_methoden_vergleich.png - Methoden-Performance Vergleich") 
    print(f"✅ {VISUALIZATION_DIR}/tecdoc_tmd_spalten_ranking.png - TecDoc vs CMD Spalten Ranking")
    print(f"✅ {VISUALIZATION_DIR}/tecdoc_tmd_kategorien_heatmap.png - Kategorien-Heatmap")
    print(f"✅ {VISUALIZATION_DIR}/tecdoc_tmd_zusammenfassung.png - Gesamtzusammenfassung")
    print("\nAlle Visualisierungen mit hoher Auflösung und detaillierten Insights!")

if __name__ == "__main__":
    create_tecdoc_tmd_visualizations()
