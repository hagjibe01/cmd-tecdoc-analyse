# CMD-TecDoc Datenanalyse - DHBW Projektarbeit

## Überblick
Analyse und Matching von Fahrzeugteile-Daten zwischen CMD und TecDoc Datenquellen.

## Projektstruktur

### 📁 scripts/
- **core/**: Kernfunktionalität und Hauptanalyse-Skripte
- **analysis/**: Datenanalyse und Tabellenerstellung
- **visualization/**: Alle Visualisierungsskripte
- **utilities/**: Hilfsskripte und Utilities

### 📁 data/
- **input/**: Eingangsdaten (CSV/XML Dateien)
- **output/**: Verarbeitete Ausgangsdaten

### 📁 results/
- **tables/**: Ergebnis-Tabellen (CSV/TXT)
- **visualizations/**: Generierte Diagramme und Plots

### 📁 docs/
- Dokumentation und Berichte

## Schnellstart

### Komplette Analyse ausführen:
```bash
python run_main_analysis.py
```

### Nur Visualisierungen erstellen:
```bash
python run_visualizations.py
```

### Einzelne Komponenten:
```bash
# Deterministische Analyse
python scripts/core/run_deterministic_analysis.py

# Fuzzy-Matching Analyse  
python scripts/core/run_fuzzy_analysis.py

# Spezifische Visualisierung
python scripts/visualization/fuzzy_erfolgsrate_a4_optimiert.py
```

## Matching-Methoden

### Deterministische Methoden:
- Exact Match
- Substring Match
- Prefix/Suffix Match
- Numeric Exact Match
- Length-based Match

### Fuzzy-Methoden:
- Levenshtein Distance
- Jaro-Winkler
- Probabilistic Matching
- Phonetic Matching

## Datenquellen
- **CMD Business Cloud**: CSV-Format
- **CMD Platform**: XML-Format  
- **TecDoc**: XML-Referenzdaten

## Abhängigkeiten
```bash
pip install -r requirements.txt
```

## Projektergebnisse
- **70.000** Datensätze analysiert
- **66.702** deterministische Matches gefunden
- **210.480** Fuzzy-Matches identifiziert
- Multiple Visualisierungen für akademische Präsentation

## Autor
DHBW Projektarbeit - Datenanalyse und Matching-Algorithmen
