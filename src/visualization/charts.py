#!/usr/bin/env python3
"""
Visualisierung-Module für TecDoc-CMD Matching-Analyse
Optimierte, modulare Visualisierungsfunktionen
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

from ..utils.core import Config

# =============================================================================
# PLOT-KONFIGURATION
# =============================================================================

# Matplotlib/Seaborn Setup
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

# Farb-Palette
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72', 
    'accent': '#F18F01',
    'warning': '#C73E1D',
    'success': '#4ECDC4',
    'neutral': '#6C757D'
}

# =============================================================================
# VISUALISIERUNG-KLASSEN
# =============================================================================

class MatchingVisualizer:
    """Zentrale Klasse für Matching-Visualisierungen"""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir) if output_dir else Config.VIS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_method_comparison(self, df: pd.DataFrame, 
                               title: str = "Matching-Methoden Vergleich",
                               filename: str = "method_comparison") -> str:
        """Erstelle Methoden-Vergleichsdiagramm"""
        
        # Gruppiere nach Methoden
        method_stats = df.groupby('Methode')['Matches'].agg(['sum', 'count', 'mean']).reset_index()
        method_stats = method_stats.sort_values('sum', ascending=False)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot 1: Gesamtmatches pro Methode
        bars1 = ax1.bar(method_stats['Methode'], method_stats['sum'], 
                        color=COLORS['primary'], alpha=0.8)
        ax1.set_title('Gesamtmatches pro Methode')
        ax1.set_xlabel('Methode')
        ax1.set_ylabel('Anzahl Matches')
        ax1.tick_params(axis='x', rotation=45)
        
        # Werte auf Balken
        for bar in bars1:
            height = bar.get_height()
            ax1.annotate(f'{int(height):,}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom')
        
        # Plot 2: Durchschnittliche Matches pro Methode
        bars2 = ax2.bar(method_stats['Methode'], method_stats['mean'], 
                        color=COLORS['secondary'], alpha=0.8)
        ax2.set_title('Durchschnittliche Matches pro Methode')
        ax2.set_xlabel('Methode')
        ax2.set_ylabel('Ø Matches pro Spaltenpaar')
        ax2.tick_params(axis='x', rotation=45)
        
        # Werte auf Balken
        for bar in bars2:
            height = bar.get_height()
            ax2.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom')
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # Speichern
        output_path = self.output_dir / f"{filename}.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.savefig(self.output_dir / f"{filename}.pdf", bbox_inches='tight')
        plt.close()
        
        print(f"✅ Methoden-Vergleich erstellt: {output_path}")
        return str(output_path)
    
    def create_column_pairs_heatmap(self, df: pd.DataFrame,
                                  target_col: str = 'CMD_Spalte',
                                  title: str = "Spaltenpaare Heatmap",
                                  filename: str = "column_pairs_heatmap") -> str:
        """Erstelle Heatmap der Spaltenpaare"""
        
        # Pivot-Tabelle erstellen
        if target_col == 'XML_Tag':
            pivot_data = df.groupby(['TecDoc_Spalte', 'XML_Tag'])['Matches'].sum().unstack(fill_value=0)
        else:
            pivot_data = df.groupby(['TecDoc_Spalte', target_col])['Matches'].sum().unstack(fill_value=0)
        
        # Heatmap erstellen
        fig, ax = plt.subplots(figsize=(12, 8))
        
        sns.heatmap(pivot_data, annot=True, fmt='d', cmap='Blues', 
                   cbar_kws={'label': 'Anzahl Matches'}, ax=ax)
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('CMD/XML Felder' if target_col != 'XML_Tag' else 'XML Tags')
        ax.set_ylabel('TecDoc Spalten')
        
        plt.tight_layout()
        
        # Speichern
        output_path = self.output_dir / f"{filename}.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.savefig(self.output_dir / f"{filename}.pdf", bbox_inches='tight')
        plt.close()
        
        print(f"✅ Spaltenpaare-Heatmap erstellt: {output_path}")
        return str(output_path)
    
    def create_performance_dashboard(self, df: pd.DataFrame,
                                   title: str = "Performance Dashboard",
                                   filename: str = "performance_dashboard") -> str:
        """Erstelle umfassendes Performance-Dashboard"""
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Plot 1: Top Spaltenpaare
        if 'CMD_Spalte' in df.columns:
            top_pairs = df.groupby(['TecDoc_Spalte', 'CMD_Spalte'])['Matches'].sum().nlargest(10)
            pair_labels = [f"{pair[0]} → {pair[1]}" for pair in top_pairs.index]
        else:
            top_pairs = df.groupby(['TecDoc_Spalte', 'XML_Tag'])['Matches'].sum().nlargest(10)
            pair_labels = [f"{pair[0]} → {pair[1]}" for pair in top_pairs.index]
        
        ax1.barh(range(len(top_pairs)), top_pairs.values, color=COLORS['primary'])
        ax1.set_yticks(range(len(top_pairs)))
        ax1.set_yticklabels(pair_labels, fontsize=10)
        ax1.set_xlabel('Anzahl Matches')
        ax1.set_title('Top 10 Spaltenpaare')
        ax1.invert_yaxis()
        
        # Plot 2: Methodenverteilung (Pie Chart)
        method_totals = df.groupby('Methode')['Matches'].sum()
        colors_list = list(COLORS.values())[:len(method_totals)]
        
        wedges, texts, autotexts = ax2.pie(method_totals.values, labels=method_totals.index,
                                          autopct='%1.1f%%', colors=colors_list)
        ax2.set_title('Methodenverteilung')
        
        # Plot 3: Chunk-Performance (falls vorhanden)
        if 'Chunk' in df.columns:
            chunk_performance = df.groupby('Chunk')['Matches'].sum()
            ax3.plot(chunk_performance.index, chunk_performance.values, 
                    marker='o', linewidth=2, color=COLORS['accent'])
            ax3.set_xlabel('Chunk Nummer')
            ax3.set_ylabel('Anzahl Matches')
            ax3.set_title('Performance pro Chunk')
            ax3.grid(True, alpha=0.3)
        else:
            ax3.text(0.5, 0.5, 'Keine Chunk-Daten\nverfügbar', 
                    ha='center', va='center', transform=ax3.transAxes)
            ax3.set_title('Chunk-Performance')
        
        # Plot 4: Erfolgsraten-Verteilung
        if 'TecDoc_Anzahl' in df.columns and 'Matches' in df.columns:
            df_success = df[df['Matches'] > 0].copy()
            if 'CMD_Anzahl' in df.columns:
                df_success['Erfolgsrate'] = (df_success['Matches'] / df_success['CMD_Anzahl'] * 100)
            else:
                df_success['Erfolgsrate'] = (df_success['Matches'] / df_success['XML_Anzahl'] * 100)
            
            ax4.hist(df_success['Erfolgsrate'], bins=20, color=COLORS['success'], alpha=0.7)
            ax4.set_xlabel('Erfolgsrate (%)')
            ax4.set_ylabel('Häufigkeit')
            ax4.set_title('Verteilung der Erfolgsraten')
        else:
            ax4.text(0.5, 0.5, 'Keine Erfolgsraten-\nberechnung möglich', 
                    ha='center', va='center', transform=ax4.transAxes)
            ax4.set_title('Erfolgsraten-Verteilung')
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # Speichern
        output_path = self.output_dir / f"{filename}.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.savefig(self.output_dir / f"{filename}.pdf", bbox_inches='tight')
        plt.close()
        
        print(f"✅ Performance-Dashboard erstellt: {output_path}")
        return str(output_path)

# =============================================================================
# EINFACHE VISUALISIERUNGSFUNKTIONEN
# =============================================================================

def create_simple_comparison(df: pd.DataFrame, 
                           output_dir: str = None,
                           title: str = "Einfacher Vergleich") -> str:
    """Erstelle einfache Vergleichsvisualisierung"""
    
    output_dir = Path(output_dir) if output_dir else Config.VIS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Für XML vs CSV unterscheiden
    if 'XML_Tag' in df.columns:
        # XML-Daten: TradeNo vs SupplierPtNo
        tradeno_df = df[df['XML_Tag'] == 'TradeNo'].groupby('Methode')['Matches'].sum()
        supplier_df = df[df['XML_Tag'] == 'SupplierPtNo'].groupby('Methode')['Matches'].sum()
        
        all_methods = list(set(tradeno_df.index) | set(supplier_df.index))
        tradeno_counts = [tradeno_df.get(m, 0) for m in all_methods]
        supplier_counts = [supplier_df.get(m, 0) for m in all_methods]
        
        # Balkendiagramm
        fig, ax = plt.subplots(figsize=(12, 6))
        x = np.arange(len(all_methods))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, tradeno_counts, width, label='TradeNo', 
                      color=COLORS['primary'], alpha=0.8)
        bars2 = ax.bar(x + width/2, supplier_counts, width, label='SupplierPtNo', 
                      color=COLORS['secondary'], alpha=0.8)
        
        ax.set_xlabel('Matching-Methode')
        ax.set_ylabel('Anzahl Matches')
        ax.set_title('TradeNo vs SupplierPtNo - Performance Vergleich')
        ax.set_xticks(x)
        ax.set_xticklabels(all_methods, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    else:
        # CSV-Daten: Methoden-Vergleich
        method_counts = df.groupby('Methode')['Matches'].sum().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(method_counts.index, method_counts.values, 
                     color=COLORS['primary'], alpha=0.8)
        
        ax.set_xlabel('Matching-Methode')
        ax.set_ylabel('Anzahl Matches')
        ax.set_title('Matching-Performance nach Methoden')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)
        
        # Werte auf Balken
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height):,}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3), textcoords="offset points",
                       ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Speichern
    output_path = output_dir / "simple_comparison.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / "simple_comparison.pdf", bbox_inches='tight')
    plt.close()
    
    print(f"✅ Einfache Visualisierung erstellt: {output_path}")
    return str(output_path)

# =============================================================================
# HAUPTFUNKTIONEN
# =============================================================================

def create_all_visualizations(df: pd.DataFrame, 
                            output_dir: str = None,
                            title_prefix: str = "") -> List[str]:
    """Erstelle alle Standardvisualisierungen"""
    
    visualizer = MatchingVisualizer(output_dir)
    created_files = []
    
    print("🎨 Erstelle Visualisierungen...")
    
    # Methoden-Vergleich
    try:
        file_path = visualizer.create_method_comparison(
            df, title=f"{title_prefix}Methoden-Vergleich", 
            filename="method_comparison"
        )
        created_files.append(file_path)
    except Exception as e:
        print(f"⚠️ Fehler bei Methoden-Vergleich: {e}")
    
    # Spaltenpaare-Heatmap
    try:
        target_col = 'XML_Tag' if 'XML_Tag' in df.columns else 'CMD_Spalte'
        file_path = visualizer.create_column_pairs_heatmap(
            df, target_col=target_col,
            title=f"{title_prefix}Spaltenpaare-Heatmap", 
            filename="column_pairs_heatmap"
        )
        created_files.append(file_path)
    except Exception as e:
        print(f"⚠️ Fehler bei Spaltenpaare-Heatmap: {e}")
    
    # Performance-Dashboard
    try:
        file_path = visualizer.create_performance_dashboard(
            df, title=f"{title_prefix}Performance-Dashboard", 
            filename="performance_dashboard"
        )
        created_files.append(file_path)
    except Exception as e:
        print(f"⚠️ Fehler bei Performance-Dashboard: {e}")
    
    # Einfache Visualisierung
    try:
        file_path = create_simple_comparison(
            df, output_dir=visualizer.output_dir,
            title=f"{title_prefix}Einfacher Vergleich"
        )
        created_files.append(file_path)
    except Exception as e:
        print(f"⚠️ Fehler bei einfacher Visualisierung: {e}")
    
    print(f"🎉 {len(created_files)} Visualisierungen erstellt!")
    return created_files
