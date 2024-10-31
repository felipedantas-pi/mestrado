import re
import pandas as pd

# Planilha da Prévia da População
# Contempla a última atualização, devidos a processos judiciais
# Há 5570 municípios no último censo 2022
URL_PREVIA_POPULACAO = "https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Previa_da_Populacao/POP2022_Municipios_20230622.xls"

# Fazendo a leitura da planilha execel com Pandas
df_pop_bruto = pd.read_excel(URL_PREVIA_POPULACAO, skiprows=1)

# Verificando o tamanho da matriz
df_pop_bruto.shape # 5605 linhas

# Verificando o tipo dos dados
df_pop_bruto.dtypes

# Exclui as últimas 35 linhas = footer
df_pop_bruto = df_pop_bruto.iloc[:-35]

# Função para remover índices e converter para inteiro
def limpar_indices(populacao):
    if isinstance(populacao, str):
        # Remove qualquer coisa entre parênteses e converte para inteiro
        populacao = re.sub(r'\(\d+\)', '', populacao)
        # Remove pontos
        populacao = populacao.replace('.', '')
        return int(populacao)
    elif isinstance(populacao, (int, float)):
        return int(populacao)
    else:
        return None

# Aplicar a função à coluna 'POPULAÇÃO'
df_pop_bruto.loc[:, 'POPULAÇÃO'] = df_pop_bruto['POPULAÇÃO'].apply(limpar_indices)

# Lista obtida com os nomes atuais das colunas
cols_old = df_pop_bruto.columns.to_list()
# Lista com os novos nomes de coluna
cols_new = ['sigla_uf','cod_uf','cod_municipio','nm_municipio','pop_2022']
# Criando um dicionário a partir do mapeamento da colunas antiga e nova
cols_mapping = dict(zip(cols_old, cols_new))
# Criando um novo DataFrame contendo os novos nomes de colunas
df = df_pop_bruto.rename(columns=cols_mapping).reset_index(drop=True)


# Função para criar um subconjunto
def extraiMunicipiosPorEstado(dataframe, nm_col, nm_uf):
    """
    Extrai um subconjunto contendo os municípios de uma estado com base no valor da coluna especificada.

    Parameters:
    dataframe (pd.DataFrame): O DataFrame de onde extrair os dados.
    col (str): O nome da coluna a ser filtrada.
    valor: O nome do estado a ser filtrado na coluna.

    Returns:
    pd.DataFrame: O subconjunto do DataFrame que atende ao critério de filtragem.
    """
    df = dataframe[dataframe[nm_col] == nm_uf]
    return df

df_pi = extraiMunicipiosPorEstado(df, 'sigla_uf' ,'PI')