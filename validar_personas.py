"""Fase 4: executa as dez personas de teste e exibe o resultado no terminal."""
import json
from pathlib import Path
from conhecimento import TRILHAS
from motor import avaliar


if __name__ == "__main__":
    personas = json.loads((Path(__file__).parent / "personas.json").read_text(encoding="utf-8"))
    acertos = 0
    for persona in personas:
        resultado = avaliar(persona["respostas"])
        acertou = resultado.recomendacao == persona["esperada"]
        acertos += int(acertou)
        status = "OK" if acertou else "FALHOU"
        print(f"[{status}] {persona['nome']}: {TRILHAS[resultado.recomendacao]['nome']} "
              f"({resultado.ranking[0][1]} pts)")
    print(f"\nResultado: {acertos}/{len(personas)} personas corretas.")
    if acertos != len(personas):
        raise SystemExit(1)
