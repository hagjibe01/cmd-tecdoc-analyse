#!/usr/bin/env python3
"""
CMD-Daten Konsolidierung
Erstellt einheitliche cmd_daten.csv aus Business Cloud Daten
"""

import pandas as pd
from pathlib import Path

def main():
    """Konsolidiere CMD-Daten"""
    
    print("📊 CMD-DATEN KONSOLIDIERUNG")
    print("=" * 40)
    
    base_dir = Path("data/input")
    cmd_dir = base_dir / "cmd_business_cloud_data"
    
    all_cmd_data = []
    
    for csv_file in cmd_dir.glob("*.csv"):
        print(f"📂 Lade: {csv_file.name}")
        try:
            df = pd.read_csv(csv_file, encoding='utf-8', sep=',', on_bad_lines='skip')
            print(f"   📊 {len(df)} Zeilen geladen")
            all_cmd_data.append(df)
        except Exception as e:
            print(f"⚠️ Fehler beim Laden von {csv_file}: {e}")
    
    if all_cmd_data:
        # Kombiniere alle Daten
        combined_df = pd.concat(all_cmd_data, ignore_index=True)
        
        # Speichere konsolidierte Datei
        output_path = base_dir / "cmd_daten.csv"
        combined_df.to_csv(output_path, index=False, encoding='utf-8')
        
        print(f"\n✅ Konsolidierung abgeschlossen!")
        print(f"📁 Ausgabe: {output_path}")
        print(f"📊 Gesamt: {len(combined_df)} Zeilen")
        print(f"📋 Spalten: {', '.join(combined_df.columns.tolist())}")
    else:
        print("⚠️ Keine CMD-Daten gefunden!")

if __name__ == "__main__":
    main()
