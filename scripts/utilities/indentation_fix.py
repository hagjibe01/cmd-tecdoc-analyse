#!/usr/bin/env python3
"""
Python Einrückungs-Reparatur Script
Repariert beschädigte Einrückungen in Python-Dateien
"""

import os
import glob
import re

def fix_indentation(file_path):
    """Repariert die Einrückung in einer Python-Datei"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        fixed_lines = []
        indent_level = 0
        in_function = False
        in_class = False
        in_try_block = False
        
        for i, line in enumerate(lines):
            original_line = line
            stripped = line.strip()
            
            # Leere Zeilen und Kommentare unverändert lassen
            if not stripped or stripped.startswith('#'):
                fixed_lines.append(line)
                continue
            
            # Bestimme Einrückungsebene basierend auf Python-Syntax
            if stripped.startswith(('def ', 'class ', 'if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except', 'finally:', 'with ')):
                if stripped.startswith('def ') or stripped.startswith('class '):
                    indent_level = 0
                    in_function = stripped.startswith('def ')
                    in_class = stripped.startswith('class ')
                elif stripped.startswith('try:'):
                    in_try_block = True
                elif stripped.startswith(('except', 'finally:')):
                    # except/finally auf gleicher Ebene wie try
                    pass
                else:
                    # if, elif, else, for, while, with
                    if not (in_function or in_class):
                        indent_level = 0
                
                # Füge korrekte Einrückung hinzu
                fixed_line = '    ' * indent_level + stripped + '\n'
                fixed_lines.append(fixed_line)
                
                # Erhöhe Einrückung für nachfolgende Zeilen
                if stripped.endswith(':'):
                    indent_level += 1
                
            elif stripped.startswith(('return', 'pass', 'break', 'continue')):
                # Diese sind normalerweise in einem Block
                if indent_level == 0:
                    indent_level = 1
                fixed_line = '    ' * indent_level + stripped + '\n'
                fixed_lines.append(fixed_line)
                
            else:
                # Normale Code-Zeilen
                if indent_level == 0 and (in_function or in_class or in_try_block):
                    indent_level = 1
                
                fixed_line = '    ' * indent_level + stripped + '\n'
                fixed_lines.append(fixed_line)
        
        # Schreibe reparierte Datei
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        
        print(f"[REPARIERT] {file_path}")
        return True
        
    except Exception as e:
        print(f"[FEHLER] {file_path}: {e}")
        return False

def main():
    """Repariert alle Python-Dateien mit Einrückungsproblemen"""
    
    print("PYTHON EINRÜCKUNGS-REPARATUR")
    print("=" * 40)
    
    # Finde alle Python-Dateien
    python_files = glob.glob('scripts/**/*.py', recursive=True)
    
    # Spezielle Problematische Dateien
    problem_files = [
        'scripts/utilities/emoji_cleanup.py',
        'scripts/utilities/repository_cleanup.py', 
        'scripts/utilities/final_cleanup.py',
        'scripts/analysis/deterministic_results_table.py',
        'scripts/analysis/fuzzy_results_table.py'
    ]
    
    fixed_count = 0
    
    for file_path in problem_files:
        if os.path.exists(file_path):
            if fix_indentation(file_path):
                fixed_count += 1
    
    print(f"\nReparierte Dateien: {fixed_count}")
    print("Einrückungen wurden korrigiert!")

if __name__ == "__main__":
    main()
