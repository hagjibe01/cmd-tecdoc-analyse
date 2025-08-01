import pandas as pd

# Dateien laden
cmd_df = pd.read_csv("tmd_001000106869000000000065516001_data_2025-07-15-09-42-29-416.csv", sep=";", dtype=str)
tecdoc_articles = pd.read_csv("200_Article_Table.csv", dtype=str)

# Bereinigen
cmd_df['article_number_clean'] = cmd_df['article_number'].astype(str).str.upper().str.replace(r'\W+', '', regex=True)
tecdoc_articles['article_number_clean'] = tecdoc_articles['artno'].astype(str).str.upper().str.replace(r'\W+', '', regex=True)

# Debug
common = set(cmd_df['article_number_clean']) & set(tecdoc_articles['article_number_clean'])
print(f"🟡 Gemeinsame Artikelnummern: {len(common)}")

# Match nur über Artikelnummer
matched = pd.merge(
    cmd_df,
    tecdoc_articles,
    on='article_number_clean',
    how='inner'
)

print(f"✅ Gefundene Matches (nur Artikelnummer): {len(matched)}")
print(tecdoc_terms['datasupplier_id'].value_counts().head(10))
print(tecdoc_terms[['datasupplier_id', 'term']].dropna().drop_duplicates().head(20))


# Speichern
#matched.to_csv("matching_output/match_article_only.csv", index=False)
