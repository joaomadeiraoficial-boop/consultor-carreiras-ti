"""Motor de inferência ponderada da Etapa 2 (Dia 2).

Independente da interface e do Experta da Etapa 1: o questionário gradual
será conectado a este motor no Dia 3. Todas as afinidades, pesos e regras
extras são carregados do JSON externo, sem dados de carreira fixos no código.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from base_conhecimento import carregar_base


@dataclass(frozen=True)
class Evidencia:
    codigo: str
    tipo: str  # afinidade | penalidade | ajuste
    impacto: float  # pontos percentuais; no item de afinidade, contribuição positiva
    motivo: str


@dataclass(frozen=True)
class PontuacaoTrilha:
    identificador: str
    nome: str
    percentual: float
    base_percentual: float
    bonus: float
    penalidade: float
    evidencias: tuple[Evidencia, ...]


@dataclass(frozen=True)
class ResultadoPonderado:
    ranking: tuple[PontuacaoTrilha, ...]
    top3: tuple[PontuacaoTrilha, ...]
    criterio_desempate: str

    @property
    def recomendacao(self) -> str:
        return self.ranking[0].identificador


def _validar_respostas(respostas: dict[str, int], base: dict[str, Any]) -> None:
    if not isinstance(respostas, dict):
        raise ValueError("As respostas precisam ser um dicionário.")
    dimensoes = set(base["dimensoes"])
    if set(respostas) != dimensoes:
        ausentes = sorted(dimensoes - set(respostas))
        inesperadas = sorted(set(respostas) - dimensoes)
        raise ValueError(f"Dimensões incorretas. Ausentes: {ausentes}; inesperadas: {inesperadas}.")
    escala = base["escala_afinidade"]
    minimo, maximo = escala["minimo"], escala["maximo"]
    if type(minimo) is not int or type(maximo) is not int or minimo >= maximo:
        raise ValueError("A escala de afinidade está inválida no JSON.")
    for dimensao, valor in respostas.items():
        if type(valor) is not int or not minimo <= valor <= maximo:
            raise ValueError(f"A resposta de '{dimensao}' deve ser um inteiro de {minimo} a {maximo}.")


def _regra_corresponde(regra: dict[str, Any], respostas: dict[str, int]) -> bool:
    """Condições min/max são declaradas no JSON e ligadas por E lógico."""
    for dimensao, limites in regra["condicoes"].items():
        if dimensao not in respostas or not isinstance(limites, dict):
            raise ValueError(f"Dimensão/regra inválida: {dimensao}.")
        if not limites or set(limites) - {"min", "max"}:
            raise ValueError(f"Operador inválido para {dimensao}.")
        if "min" in limites and respostas[dimensao] < limites["min"]:
            return False
        if "max" in limites and respostas[dimensao] > limites["max"]:
            return False
    return True


def avaliar_ponderado(respostas: dict[str, int], base: dict[str, Any] | None = None) -> ResultadoPonderado:
    """Calcula o Top 3 por afinidade ponderada com ajuste e penalidade.

    Percentuais representam aderência HEURÍSTICA ao perfil descrito no JSON,
    não probabilidade de emprego/sucesso nem percentuais que somam 100.
    """
    if base is None:
        base = carregar_base()
    _validar_respostas(respostas, base)

    conf = base["parametros_inferencia"]
    limiar = conf["limiar_baixa_afinidade"]
    peso_essencial = conf["peso_criterio_essencial"]
    penalidade_unitaria = conf["penalidade_por_criterio_essencial"]
    if not all(type(v) in (int, float) and v >= 0 for v in (limiar, peso_essencial, penalidade_unitaria)):
        raise ValueError("Parâmetros de penalidade inválidos no JSON.")

    escala = base["escala_afinidade"]
    menor, maior = escala["minimo"], escala["maximo"]
    trilhas: list[PontuacaoTrilha] = []
    for codigo, carreira in base["trilhas"].items():
        pesos = carreira["pesos"]
        total_pesos = sum(pesos.values())
        if total_pesos <= 0:
            raise ValueError(f"A trilha {codigo} não possui pesos positivos.")
        evidencias: list[Evidencia] = []
        soma = 0.0
        penalidade = 0.0
        for dim, peso in pesos.items():
            afinidade = (respostas[dim] - menor) / (maior - menor)
            contribuicao = 100 * (peso / total_pesos) * afinidade
            soma += contribuicao
            if peso > 0 and contribuicao > 0:
                evidencias.append(Evidencia(
                    f"P-{dim}", "afinidade", round(contribuicao, 2),
                    f"{base['dimensoes'][dim]['titulo']}: nota {respostas[dim]}/{maior}, peso {peso}."
                ))
            if peso >= peso_essencial and respostas[dim] <= limiar:
                penalidade += penalidade_unitaria
                evidencias.append(Evidencia(
                    f"L-{dim}", "penalidade", -float(penalidade_unitaria),
                    f"Baixa afinidade ({respostas[dim]}/{maior}) em competência essencial: "
                    f"{base['dimensoes'][dim]['titulo']}."
                ))

        bonus = 0.0
        for regra in base.get("regras_ajuste", []):
            if regra["trilha"] == codigo and _regra_corresponde(regra, respostas):
                ajuste = float(regra["pontos"])
                if ajuste >= 0:
                    bonus += ajuste
                else:
                    penalidade += abs(ajuste)
                evidencias.append(Evidencia(regra["id"], "ajuste", ajuste, regra["motivo"]))

        base_pct = soma  # contribuições já expressas em pontos percentuais
        percentual = min(100.0, max(0.0, base_pct + bonus - penalidade))
        evidencias.sort(key=lambda ev: (-abs(ev.impacto), ev.codigo))
        trilhas.append(PontuacaoTrilha(
            identificador=codigo,
            nome=carreira["nome"],
            percentual=round(percentual, 2),
            base_percentual=round(base_pct, 2),
            bonus=round(bonus, 2),
            penalidade=round(penalidade, 2),
            evidencias=tuple(evidencias),
        ))

    # A ordem declarada no JSON é usada somente em caso de empate completo.
    ranking = tuple(sorted(trilhas, key=lambda item: (-item.percentual, item.penalidade)))
    criterio = (
        "Ranking por compatibilidade ponderada; em empate, menor penalidade e, "
        "persistindo a igualdade, ordem fixa das trilhas no JSON."
    )
    return ResultadoPonderado(ranking=ranking, top3=ranking[:3], criterio_desempate=criterio)
