"""Dados e validações da entrevista gradual da Etapa 2.

Módulo sem dependência de Streamlit: a interface coleta as respostas,
este módulo valida e monta um relatório exportável, e o motor ponderado
faz os cálculos com as regras carregadas de regras_carreiras.json.
"""
from __future__ import annotations

from dataclasses import asdict
from typing import Any

from motor_ponderado import ResultadoPonderado
from modulo_roadmap import PlanoCarreira

ETAPAS = ("Perfil pessoal", "Afinidades técnicas", "Objetivos de carreira")
EXPERIENCIAS = (
    "Iniciante (ainda não programei)",
    "Básico (já fiz exercícios ou projetos pequenos)",
    "Intermediário (já desenvolvi projetos completos)",
    "Avançado (experiência profissional ou projetos complexos)",
)
CONHECIMENTOS = (
    "Python", "JavaScript", "HTML e CSS", "Bancos de dados",
    "Linux e redes", "Cloud", "Testes de software", "Design e UX",
)
OBJETIVOS = (
    "Descobrir uma área de TI",
    "Conseguir a primeira oportunidade",
    "Mudar de área de atuação",
    "Aprofundar conhecimentos na área atual",
)
IMPACTOS = (
    "Criar produtos e interfaces para usuários",
    "Trabalhar com dados e decisões",
    "Proteger sistemas e informações",
    "Manter e automatizar infraestrutura",
    "Organizar produto e necessidades de negócio",
    "Ainda não tenho preferência",
)


def afinidades_iniciais(base: dict[str, Any]) -> dict[str, int]:
    """Inicia todas as escalas em 3, sem privilegiar uma carreira."""
    return {dimensao: 3 for dimensao in base["dimensoes"]}


def validar_afinidades(respostas: dict[str, int], base: dict[str, Any]) -> dict[str, int]:
    """Confere presença, ausência de extras e valores inteiros da escala externa."""
    if not isinstance(respostas, dict):
        raise ValueError("As afinidades precisam estar em um dicionário.")
    esperadas = set(base["dimensoes"])
    recebidas = set(respostas)
    if esperadas != recebidas:
        faltantes = sorted(esperadas - recebidas)
        extras = sorted(recebidas - esperadas)
        raise ValueError(f"Afinidades incompletas. Faltantes: {faltantes}; extras: {extras}.")
    minimo = base["escala_afinidade"]["minimo"]
    maximo = base["escala_afinidade"]["maximo"]
    for dimensao, valor in respostas.items():
        if type(valor) is not int or not minimo <= valor <= maximo:
            raise ValueError(f"'{dimensao}' deve ser um número inteiro de {minimo} a {maximo}.")
    # Garante ordem igual à base de conhecimento (útil para relatório estável).
    return {dimensao: respostas[dimensao] for dimensao in base["dimensoes"]}


def validar_contexto(perfil: dict[str, Any], objetivos: dict[str, Any]) -> None:
    """Valida campos das etapas 1 e 3, que contextualizam o diagnóstico."""
    if not isinstance(perfil, dict) or perfil.get("experiencia") not in EXPERIENCIAS:
        raise ValueError("Selecione uma experiência válida.")
    tecnologias = perfil.get("conhecimentos")
    if not isinstance(tecnologias, (list, tuple)) or any(x not in CONHECIMENTOS for x in tecnologias):
        raise ValueError("Há conhecimentos prévios inválidos.")
    if not isinstance(objetivos, dict) or objetivos.get("objetivo") not in OBJETIVOS:
        raise ValueError("Selecione um objetivo válido.")
    if objetivos.get("impacto") not in IMPACTOS:
        raise ValueError("Selecione uma preferência de entrega válida.")
    horas = objetivos.get("horas_semanais")
    if type(horas) is not int or not 1 <= horas <= 40:
        raise ValueError("As horas semanais devem estar entre 1 e 40.")


def montar_relatorio(
    base: dict[str, Any],
    perfil: dict[str, Any],
    afinidades: dict[str, int],
    objetivos: dict[str, Any],
    resultado: ResultadoPonderado,
    plano: PlanoCarreira | None = None,
) -> dict[str, Any]:
    """Monta um JSON transparente e sem dados pessoais identificáveis."""
    respostas = validar_afinidades(afinidades, base)
    validar_contexto(perfil, objetivos)
    return {
        "sistema": "Consultor Avançado de Carreiras em TI — Etapa 2",
        "metodo": "média ponderada com regras extras, bônus e penalidades do JSON",
        "aviso": (
            "Os percentuais expressam compatibilidade heurística: "
            "não são probabilidade de sucesso e não precisam somar 100%."
        ),
        "perfil": {"experiencia": perfil["experiencia"], "conhecimentos": list(perfil["conhecimentos"])},
        "objetivos": {
            "objetivo": objetivos["objetivo"],
            "impacto": objetivos["impacto"],
            "horas_semanais": objetivos["horas_semanais"],
        },
        "observacao_contexto": (
            "O ranking é calculado pelas 13 afinidades. A orientação de estudos "
            "considera a autoavaliação de conhecimentos, o objetivo e as horas disponíveis; "
            "a experiência informada contextualiza o histórico do usuário."
        ),
        "orientacao_profissional": plano.para_json() if plano is not None else None,
        "afinidades": [
            {
                "dimensao": codigo,
                "nome": base["dimensoes"][codigo]["titulo"],
                "nota": nota,
            }
            for codigo, nota in respostas.items()
        ],
        "recomendacao": resultado.ranking[0].nome,
        "top3": [asdict(item) for item in resultado.top3],
        "ranking": [
            {"carreira": item.nome, "percentual": item.percentual,
             "base": item.base_percentual, "bonus": item.bonus, "penalidade": item.penalidade}
            for item in resultado.ranking
        ],
        "desempate": resultado.criterio_desempate,
    }
