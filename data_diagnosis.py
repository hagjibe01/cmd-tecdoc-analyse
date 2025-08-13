import pandas as pd
import os

def diagnose_data():
    """Diagnostiziert die Daten um zu verstehen warum keine Matches gefunden werden"""
    print("🔍 DATENDIAGNOSE: TecDoc vs CMD TMD")
    print("="*60)
    
    # Lade kleine Stichproben
    print("1️⃣ Lade TecDoc Stichprobe...")
    try:
        tecdoc_sample = pd.read_csv('200_Article_Table.csv', nrows=1000, dtype=str)
        print(f"   ✅ TecDoc: {len(tecdoc_sample)} Zeilen geladen")
        print(f"   📊 Spalten: {list(tecdoc_sample.columns)}")
        
        # Zeige Beispielwerte für wichtige Spalten
        for col in ['artno', 'brandno', 'batchsize1', 'batchsize2', 'tableno']:
            if col in tecdoc_sample.columns:
                non_null = tecdoc_sample[col].dropna()
                if len(non_null) > 0:
                    print(f"   🔸 {col}: {len(non_null)} Werte, Beispiele: {list(non_null.head(3))}")
                else:
                    print(f"   ❌ {col}: Keine Werte")
    except Exception as e:
        print(f"   ❌ TecDoc Fehler: {e}")
        return
    
    print("\n2️⃣ Lade CMD TMD Stichprobe...")
    try:
        cmd_sample = pd.read_csv(
            'tmd_001000106869000000000065516001_data_2025-07-15-09-42-29-416.csv', 
            nrows=1000, 
            dtype=str,
            on_bad_lines='skip'
        )
        print(f"   ✅ CMD: {len(cmd_sample)} Zeilen geladen")
        print(f"   📊 Spalten: {len(cmd_sample.columns)} total")
        print(f"   📋 Erste 10 Spalten: {list(cmd_sample.columns[:10])}")
        
        # Zeige Beispielwerte für wichtige Spalten
        important_cols = ['article_number', 'brand', 'tec_doc_article_number', 
                         'article_description_de', 'article_description_en',
                         'min_order_qty', 'max_order_qty']
        
        for col in important_cols:
            if col in cmd_sample.columns:
                non_null = cmd_sample[col].dropna()
                if len(non_null) > 0:
                    print(f"   🔸 {col}: {len(non_null)} Werte, Beispiele: {list(non_null.head(3))}")
                else:
                    print(f"   ❌ {col}: Keine Werte")
            else:
                print(f"   ⚠️  {col}: Spalte nicht gefunden")
                
    except Exception as e:
        print(f"   ❌ CMD Fehler: {e}")
        return
    
    print("\n3️⃣ DIREKTER VERGLEICH:")
    print("-"*40)
    
    # Teste TecDoc artno vs CMD article_number
    if 'artno' in tecdoc_sample.columns and 'article_number' in cmd_sample.columns:
        tec_artno = set(str(x).strip().upper() for x in tecdoc_sample['artno'].dropna() if str(x).strip())
        cmd_artno = set(str(x).strip().upper() for x in cmd_sample['article_number'].dropna() if str(x).strip())
        
        print(f"🔹 TecDoc artno: {len(tec_artno)} eindeutige Werte")
        print(f"   Beispiele: {list(list(tec_artno)[:5])}")
        
        print(f"🔹 CMD article_number: {len(cmd_artno)} eindeutige Werte") 
        print(f"   Beispiele: {list(list(cmd_artno)[:5])}")
        
        # Teste Überschneidungen
        intersection = tec_artno.intersection(cmd_artno)
        print(f"🎯 Direkte Überschneidungen: {len(intersection)}")
        if intersection:
            print(f"   Beispiele: {list(intersection)[:5]}")
    
    # Teste TecDoc artno vs CMD tec_doc_article_number
    if 'artno' in tecdoc_sample.columns and 'tec_doc_article_number' in cmd_sample.columns:
        tec_artno = set(str(x).strip().upper() for x in tecdoc_sample['artno'].dropna() if str(x).strip())
        cmd_tecdoc = set(str(x).strip().upper() for x in cmd_sample['tec_doc_article_number'].dropna() if str(x).strip())
        
        print(f"\n🔹 CMD tec_doc_article_number: {len(cmd_tecdoc)} eindeutige Werte")
        print(f"   Beispiele: {list(list(cmd_tecdoc)[:5])}")
        
        intersection2 = tec_artno.intersection(cmd_tecdoc)
        print(f"🎯 TecDoc artno ↔ CMD tec_doc_article_number: {len(intersection2)} Überschneidungen")
        if intersection2:
            print(f"   Beispiele: {list(intersection2)[:5]}")
    
    print("\n4️⃣ EMPFEHLUNGEN:")
    print("-"*40)
    if len(intersection) == 0 and len(intersection2) == 0:
        print("⚠️  Keine direkten Matches in Stichprobe gefunden")
        print("💡 Mögliche Ursachen:")
        print("   • Unterschiedliche Datenquellen/Zeiträume")
        print("   • Verschiedene Artikelnummer-Formate")
        print("   • Fehlende Normalisierung nötig")
        print("   • Fuzzy-Matching könnte besser sein")
        
        print("\n🔄 Teste Substring/Fuzzy-Ansätze:")
        # Teste ob Teilstrings funktionieren könnten
        tec_short = [x[:5] for x in tec_artno if len(x) >= 5][:10]
        for tec_part in tec_short:
            matches = [x for x in cmd_artno if tec_part in x]
            if matches:
                print(f"   🔍 TecDoc '{tec_part}' gefunden in CMD: {matches[:3]}")
    else:
        print("✅ Direkte Matches gefunden! Algorithmus sollte funktionieren.")

if __name__ == "__main__":
    diagnose_data()
