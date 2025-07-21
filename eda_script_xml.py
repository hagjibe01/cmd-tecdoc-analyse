import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import xml.etree.ElementTree as ET

def parse_xml_to_df(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # XML-Namespace extrahieren
    ns = {'ns': root.tag.split('}')[0].strip('{')}

    articles = []
    for article in root.findall('.//ns:Article', ns):
        data = {
            'SupplierPtNo': article.findtext('ns:SupplierPtNo', default='', namespaces=ns),
            'Brand': article.findtext('ns:Brand', default='', namespaces=ns),
            'SalesCountry': article.findtext('ns:SalesCountry', default='', namespaces=ns),
            'CommodityCode': article.findtext('ns:CommodityCode', default='', namespaces=ns),
            'ExchangePart': article.findtext('ns:ExchangePart', default='', namespaces=ns),
            'BaseUOM': article.findtext('ns:BaseUOM', default='', namespaces=ns),
            'MinOrderQuantity': article.findtext('ns:MinOrderQuantity', default='', namespaces=ns),
            'MaxOrderQuantity': article.findtext('ns:MaxOrderQuantity', default='', namespaces=ns),
            'GrossWeight': article.find('.//ns:GrossWeight', ns).text if article.find('.//ns:GrossWeight', ns) is not None else '',
            'Volume': article.find('.//ns:Volume', ns).text if article.find('.//ns:Volume', ns) is not None else '',
            'ArticleDescription_DE': '',
            'ArticleDescription_EN': ''
        }

        # Mehrsprachige Beschreibungen extrahieren
        for desc in article.findall('.//ns:ArticleDescription', ns):
            lang = desc.attrib.get('Language')
            if lang == 'DE':
                data['ArticleDescription_DE'] = desc.text
            elif lang == 'EN':
                data['ArticleDescription_EN'] = desc.text

        articles.append(data)

    return pd.DataFrame(articles)


# EDA-Funktion
def perform_eda(file_path, file_label):
    print(f"\n--- EDA for {file_label} ---")
    output_dir = f"eda_output/{file_label.replace(' ', '_')}"
    os.makedirs(output_dir, exist_ok=True)

    # XML oder CSV?
    try:
        if file_path.lower().endswith('.xml'):
            df = parse_xml_to_df(file_path)
        else:
            df = pd.read_csv(file_path, encoding='utf-8', sep=None, engine='python')
    except Exception as e:
        print(f"Fehler beim Einlesen der Datei: {e}")
        return

    # 1. Datentypen
    column_types = pd.DataFrame(df.dtypes, columns=["DataType"])
    column_types.to_csv(f"{output_dir}/column_types.csv")
    print("\nSpalten und Datentypen:")
    print(column_types)

    # 2. Fehlende Werte
    missing_values = df.isnull().sum()
    missing_values = missing_values[missing_values > 0]
    missing_values_df = pd.DataFrame(missing_values, columns=["MissingValues"])
    missing_values_df.to_csv(f"{output_dir}/missing_values.csv")
    print("\nFehlende Werte pro Spalte:")
    print(missing_values_df)

    # 3. Eindeutige Werte
    unique_values = df.nunique()
    unique_values_df = pd.DataFrame(unique_values, columns=["UniqueValues"])
    unique_values_df.to_csv(f"{output_dir}/unique_values.csv")
    print("\nEindeutige Werte pro Spalte:")
    print(unique_values_df)

    # 4. Duplikate
    num_duplicates = df.duplicated().sum()
    with open(f"{output_dir}/duplicates.txt", "w") as f:
        f.write(f"Number of fully duplicated rows: {num_duplicates}\n")
    print(f"\nVollständige Duplikate: {num_duplicates}")

    # 5. Statistiken
    stats = df.describe(include='all')
    stats.to_csv(f"{output_dir}/summary_statistics.csv")
    print("\nStatistische Zusammenfassung:")
    print(stats)

    # 6. Plot fehlender Werte
    if not missing_values.empty:
        plt.figure(figsize=(10, 4))
        sns.barplot(x=missing_values.index, y=missing_values.values)
        plt.title(f"Fehlende Werte pro Spalte ({file_label})")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/missing_values_plot.png")
        plt.close()
        print(f"Plot der fehlenden Werte gespeichert unter {output_dir}")

# Beispielnutzung:
# perform_eda("deine_datei.csv", "CSV Datei")
# perform_eda("MAT-684500001-20250712112631.xml", "XML Artikel Daten")
perform_eda("MAT-684500006-20250712112627.xml", "TecCMD_Plattform_Daten-ZF-06")    