import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Detaillierte Ergebnisse aus dem Matching-Skript
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

def create_readable_visualizations():
    """Erstellt gut lesbare Visualisierungen mit größerer Schrift und besserer Aufteilung"""
    
    # Aufbereitung der Daten
    column_performance = {}
    for key, matches in matching_results.items():
        method, pair = key.split(": ", 1)
        tec_col, cmd_col = pair.split(" <-> ")
        pair_key = f"{tec_col} ↔ {cmd_col}"
        
        if pair_key not in column_performance:
            column_performance[pair_key] = {
                'total_matches': 0,
                'methods_tested': 0,
                'successful_methods': 0,
                'best_method': '',
                'best_score': 0,
                'methods_detail': {}
            }
        
        column_performance[pair_key]['total_matches'] += matches
        column_performance[pair_key]['methods_tested'] += 1
        column_performance[pair_key]['methods_detail'][method] = matches
        
        if matches > 0:
            column_performance[pair_key]['successful_methods'] += 1
            if matches > column_performance[pair_key]['best_score']:
                column_performance[pair_key]['best_score'] = matches
                column_performance[pair_key]['best_method'] = method

    # Set global style parameters for better readability
    plt.rcParams.update({
        'font.size': 12,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16
    })
    
    # 1. TOP SPALTENPAARE (einzelnes großes Diagramm)
    plt.figure(figsize=(16, 10))
    
    pairs = list(column_performance.keys())
    total_matches = [column_performance[pair]['total_matches'] for pair in pairs]
    sorted_pairs = sorted(zip(pairs, total_matches), key=lambda x: x[1], reverse=True)
    
    # Nur Paare mit Matches zeigen
    successful_pairs = [(p, m) for p, m in sorted_pairs if m > 0]
    
    if successful_pairs:
        pairs_success = [p[0] for p in successful_pairs]
        matches_success = [p[1] for p in successful_pairs]
        
        colors = ['#e74c3c', '#3498db', '#2ecc71']  # Rot, Blau, Grün
        bars = plt.barh(range(len(pairs_success)), matches_success, color=colors)
        
        plt.yticks(range(len(pairs_success)), pairs_success, fontsize=14)
        plt.xlabel('Anzahl Matches', fontsize=14)
        plt.title('TOP-PERFORMING SPALTENPAARE\n(Gesamte Matches aller Methoden)', fontsize=16, pad=20)
        plt.xscale('log')
        plt.grid(axis='x', alpha=0.3)
        
        # Werte deutlich sichtbar machen
        for i, (bar, value) in enumerate(zip(bars, matches_success)):
            width = bar.get_width()
            plt.text(width * 1.1, bar.get_y() + bar.get_height()/2.,
                    f'{value:,}', ha='left', va='center', fontsize=12, weight='bold')
    
    plt.tight_layout()
    plt.savefig('top_spaltenpaare.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 2. TECDOC vs CMD SPALTEN VERGLEICH
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # TecDoc Spalten
    tec_columns = {}
    for pair in column_performance:
        tec_col = pair.split(" ↔ ")[0]
        if tec_col not in tec_columns:
            tec_columns[tec_col] = {'matches': 0, 'pairs_tested': 0, 'successful_pairs': 0}
        tec_columns[tec_col]['matches'] += column_performance[pair]['total_matches']
        tec_columns[tec_col]['pairs_tested'] += 1
        if column_performance[pair]['total_matches'] > 0:
            tec_columns[tec_col]['successful_pairs'] += 1
    
    tec_sorted = sorted(tec_columns.items(), key=lambda x: x[1]['matches'], reverse=True)
    tec_cols = [item[0] for item in tec_sorted]
    tec_matches = [item[1]['matches'] for item in tec_sorted]
    tec_success_rate = [item[1]['successful_pairs'] / item[1]['pairs_tested'] * 100 for item in tec_sorted]
    
    bars1 = ax1.bar(range(len(tec_cols)), tec_matches, color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12'])
    ax1.set_xticks(range(len(tec_cols)))
    ax1.set_xticklabels(tec_cols, fontsize=14)
    ax1.set_ylabel('Gesamte Matches', fontsize=14)
    ax1.set_title('TecDoc Spalten Performance', fontsize=16)
    ax1.set_yscale('log')
    ax1.grid(axis='y', alpha=0.3)
    
    # Werte und Erfolgsrate anzeigen
    for i, (bar, rate, matches) in enumerate(zip(bars1, tec_success_rate, tec_matches)):
        height = bar.get_height()
        if matches > 0:
            ax1.text(bar.get_x() + bar.get_width()/2., height * 1.1,
                    f'{matches:,}\n({rate:.0f}%)', ha='center', va='bottom', fontsize=11, weight='bold')
    
    # CMD Spalten
    cmd_columns = {}
    for pair in column_performance:
        cmd_col = pair.split(" ↔ ")[1]
        if cmd_col not in cmd_columns:
            cmd_columns[cmd_col] = {'matches': 0, 'pairs_tested': 0, 'successful_pairs': 0}
        cmd_columns[cmd_col]['matches'] += column_performance[pair]['total_matches']
        cmd_columns[cmd_col]['pairs_tested'] += 1
        if column_performance[pair]['total_matches'] > 0:
            cmd_columns[cmd_col]['successful_pairs'] += 1
    
    cmd_sorted = sorted(cmd_columns.items(), key=lambda x: x[1]['matches'], reverse=True)
    cmd_cols = [item[0] for item in cmd_sorted]
    cmd_matches = [item[1]['matches'] for item in cmd_sorted]
    cmd_success_rate = [item[1]['successful_pairs'] / item[1]['pairs_tested'] * 100 for item in cmd_sorted]
    
    bars2 = ax2.barh(range(len(cmd_cols)), cmd_matches, color=plt.cm.viridis(np.linspace(0, 1, len(cmd_cols))))
    ax2.set_yticks(range(len(cmd_cols)))
    # Kürze lange Namen für bessere Lesbarkeit
    cmd_labels = [col.replace('ArticleDescription_', 'Desc_').replace('OrderQuantity', 'Order') for col in cmd_cols]
    ax2.set_yticklabels(cmd_labels, fontsize=12)
    ax2.set_xlabel('Gesamte Matches', fontsize=14)
    ax2.set_title('CMD Spalten Performance', fontsize=16)
    ax2.set_xscale('log')
    ax2.grid(axis='x', alpha=0.3)
    
    # Werte anzeigen
    for i, (bar, rate, matches) in enumerate(zip(bars2, cmd_success_rate, cmd_matches)):
        if matches > 0:
            width = bar.get_width()
            ax2.text(width * 1.1, bar.get_y() + bar.get_height()/2.,
                    f'{matches:,} ({rate:.0f}%)', ha='left', va='center', fontsize=11, weight='bold')
    
    plt.tight_layout()
    plt.savefig('spalten_vergleich.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 3. METHODEN-PERFORMANCE MATRIX
    plt.figure(figsize=(14, 8))
    
    methods = ['Exakt', 'Normalisiert', 'Teilstring', 'Prefix_5']
    successful_pairs_only = [p for p, m in sorted_pairs if m > 0]
    
    heatmap_data = []
    for method in methods:
        method_row = []
        for pair in successful_pairs_only:
            pair_data = column_performance[pair]['methods_detail']
            value = pair_data.get(method, 0)
            method_row.append(value)
        heatmap_data.append(method_row)
    
    heatmap_array = np.array(heatmap_data)
    
    # Verwende originale Werte für Annotation, log für Farbskala
    mask = heatmap_array == 0
    
    sns.heatmap(heatmap_array, 
                xticklabels=successful_pairs_only,
                yticklabels=methods,
                annot=True,
                fmt='d',
                cmap='YlOrRd',
                mask=mask,
                cbar_kws={'label': 'Anzahl Matches'},
                annot_kws={'size': 12, 'weight': 'bold'})
    
    plt.title('Methoden-Performance Matrix\n(Nur erfolgreiche Spaltenpaare)', fontsize=16, pad=20)
    plt.xlabel('Spaltenpaare', fontsize=14)
    plt.ylabel('Matching-Methoden', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(rotation=0, fontsize=12)
    
    plt.tight_layout()
    plt.savefig('methoden_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 4. ERFOLGSRATEN-ANALYSE
    plt.figure(figsize=(14, 8))
    
    # Erfolgsrate pro Spaltenpaar
    success_data = []
    for pair in pairs:
        perf = column_performance[pair]
        if perf['methods_tested'] > 0:
            rate = perf['successful_methods'] / perf['methods_tested'] * 100
            success_data.append((pair, rate, perf['total_matches']))
    
    success_data.sort(key=lambda x: x[2], reverse=True)  # Nach Gesamtmatches sortieren
    
    pair_names = [item[0] for item in success_data]
    success_rates = [item[1] for item in success_data]
    total_matches = [item[2] for item in success_data]
    
    # Farbe basiert auf Anzahl Matches
    colors = plt.cm.RdYlGn(np.array(success_rates)/100)
    
    bars = plt.bar(range(len(pair_names)), success_rates, color=colors)
    plt.xticks(range(len(pair_names)), pair_names, rotation=45, ha='right', fontsize=11)
    plt.ylabel('Erfolgsrate (%)', fontsize=14)
    plt.title('Erfolgsrate pro Spaltenpaar\n(% der Methoden mit Matches > 0)', fontsize=16, pad=20)
    plt.ylim(0, 100)
    plt.grid(axis='y', alpha=0.3)
    
    # Werte und Matches anzeigen
    for i, (bar, rate, matches) in enumerate(zip(bars, success_rates, total_matches)):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{rate:.0f}%\n({matches:,})', ha='center', va='bottom', fontsize=10, weight='bold')
    
    plt.tight_layout()
    plt.savefig('erfolgsraten.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\n" + "="*80)
    print("VISUALISIERUNGEN ERSTELLT:")
    print("="*80)
    print("✅ top_spaltenpaare.png - Beste Spaltenpaare Ranking")
    print("✅ spalten_vergleich.png - TecDoc vs CMD Spalten Performance") 
    print("✅ methoden_matrix.png - Heatmap aller Methoden vs Spaltenpaare")
    print("✅ erfolgsraten.png - Erfolgsraten-Analyse")
    print("\nAlle Diagramme wurden mit verbesserter Lesbarkeit erstellt!")

if __name__ == "__main__":
    create_readable_visualizations()
