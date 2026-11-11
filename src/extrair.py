import requests
import pandas as pd

def buscar_sidra(tabela, variavel, periodo, nivel="n1"):
    """Busca uma série do SIDRA/IBGE e devolve um DataFrame."""
    url = f"https://apisidra.ibge.gov.br/values/t/{tabela}/{nivel}/all/v/{variavel}/p/{periodo}"
    
    resposta = requests.get(url, timeout=30)
    
    
    if resposta.status_code != 200:
        raise RuntimeError(f"Erro {resposta.status_code}: {resposta.text}")
    
    dados = resposta.json()
    
    if len(dados) <= 1:
        print("Sem dados para o período")
        return pd.DataFrame()
    
    cabecalho = dados[0]
    linhas = dados[1:]
    df = pd.DataFrame(linhas).rename(columns=cabecalho)
    return df