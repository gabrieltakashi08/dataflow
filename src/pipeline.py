from src.extract import extrair_dados
from src.transform import transformar_dados
from src.validacao import validar_vendas_clientes
from src.dashboard.dashboard import gerar_dashboard
from src.load_postgres import carregar

import subprocess
import sys


def executar_pipeline():

    print("\n================================")
    print("      DATAFLOW PIPELINE")
    print("================================\n")

    print("ETAPA 1 - EXTRACT")
    dados = extrair_dados()

    print("\nETAPA 2 - TRANSFORM")
    vendas_clientes = transformar_dados(dados)

    print("\nETAPA 3 - VALIDAÇÃO")
    validar_vendas_clientes(vendas_clientes)
    print("Validação concluída com sucesso!")

    print("\nETAPA 4 - LOAD POSTGRESQL")
    carregar()

    print("\nETAPA 5 - ANÁLISE")
    subprocess.run(
        [sys.executable, "src/analise.py"],
        check=True
    )

    print("\nETAPA 6 - DASHBOARD")
    gerar_dashboard()

    print("\nPipeline executado com sucesso!")


if __name__ == "__main__":
    executar_pipeline()