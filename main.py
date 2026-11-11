from src.extrair import buscar_sidra
from src.transformar import transformar_sidra
from src.carregar import carregar


def main():
    df_cru = buscar_sidra(7060, 63, "last 12", nivel="n7")
    carregar(df_cru, "bronze", "ipca_regiao")

    df_ipca = transformar_sidra(df_cru)
    carregar(df_ipca, "silver", "ipca_regiao")


if __name__ == "__main__":
    main()