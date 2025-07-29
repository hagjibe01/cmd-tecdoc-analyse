import pandas as pd
import matplotlib.pyplot as plt

# Eingabedateien
cmd_file = "mahle_001000106983000000000074658001_data_2025-07-16-07-16-34-689.csv"
tecdoc_file = "200 - Article Table.csv"

# CMD einlesen
cmd_df = pd.read_csv(cmd_file, dtype=str, sep=None, engine='python')
print("CMD-Daten geladen")

def clean_column(col):
    return col.astype(str).str.strip().str.upper()

cmd_df['tec_doc_article_number_clean'] = clean_column(cmd_df['tec_doc_article_number'])

# Matching vorbereiten
match_tecdoc_nr_list = []

chunksize = 100_000
for chunk in pd.read_csv(tecdoc_file, dtype=str, chunksize=chunksize):
    #print("Verarbeite neuen TecDoc-Chunk...")
    chunk['artno_clean'] = clean_column(chunk['artno'])

    match_tecdoc = pd.merge(
        cmd_df,
        chunk,
        left_on='tec_doc_article_number_clean',
        right_on='artno_clean',
        suffixes=('_cmd', '_tecdoc')
    )

    print(f"Chunk-Matches: {len(match_tecdoc)}")
    match_tecdoc_nr_list.append(match_tecdoc)

# Nur wenn Matches vorhanden sind
if match_tecdoc_nr_list:
    all_tecdoc_matches = pd.concat(match_tecdoc_nr_list, ignore_index=True)

    # Nur wichtige Spalten behalten
    wichtige_spalten = [
        'tec_doc_article_number',  # aus CMD
        'article_description_de',
        'ean'
    ]
    vorhandene_spalten = [s for s in wichtige_spalten if s in all_tecdoc_matches.columns]
    reduced_df = all_tecdoc_matches[vorhandene_spalten]
    
    # Filter auf gültige TecDoc-Artikelnummern
    reduced_df = reduced_df[reduced_df['tec_doc_article_number'].notna()]

    # EAN als Text für bessere Darstellung
    reduced_df['ean'] = "'" + reduced_df['ean'].astype(str)
    
    # CSV speichern
    output_path = "matching_output/match_tecdoc_kompakt-1.csv"
    reduced_df.to_csv(output_path, index=False)
else:
    print("Keine TecDoc-Nr-Matches gefunden.")

    
# Anzahl der Gesamtdatensätze (CMD als Referenz)
total_cmd_rows = len(cmd_df)

# Nur TecDoc-Nr-Matching vorhanden
unique_matches = all_tecdoc_matches['tec_doc_article_number'].nunique()
unique_cmd = cmd_df['tec_doc_article_number'].nunique()
pct_tecdoc = unique_matches / unique_cmd * 100


# Ausgabe
print("\n--- Matching-Ergebnisse ---")
print(f"CMD-Datensätze gesamt: {total_cmd_rows}")
print(f"TecDoc-Nr-Matches: {len(all_tecdoc_matches)} ({pct_tecdoc:.2f}%)")
print("Eindeutige CMD-Artikelnummern:", cmd_df['tec_doc_article_number'].nunique())
print("Eindeutige TecDoc-Artikelnummern:", all_tecdoc_matches['tec_doc_article_number'].nunique())
print("Eindeutige Matches:", all_tecdoc_matches['tec_doc_article_number'].nunique())
pct_correct = all_tecdoc_matches['tec_doc_article_number'].nunique() / cmd_df['tec_doc_article_number'].nunique() * 100
print(f"Korrigierte Match-Quote: {pct_correct:.2f}%")


# Visualisierung
import matplotlib.pyplot as plt

plt.figure(figsize=(6, 4))
bars = plt.bar(["TecDoc-Nr"], [all_tecdoc_matches['tec_doc_article_number'].nunique()], color='mediumseagreen')
plt.title("Anzahl der TecDoc-Nr-Matches")
plt.ylabel("Anzahl Matches")

# Prozent über dem Balken anzeigen
plt.text(0, all_tecdoc_matches['tec_doc_article_number'].nunique(), f"{pct_tecdoc:.1f}%", ha='center', va='bottom')
plt.tight_layout()
plt.savefig("tecdoc_match_overview.png")
plt.show()
# Abschlussmeldung
print("Matching abgeschlossen. Ergebnisse gespeichert und visualisiert.")