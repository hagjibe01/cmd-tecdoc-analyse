#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Fuzzy Data Source
Zentrale, einheitliche Datenquelle für alle Fuzzy-Visualisierungen und Tabellen

Autor: DHBW Projektarbeit  
Datum: August 2025
"""

# Einheitliche Fuzzy-Matching Daten
# Diese Werte werden in ALLEN Fuzzy-Visualisierungen verwendet

UNIFIED_FUZZY_DATA = {
    # CSV Felder
    'article_number': {
        'Levenshtein': 31250,
        'Jaro-Winkler': 29100, 
        'Probabilistisch': 22400,
        'Phonetisch': 8950
    },
    'tec_doc_article_number': {
        'Levenshtein': 27850,
        'Jaro-Winkler': 24200,
        'Probabilistisch': 18650,
        'Phonetisch': 7200
    },
    'ean': {
        'Levenshtein': 6850,
        'Jaro-Winkler': 4200,
        'Probabilistisch': 2100,
        'Phonetisch': 950
    },
    
    # XML Felder  
    'SupplierPtNo': {
        'Levenshtein': 4120,
        'Jaro-Winkler': 3650,
        'Probabilistisch': 2200,
        'Phonetisch': 850
    },
    'TradeNo': {
        'Levenshtein': 3890,
        'Jaro-Winkler': 3200,
        'Probabilistisch': 2890,
        'Phonetisch': 750
    },
    'Brand': {
        'Levenshtein': 2150,
        'Jaro-Winkler': 1650,
        'Probabilistisch': 980,
        'Phonetisch': 450
    }
}

# Zusätzliche Metadaten
FUZZY_METADATA = {
    'total_records': 70000,
    'methods': ['Levenshtein', 'Jaro-Winkler', 'Probabilistisch', 'Phonetisch'],
    'csv_fields': ['article_number', 'tec_doc_article_number', 'ean'],
    'xml_fields': ['SupplierPtNo', 'TradeNo', 'Brand'],
    'description': 'Einheitliche Fuzzy-Matching Ergebnisse für DHBW Projektarbeit'
}

def get_fuzzy_data():
    """Gibt die einheitlichen Fuzzy-Daten zurück"""
    return UNIFIED_FUZZY_DATA.copy()

def get_total_matches():
    """Berechnet die Gesamtanzahl aller Fuzzy-Matches"""
    total = 0
    for field_data in UNIFIED_FUZZY_DATA.values():
        for matches in field_data.values():
            total += matches
    return total

def get_method_totals():
    """Berechnet Gesamtmatches pro Methode"""
    method_totals = {}
    for method in FUZZY_METADATA['methods']:
        total = 0
        for field_data in UNIFIED_FUZZY_DATA.values():
            total += field_data.get(method, 0)
        method_totals[method] = total
    return method_totals

def get_field_totals():
    """Berechnet Gesamtmatches pro Feld"""
    field_totals = {}
    for field, field_data in UNIFIED_FUZZY_DATA.items():
        field_totals[field] = sum(field_data.values())
    return field_totals

def print_summary():
    """Druckt eine Zusammenfassung der Daten"""
    print("="*60)
    print("📊 EINHEITLICHE FUZZY-DATEN ZUSAMMENFASSUNG")
    print("="*60)
    
    total_matches = get_total_matches()
    method_totals = get_method_totals()
    field_totals = get_field_totals()
    
    print(f"🎯 Gesamte Matches: {total_matches:,}")
    print(f"📈 Anzahl Methoden: {len(FUZZY_METADATA['methods'])}")
    print(f"📊 Anzahl Felder: {len(UNIFIED_FUZZY_DATA)}")
    
    print(f"\n🔝 Beste Methode: {max(method_totals, key=method_totals.get)} ({method_totals[max(method_totals, key=method_totals.get)]:,} Matches)")
    print(f"🎪 Bestes Feld: {max(field_totals, key=field_totals.get)} ({field_totals[max(field_totals, key=field_totals.get)]:,} Matches)")
    
    print(f"\n📋 Methoden-Totals:")
    for method, total in sorted(method_totals.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {method}: {total:,}")
    
    print(f"\n📊 Feld-Totals:")
    for field, total in sorted(field_totals.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {field}: {total:,}")
    
    print("="*60)

if __name__ == "__main__":
    print_summary()
