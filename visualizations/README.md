# 📊 VISUALISIERUNGEN - ORGANISIERTE STRUKTUR

## 🗂️ **Ordneraufteilung**

### 📁 **visualizations/**
```
📂 tecdoc_xml_analysis/          # TecDoc ↔ XML Matching-Analysen
📂 cmd_csv_analysis/             # TecDoc ↔ CMD CSV Matching-Analysen  
📂 deterministic_matching/       # Rein deterministische Verfahren
📂 fuzzy_matching/              # Fuzzy/Probabilistic Verfahren
```

---

## 🎯 **1. TecDoc XML Analysis**
**Ordner**: `visualizations/tecdoc_xml_analysis/`

| Datei | Beschreibung |
|-------|--------------|
| `erfolgsraten.png` | Erfolgsraten verschiedener Matching-Methoden |
| `matching_results_visualization.png` | Hauptvisualisierung der Matching-Ergebnisse |
| `methoden_matrix.png` | Matrix-Darstellung der Methoden-Performance |
| `spalten_vergleich.png` | Vergleich der TecDoc vs XML Spalten |
| `tecdoc_match_overview.png` | Gesamtübersicht der TecDoc-Matches |
| `top_spaltenpaare.png` | Top-performende Spaltenpaare |

**Datenquelle**: TecDoc 200_Article_Table.csv ↔ XML-Dateien (CMD Platform)

---

## 🗃️ **2. CMD CSV Analysis** 
**Ordner**: `visualizations/cmd_csv_analysis/`

| Datei | Beschreibung |
|-------|--------------|
| `tecdoc_tmd_top_matches.png` | Top-performende TecDoc ↔ TMD Spaltenpaare |
| `tecdoc_tmd_methoden_vergleich.png` | Vergleich aller 8 Matching-Methoden |
| `tecdoc_tmd_spalten_ranking.png` | Ranking der erfolgreichsten Spalten |
| `tecdoc_tmd_kategorien_heatmap.png` | Heatmap nach Daten-Kategorien |
| `tecdoc_tmd_zusammenfassung.png` | Gesamtzusammenfassung der Analyse |

**Datenquelle**: TecDoc 200_Article_Table.csv ↔ CMD TMD CSV (Business Cloud)

---

## 🔧 **3. Deterministic Matching**
**Ordner**: `visualizations/deterministic_matching/`

**Verfahren**:
- ✅ Exact Match (exakte Übereinstimmung)
- ✅ Substring Match (Teilstring-Suche)
- ✅ Prefix/Suffix Match (Anfang/Ende)
- ✅ Numeric Exact Match (exakte Zahlen)
- ✅ Length-based Match (gleiche Länge)

**Ausgabe**: `deterministic_matching_results_pure.csv`

---

## 🌊 **4. Fuzzy/Probabilistic Matching**
**Ordner**: `visualizations/fuzzy_matching/`

**Verfahren**:
- 🎯 Numeric Tolerance (±10% Toleranz)
- 📝 Levenshtein Distance (Edit Distance)
- 🔤 Phonetic Matching (ähnlich klingende Wörter)
- 📊 Similarity Ratio (Ähnlichkeits-Score)

**Ausgabe**: `fuzzy_matching_results.csv`

---

## 🚀 **Ausführung der Skripte**

### **XML-Analysen**:
```powershell
python matching_visualization.py
```

### **CSV-Analysen**:
```powershell
python tecdoc_tmd_visualization.py
```

### **Deterministic Matching**:
```powershell
python deterministic_matching_pure.py
```

### **Fuzzy Matching**:
```powershell
python fuzzy_matching_advanced.py
```

---

## 📈 **Ergebnisse im Überblick**

| Analyse-Typ | Datenquellen | Beste Methode | Top-Match |
|-------------|--------------|---------------|-----------|
| **XML** | TecDoc ↔ XML Platform | Teilstring | artno ↔ SupplierPtNo |
| **CSV** | TecDoc ↔ TMD CSV | Numerische Toleranz | 100.698 Matches |
| **Deterministisch** | TecDoc ↔ TMD | Exakt | Regelbasiert |
| **Fuzzy** | TecDoc ↔ TMD | Tolerance ±10% | Flexibel |

---

## 🔄 **Letzte Aktualisierung**
- **Datum**: 13. August 2025
- **Status**: Vollständig organisiert und getestet
- **Struktur**: Wissenschaftlich korrekt getrennt

**📊 Alle Visualisierungen sind hochauflösend (300 DPI) und publication-ready!**
