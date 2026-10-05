from src.data.postgres import conectar


def faturamento_por_mes():
    conn = conectar()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    DATE_TRUNC('month', v.data_venda)::date AS mes,
                    SUM(v.valor_total) AS faturamento,
                    COUNT(*) AS quantidade_vendas,
                    AVG(v.valor_total) AS ticket_medio
                FROM vendas v
                GROUP BY 1
                ORDER BY 1;
                """
            )

            return cur.fetchall()
    finally:
        conn.close()


def ranking_clientes():
    conn = conectar()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                WITH clientes AS (
                    SELECT
                        c.id,
                        c.nome,
                        SUM(v.valor_total) AS faturamento,
                        COUNT(v.id) AS quantidade_compras,
                        AVG(v.valor_total) AS ticket_medio
                    FROM clientes c
                    JOIN vendas v
                        ON v.cliente_id = c.id
                    GROUP BY c.id, c.nome
                )

                SELECT
                    nome,
                    faturamento,
                    quantidade_compras,
                    ticket_medio,
                    RANK() OVER (
                        ORDER BY faturamento DESC
                    ) AS ranking
                FROM clientes
                ORDER BY ranking;
                """
            )

            return cur.fetchall()
    finally:
        conn.close()


def pareto_clientes():
    conn = conectar()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                WITH clientes AS (
                    SELECT
                        c.nome,
                        SUM(v.valor_total) AS faturamento
                    FROM clientes c
                    JOIN vendas v
                        ON v.cliente_id = c.id
                    GROUP BY c.nome
                ),

                calculo AS (
                    SELECT
                        nome,
                        faturamento,

                        SUM(faturamento) OVER (
                            ORDER BY faturamento DESC
                        ) AS faturamento_acumulado,

                        SUM(faturamento) OVER () AS faturamento_total

                    FROM clientes
                )

                SELECT
                    nome,
                    faturamento,
                    ROUND(
                        (
                            faturamento_acumulado
                            / NULLIF(faturamento_total, 0)
                        ) * 100,
                        2
                    ) AS percentual_acumulado

                FROM calculo

                ORDER BY faturamento DESC;
                """
            )

            return cur.fetchall()
    finally:
        conn.close()


def crescimento_mensal():
    conn = conectar()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                WITH mensal AS (
                    SELECT
                        DATE_TRUNC(
                            'month',
                            data_venda
                        )::date AS mes,

                        SUM(valor_total) AS faturamento

                    FROM vendas

                    GROUP BY 1
                ),

                comparacao AS (
                    SELECT
                        mes,
                        faturamento,

                        LAG(faturamento) OVER (
                            ORDER BY mes
                        ) AS faturamento_anterior

                    FROM mensal
                )

                SELECT
                    mes,
                    faturamento,
                    faturamento_anterior,

                    ROUND(
                        (
                            (
                                faturamento
                                - faturamento_anterior
                            )
                            / NULLIF(
                                faturamento_anterior,
                                0
                            )
                        ) * 100,
                        2
                    ) AS crescimento_percentual

                FROM comparacao

                ORDER BY mes;
                """
            )

            return cur.fetchall()
    finally:
        conn.close()


def produtos_ranking():
    conn = conectar()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    p.nome AS produto,
                    p.categoria,

                    SUM(iv.quantidade) AS quantidade_vendida,

                    SUM(
                        iv.quantidade * iv.preco_uni
                    ) AS receita,

                    RANK() OVER (
                        ORDER BY
                            SUM(
                                iv.quantidade
                                * iv.preco_uni
                            ) DESC
                    ) AS ranking

                FROM itens_venda iv

                JOIN produtos p
                    ON p.id = iv.produto_id

                GROUP BY
                    p.id,
                    p.nome,
                    p.categoria

                ORDER BY ranking;
                """
            )

            return cur.fetchall()
    finally:
        conn.close()


def estoque_critico():
    conn = conectar()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    p.nome AS produto,
                    p.categoria,
                    e.quantidade,
                    e.estoque_min,

                    CASE
                        WHEN e.quantidade <= e.estoque_min
                        THEN 'CRÍTICO'
                        ELSE 'NORMAL'
                    END AS status

                FROM estoque e

                JOIN produtos p
                    ON p.id = e.produto_id

                ORDER BY
                    CASE
                        WHEN e.quantidade <= e.estoque_min
                        THEN 0
                        ELSE 1
                    END,

                    e.quantidade ASC;
                """
            )

            return cur.fetchall()
    finally:
        conn.close()


def faturamento_produto_mes():
    conn = conectar()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    DATE_TRUNC(
                        'month',
                        v.data_venda
                    )::date AS mes,
                    p.nome AS produto,
                    p.categoria,
                    SUM(
                        iv.quantidade * iv.preco_uni
                    ) AS receita,
                    SUM(iv.quantidade) AS quantidade_vendida
                FROM itens_venda iv
                JOIN vendas v
                    ON v.id = iv.vendas_id
                JOIN produtos p
                    ON p.id = iv.produto_id
                GROUP BY
                    1,
                    p.id,
                    p.nome,
                    p.categoria
                ORDER BY
                    mes,
                    receita DESC;
                """
            )

            return cur.fetchall()

    finally:
        conn.close()


def faturamento_categoria_mes():
    conn = conectar()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    DATE_TRUNC(
                        'month',
                        v.data_venda
                    )::date AS mes,
                    p.categoria,
                    SUM(
                        iv.quantidade * iv.preco_uni
                    ) AS receita,
                    SUM(iv.quantidade) AS quantidade_vendida
                FROM itens_venda iv
                JOIN vendas v
                    ON v.id = iv.vendas_id
                JOIN produtos p
                    ON p.id = iv.produto_id
                GROUP BY
                    1,
                    p.categoria
                ORDER BY
                    mes,
                    receita DESC;
                """
            )

            return cur.fetchall()

    finally:
        conn.close()


def faturamento_cliente_mes():
    conn = conectar()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    DATE_TRUNC(
                        'month',
                        v.data_venda
                    )::date AS mes,
                    c.nome AS cliente,
                    SUM(v.valor_total) AS faturamento,
                    COUNT(v.id) AS quantidade_compras,
                    AVG(v.valor_total) AS ticket_medio
                FROM vendas v
                JOIN clientes c
                    ON c.id = v.cliente_id
                GROUP BY
                    1,
                    c.id,
                    c.nome
                ORDER BY
                    mes,
                    faturamento DESC;
                """
            )

            return cur.fetchall()

    finally:
        conn.close()


def contribuicao_crescimento_mensal():
    conn = conectar()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                WITH mensal AS (
                    SELECT
                        DATE_TRUNC(
                            'month',
                            v.data_venda
                        )::date AS mes,
                        SUM(v.valor_total) AS faturamento
                    FROM vendas v
                    GROUP BY 1
                ),

                comparacao AS (
                    SELECT
                        mes,
                        faturamento,
                        LAG(faturamento) OVER (
                            ORDER BY mes
                        ) AS faturamento_anterior
                    FROM mensal
                )

                SELECT
                    mes,
                    faturamento,
                    faturamento_anterior,
                    faturamento
                        - faturamento_anterior
                        AS variacao_absoluta,
                    ROUND(
                        (
                            (
                                faturamento
                                - faturamento_anterior
                            )
                            / NULLIF(
                                faturamento_anterior,
                                0
                            )
                        ) * 100,
                        2
                    ) AS variacao_percentual
                FROM comparacao
                WHERE faturamento_anterior IS NOT NULL
                ORDER BY mes;
                """
            )

            return cur.fetchall()

    finally:
        conn.close()
