# Importando bibliotecas
import requests

# Exploração e Analise de dados
import pandas as pd

# Exploração e Analise de dados Geoespaciais
import geopandas as gpd

# URL do arquivo JSON
url = "https://raw.githubusercontent.com/hildebrandosegundo/fms/master/LFCES004.json"

# Baixando o arquivo JSON
response = requests.get(url)
response.raise_for_status()  # Verifica se houve algum erro na requisição

# Lendo os dados em formato JSON
json_data = response.json()

# Extraindo a lista de unidades de saúde
data = json_data.get("data", [])

# Estruturando os dados em um DataFrame do pandas
df = pd.DataFrame(data)

# Exibindo as primeiras linhas do DataFrame
df.head()

df.to_csv("C:/Users/labgeo/workspace/mestrado_2024/repositorios/saude/data/raw/rede_de_sade_fms_site.csv", sep=';', encoding="UTF-8", index=False)
