import pandas as pd
import matplotlib.pyplot as plt


def gerar_dashboard():

    clientes = pd.read_csv(
        "data/analytics/clientes_analytics.csv",
        index_col=0
    )

    mensal = pd.read_csv(
        "data/analytics/mensal_analytics.csv",
        index_col=0
    )

    cidades = pd.read_csv(
        "data/analytics/cidade_analytics.csv",
        index_col=0
    )

    # Evolução do faturamento
    plt.figure(figsize=(10, 5))
    plt.plot(
        mensal.index,
        mensal["faturamento"],
        marker="o"
    )
    plt.title("Evolução do Faturamento Mensal")
    plt.xlabel("Mês")
    plt.ylabel("Faturamento (R$)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(
        "data/analytics/evolucao_faturamento.png",
        bbox_inches="tight"
    )
    plt.close()

    # Top clientes
    top_clientes = clientes.head(10).sort_values(
        "faturamento"
    )

    plt.figure(figsize=(10, 6))
    plt.barh(
        top_clientes.index,
        top_clientes["faturamento"]
    )
    plt.title("Top 10 Clientes por Faturamento")
    plt.xlabel("Faturamento (R$)")
    plt.ylabel("Cliente")
    plt.tight_layout()
    plt.savefig(
        "data/analytics/top_clientes.png",
        bbox_inches="tight"
    )
    plt.close()

    # Top cidades
    top_cidades = cidades.head(10).sort_values(
        "faturamento"
    )

    plt.figure(figsize=(10, 6))
    plt.barh(
        top_cidades.index,
        top_cidades["faturamento"]
    )
    plt.title("Top 10 Cidades por Faturamento")
    plt.xlabel("Faturamento (R$)")
    plt.ylabel("Cidade")
    plt.tight_layout()
    plt.savefig(
        "data/analytics/top_cidades.png",
        bbox_inches="tight"
    )
    plt.close()

    # Ticket médio mensal
    plt.figure(figsize=(10, 5))
    plt.plot(
        mensal.index,
        mensal["ticket_medio"],
        marker="o"
    )
    plt.title("Ticket Médio Mensal")
    plt.xlabel("Mês")
    plt.ylabel("Ticket Médio (R$)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(
        "data/analytics/ticket_medio_mensal.png",
        bbox_inches="tight"
    )
    plt.close()

    print("Dashboard gerado com sucesso!")


if __name__ == "__main__":
    gerar_dashboard()
