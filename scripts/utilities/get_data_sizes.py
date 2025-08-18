#!/usr/bin/env python3
"""
Ermittelt die tatsächlichen Datengrößen für die korrekten theoretischen Maxima
"""

import pandas as pd
import xml.etree.ElementTree as ET
import os
from pathlib import Path

def get_actual_data_sizes():
    """Ermittelt die tatsächlichen Datengrößen"""
    
    print("🔍 ERMITTLUNG DER TATSÄCHLICHEN DATENGRÖSSEN")
    print("=" * 60)
    
    # CSV-Daten (CMD)
    try:
        csv_data = pd.read_csv('data/input/cmd_daten.csv', sep=';', low_memory=False)
        csv_size = len(csv_data)
        print(f"📊 CMD CSV-Daten: {csv_size:,} Einträge")
    except Exception as e:
        print(f"❌ Fehler beim CSV-Einlesen: {e}")
        csv_size = 0
    
    # TecDoc-Daten
    try:
        tecdoc_data = pd.read_csv('data/input/200_Article_Table.csv')
        tecdoc_size = len(tecdoc_data)
        print(f"📊 TecDoc-Daten: {tecdoc_size:,} Einträge")
    except Exception as e:
        print(f"❌ Fehler beim TecDoc-Einlesen: {e}")
        tecdoc_size = 0
    
    # XML-Daten (CMD Platform)
    xml_total = 0
    xml_files = 0
    xml_dir = Path('data/input/cmd_platform_data')
    
    if xml_dir.exists():
        for xml_file in xml_dir.glob('*.xml'):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Zähle Artikel-Elemente (nicht alle XML-Elemente)
                articles = 0
                
                # Verschiedene mögliche Artikel-Strukturen
                for tag in ['Article', 'article', 'Product', 'product', 'Item', 'item']:
                    articles += len(root.findall(f'.//{tag}'))
                
                if articles == 0:
                    # Fallback: Zähle direkte Kinder des Root-Elements
                    articles = len(list(root))
                
                xml_total += articles
                xml_files += 1
                print(f"📊 {xml_file.name}: {articles:,} Artikel")
                
            except Exception as e:
                print(f"❌ Fehler bei {xml_file.name}: {e}")
    
    print(f"📊 XML-Daten gesamt: {xml_total:,} Artikel aus {xml_files} Dateien")
    
    # Theoretische Maxima berechnen
    print("\n" + "=" * 60)
    print("🎯 THEORETISCHE MAXIMA FÜR MATCHING")
    print("=" * 60)
    
    print(f"CSV-Matching Maximum: {csv_size:,} (CMD-Daten)")
    print(f"XML-Matching Maximum: {xml_total:,} (CMD Platform-Daten)")
    print(f"TecDoc-Referenz-Größe: {tecdoc_size:,} (Vergleichsdatensatz)")
    
    # Realistische Matching-Maxima
    csv_realistic = min(csv_size, tecdoc_size) if tecdoc_size > 0 else csv_size
    xml_realistic = xml_total
    
    print(f"\nREALISTISCHE MATCHING-MAXIMA:")
    print(f"CSV-Matching (realistisch): {csv_realistic:,}")
    print(f"XML-Matching (realistisch): {xml_realistic:,}")
    print(f"Gesamt-Maximum: {csv_realistic + xml_realistic:,}")
    
    return {
        'csv_size': csv_size,
        'xml_size': xml_total,
        'tecdoc_size': tecdoc_size,
        'csv_realistic': csv_realistic,
        'xml_realistic': xml_realistic,
        'total_realistic': csv_realistic + xml_realistic
    }

if __name__ == "__main__":
    sizes = get_actual_data_sizes()
    
    print(f"\n💡 EMPFEHLUNG FÜR VISUALISIERUNG:")
    print(f"   max_possible_csv = {sizes['csv_realistic']:,}")
    print(f"   max_possible_xml = {sizes['xml_realistic']:,}")
    print(f"   max_total = {sizes['total_realistic']:,}")
