#!/usr/bin/env python3
"""
Emoji-Bereinigungsskript für alle Python-Dateien
Entfernt alle Emojis aus Python-Skripten für akademische Präsentation
"""

import os
import re
import glob

def remove_emojis_from_file(file_path):
    """Entfernt Emojis aus einer Python-Datei"""

 # Liste häufiger Emojis die entfernt werden sollen
    emoji_replacements = {
    '': '',
    '': '',
    '[OK]': '[OK]',
    '[ERROR]': '[ERROR]',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '[WARNING]': '[WARNING]',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '[OK]': '[OK]',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': ''
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

            original_content = content

 # Ersetze spezifische Emojis
            for emoji, replacement in emoji_replacements.items():
                content = content.replace(emoji, replacement)

 # Entferne verbleibende Emojis mit Regex
 # Unicode-Bereiche für Emojis
                emoji_pattern = re.compile(
                "["
                "\U0001F600-\U0001F64F" # emoticons
                "\U0001F300-\U0001F5FF" # symbols & pictographs
                "\U0001F680-\U0001F6FF" # transport & map symbols
                "\U0001F1E0-\U0001F1FF" # flags (iOS)
                "\U00002702-\U000027B0"
                "\U000024C2-\U0001F251"
                "]+", flags=re.UNICODE)

                content = emoji_pattern.sub('', content)

 # Bereinige mehrfache Leerzeichen
                content = re.sub(r' +', ' ', content)
                content = re.sub(r'\n +\n', '\n\n', content)

 # Schreibe nur zurück wenn sich etwas geändert hat
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                        return True

                        return False

                        except Exception as e:
                            print(f"Fehler beim Bearbeiten von {file_path}: {e}")
                            return False

def clean_all_python_files():
    """Bereinigt alle Python-Dateien im Repository"""

    print("EMOJI-BEREINIGUNG FÜR DHBW PROJEKTARBEIT")
    print("=" * 50)

 # Finde alle Python-Dateien
    python_files = []
    python_files.extend(glob.glob('scripts/**/*.py', recursive=True))
    python_files.extend(glob.glob('*.py'))

    cleaned_files = 0
    total_files = len(python_files)

    for file_path in python_files:
        if os.path.exists(file_path):
            was_cleaned = remove_emojis_from_file(file_path)
            if was_cleaned:
                print(f"[BEREINIGT] {file_path}")
                cleaned_files += 1
                else:
                    print(f"[UNVERÄNDERT] {file_path}")

                    print("\n" + "=" * 50)
                    print(f"BEREINIGUNG ABGESCHLOSSEN")
                    print(f"Dateien bearbeitet: {cleaned_files} von {total_files}")
                    print(f"Repository ist jetzt emoji-frei und akademisch geeignet!")

                    if __name__ == "__main__":
                        clean_all_python_files()
