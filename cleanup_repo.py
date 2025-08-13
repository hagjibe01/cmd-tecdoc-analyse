#!/usr/bin/env python3
"""
Repository Cleanup und Migration-Script
Räumt das Repository auf und migriert zu modularer Struktur
"""

import os
import shutil
from pathlib import Path

def main():
    """Hauptfunktion für Repository-Cleanup"""
    
    print("🧹 REPOSITORY CLEANUP")
    print("=" * 40)
    
    base_dir = Path(".")
    
    # Erstelle Backup-Verzeichnis für wichtige alte Dateien
    backup_dir = base_dir / "backup_old_scripts"
    backup_dir.mkdir(exist_ok=True)
    
    # Dateien zum Löschen (redundant)
    files_to_remove = [
        "bfg-1.15.0.jar",
        "match_tecdoc_nr.csv",
        "mahle_001000106983000000000074658001_data_2025-07-16-07-16-34-689.csv",
        "MAT-684500001-20250712112631.xml",
        "tmd_001000106869000000000065516001_data_2025-07-15-09-42-29-416.csv"
    ]
    
    # Verzeichnisse zum Aufräumen
    dirs_to_cleanup = [
        "backup-repo.git",
        "eda_script.git", 
        "matching_output",
        "eda_output"
    ]
    
    # Entferne redundante Dateien
    removed_files = 0
    for file_name in files_to_remove:
        file_path = base_dir / file_name
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"🗑️  Entfernt: {file_name}")
                removed_files += 1
            except Exception as e:
                print(f"⚠️ Fehler beim Entfernen von {file_name}: {e}")
    
    # Verschiebe alte Verzeichnisse ins Backup
    moved_dirs = 0
    for dir_name in dirs_to_cleanup:
        dir_path = base_dir / dir_name
        backup_path = backup_dir / dir_name
        if dir_path.exists() and dir_path.is_dir():
            try:
                shutil.move(str(dir_path), str(backup_path))
                print(f"📦 Verschoben nach Backup: {dir_name}")
                moved_dirs += 1
            except Exception as e:
                print(f"⚠️ Fehler beim Verschieben von {dir_name}: {e}")
    
    # Verschiebe verbleibende Daten-Dateien
    data_files = ["209_GTIN.csv", "400_Article_Linkage.csv"]
    data_input_dir = base_dir / "data" / "input"
    
    for file_name in data_files:
        file_path = base_dir / file_name
        target_path = data_input_dir / file_name
        if file_path.exists() and not target_path.exists():
            try:
                shutil.move(str(file_path), str(target_path))
                print(f"📁 Verschoben nach data/input: {file_name}")
            except Exception as e:
                print(f"⚠️ Fehler beim Verschieben von {file_name}: {e}")
    
    # Verschiebe CMD-Daten-Verzeichnisse
    cmd_dirs = ["cmd_business_cloud_data", "cmd_platform_data", "tecdoc_data"]
    for dir_name in cmd_dirs:
        dir_path = base_dir / dir_name
        target_path = data_input_dir / dir_name
        if dir_path.exists() and not target_path.exists():
            try:
                shutil.move(str(dir_path), str(target_path))
                print(f"📁 Verschoben nach data/input: {dir_name}")
            except Exception as e:
                print(f"⚠️ Fehler beim Verschieben von {dir_name}: {e}")
    
    print(f"\n✅ Cleanup abgeschlossen!")
    print(f"🗑️  {removed_files} Dateien entfernt")
    print(f"📦 {moved_dirs} Verzeichnisse ins Backup verschoben")
    print(f"📁 Daten in data/input/ strukturiert")
    print(f"💾 Backup erstellt in: {backup_dir}")

if __name__ == "__main__":
    main()
