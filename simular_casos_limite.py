"""Demonstra cinco cenários de validação da Etapa 2, sem Streamlit.

Executar na pasta do projeto: python simular_casos_limite.py
"""
from __future__ import annotations

from base_conhecimento import carregar_base
from motor_ponderado import avaliar_ponderado
from painel_resultados import analisar_proximidade


def executar() -> None:
    base = carregar_base()
    dimensoes = tuple(base["dimensoes"])

    def perfil(padrao: int, **alteracoes: int) -> dict[str, int]:
        return {**dict.fromkeys(dimensoes, padrao), **alteracoes}

    casos = {
        "Iniciante sem afinidade definida (todas 1)": perfil(1),
        "Afinidade máxima em tudo (todas 5)": perfil(5),
        "Perfil dividido entre interfaces e mobile": perfil(
            3, logica=5, design_ux=5, mobile=5, bancos_dados=5, testes_qualidade=4,
        ),
        "Ciência de Dados versus Engenharia de Dados": perfil(
            2, logica=4, matematica_estatistica=5, modelagem_preditiva=5,
            pipelines_dados=4, bancos_dados=4,
        ),
        "DevOps e Cloud simultaneamente": perfil(
            2, automacao=5, nuvem=5, logica=4, seguranca=4,
            testes_qualidade=4,
        ),
    }

    print("VALIDAÇÃO DE CASOS-LIMITE — ETAPA 2 / DIA 5")
    print("Os números são índices heurísticos de afinidade, não probabilidade de emprego.\n")
    for titulo, respostas in casos.items():
        resultado = avaliar_ponderado(respostas, base)
        proximidade = analisar_proximidade(resultado)
        print("=" * 65)
        print(titulo)
        for indice, trilha in enumerate(resultado.top3, 1):
            print(f"{indice}º {trilha.nome}: {trilha.percentual:.2f}%")
        print(proximidade.mensagem)
    print("\nPara executar a suíte completa: python -m unittest discover -s tests -v")


if __name__ == "__main__":
    executar()
