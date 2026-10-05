import os

from openai import OpenAI

from src.ai.prompts import SYSTEM_PROMPT


DEFAULT_MODEL = os.getenv(
    "DATAFLOW_AI_MODEL",
    "gpt-6-luna",
)


def criar_cliente():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY não configurada."
        )

    return OpenAI(api_key=api_key)


def analisar(pergunta, contexto):
    cliente = criar_cliente()

    prompt = f"""
CONTEXTO ANALÍTICO DO DATAFLOW:

{contexto}

PERGUNTA DO USUÁRIO:

{pergunta}
"""

    resposta = cliente.responses.create(
        model=DEFAULT_MODEL,
        instructions=SYSTEM_PROMPT,
        input=prompt,
    )

    return resposta.output_text
