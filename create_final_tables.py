#!/usr/bin/env python3
"""
Finale Tabellen-Generator
Erstellt finale duplikatfreie Ergebnistabellen aus allen Analysen
"""

import sys
import pandas as pd
from pathlib import Path

# Füge src-Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.core import setup_environment, save_results_table, Config

def create_final_csv_table() -> pd.DataFrame:
    """Erstelle finale CSV-Tabelle"""
    print("📊 Erstelle finale CSV-Tabelle...")
    
    try:
        # Lade deterministische CSV-Ergebnisse
        det_file = Config.TABLES_DIR / "deterministic_csv_results.csv"
        if det_file.exists():
            df = pd.read_csv(det_file)
            
            # Gruppiere und aggregiere
            final_table = df.groupby(['TecDoc_Spalte', 'CMD_Spalte', 'Methode']).agg({
                'Matches': 'sum',
                'TecDoc_Anzahl': 'first',
                'CMD_Anzahl': 'first'
            }).reset_index()
            
            # Berechne Anteile
            final_table['Anteil_TecDoc_%'] = (final_table['Matches'] / final_table['TecDoc_Anzahl'] * 100).round(2)
            final_table['Anteil_CMD_%'] = (final_table['Matches'] / final_table['CMD_Anzahl'] * 100).round(2)
            
            # Sortiere nach Matches
            final_table = final_table.sort_values('Matches', ascending=False)
            
            print(f"✅ CSV-Tabelle: {len(final_table)} Spaltenpaare, {final_table['Matches'].sum():,} Matches")
            return final_table
        else:
            print("⚠️ Keine CSV-Ergebnisse gefunden")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"❌ Fehler bei CSV-Tabelle: {e}")
        return pd.DataFrame()

def create_final_xml_table() -> pd.DataFrame:
    """Erstelle finale XML-Tabelle"""
    print("📊 Erstelle finale XML-Tabelle...")
    
    try:
        # Lade deterministische XML-Ergebnisse
        det_file = Config.TABLES_DIR / "deterministic_xml_results.csv"
        if det_file.exists():
            df = pd.read_csv(det_file)
            
            # Gruppiere und aggregiere
            final_table = df.groupby(['TecDoc_Spalte', 'XML_Tag', 'Methode']).agg({
                'Matches': 'sum',
                'TecDoc_Anzahl': 'first',
                'XML_Anzahl': 'first'
            }).reset_index()
            
            # Berechne Anteile
            final_table['Anteil_TecDoc_%'] = (final_table['Matches'] / final_table['TecDoc_Anzahl'] * 100).round(2)
            final_table['Anteil_XML_%'] = (final_table['Matches'] / final_table['XML_Anzahl'] * 100).round(2)
            
            # Sortiere nach Matches
            final_table = final_table.sort_values('Matches', ascending=False)
            
            print(f"✅ XML-Tabelle: {len(final_table)} Feld-Paare, {final_table['Matches'].sum():,} Matches")
            return final_table
        else:
            print("⚠️ Keine XML-Ergebnisse gefunden")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"❌ Fehler bei XML-Tabelle: {e}")
        return pd.DataFrame()

