"""Transformações puras dos resultados para o painel comparativo da Etapa 2.

Não altera o motor ponderado; prepara os dados dos gráficos e sinaliza
recomendações com percentuais próximos. Sem dependência de Streamlit.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Any

from motor_ponderado import ResultadoPonderado


@dataclass(frozen=True)
class ProximidadeRanking:
    diferenca: float
    empate: bool
    muito_proximas: bool
    mensagem: str


def analisar_proximidade(
    resultado: ResultadoPonderado, limiar_proximidade: float = 5.0,
) -> ProximidadeRanking:
    """Indica empate exato ou diferença pequena entre os dois primeiros.

    limiar_proximidade representa pontos percentuais, e não porcentagem
    relativa ou probabilidade. Empates seguem os critérios do próprio motor.
    """
    if type(limiar_proximidade) not in (int, float) or not isfinite(limiar_proximidade) or not 0 <= limiar_proximidade <= 100:
        raise ValueError("O limiar deve ser um número de 0 a 100.")
    if len(resultado.ranking) < 2:
        raise ValueError("São necessárias pelo menos duas carreiras para comparar.")
    primeiro, segundo = resultado.ranking[:2]
    diferenca = round(primeiro.percentual - segundo.percentual, 2)
    if diferenca < 0:
        raise ValueError("O ranking precisa estar ordenado do maior para o menor.")
    if diferenca == 0:
        mensagem = (
            "Empate na compatibilidade calculada entre as duas primeiras trilhas. "
            "A ordem exibida segue o critério de desempate do motor; vale explorar ambas."
        )
    elif diferenca <= limiar_proximidade:
        mensagem = (
            f"As duas primeiras trilhas ficaram separadas por apenas {diferenca:.2f} "
            "pontos percentuais. O resultado é próximo, e ambas merecem atenção."
        )
    else:
        mensagem = (
            f"A primeira trilha ficou {diferenca:.2f} pontos percentuais acima da segunda. "
            "Esse índice é uma comparação heurística, não uma previsão de desempenho."
        )
    return ProximidadeRanking(
        diferenca=diferenca,
        empate=diferenca == 0,
        muito_proximas=diferenca <= limiar_proximidade,
        mensagem=mensagem,
    )


def tabela_ranking(resultado: ResultadoPonderado) -> list[dict[str, Any]]:
    """Devolve o ranking completo ordenado, pronto para gráfico ou tabela."""
    return [
        {
            "Posição": posicao,
            "Carreira": trilha.nome,
            "Compatibilidade (%)": trilha.percentual,
        }
        for posicao, trilha in enumerate(resultado.ranking, start=1)
    ]


def tabela_composicao_top3(resultado: ResultadoPonderado) -> list[dict[str, Any]]:
    """Exibe os componentes sem esconder penalidades ou arredondamento."""
    return [
        {
            "Carreira": trilha.nome,
            "Base (p.p.)": trilha.base_percentual,
            "Bônus (p.p.)": trilha.bonus,
            "Penalidades (p.p.)": -trilha.penalidade,
            "Resultado (%)": trilha.percentual,
        }
        for trilha in resultado.top3
    ]


def pesos_destaque_top3(
    resultado: ResultadoPonderado,
    base: dict[str, Any],
    quantidade: int = 6,
) -> list[dict[str, Any]]:
    """Compara os pesos declarados no JSON das trilhas do Top 3.

    São PESOS das carreiras, não novas respostas nem as contribuições
    individuais já usadas pelo motor. Seleciona dimensões mais relevantes.
    """
    if type(quantidade) is not int or quantidade < 1:
        raise ValueError("A quantidade deve ser um inteiro positivo.")
    trilhas = base["trilhas"]
    dimensoes = base["dimensoes"]
    if not resultado.top3:
        raise ValueError("O resultado não possui carreiras no Top 3.")
    selecionadas = [trilhas[item.identificador] for item in resultado.top3]
    nomes = [item.nome for item in resultado.top3]
    ordenadas = sorted(
        dimensoes,
        key=lambda cod: (
            -sum(trilha["pesos"][cod] for trilha in selecionadas),
            -max(trilha["pesos"][cod] for trilha in selecionadas),
            list(dimensoes).index(cod),
        ),
    )
    tabela = []
    for codigo in ordenadas[:quantidade]:
        linha = {"Afinidade": dimensoes[codigo]["titulo"]}
        for nome, trilha in zip(nomes, selecionadas):
            linha[nome] = trilha["pesos"][codigo]
        tabela.append(linha)
    return tabela
