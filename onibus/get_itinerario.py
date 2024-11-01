import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
import mapclassify
from collections import defaultdict

# import certifi
# import urllib3

# http = urllib3.PoolManager(
#     cert_reqs="CERT_REQUIRED",
#     ca_certs=certifi.where()
# )


# Valores armazenados das zonas administrativas dos itinerários 
ZONAS_THE = ['NORTE', 'SUL', 'LESTE', 'SUDESTE', 'S']

# URLs da API
URL_ZONA = "https://setut.com.br/setut_map/lines/?zona="
URL_LINHA = "https://setut.com.br/setut_map/lines/rotas?linha="

# Inicializa uma lista para armazenar os dicionários aninhados
flattened_data = []

# Cabeçalhos HTTP para a requisição
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8"
}

# Requisição para cada zona administrativa
for zona in ZONAS_THE:
    response = requests.get(f"{URL_ZONA}{zona}", headers=headers, verify=False)

    if response.status_code == 200:
        data = response.json()
        # Achata a lista e adiciona ao flattened_data
        flattened_data.extend([item[0] for item in data])
    else:
        print(f"Erro ao acessar a URL: {response.status_code}")

# Converte a lista de dicionários para um DataFrame
df_zonas = pd.DataFrame(flattened_data)

# Converter valores numéricos armazenados como 'str' para 'int32'
df_zonas['id'] = df_zonas['id'].astype('int32')
df_zonas['codigo'] = df_zonas['codigo'].astype('int32')

df_zonas.to_csv('onibus\itinerario_zona.csv', encoding='UTF-8', index=False, sep=';')

# Lista para armazenar os dados de todas as rotas
rotas_data = []

# Requisição para buscar rotas por código de linha
for codigo in df_zonas['codigo']:
    response = requests.get(f"{URL_LINHA}{codigo}", verify=False)

    if response.status_code == 200:
        rotas = response.json()
        # Adiciona o código da linha a cada coordenada
        for rota in rotas:
            rota['codigo'] = codigo
        rotas_data.extend(rotas)
    else:
        print(f"Erro ao acessar a URL para a linha {codigo}: {response.status_code}")

# Usando defaultdict para agrupar por 'codigo'
grouped_data = defaultdict(list)

for item in rotas_data:
    # Convertendo coordenadas para floats e armazenando como tuplas
    grouped_data[item['codigo']].append((float(item['lng']), float(item['lat'])))

result = [{'codigo': codigo, 'coordenadas': coordenadas} for codigo, coordenadas in grouped_data.items()]

# Converte a lista de dicionários para um DataFrame
df_itinerarios = pd.geoDataFrame(result)

df_itinerarios['geometry'] = df_itinerarios['coordenadas'].apply(LineString)
geodf_itinerarios = gpd.GeoDataFrame(df_itinerarios, geometry='geometry', crs='EPSG:4326')
geodf_itinerarios.explore()

# Meclado informações dos itinerários por zona, relação muitos-para-um
geodf_onibus = pd.merge(df_zonas, df_itinerarios, how='right', on='codigo')

geodf_onibus.dtypes

# Define o sistema de coordenadas geográficas (CRS)
geodf_onibus.crs is None
geodf_onibus.set_crs(epsg=4326)
geodf_onibus