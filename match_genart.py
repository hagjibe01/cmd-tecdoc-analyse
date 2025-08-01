import pandas as pd
import os

# =====================
# 🔹 Konfiguration
# =====================
CMD_PATH = "tmd_001000106869000000000065516001_data_2025-07-15-09-42-29-416.csv"
TECDOC_PATH = "400_Article_Linkage.csv"
CHUNKSIZE = 100_000
OUTPUT_PATH = "matching_output/match_genart_datasupplier_chunked.csv"
# Optional: Nur die ersten N Chunks verarbeiten (None = alle)
MAX_CHUNKS = 500  # z.B. 5 Chunks für schnellen Test, None für alle

# =====================
# 🔹 CMD-Daten laden
# =====================
cmd_df = pd.read_csv(CMD_PATH, sep=";", dtype=str)

cmd_df['article_number_clean'] = cmd_df['article_number'].astype(str).str.upper().str.replace(r'\W+', '', regex=True)
cmd_df['genartno'] = cmd_df['generic_article_no'].astype(str).str.strip()
cmd_df['datasupplier_id_clean'] = cmd_df['tec_doc_data_supplier_number'].astype(str).str.strip()

# =====================
# 🔹 Vorbereitung für Matching
# =====================
matches = []

# =====================
# 🔹 Chunkweises Lesen der TecDoc-Daten
# =====================

chunk_iter = pd.read_csv(TECDOC_PATH, sep=",", dtype=str, chunksize=CHUNKSIZE)

for i, chunk in enumerate(chunk_iter, 1):
    print(f"🔍 Bearbeite Chunk {i} ...")
    chunk['article_number_clean'] = chunk['artno'].astype(str).str.upper().str.replace(r'\W+', '', regex=True)
    chunk['genartno'] = chunk['genartno'].astype(str).str.strip()
    chunk['datasupplier_id_clean'] = chunk['datasupplier_id'].astype(str).str.strip()

    merged = pd.merge(
        cmd_df,
        chunk[['article_number_clean', 'genartno', 'datasupplier_id_clean']],
        on=['article_number_clean', 'genartno', 'datasupplier_id_clean'],
        how='inner'
    )

    if not merged.empty:
        print(f"✅ {len(merged)} Matches in Chunk {i}")
        matches.append(merged)
    if MAX_CHUNKS is not None and i >= MAX_CHUNKS:
        print(f"⏹️  Abbruch nach {MAX_CHUNKS} Chunks (Testmodus)")
        break

# =====================
# 🔹 Ergebnisse speichern
# =====================
if matches:
    final_df = pd.concat(matches, ignore_index=True)
    os.makedirs("matching_output", exist_ok=True)
    final_df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Gefundene Matches: {len(final_df)} – gespeichert unter {OUTPUT_PATH}")
else:
    print("⚠️ Keine Übereinstimmungen gefunden.")
