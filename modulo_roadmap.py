"""Autoavaliação de competências Júnior e roadmap gerado a partir de JSON externo.

Os níveis são autorrelatados: 0 = nunca estudei; 5 = consigo aplicar com autonomia.
Não inferimos domínio técnico a partir de afinidade ou interesse pela carreira.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import ceil
from pathlib import Path
from typing import Any
import json

from base_conhecimento import carregar_base, IDS_TRILHAS

ROTEIROS_PADRAO = Path(__file__).resolve().with_name("roteiros_carreiras.json")


@dataclass(frozen=True)
class AvaliacaoCompetencia:
    id: str
    nome: str
    nivel_atual: int
    nivel_junior: int
    lacuna: int
    situacao: str


@dataclass(frozen=True)
class PassoEstudo:
    ordem: int
    competencia: str
    semanas: int
    inicio_semana: int
    fim_semana: int
    horas_estimadas: int
    topicos: tuple[str, ...]
    atividade_pratica: str


@dataclass(frozen=True)
class PlanoCarreira:
    carreira_id: str
    carreira: str
    objetivo: str
    horas_semanais: int
    preparo_estimado: float
    avaliacoes: tuple[AvaliacaoCompetencia, ...]
    etapas: tuple[PassoEstudo, ...]
    total_semanas: int
    projeto_portfolio: str
    certificacoes_opcionais: tuple[str, ...]
    aviso: str

    def para_json(self) -> dict[str, Any]:
        return asdict(self)


def carregar_roteiros(caminho: str | Path = ROTEIROS_PADRAO, base: dict[str, Any] | None = None) -> dict[str, Any]:
    """Valida cobertura das dez trilhas e correspondência exata entre habilidades e estudos."""
    if base is None:
        base = carregar_base()
    with Path(caminho).open(encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    trilhas = dados.get("trilhas") if isinstance(dados, dict) else None
    if not isinstance(trilhas, dict) or set(trilhas) != set(IDS_TRILHAS):
        raise ValueError("O arquivo de roteiros deve conter exatamente as dez carreiras.")
    for carreira_id, config in trilhas.items():
        if not isinstance(config, dict):
            raise ValueError(f"Roteiro inválido: {carreira_id}.")
        esperadas = {c["id"] for c in base["trilhas"][carreira_id]["competencias_junior"]}
        competencias = config.get("competencias")
        if not isinstance(competencias, dict) or set(competencias) != esperadas:
            raise ValueError(f"Competências não correspondem ao nível Júnior: {carreira_id}.")
        for habilidade_id, instrucao in competencias.items():
            if (not isinstance(instrucao, dict)
                    or not isinstance(instrucao.get("topicos"), list)
                    or not instrucao["topicos"]
                    or not all(isinstance(t, str) and t.strip() for t in instrucao["topicos"])
                    or not isinstance(instrucao.get("atividade_pratica"), str)
                    or not instrucao["atividade_pratica"].strip()
                    or type(instrucao.get("horas_por_nivel")) is not int
                    or not 1 <= instrucao["horas_por_nivel"] <= 60):
                raise ValueError(f"Conteúdo de estudos inválido em {carreira_id}/{habilidade_id}.")
        certs = config.get("certificacoes_opcionais")
        if not isinstance(certs, list) or not all(isinstance(c, str) and c.strip() for c in certs):
            raise ValueError(f"Certificações inválidas para {carreira_id}.")
    return dados


def gerar_roadmap(
    carreira_id: str,
    niveis: dict[str, int],
    horas_semanais: int,
    objetivo: str,
    base: dict[str, Any] | None = None,
    roteiros: dict[str, Any] | None = None,
) -> PlanoCarreira:
    """Prioriza gaps maiores e estima semanas com a disponibilidade informada.

    Duração é uma aproximação didática; não constitui promessa de contratação.
    """
    if base is None:
        base = carregar_base()
    if carreira_id not in base["trilhas"]:
        raise ValueError("Carreira inexistente na base de conhecimento.")
    if roteiros is None:
        roteiros = carregar_roteiros(base=base)
    if type(horas_semanais) is not int or not 1 <= horas_semanais <= 40:
        raise ValueError("Horas semanais devem ser um número inteiro de 1 a 40.")
    if not isinstance(objetivo, str) or not objetivo.strip():
        raise ValueError("Objetivo profissional não informado.")
    habilidades = base["trilhas"][carreira_id]["competencias_junior"]
    esperado = {item["id"] for item in habilidades}
    if not isinstance(niveis, dict) or set(niveis) != esperado:
        raise ValueError("Informe a autoavaliação de todas as competências da carreira.")
    if any(type(n) is not int or not 0 <= n <= 5 for n in niveis.values()):
        raise ValueError("Cada nível precisa ser um número inteiro entre 0 e 5.")
    configuracao = roteiros["trilhas"][carreira_id]
    avaliacoes = []
    for c in habilidades:
        nivel = niveis[c["id"]]
        requerido = c["nivel_requerido"]
        if type(requerido) is not int or not 1 <= requerido <= 5:
            raise ValueError(f"Nível Júnior inválido para {c['id']}.")
        diferenca = max(0, requerido - nivel)
        avaliacoes.append(AvaliacaoCompetencia(
            id=c["id"], nome=c["nome"], nivel_atual=nivel,
            nivel_junior=requerido, lacuna=diferenca,
            situacao="Prioridade alta" if diferenca >= 2 else (
                "Precisa reforçar" if diferenca == 1 else "Meta de referência atingida"
            ),
        ))
    # Exibir os conteúdos que mais faltam primeiro; desempate preserva ordem do JSON.
    faltantes = sorted(
        (a for a in avaliacoes if a.lacuna > 0), key=lambda item: -item.lacuna,
    )
    semana = 1
    etapas = []
    for item in faltantes:
        materiais = configuracao["competencias"][item.id]
        horas = item.lacuna * materiais["horas_por_nivel"]
        duracao = max(1, ceil(horas / horas_semanais))
        etapas.append(PassoEstudo(
            ordem=len(etapas) + 1,
            competencia=item.nome, semanas=duracao,
            inicio_semana=semana, fim_semana=semana + duracao - 1,
            horas_estimadas=horas,
            topicos=tuple(materiais["topicos"]),
            atividade_pratica=materiais["atividade_pratica"],
        ))
        semana += duracao
    soma_necessaria = sum(c.nivel_junior for c in avaliacoes)
    indice = (sum(min(c.nivel_atual, c.nivel_junior) for c in avaliacoes) / soma_necessaria * 100)
    return PlanoCarreira(
        carreira_id=carreira_id,
        carreira=base["trilhas"][carreira_id]["nome"],
        objetivo=objetivo,
        horas_semanais=horas_semanais,
        preparo_estimado=round(indice, 1),
        avaliacoes=tuple(avaliacoes),
        etapas=tuple(etapas),
        total_semanas=semana - 1,
        projeto_portfolio=base["trilhas"][carreira_id]["projeto_portfolio"],
        certificacoes_opcionais=tuple(configuracao["certificacoes_opcionais"]),
        aviso=(
            "Índice orientativo baseado exclusivamente em autoavaliação; não certifica "
            "competência nem garante contratação. Tempos são estimativas de estudo. "
            "Certificações são opcionais e devem ser verificadas com o emissor."
        ),
    )
