import pandas as pd

def transformar_sidra(df):
    """Converte tipos, seleciona e renomeia as colunas do SIDRA"""
    if df.empty:
        return df

    df = df.copy()
    
    #Converter valor e Mês (Código)
    df["Valor"] = pd.to_numeric(df["Valor"], errors ="coerce")
    df["Mês (Código)"] = pd.to_datetime(df["Mês (Código)"], format="%Y%m")
    #Selecionar e renomear colunas#
    df = df[[
        "Nível Territorial (Código)",
        "Unidade de Medida (Código)",
        "Valor",
        "Região Metropolitana até 2020 (Código)",
        "Região Metropolitana até 2020",
        "Variável (Código)",
        "Variável",
        "Mês (Código)",
        "Geral, grupo, subgrupo, item e subitem (Código)",
        "Geral, grupo, subgrupo, item e subitem"
    ]].rename(columns={
        "Nível Territorial (Código)": "nivel_id",
        "Unidade de Medida (Código)": "unidade_medida_id",
        "Valor": "val",
        "Região Metropolitana até 2020 (Código)": "regiao_2020_id",
        "Região Metropolitana até 2020": "regiao_2020",
        "Variável (Código)": "variavel_id",
        "Variável": "variavel",
        "Mês (Código)": "data",
        "Geral, grupo, subgrupo, item e subitem (Código)": "item_id",
        "Geral, grupo, subgrupo, item e subitem": "item"
    })
    return df