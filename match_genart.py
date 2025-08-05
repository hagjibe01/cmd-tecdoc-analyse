
import pandas as pd
import os

def match_by_generic_article(cmd_path, tecdoc_path, output_path, chunksize=100_000, max_chunks=None):
    """
    Führt Matching basierend auf generic_article_no durch und speichert die Ergebnisse als CSV.
    """
    cmd_df = pd.read_csv(cmd_path, sep=";", dtype=str)
    cmd_df['genartno'] = cmd_df['generic_article_no'].astype(str).str.strip().str.upper()

    matches = []
    chunk_iter = pd.read_csv(tecdoc_path, sep=",", dtype=str, chunksize=chunksize)
    for i, chunk in enumerate(chunk_iter, 1):
        print(f"🔍 Bearbeite Chunk {i} ...")
        if i == 1:
            print("Spalten im TecDoc-Chunk:", chunk.columns.tolist())
        # Passe hier den Spaltennamen an! Beispiel: 'genartno' statt 'generic_article_no'
        tecdoc_genart_col = 'genartno' if 'genartno' in chunk.columns else 'generic_article_no'
        chunk['genartno'] = chunk[tecdoc_genart_col].astype(str).str.strip().str.upper()
        merged = pd.merge(cmd_df, chunk[['genartno']], on='genartno', how='inner')
        if not merged.empty:
            print(f"✅ {len(merged)} Matches in Chunk {i}")
            matches.append(merged)
        if max_chunks is not None and i >= max_chunks:
            print(f"⏹️  Abbruch nach {max_chunks} Chunks (Testmodus)")
            break
    if matches:
        final_df = pd.concat(matches, ignore_index=True)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        final_df.to_csv(output_path, index=False)
        print(f"✅ Gefundene Matches: {len(final_df)} – gespeichert unter {output_path}")
        return final_df
    else:
        print("⚠️ Keine Übereinstimmungen gefunden.")
        return pd.DataFrame()

# Beispielaufruf:
# match_by_generic_article(
#     cmd_path="tmd_001000106869000000000065516001_data_2025-07-15-09-42-29-416.csv",
#     tecdoc_path="400_Article_Linkage.csv",
#     output_path="matching_output/match_genart_datasupplier_chunked.csv",
#     chunksize=100_000,
#     max_chunks=5
# )

if __name__ == "__main__":
    match_by_generic_article(
        cmd_path="tmd_001000106869000000000065516001_data_2025-07-15-09-42-29-416.csv",
        tecdoc_path="400_Article_Linkage.csv",
        output_path="matching_output/match_genart_datasupplier_chunked.csv",
        chunksize=100_000,
        max_chunks=5
    )
