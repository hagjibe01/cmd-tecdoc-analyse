#!/usr/bin/env python3
"""
Umfassende Match-Visualisierung
Kombiniert Gesamt-Match-Analyse und Methodenvergleich in einem Script
"""

import sys
import os
sys.path.append('scripts/analysis')

def run_comprehensive_match_analysis():
    """Führt alle Match-Analysen durch"""
    
    print("🔍 UMFASSENDE MATCH-ANALYSE")
    print("=" * 60)
    
    try:
        # 1. Gesamt-Match-Analyse
        print("\n1. GESAMT-MATCH-ANALYSE")
        print("-" * 30)
        from total_matches_analysis import create_total_matches_analysis
        create_total_matches_analysis()
        
        # 2. Methodenvergleich-Analyse  
        print("\n2. METHODENVERGLEICH-ANALYSE")
        print("-" * 30)
        from method_comparison_analysis import create_method_comparison_analysis
        create_method_comparison_analysis()
        
        print("\n" + "=" * 60)
        print("✅ ALLE MATCH-ANALYSEN ABGESCHLOSSEN!")
        print("📊 Ergebnisse verfügbar in:")
        print("   • visualizations/total_matches_analysis/")
        print("   • visualizations/method_comparison/")
        print("   • results/tables/")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ FEHLER: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = run_comprehensive_match_analysis()
    if success:
        print("\n🎉 Alle Visualisierungen erfolgreich erstellt!")
    else:
        print("\n❌ Es gab Probleme bei der Erstellung der Visualisierungen.")
