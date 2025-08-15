#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fuzzy Matching-Ergebnisse Tabelle
Erstellt eine detaillierte Tabelle basierend auf den fuzzy_methods_overview Werten

Autor: DHBW Projektarbeit
Datum: August 2025
"""

import pandas as pd
import numpy as np

def create_fuzzy_results_table():
    """Erstellt detaillierte Tabelle mit Fuzzy Matching-Ergebnissen"""

 # Daten aus unified_fuzzy_data.py - einheitliche Werte
    data = {
    'article_number': {'Levenshtein': 31250, 'Jaro-Winkler': 29100, 'Probabilistisch': 22400, 'Phonetisch': 8950},
    'tec_doc_article_number': {'Levenshtein': 27850, 'Jaro-Winkler': 24200, 'Probabilistisch': 18650, 'Phonetisch': 7200},
    'ean': {'Levenshtein': 6850, 'Jaro-Winkler': 4200, 'Probabilistisch': 2100, 'Phonetisch': 950},
    'SupplierPtNo': {'Levenshtein': 4120, 'Jaro-Winkler': 3650, 'Probabilistisch': 2200, 'Phonetisch': 850},
    'TradeNo': {'Levenshtein': 3890, 'Jaro-Winkler': 3200, 'Probabilistisch': 2890, 'Phonetisch': 750},
    'Brand': {'Levenshtein': 2150, 'Jaro-Winkler': 1650, 'Probabilistisch': 980, 'Phonetisch': 450}
    }

 # Gesamtzahl der Datensätze für Prozentberechnung
    total_records = 70000 # Angenommene Gesamtzahl

 # Tabelle erstellen
    table_rows = []

 # CSV Felder (erste 3)
    csv_fields = ['article_number', 'tec_doc_article_number', 'ean']
    xml_fields = ['SupplierPtNo', 'TradeNo', 'Brand']

    for field in csv_fields:
        if field in data:
            for method, matches in data[field].items():
                if matches > 0: # Nur Einträge mit Matches
                success_rate = (matches / total_records) * 100
                table_rows.append({
                'Quelle': 'CSV',
                'Zielspalte': field,
                'Methode': method,
                'Matches': f"{matches:,}".replace(",", "."),
                'Erfolgsrate (%)': f"{success_rate:.1f}"
                })

 # XML Felder
                for field in xml_fields:
                    if field in data:
                        for method, matches in data[field].items():
                            if matches > 0: # Nur Einträge mit Matches
                            success_rate = (matches / total_records) * 100
                            table_rows.append({
                            'Quelle': 'XML',
                            'Zielspalte': field,
                            'Methode': method,
                            'Matches': f"{matches:,}".replace(",", "."),
                            'Erfolgsrate (%)': f"{success_rate:.1f}"
                            })

 # DataFrame erstellen
                            df = pd.DataFrame(table_rows)

 # Nach Matches sortieren (absteigend)
                            df = df.sort_values('Matches', key=lambda x: x.str.replace('.', '').astype(int), ascending=False)

                            return df

def save_table_formats(df):
    """Speichert die Tabelle in verschiedenen Formaten"""

 # CSV speichern
    df.to_csv('results/tables/fuzzy_matching_results.csv',
    index=False, encoding='utf-8', sep=';')

 # Excel speichern (falls openpyxl verfügbar)
    try:
        df.to_excel('results/tables/fuzzy_matching_results.xlsx',
        index=False, sheet_name='Fuzzy_Ergebnisse')
        print("[OK] Excel-Datei erstellt!")
        except ImportError:
            print("[WARNING] Excel-Export nicht verfügbar (openpyxl fehlt)")

 # Einfache Textdatei für Dokumentation
            with open('results/tables/fuzzy_matching_results.txt', 'w', encoding='utf-8') as f:
                f.write("# Fuzzy Matching-Ergebnisse\n\n")
                f.write("Basierend auf fuzzy_methods_overview Daten\n\n")
                f.write(df.to_string(index=False))

 # Schöne Konsolen-Ausgabe
                print("\n" + "="*80)
                print(" FUZZY MATCHING-ERGEBNISSE TABELLE")
                print("="*80)
                print(df.to_string(index=False))
                print("="*80)

 # Zusammenfassung
                total_matches = df['Matches'].str.replace('.', '').astype(int).sum()
                print(f"\n ZUSAMMENFASSUNG:")
                print(f" • Gesamte Matches: {total_matches:,}")
                print(f" • Anzahl Methoden: {df['Methode'].nunique()}")
                print(f" • Anzahl Felder: {df['Zielspalte'].nunique()}")
                print(f" • Beste Einzelergebnis: {df.iloc[0]['Zielspalte']} mit {df.iloc[0]['Matches']} Matches")
                print(f" • Beste Methode: {df.groupby('Methode')['Matches'].apply(lambda x: x.str.replace('.', '').astype(int).sum()).idxmax()}")

                return df

def main():
    """Hauptfunktion"""
    print(" Erstelle Fuzzy Matching-Ergebnisse Tabelle...")

 # Tabelle erstellen
    df = create_fuzzy_results_table()

 # In verschiedenen Formaten speichern
    save_table_formats(df)

    print(f"\n Dateien gespeichert:")
    print(f" • results/tables/fuzzy_matching_results.csv")
    print(f" • results/tables/fuzzy_matching_results.xlsx (falls möglich)")
    print(f" • results/tables/fuzzy_matching_results.txt")

    if __name__ == "__main__":
        main()
