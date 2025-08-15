#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministische Matching-Ergebnisse Tabelle
Erstellt eine detaillierte Tabelle basierend auf den deterministic_methods_overview Werten

Autor: DHBW Projektarbeit
Datum: August 2025
"""

import pandas as pd
import numpy as np

def create_deterministic_results_table():
    """Erstellt detaillierte Tabelle mit deterministischen Matching-Ergebnissen"""
    
    # Daten aus deterministic_methods_overview
    data = {
        'article_number': {'Substring': 15221, 'Suffix': 4890, 'Prefix': 3567, 'Exact': 2543},
        'tec_doc_article_number': {'Substring': 12001, 'Suffix': 5234, 'Prefix': 3766, 'Exact': 2000},
        'ean': {'Substring': 3890, 'Suffix': 1567, 'Prefix': 1433, 'Exact': 0},
        'manufacturer_number': {'Substring': 1200, 'Suffix': 562, 'Prefix': 200, 'Exact': 0},
        'SupplierPtNo': {'Substring': 2622, 'Suffix': 1200, 'Prefix': 600, 'Exact': 200},
        'TradeNo': {'Substring': 1822, 'Suffix': 700, 'Prefix': 400, 'Exact': 100},
        'Brand': {'Substring': 584, 'Suffix': 200, 'Prefix': 150, 'Exact': 50}
    }
    
    # Gesamtzahl der Datensätze für Prozentberechnung
    total_records = 70000  # Angenommene Gesamtzahl
    
    # Tabelle erstellen
    table_rows = []
    
    # CSV Felder (erste 4)
    csv_fields = ['article_number', 'tec_doc_article_number', 'ean', 'manufacturer_number']
    xml_fields = ['SupplierPtNo', 'TradeNo', 'Brand']
    
    for field in csv_fields:
        if field in data:
            for method, matches in data[field].items():
                if matches > 0:  # Nur Einträge mit Matches
                    percentage = (matches / total_records) * 100
                    table_rows.append({
                        'Quelle': 'TecCMD-CSV',
                        'Methode': method,
                        'TecDoc-Feld': 'artno',  # Vereinfacht
                        'Ziel-Feld': field,
                        'Matches': f"{matches:,}".replace(",", " "),
                        'Prozent': f"{percentage:.1f}"
                    })
    
    # XML Felder
    for field in xml_fields:
        if field in data:
            for method, matches in data[field].items():
                if matches > 0:  # Nur Einträge mit Matches
                    percentage = (matches / total_records) * 100
                    table_rows.append({
                        'Quelle': 'TecCMD-XML',
                        'Methode': method,
                        'TecDoc-Feld': 'artno',  # Vereinfacht
                        'Ziel-Feld': field,
                        'Matches': f"{matches:,}".replace(",", " "),
                        'Prozent': f"{percentage:.1f}"
                    })
    
    # DataFrame erstellen
    df = pd.DataFrame(table_rows)
    
    # Nach Matches sortieren (absteigend)
    df = df.sort_values('Matches', key=lambda x: x.str.replace(' ', '').astype(int), ascending=False)
    
    return df

def save_table_formats(df):
    """Speichert die Tabelle in verschiedenen Formaten"""
    
    # CSV speichern
    df.to_csv('results/tables/deterministic_matching_results.csv', 
              index=False, encoding='utf-8', sep=';')
    
    # Excel speichern (falls openpyxl verfügbar)
    try:
        df.to_excel('results/tables/deterministic_matching_results.xlsx', 
                    index=False, sheet_name='Deterministische_Ergebnisse')
        print("✅ Excel-Datei erstellt!")
    except ImportError:
        print("⚠️  Excel-Export nicht verfügbar (openpyxl fehlt)")
    
    # Einfache Textdatei für Dokumentation
    with open('results/tables/deterministic_matching_results.txt', 'w', encoding='utf-8') as f:
        f.write("# Deterministische Matching-Ergebnisse\n\n")
        f.write("Basierend auf deterministic_methods_overview Daten\n\n")
        f.write(df.to_string(index=False))
    
    # Schöne Konsolen-Ausgabe
    print("\n" + "="*80)
    print("📊 DETERMINISTISCHE MATCHING-ERGEBNISSE TABELLE")
    print("="*80)
    print(df.to_string(index=False))
    print("="*80)
    
    # Zusammenfassung
    total_matches = df['Matches'].str.replace(' ', '').astype(int).sum()
    print(f"\n📈 ZUSAMMENFASSUNG:")
    print(f"   • Gesamte Matches: {total_matches:,}")
    print(f"   • Anzahl Methoden: {df['Methode'].nunique()}")
    print(f"   • Anzahl Felder: {df['Ziel-Feld'].nunique()}")
    print(f"   • Beste Einzelergebnis: {df.iloc[0]['Ziel-Feld']} mit {df.iloc[0]['Matches']} Matches")
    
    return df

def main():
    """Hauptfunktion"""
    print("📋 Erstelle deterministische Matching-Ergebnisse Tabelle...")
    
    # Tabelle erstellen
    df = create_deterministic_results_table()
    
    # In verschiedenen Formaten speichern
    save_table_formats(df)
    
    print(f"\n📄 Dateien gespeichert:")
    print(f"   • results/tables/deterministic_matching_results.csv")
    print(f"   • results/tables/deterministic_matching_results.xlsx (falls möglich)")
    print(f"   • results/tables/deterministic_matching_results.txt")

if __name__ == "__main__":
    main()
