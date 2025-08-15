#!/usr/bin/env python3
import pandas as pd

# Deterministische Ergebnisse berechnen
df = pd.read_csv('results/tables/deterministic_matching_results.csv', sep=';')
# Matches-Spalte bereinigen (Leerzeichen entfernen)
df['Matches'] = df['Matches'].astype(str).str.replace(' ', '').astype(int)

print(f"📊 DETERMINISTISCHE MATCHING-ERGEBNISSE:")
print(f"   Gesamte Matches: {df['Matches'].sum():,}")
print(f"   CSV Matches: {df[df['Quelle'] == 'TecCMD-CSV']['Matches'].sum():,}")
print(f"   XML Matches: {df[df['Quelle'] == 'TecCMD-XML']['Matches'].sum():,}")
print(f"   Anzahl Verfahren: {df['Methode'].nunique()}")
print(f"   Anzahl TecDoc-Felder: {df['TecDoc-Feld'].nunique()}")
print(f"   Anzahl Ziel-Felder: {df['Ziel-Feld'].nunique()}")

# Fuzzy Ergebnisse aus unified_fuzzy_data
from unified_fuzzy_data import get_fuzzy_data
fuzzy_data = get_fuzzy_data()

csv_total = sum(sum(fuzzy_data[field].values()) for field in ['article_number', 'tec_doc_article_number', 'ean'])
xml_total = sum(sum(fuzzy_data[field].values()) for field in ['SupplierPtNo', 'TradeNo', 'Brand'])

print(f"\n📊 FUZZY MATCHING-ERGEBNISSE:")
print(f"   Gesamte Matches: {csv_total + xml_total:,}")
print(f"   CSV Matches: {csv_total:,}")
print(f"   XML Matches: {xml_total:,}")
print(f"   Anzahl Verfahren: 4 (Levenshtein, Jaro-Winkler, Probabilistisch, Phonetisch)")

print(f"\n📏 SAMPLE-KONFIGURATION:")
print(f"   Sample-Größe: 70.000 Datensätze (statt 40GB)")
print(f"   Chunk-Größe: 10.000 Datensätze pro Iteration")
print(f"   Iterationen: 5 Chunks (deterministic) / 2 Chunks (fuzzy)")
print(f"   Duplikat-Kontrolle: Set-basierte (TecDoc-Wert, CMD-Wert)-Paare")
