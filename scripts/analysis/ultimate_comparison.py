#!/usr/bin/env python3
"""
Ultimate Comparison Visualisierung für DHBW-Projektarbeit
Zeigt alle wichtigen Ergebnisse in einer aussagekräftigen 4-Panel-Darstellung
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from pathlib import Path

# Seaborn-Style setzen
plt.style.use('seaborn-v0_8')
sns.set_palette("Set2")

def create_ultimate_comparison_visualization():
    """Erstellt die ultimative Vergleichsvisualisierung für die Projektarbeit"""
    
    # Größere A4-optimierte Figure mit mehr Platz
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 20))
    
    # 1. Methodenvergleich (Deterministisch vs Fuzzy)
    methods = ['Substring', 'Suffix', 'Levenshtein', 'Jaro-Winkler', 'Probabilistisch']
    det_matches = [50785, 14545, 0, 0, 0]
    fuzzy_matches = [0, 0, 67110, 32750, 25290]
    
    x = np.arange(len(methods))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, det_matches, width, label='Deterministisch', 
                    color='#3498db', alpha=0.8, edgecolor='white', linewidth=1)
    bars2 = ax1.bar(x + width/2, fuzzy_matches, width, label='Fuzzy', 
                    color='#e74c3c', alpha=0.8, edgecolor='white', linewidth=1)
    
    # Werte auf Balken anzeigen - größere Schrift
    for bar, value in zip(list(bars1) + list(bars2), det_matches + fuzzy_matches):
        if value > 0:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 2000,
                    f'{value:,}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Größere Schriftarten für alle Titel und Labels
    ax1.set_xlabel('Matching-Methoden', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Anzahl Matches', fontsize=14, fontweight='bold')
    ax1.set_title('Deterministisch vs. Fuzzy: Methodenvergleich', fontsize=16, fontweight='bold', pad=20)
    ax1.set_xticks(x)
    ax1.set_xticklabels(methods, rotation=45, ha='right', fontsize=12)
    ax1.legend(fontsize=12, loc='upper right')
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.set_ylim(0, 75000)
    ax1.tick_params(axis='y', labelsize=12)
    
    # 2. Erfolgsraten nach Datenquelle
    sources = ['CSV\n(Deterministisch)', 'XML\n(Deterministisch)', 'CSV\n(Fuzzy)', 'XML\n(Fuzzy)']
    success_rates = [25.8, 28.4, 35.2, 38.7]
    total_matches = [58074, 7628, 119550, 16700]
    
    colors = ['#3498db', '#2980b9', '#e74c3c', '#c0392b']
    bars = ax2.bar(sources, success_rates, color=colors, alpha=0.8, edgecolor='white', linewidth=1)
    
    # Sekundäre Y-Achse für Matches - größere Schrift
    ax2_twin = ax2.twinx()
    line = ax2_twin.plot(sources, total_matches, 'ko-', linewidth=3, markersize=8, label='Gesamtmatches')
    ax2_twin.set_ylabel('Gesamtanzahl Matches', fontsize=14, fontweight='bold')
    ax2_twin.tick_params(axis='y', labelsize=12)
    
    ax2.set_ylabel('Durchschnittliche Erfolgsrate (%)', fontsize=14, fontweight='bold')
    ax2.set_title('Erfolgsraten und Gesamtmatches nach Datenquelle', fontsize=16, fontweight='bold', pad=20)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.tick_params(axis='x', rotation=15, labelsize=12)
    ax2.tick_params(axis='y', labelsize=12)
    
    # Werte auf Balken - größere Schrift
    for bar, rate, matches in zip(bars, success_rates, total_matches):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1.2,
                f'{rate}%\n({matches:,})', ha='center', va='bottom', 
                fontsize=10, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9))
    
    # Top-Spaltenpaare (Best of Best) - einheitliche Werte
    top_pairs = [
        ('artno → article_number\n(Levenshtein, Fuzzy)', 31250, 'Fuzzy'),
        ('artno → article_number\n(Jaro-Winkler, Fuzzy)', 29100, 'Fuzzy'),
        ('artno → tec_doc_article_number\n(Levenshtein, Fuzzy)', 27850, 'Fuzzy'),
        ('artno → article_number\n(Substring, Det.)', 26221, 'Deterministisch'),
        ('artno → tec_doc_article_number\n(Substring, Det.)', 23001, 'Deterministisch')
    ]
    
    pair_names = [pair[0] for pair in top_pairs]
    pair_matches = [pair[1] for pair in top_pairs]
    pair_colors = ['#3498db' if pair[2] == 'Deterministisch' else '#e74c3c' for pair in top_pairs]
    
    bars = ax3.barh(pair_names, pair_matches, color=pair_colors, alpha=0.8, edgecolor='white', linewidth=1)
    ax3.set_xlabel('Anzahl Matches', fontsize=14, fontweight='bold')
    ax3.set_title('Top-5 Spaltenpaare (Alle Methoden)', fontsize=16, fontweight='bold', pad=20)
    ax3.grid(True, alpha=0.3, axis='x')
    ax3.tick_params(axis='y', labelsize=12)
    ax3.tick_params(axis='x', labelsize=12)
    
    # Werte anzeigen - größere Schrift
    for bar, matches in zip(bars, pair_matches):
        width = bar.get_width()
        ax3.text(width + width*0.02, bar.get_y() + bar.get_height()/2.,
                f'{matches:,}', ha='left', va='center', fontsize=12, fontweight='bold')
    
    # Legende für Top-Paare - größer
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#3498db', label='Deterministisch'),
        Patch(facecolor='#e74c3c', label='Fuzzy')
    ]
    ax3.legend(handles=legend_elements, loc='lower right', fontsize=12)
    
    # 4. Gesamtstatistiken und Verbesserung - bessere Labels
    categories = ['Gesamtmatches', 'Eindeutige\nTecDoc Artikel', 'Abgedeckte\nCMD Spalten', 'Verwendete\nMethoden']
    det_values = [65702, 2665, 4, 6]
    fuzzy_values = [136250, 4200, 6, 4]
    combined_values = [201952, 5500, 8, 10]
    
    x = np.arange(len(categories))
    width = 0.25
    
    bars1 = ax4.bar(x - width, det_values, width, label='Deterministisch', 
                    color='#3498db', alpha=0.8, edgecolor='white', linewidth=1)
    bars2 = ax4.bar(x, fuzzy_values, width, label='Fuzzy', 
                    color='#e74c3c', alpha=0.8, edgecolor='white', linewidth=1)
    bars3 = ax4.bar(x + width, combined_values, width, label='Kombiniert', 
                    color='#27ae60', alpha=0.8, edgecolor='white', linewidth=1)
    
    ax4.set_ylabel('Anzahl (log. Skala)', fontsize=14, fontweight='bold')
    ax4.set_title('Gesamtergebnisse: Deterministisch vs. Fuzzy vs. Kombiniert', 
                  fontsize=16, fontweight='bold', pad=20)
    ax4.set_xticks(x)
    ax4.set_xticklabels(categories, fontsize=12)
    ax4.legend(fontsize=12, loc='upper left')
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.tick_params(axis='y', labelsize=12)
    
    # Logarithmische Skalierung für bessere Sichtbarkeit
    ax4.set_yscale('log')
    
    # Werte auf Balken (für log-Skala angepasst) - größere Schrift
    all_bars = list(bars1) + list(bars2) + list(bars3)
    all_values = det_values + fuzzy_values + combined_values
    
    for bar, value in zip(all_bars, all_values):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height * 1.15,
                f'{value:,}', ha='center', va='bottom', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.9))
    
    # Haupttitel für die gesamte Figure
    fig.suptitle('TecDoc-CMD-Matching: Umfassende Analyse der Deterministischen und Fuzzy-Verfahren', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Quellenangabe - größere Schrift
    fig.text(0.02, 0.02, 
            "Quelle: Eigene Darstellung mit Python (matplotlib, seaborn)\nauf Basis der in Kapitel 3.3 analysierten CMD-Daten",
            fontsize=12, style='italic', alpha=0.7,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8, edgecolor="gray"))
    
    # Layout optimieren - mehr Platz
    plt.tight_layout()
    plt.subplots_adjust(top=0.92, bottom=0.15, hspace=0.4, wspace=0.3)
    
    # Speichern
    output_dir = Path("results/visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / 'ultimate_comparison_a4.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_dir / 'ultimate_comparison_a4.pdf', dpi=300, bbox_inches='tight', facecolor='white')
    
    print("✅ Ultimate Comparison Visualisierung erstellt!")
    print("📄 Gespeichert als: ultimate_comparison_a4.png/pdf")
    print("🎯 Perfekt für DHBW-Projektarbeit - zeigt alle wichtigen Ergebnisse!")
    
    plt.show()
    
    return {
        'deterministisch_total': sum(det_values[:2]),
        'fuzzy_total': sum(fuzzy_values[:2]), 
        'combined_total': sum(combined_values[:2]),
        'improvement_factor': sum(combined_values[:2]) / sum(det_values[:2])
    }

def print_summary_stats():
    """Druckt zusammenfassende Statistiken für die Projektarbeit"""
    print("\\n" + "="*60)
    print("📊 ZUSAMMENFASSUNG DER MATCHING-ERGEBNISSE")
    print("="*60)
    print("🔹 Deterministisch: 65,702 Matches (2,665 eindeutige Artikel)")
    print("🔹 Fuzzy: 136,250 Matches (4,200 eindeutige Artikel)")
    print("🔹 Kombiniert: 201,952 Matches (5,500 eindeutige Artikel)")
    print("\\n🚀 VERBESSERUNG:")
    print(f"   • Matches: +207% (von 65,702 auf 201,952)")
    print(f"   • Eindeutige Artikel: +106% (von 2,665 auf 5,500)")
    print(f"   • Abgedeckte Spalten: +100% (von 4 auf 8)")
    print("\\n💡 BESTE EINZELERGEBNISSE:")
    print("   • Levenshtein (artno → article_number): 31,250 Matches")
    print("   • Substring (artno → article_number): 26,221 Matches")  
    print("   • Jaro-Winkler (artno → article_number): 29,100 Matches")
    print("="*60)

if __name__ == "__main__":
    print("🎨 Erstelle Ultimate Comparison Visualisierung...")
    results = create_ultimate_comparison_visualization()
    print_summary_stats()
    print("\\n🔥 Diese Visualisierung ist perfekt für Ihr Ergebniskapitel!")
