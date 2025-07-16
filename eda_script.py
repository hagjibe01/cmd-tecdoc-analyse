import pandas as pd
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns

# Funktion zur Durchführung der EDA auf einer CSV-Datei
def perform_eda(file_path, file_label):
    print(f"\n--- EDA für {file_label} ---")

    # 1. Einlesen der Datei
    try:
        df = pd.read_csv(file_path, encoding='utf-8', sep=None, engine='python')
    except Exception as e:
        print(f"Fehler beim Einlesen der Datei {file_path}: {e}")
        return

    # 2. Überblick über Spalten und Datentypen
    print("\nSpalten und Datentypen:")
    print(df.dtypes)

    # 3. Anzahl fehlender Werte pro Spalte
    print("\nAnzahl fehlender Werte pro Spalte:")
    print(df.isnull().sum())

    # 4. Anzahl eindeutiger Werte pro Spalte
    print("\nAnzahl eindeutiger Werte pro Spalte:")
    print(df.nunique())

    # 5. Erkennung von Dubletten
    num_duplicates = df.duplicated().sum()
    print(f"\nAnzahl vollständig doppelter Zeilen: {num_duplicates}")

    # 6. Grundlegende Statistik für numerische Felder
    print("\nStatistische Kennzahlen für numerische Felder:")
    print(df.describe())

    # 7. Visualisierung: Verteilung der Anzahl fehlender Werte
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        plt.figure(figsize=(10, 4))
        sns.barplot(x=missing.index, y=missing.values)
        plt.title(f"Fehlende Werte pro Spalte ({file_label})")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

# Beispielhafte Dateipfade (anpassen!)
cmd_file = "cmd_daten.csv"
tecdoc_file = "tecdoc_daten.csv"

# EDA für beide Dateien durchführen
perform_eda(cmd_file, "CMD-Daten")
perform_eda(tecdoc_file, "TecDoc-Daten")
