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

def analyze_column_pairs():
    """Detaillierte Analyse der Spaltenpaare und ihrer Performance"""
    
    # Aufbereitung der Daten für Spalten-Analyse
    column_performance = {}
    method_performance = {}
    
    for key, matches in matching_results.items():
        method, pair = key.split(": ", 1)
        tec_col, cmd_col = pair.split(" <-> ")
        
        # Spalten-Performance tracken
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
    
    # Erstelle Visualisierung
    fig = plt.figure(figsize=(20, 16))
    
    # 1. Spaltenpaare nach Gesamtperformance
    ax1 = plt.subplot(3, 3, 1)
    pairs = list(column_performance.keys())
    total_matches = [column_performance[pair]['total_matches'] for pair in pairs]
    
    # Sortiere nach Performance
    sorted_pairs = sorted(zip(pairs, total_matches), key=lambda x: x[1], reverse=True)
    pairs_sorted = [p[0] for p in sorted_pairs]
    matches_sorted = [p[1] for p in sorted_pairs]
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(pairs_sorted)))
    bars = ax1.barh(range(len(pairs_sorted)), matches_sorted, color=colors)
    ax1.set_yticks(range(len(pairs_sorted)))
    ax1.set_yticklabels(pairs_sorted, fontsize=9)
    ax1.set_xlabel('Gesamte Matches')
    ax1.set_title('Spaltenpaare: Gesamtperformance\n(Summe aller Matching-Methoden)')
    ax1.set_xscale('log')
    
    # Werte anzeigen
    for i, (bar, value) in enumerate(zip(bars, matches_sorted)):
        if value > 0:
            width = bar.get_width()
            ax1.text(width, bar.get_y() + bar.get_height()/2.,
                    f' {value:,}', ha='left', va='center', fontsize=8)
    
    # 2. TecDoc Spalten Performance
    ax2 = plt.subplot(3, 3, 2)
    tec_columns = {}
    for pair in column_performance:
        tec_col = pair.split(" ↔ ")[0]
        if tec_col not in tec_columns:
            tec_columns[tec_col] = {'matches': 0, 'pairs_tested': 0, 'successful_pairs': 0}
        tec_columns[tec_col]['matches'] += column_performance[pair]['total_matches']
        tec_columns[tec_col]['pairs_tested'] += 1
        if column_performance[pair]['total_matches'] > 0:
            tec_columns[tec_col]['successful_pairs'] += 1
    
    tec_cols = list(tec_columns.keys())
    tec_matches = [tec_columns[col]['matches'] for col in tec_cols]
    tec_success_rate = [tec_columns[col]['successful_pairs'] / tec_columns[col]['pairs_tested'] * 100 
                       for col in tec_cols]
    
    bars = ax2.bar(tec_cols, tec_matches, color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12'])
    ax2.set_ylabel('Gesamte Matches')
    ax2.set_title('TecDoc Spalten: Performance')
    ax2.tick_params(axis='x', rotation=45)
    ax2.set_yscale('log')
    
    # Erfolgsrate als Text
    for i, (bar, rate, matches) in enumerate(zip(bars, tec_success_rate, tec_matches)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{matches:,}\n({rate:.0f}%)', ha='center', va='bottom', fontsize=8)
    
    # 3. CMD Spalten Performance
    ax3 = plt.subplot(3, 3, 3)
    cmd_columns = {}
    for pair in column_performance:
        cmd_col = pair.split(" ↔ ")[1]
        if cmd_col not in cmd_columns:
            cmd_columns[cmd_col] = {'matches': 0, 'pairs_tested': 0, 'successful_pairs': 0}
        cmd_columns[cmd_col]['matches'] += column_performance[pair]['total_matches']
        cmd_columns[cmd_col]['pairs_tested'] += 1
        if column_performance[pair]['total_matches'] > 0:
            cmd_columns[cmd_col]['successful_pairs'] += 1
    
    # Sortiere CMD Spalten nach Performance
    cmd_sorted = sorted(cmd_columns.items(), key=lambda x: x[1]['matches'], reverse=True)
    cmd_cols = [item[0] for item in cmd_sorted]
    cmd_matches = [item[1]['matches'] for item in cmd_sorted]
    cmd_success_rate = [item[1]['successful_pairs'] / item[1]['pairs_tested'] * 100 
                       for item in cmd_sorted]
    
    bars = ax3.barh(range(len(cmd_cols)), cmd_matches, 
                   color=plt.cm.plasma(np.linspace(0, 1, len(cmd_cols))))
    ax3.set_yticks(range(len(cmd_cols)))
    ax3.set_yticklabels([col.replace('_', '\n') for col in cmd_cols], fontsize=8)
    ax3.set_xlabel('Gesamte Matches')
    ax3.set_title('CMD Spalten: Performance')
    ax3.set_xscale('log')
    
    # Werte und Erfolgsrate anzeigen
    for i, (bar, rate, matches) in enumerate(zip(bars, cmd_success_rate, cmd_matches)):
        if matches > 0:
            width = bar.get_width()
            ax3.text(width, bar.get_y() + bar.get_height()/2.,
                    f' {matches:,} ({rate:.0f}%)', ha='left', va='center', fontsize=7)
    
    # 4. Erfolgsrate pro Spaltenpaar
    ax4 = plt.subplot(3, 3, 4)
    success_rates = []
    pair_labels = []
    for pair in pairs_sorted:
        if column_performance[pair]['methods_tested'] > 0:
            rate = column_performance[pair]['successful_methods'] / column_performance[pair]['methods_tested'] * 100
            success_rates.append(rate)
            pair_labels.append(pair.replace(' ↔ ', '\n↔\n'))
    
    bars = ax4.bar(range(len(success_rates)), success_rates, 
                  color=plt.cm.RdYlGn(np.array(success_rates)/100))
    ax4.set_xticks(range(len(pair_labels)))
    ax4.set_xticklabels(pair_labels, rotation=45, ha='right', fontsize=8)
    ax4.set_ylabel('Erfolgsrate (%)')
    ax4.set_title('Erfolgsrate pro Spaltenpaar\n(% der Methoden mit Matches)')
    ax4.set_ylim(0, 100)
    
    # Werte anzeigen
    for bar, rate in zip(bars, success_rates):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{rate:.0f}%', ha='center', va='bottom', fontsize=8)
    
    # 5. Heatmap: Methode vs Spaltenpaar
    ax5 = plt.subplot(3, 3, 5)
    methods = ['Exakt', 'Normalisiert', 'Teilstring', 'Prefix_5']
    heatmap_data = []
    
    for method in methods:
        method_row = []
        for pair in pairs_sorted[:8]:  # Top 8 Paare
            pair_data = column_performance[pair]['methods_detail']
            value = pair_data.get(method, 0)
            method_row.append(value)
        heatmap_data.append(method_row)
    
    # Log-transformierte Werte
    heatmap_array = np.array(heatmap_data)
    heatmap_log = np.log10(heatmap_array + 1)
    
    sns.heatmap(heatmap_log, 
                xticklabels=[p.replace(' ↔ ', '\n↔\n') for p in pairs_sorted[:8]],
                yticklabels=methods,
                annot=heatmap_array,
                fmt='d',
                cmap='YlOrRd',
                ax=ax5,
                cbar_kws={'label': 'log10(Matches + 1)'})
    ax5.set_title('Methoden-Performance pro Spaltenpaar')
    ax5.tick_params(axis='x', rotation=45)
    
    # 6. Beste Methode pro Spaltenpaar
    ax6 = plt.subplot(3, 3, 6)
    best_methods = []
    best_scores = []
    for pair in pairs_sorted:
        if column_performance[pair]['best_score'] > 0:
            best_methods.append(f"{pair}\n({column_performance[pair]['best_method']})")
            best_scores.append(column_performance[pair]['best_score'])
    
    colors_method = {'Exakt': '#e74c3c', 'Teilstring': '#3498db', 'Prefix_5': '#2ecc71', 'Normalisiert': '#f39c12'}
    bar_colors = []
    for pair in pairs_sorted:
        if column_performance[pair]['best_score'] > 0:
            method = column_performance[pair]['best_method']
            bar_colors.append(colors_method.get(method, '#95a5a6'))
    
    bars = ax6.barh(range(len(best_scores)), best_scores, color=bar_colors)
    ax6.set_yticks(range(len(best_methods)))
    ax6.set_yticklabels([m.split('\n')[0].replace(' ↔ ', '\n↔\n') for m in best_methods], fontsize=8)
    ax6.set_xlabel('Beste Score')
    ax6.set_title('Beste Methode pro Spaltenpaar')
    ax6.set_xscale('log')
    
    # 7-9. Detailanalyse für Top-Spalten
    top_tec_cols = sorted(tec_columns.items(), key=lambda x: x[1]['matches'], reverse=True)[:3]
    
    for idx, (col_name, col_data) in enumerate(top_tec_cols):
        ax = plt.subplot(3, 3, 7 + idx)
        
        # Finde alle CMD-Spalten für diese TecDoc-Spalte
        cmd_matches = {}
        for pair in column_performance:
            if pair.startswith(col_name + " ↔ "):
                cmd_col = pair.split(" ↔ ")[1]
                cmd_matches[cmd_col] = column_performance[pair]['total_matches']
        
        if cmd_matches:
            cmd_cols = list(cmd_matches.keys())
            matches = list(cmd_matches.values())
            
            bars = ax.bar(range(len(cmd_cols)), matches, 
                         color=plt.cm.Set3(np.linspace(0, 1, len(cmd_cols))))
            ax.set_xticks(range(len(cmd_cols)))
            ax.set_xticklabels([c.replace('_', '\n') for c in cmd_cols], rotation=45, ha='right', fontsize=8)
            ax.set_ylabel('Matches')
            ax.set_title(f'TecDoc: {col_name}\nMatching mit CMD-Spalten')
            if max(matches) > 10:
                ax.set_yscale('log')
            
            # Werte anzeigen
            for bar, value in zip(bars, matches):
                if value > 0:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{value:,}', ha='center', va='bottom', fontsize=7, rotation=90)
    
    plt.tight_layout()
    plt.savefig('column_pair_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Detaillierte Textausgabe
    print("\n" + "="*100)
    print("DETAILLIERTE SPALTENPAARE-ANALYSE")
    print("="*100)
    
    print("\n🏆 TOP-PERFORMING SPALTENPAARE:")
    print("-" * 60)
    for i, (pair, matches) in enumerate(sorted_pairs[:5]):
        perf = column_performance[pair]
        print(f"{i+1:2d}. {pair}")
        print(f"    Gesamte Matches: {matches:,}")
        print(f"    Beste Methode: {perf['best_method']} ({perf['best_score']:,} Matches)")
        print(f"    Erfolgsrate: {perf['successful_methods']}/{perf['methods_tested']} Methoden ({perf['successful_methods']/perf['methods_tested']*100:.1f}%)")
        print()
    
    print("\n📊 TECDOC SPALTEN RANKING:")
    print("-" * 60)
    for i, (col, data) in enumerate(sorted(tec_columns.items(), key=lambda x: x[1]['matches'], reverse=True)):
        success_rate = data['successful_pairs'] / data['pairs_tested'] * 100
        print(f"{i+1:2d}. {col}")
        print(f"    Gesamte Matches: {data['matches']:,}")
        print(f"    Getestete Paare: {data['pairs_tested']}")
        print(f"    Erfolgreiche Paare: {data['successful_pairs']} ({success_rate:.1f}%)")
        print()
    
    print("\n📋 CMD SPALTEN RANKING:")
    print("-" * 60)
    for i, (col, data) in enumerate(cmd_sorted):
        success_rate = data['successful_pairs'] / data['pairs_tested'] * 100
        print(f"{i+1:2d}. {col}")
        print(f"    Gesamte Matches: {data['matches']:,}")
        print(f"    Getestete Paare: {data['pairs_tested']}")
        print(f"    Erfolgreiche Paare: {data['successful_pairs']} ({success_rate:.1f}%)")
        print()
    
    print("\n🎯 SCHLUSSFOLGERUNGEN:")
    print("-" * 60)
    print("✅ BESTE SPALTENPAARE:")
    best_pairs = [pair for pair, matches in sorted_pairs[:3] if matches > 0]
    for pair in best_pairs:
        print(f"   • {pair}")
    
    print("\n❌ SCHWIERIGE SPALTENPAARE:")
    difficult_pairs = [pair for pair, matches in sorted_pairs if matches == 0]
    for pair in difficult_pairs[:5]:
        print(f"   • {pair}")
    
    print(f"\n📈 EMPFEHLUNGEN FÜR 1:1 MATCHING:")
    print("   • artno ↔ SupplierPtNo: Höchste Priorität (15,644 Matches gesamt)")
    print("   • batchsize1/2 ↔ GrossWeight/Volume: Gute numerische Matches")
    print("   • Brand-Matching schwierig - alternative Ansätze testen")
    print("   • Description-Felder bisher ungenutzt - Potenzial für Fuzzy-Matching")

if __name__ == "__main__":
    analyze_column_pairs()