def create_combined_summary(csv_table: pd.DataFrame, xml_table: pd.DataFrame) -> pd.DataFrame:
    """Erstelle kombinierte Zusammenfassung"""
    print("📊 Erstelle kombinierte Zusammenfassung...")
    
    try:
        # Fuzzy-Ergebnisse laden (optional)
        fuzzy_csv_matches = 0
        fuzzy_xml_matches = 0
        
        fuzzy_csv_file = Config.TABLES_DIR / "fuzzy_csv_results.csv"
        if fuzzy_csv_file.exists():
            fuzzy_csv_df = pd.read_csv(fuzzy_csv_file)
            fuzzy_csv_matches = fuzzy_csv_df['Matches'].sum()
        
        fuzzy_xml_file = Config.TABLES_DIR / "fuzzy_xml_results.csv"
        if fuzzy_xml_file.exists():
            fuzzy_xml_df = pd.read_csv(fuzzy_xml_file)
            fuzzy_xml_matches = fuzzy_xml_df['Matches'].sum()
        
        # Zusammenfassung erstellen
        summary_data = []
        
        if not csv_table.empty:
            csv_top_method = csv_table.groupby('Methode')['Matches'].sum().idxmax()
            csv_top_matches = csv_table.groupby('Methode')['Matches'].sum().max()
            
            summary_data.append({
                'Datenquelle': 'TecCMD-CSV (Deterministisch)',
                'Spaltenpaare': len(csv_table),
                'Gesamtmatches': csv_table['Matches'].sum(),
                'Top_Methode': csv_top_method,
                'Top_Methode_Matches': csv_top_matches
            })
        
        if fuzzy_csv_matches > 0:
            summary_data.append({
                'Datenquelle': 'TecCMD-CSV (Fuzzy)',
                'Spaltenpaare': 'N/A',
                'Gesamtmatches': fuzzy_csv_matches,
                'Top_Methode': 'Fuzzy',
                'Top_Methode_Matches': fuzzy_csv_matches
            })
        
        if not xml_table.empty:
            xml_top_method = xml_table.groupby('Methode')['Matches'].sum().idxmax()
            xml_top_matches = xml_table.groupby('Methode')['Matches'].sum().max()
            
            summary_data.append({
                'Datenquelle': 'TecCMD-XML (Deterministisch)',
                'Spaltenpaare': len(xml_table),
                'Gesamtmatches': xml_table['Matches'].sum(),
                'Top_Methode': xml_top_method,
                'Top_Methode_Matches': xml_top_matches
            })
        
        if fuzzy_xml_matches > 0:
            summary_data.append({
                'Datenquelle': 'TecCMD-XML (Fuzzy)',
                'Spaltenpaare': 'N/A',
                'Gesamtmatches': fuzzy_xml_matches,
                'Top_Methode': 'Fuzzy',
                'Top_Methode_Matches': fuzzy_xml_matches
            })
        
        summary_df = pd.DataFrame(summary_data)
        print(f"✅ Zusammenfassung: {len(summary_df)} Datenquellen")
        return summary_df
        
    except Exception as e:
        print(f"❌ Fehler bei Zusammenfassung: {e}")
        return pd.DataFrame()

def main():
    """Hauptfunktion"""
    print("🎯 FINALE TABELLEN GENERATOR")
    print("=" * 50)
    
    # Setup
    setup_environment()
    
    # Erstelle finale Tabellen
    csv_table = create_final_csv_table()
    xml_table = create_final_xml_table()
    
    # Speichere Tabellen
    if not csv_table.empty:
        save_results_table(csv_table, "finale_teccmd_csv_tabelle.csv")
        
        # Zeige Top 5
        print("\n🏆 TOP 5 CSV-SPALTENPAARE:")
        for _, row in csv_table.head(5).iterrows():
            print(f"   {row['TecDoc_Spalte']:15} → {row['CMD_Spalte']:25} ({row['Methode']:12}): {row['Matches']:6,} Matches")
    
    if not xml_table.empty:
        save_results_table(xml_table, "finale_teccmd_xml_tabelle.csv")
        
        # Zeige Top 5
        print("\n🏆 TOP 5 XML-FELDPAARE:")
        for _, row in xml_table.head(5).iterrows():
            print(f"   {row['TecDoc_Spalte']:15} → {row['XML_Tag']:25} ({row['Methode']:12}): {row['Matches']:6,} Matches")
    
    # Erstelle Zusammenfassung
    if not csv_table.empty or not xml_table.empty:
        summary = create_combined_summary(csv_table, xml_table)
        if not summary.empty:
            save_results_table(summary, "finale_zusammenfassung.csv")
            
            print("\n📈 FINALE ZUSAMMENFASSUNG:")
            print("=" * 50)
            for _, row in summary.iterrows():
                print(f"   {row['Datenquelle']:30}: {str(row['Spaltenpaare']):>4} Paare, {row['Gesamtmatches']:>7,} Matches")
    
    print(f"\n🎉 Finale Tabellen erstellt in: {Config.TABLES_DIR}")

if __name__ == "__main__":
    main()
