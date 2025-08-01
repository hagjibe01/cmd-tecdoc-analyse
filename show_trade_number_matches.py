import pandas as pd

# Zeige die ersten 10 Zeilen der großen Match-Datei
file = "matching_output/exact_match_tmd_trade_tecdoc200.csv"
df = pd.read_csv(file, sep=None, engine="python", nrows=10)
print(df.head(10))
