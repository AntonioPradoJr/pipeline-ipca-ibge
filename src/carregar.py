from pathlib import Path

def carregar(df, camada, nome):
    if df.empty:
        print(f"{nome}: DataFrame vazio, nada gravado")
        return
    
    pasta = Path("dados")/camada
    pasta.mkdir(parents=True, exist_ok=True)
    
    arquivo = pasta/f"{nome}.parquet"
    
    df.to_parquet(arquivo, index=False)
    
    print(f"{len(df)} linhas. Linhas gravadas em {arquivo}")