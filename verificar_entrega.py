"""Verificação integrada da Etapa 2, sem depender da interface gráfica.

Execute na pasta do projeto: python verificar_entrega.py
Esta verificação não substitui os testes unittest nem o teste visual no navegador.
"""
from __future__ import annotations

import json
from pathlib import Path

from base_conhecimento import carregar_base, IDS_TRILHAS
from entrevista_etapa2 import (
    ETAPAS, EXPERIENCIAS, IMPACTOS, OBJETIVOS,
    afinidades_iniciais, montar_relatorio,
)
from modulo_roadmap import carregar_roteiros, gerar_roadmap
from motor_ponderado import avaliar_ponderado
from painel_resultados import analisar_proximidade, tabela_ranking, tabela_composicao_top3

PASTA = Path(__file__).resolve().parent


def executar_verificacoes() -> list[tuple[str, bool, str]]:
    """Retorna resultados auditáveis para cada etapa da aplicação."""
    verificacoes: list[tuple[str, bool, str]] = []

    def registrar(nome: str, condicao: bool, observacao: str) -> None:
        verificacoes.append((nome, bool(condicao), observacao))

    base = carregar_base()
    roteiros = carregar_roteiros(base=base)
    registrar(
        "Base externa",
        len(base["trilhas"]) == 10 and set(base["trilhas"]) == set(IDS_TRILHAS)
        and len(base["dimensoes"]) == 13,
        f'{len(base["trilhas"])} carreiras e {len(base["dimensoes"])} afinidades',
    )
    registrar(
        "Entrevista em etapas",
        len(ETAPAS) == 3 and len(afinidades_iniciais(base)) == 13,
        "Três etapas de entrevista e treze dimensões",
    )

    notas = afinidades_iniciais(base)
    notas[next(iter(notas))] = 5
    resultado = avaliar_ponderado(notas, base=base)
    ids = [item.identificador for item in resultado.ranking]
    registrar(
        "Ranking e Top 3",
        len(ids) == 10 and len(set(ids)) == 10
        and len(resultado.top3) == 3
        and all(0 <= item.percentual <= 100 for item in resultado.ranking)
        and ids == [item.identificador for item in sorted(resultado.ranking, key=lambda x: (-x.percentual, x.penalidade))],
        "Dez carreiras distintas, Top 3 e percentuais entre 0 e 100",
    )
    registrar(
        "Resultados transparentes",
        len(tabela_ranking(resultado)) == 10
        and len(tabela_composicao_top3(resultado)) == 3
        and analisar_proximidade(resultado).diferenca >= 0,
        "Ranking, composição dos pontos e proximidade dos resultados",
    )
    registrar(
        "Roteiros externos",
        set(roteiros["trilhas"]) == set(IDS_TRILHAS),
        "Conteúdo de estudo disponível para todas as dez carreiras",
    )

    planos = {}
    for carreira_id, trilha in base["trilhas"].items():
        autoavaliacao = {competencia["id"]: 0 for competencia in trilha["competencias_junior"]}
        plano = gerar_roadmap(
            carreira_id=carreira_id,
            niveis=autoavaliacao,
            horas_semanais=6,
            objetivo=OBJETIVOS[0],
            base=base,
            roteiros=roteiros,
        )
        planos[carreira_id] = plano
    registrar(
        "Skill gaps e roadmap",
        len(planos) == 10
        and all(len(p.avaliacoes) > 0 and len(p.etapas) > 0 and p.total_semanas > 0
                and p.projeto_portfolio for p in planos.values()),
        "Gaps e planos de estudo produzidos para as dez carreiras",
    )

    relatorio = montar_relatorio(
        base=base,
        perfil={"experiencia": EXPERIENCIAS[0], "conhecimentos": []},
        afinidades=notas,
        objetivos={"objetivo": OBJETIVOS[0], "impacto": IMPACTOS[-1], "horas_semanais": 6},
        resultado=resultado,
        plano=planos[resultado.recomendacao],
    )
    arquivo = json.loads(json.dumps(relatorio, ensure_ascii=False))
    registrar(
        "Relatório exportável",
        len(arquivo["ranking"]) == 10 and len(arquivo["top3"]) == 3
        and len(arquivo["afinidades"]) == 13
        and arquivo["orientacao_profissional"]["carreira_id"] == resultado.recomendacao,
        "Relatório JSON inclui o ranking, as respostas e o plano",
    )

    arquivos = [
        "README.md", "requirements.txt", "app.py", "motor.py", "motor_ponderado.py",
        "regras_carreiras.json", "roteiros_carreiras.json", "painel_resultados.py",
        "docs/etapa2_entrega_final.md", "docs/guia_evidencias.md",
    ]
    faltando = [nome for nome in arquivos if not (PASTA / nome).is_file()]
    registrar("Arquivos da entrega", not faltando,
              "Todos os arquivos principais presentes" if not faltando else f"Ausentes: {', '.join(faltando)}")
    return verificacoes


def main() -> int:
    print("VERIFICACAO FINAL — CONSULTOR DE CARREIRAS / ETAPA 2")
    print("-" * 58)
    try:
        resultados = executar_verificacoes()
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as erro:
        print(f"[ERRO] Verificação interrompida: {erro}")
        return 1
    for descricao, aprovado, detalhes in resultados:
        marca = "OK" if aprovado else "FALHOU"
        print(f"[{marca}] {descricao}: {detalhes}")
    aprovadas = sum(1 for _, aprovado, _ in resultados if aprovado)
    print(f"\nResultado: {aprovadas}/{len(resultados)} verificações aprovadas.")
    print("Execute também: python -m unittest discover -s tests -v")
    print("E faça o teste visual: python -m streamlit run app.py")
    return 0 if aprovadas == len(resultados) else 1


if __name__ == "__main__":
    raise SystemExit(main())
