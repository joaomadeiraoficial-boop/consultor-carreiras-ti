"""Carrega e valida a base de conhecimento externa da Etapa 2.

Nesta primeira etapa, somente os dados descritivos das trilhas sao usados
pela interface antiga. O novo motor ponderado sera integrado no Dia 2.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CAMINHO_BASE = Path(__file__).resolve().with_name("regras_carreiras.json")
IDS_TRILHAS = (
    "backend", "frontend", "ciencia", "engenharia", "seguranca",
    "devops", "cloud", "mobile", "qa", "produto",
)
CAMPOS_COMPATIVEIS = ("nome", "resumo", "exemplo", "aprender")


def carregar_base(caminho: str | Path = CAMINHO_BASE) -> dict[str, Any]:
    """Lê o JSON e rejeita bases incompletas ou com pesos inválidos."""
    with Path(caminho).open(encoding="utf-8") as arquivo:
        base = json.load(arquivo)

    if not isinstance(base, dict) or not isinstance(base.get("dimensoes"), dict):
        raise ValueError("Base JSON inválida: faltam as dimensões.")
    dimensoes = set(base["dimensoes"])
    if not dimensoes:
        raise ValueError("Base JSON inválida: nenhuma dimensão configurada.")

    trilhas = base.get("trilhas")
    if not isinstance(trilhas, dict) or set(trilhas) != set(IDS_TRILHAS):
        raise ValueError("A base precisa conter as dez trilhas previstas.")

    for identificador, trilha in trilhas.items():
        if not isinstance(trilha, dict) or not all(trilha.get(c) for c in CAMPOS_COMPATIVEIS):
            raise ValueError(f"A trilha {identificador} não possui descrição completa.")
        if not isinstance(trilha["aprender"], list):
            raise ValueError(f"A lista de estudos de {identificador} é inválida.")
        pesos = trilha.get("pesos")
        if not isinstance(pesos, dict) or set(pesos) != dimensoes:
            raise ValueError(f"Os pesos de {identificador} não cobrem todas as dimensões.")
        if not all(type(valor) in (int, float) and 0 <= valor <= 5 for valor in pesos.values()):
            raise ValueError(f"Há pesos fora do intervalo de 0 a 5 em {identificador}.")
        if sum(pesos.values()) <= 0:
            raise ValueError(f"A trilha {identificador} precisa ter pesos positivos.")

    return base


def carregar_trilhas() -> dict[str, dict[str, Any]]:
    """Extrai apenas os campos que a interface da Etapa 1 já utiliza."""
    base = carregar_base()
    return {
        identificador: {campo: dados[campo] for campo in CAMPOS_COMPATIVEIS}
        for identificador, dados in base["trilhas"].items()
    }
