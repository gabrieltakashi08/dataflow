import matplotlib.pyplot as plt


def grafico_faturamento_mensal(faturamento_mensal):
    faturamento_mensal.plot(kind="bar")

    plt.title("Faturamento Mensal")
    plt.xlabel("Mês")
    plt.ylabel("Faturamento (R$)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        "data/processed/faturamento_mensal.png",
        bbox_inches="tight"
    )

    plt.close()


def grafico_faturamento_cidade(faturamento_cidade):
    faturamento_cidade.plot(kind="bar")

    plt.title("Faturamento por Cidade")
    plt.xlabel("Cidade")
    plt.ylabel("Faturamento (R$)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        "data/processed/faturamento_cidade.png",
        bbox_inches="tight"
    )

    plt.close()


def grafico_ticket_medio_cidade(ticket_medio_cidade):
    ticket_medio_cidade.plot(kind="bar")

    plt.title("Ticket Médio por Cidade")
    plt.xlabel("Cidade")
    plt.ylabel("Ticket Médio (R$)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        "data/processed/ticket_medio_cidade.png",
        bbox_inches="tight"
    )

    plt.close()

