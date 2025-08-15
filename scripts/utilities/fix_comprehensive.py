import re
import sys

def fix_comprehensive_matching_overview():
    """Repariert die Einrückungen in comprehensive_matching_overview.py"""
    
    file_path = r"C:\Users\HBE\OneDrive - TecAlliance\Dokumente\dhbw\projektarbeit_1\daten\Datenanalyse\scripts\analysis\comprehensive_matching_overview.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        fixed_lines = []
        indent_level = 0
        in_function = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Skip empty lines
            if not stripped:
                fixed_lines.append('\n')
                continue
                
            # Skip comments that are already properly formatted
            if stripped.startswith('#') and line.startswith('#'):
                fixed_lines.append(line)
                continue
            
            # Function definitions
            if stripped.startswith('def '):
                indent_level = 0
                in_function = True
                fixed_lines.append(stripped + '\n')
                continue
            
            # Class definitions  
            if stripped.startswith('class '):
                indent_level = 0
                fixed_lines.append(stripped + '\n')
                continue
                
            # Import statements
            if stripped.startswith(('import ', 'from ')):
                indent_level = 0
                fixed_lines.append(stripped + '\n')
                continue
            
            # If we're in a function, everything should be indented
            if in_function:
                # Control structures that increase indentation
                if any(stripped.startswith(x) for x in ['if ', 'for ', 'while ', 'try:', 'except', 'with ', 'def ']):
                    fixed_lines.append('    ' * (indent_level + 1) + stripped + '\n')
                    if stripped.endswith(':'):
                        indent_level += 1
                # Continuation of previous control structure
                elif line.startswith(' ') and not line.startswith('    '):
                    fixed_lines.append('    ' * (indent_level + 1) + stripped + '\n')
                # Regular function content
                else:
                    fixed_lines.append('    ' + stripped + '\n')
            else:
                # Top-level code
                fixed_lines.append(stripped + '\n')
        
        # Write the fixed file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
            
        print(f"[REPARIERT] {file_path}")
        return True
        
    except Exception as e:
        print(f"[FEHLER] Konnte {file_path} nicht reparieren: {e}")
        return False

if __name__ == "__main__":
    fix_comprehensive_matching_overview()
