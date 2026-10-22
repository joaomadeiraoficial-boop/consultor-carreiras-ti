"""Interface Streamlit do Consultor Inteligente de Carreiras em TI."""
from __future__ import annotations

import csv
import io
import json
from dataclasses import asdict
from pathlib import Path

import streamlit as st

from conhecimento import OPCOES, ROTULOS, TRILHAS
from motor import avaliar

BASE = Path(__file__).resolve().parent
st.set_page_config(
    page_title="Consultor Inteligente de Carreiras em TI",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container {max-width: 1120px; padding-top: 2.2rem;}
    h1, h2, h3 {letter-spacing: -0.03em;}
    [data-testid="stMetricValue"] {font-size: 2.0rem;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def ler_matriz():
    with (BASE / "docs" / "matriz_decisao.csv").open("r", encoding="utf-8-sig", newline="") as arq:
        return list(csv.DictReader(arq, delimiter=";"))


def perguntar(campo: str, titulo: str, ajuda: str) -> str | None:
    opcoes = [codigo for codigo, _ in OPCOES[campo]]
    return st.selectbox(
        titulo,
        options=opcoes,
        index=None,
        placeholder="Selecione uma opção...",
        format_func=lambda codigo: ROTULOS[campo][codigo],
        help=ajuda,
        key=f"pergunta_{campo}",
    )


def renderizar_resultado(respostas: dict[str, str]):
    resultado = avaliar(respostas)
    trilha = TRILHAS[resultado.recomendacao]

    st.divider()
    st.subheader("Seu diagnóstico")
    st.success(f"Trilha recomendada: **{trilha['nome']}**")
    a, b, c = st.columns(3)
    a.metric("Pontuação obtida", f"{resultado.ranking[0][1]} pontos")
    b.metric("Regras disparadas", len(resultado.evidencias[resultado.recomendacao]))
    c.metric("Trilhas analisadas", len(resultado.ranking))
    st.write(trilha["resumo"])
    st.info(f"**Exemplo de projeto:** {trilha['exemplo']}")

    st.markdown("#### Por que o sistema escolheu essa trilha?")
    for regra in resultado.evidencias[resultado.recomendacao]:
        st.markdown(f"- **{regra.codigo} (+{regra.pontos} pontos):** {regra.motivo}")
    st.caption(resultado.criterio_desempate)

    st.markdown("#### O que estudar primeiro")
    st.write(" · ".join(trilha["aprender"]))

    st.markdown("#### Comparação entre as dez trilhas")
    linhas = [
        {
            "Posição": i,
            "Carreira": TRILHAS[trilha_id]["nome"],
            "Pontos": pontos,
            "Regras ativadas": len(resultado.evidencias[trilha_id]),
        }
        for i, (trilha_id, pontos) in enumerate(resultado.ranking, start=1)
    ]
    st.dataframe(linhas, use_container_width=True, hide_index=True)
    if resultado.ranking[1][1] > 0:
        alternativa = TRILHAS[resultado.ranking[1][0]]["nome"]
        st.caption(f"Outra opção a explorar: {alternativa}.")

    with st.expander("Ver todos os motivos e pontos das outras trilhas"):
        for trilha_id, pontos in resultado.ranking:
            st.markdown(f"**{TRILHAS[trilha_id]['nome']} — {pontos} pontos**")
            if not resultado.evidencias[trilha_id]:
                st.write("Nenhuma regra foi acionada para essa trilha.")
            for regra in resultado.evidencias[trilha_id]:
                st.write(f"{regra.codigo}: +{regra.pontos} — {regra.motivo}")

    relatorio = {
        "respostas": {campo: ROTULOS[campo][codigo] for campo, codigo in respostas.items()},
        "recomendacao": trilha["nome"],
        "pontuacao": resultado.ranking[0][1],
        "justificativas": [asdict(regra) for regra in resultado.evidencias[resultado.recomendacao]],
        "ranking": linhas,
        "criterio_desempate": resultado.criterio_desempate,
    }
    st.download_button(
        "📥 Baixar meu diagnóstico em JSON",
        data=json.dumps(relatorio, indent=2, ensure_ascii=False),
        file_name="diagnostico_carreira_ti.json",
        mime="application/json",
    )
    st.caption("Pontuação é baseada em regras, não representa porcentagem de aptidão nem probabilidade de sucesso.")


with st.sidebar:
    st.subheader("🧭 Guia rápido")
    st.write("Responda às cinco perguntas; o motor de regras analisará dez carreiras possíveis.")
    st.write("**Tecnologias:** Python + Experta + Streamlit")
    st.write("**Base de conhecimento:** 46 regras SE–ENTÃO")
    st.info("O diagnóstico é uma orientação exploratória, não uma decisão definitiva sobre sua carreira.")
    st.caption("Projeto acadêmico • UNIPAC Barbacena")

st.title("🧭 Consultor Inteligente de Carreiras em TI")
st.write("Descubra uma trilha para começar a explorar com um sistema especialista explicável.")

tab_entrevista, tab_trilhas, tab_regras = st.tabs(["🎯 Fazer entrevista", "🧑‍💻 Conhecer as carreiras", "🧠 Como o sistema decide"])

with tab_entrevista:
    st.subheader("Conte um pouco sobre seus interesses")
    st.caption("Selecione uma resposta em cada campo. Não há respostas certas ou erradas.")
    with st.form("formulario_carreira"):
        esquerda, direita = st.columns(2, gap="large")
        with esquerda:
            matematica = perguntar("matematica", "1. Qual é sua afinidade com matemática e estatística?", "Considere gosto ou interesse, não apenas notas escolares.")
            atividade = perguntar("atividade", "2. O que você gostaria de fazer no dia a dia?", "Escolha a atividade que mais chama sua atenção.")
            ferramenta = perguntar("ferramenta", "3. Qual linguagem ou ferramenta mais combina com você?", "Pode selecionar 'Nenhuma' caso esteja começando.")
        with direita:
            entrega = perguntar("entrega", "4. Que resultado você gostaria de entregar?", "Pense no impacto principal do seu trabalho.")
            estilo = perguntar("estilo", "5. Qual modo de trabalhar você prefere?", "Escolha o tipo de atividade com que gostaria de passar mais tempo.")
        enviado = st.form_submit_button("🔎 Analisar meu perfil", type="primary", use_container_width=True)

    if enviado:
        respostas = dict(matematica=matematica, atividade=atividade, ferramenta=ferramenta, entrega=entrega, estilo=estilo)
        if any(resposta is None for resposta in respostas.values()):
            st.warning("Preencha as cinco respostas para gerar seu diagnóstico.")
            st.session_state.pop("diagnostico", None)
        else:
            st.session_state["diagnostico"] = respostas

    if "diagnostico" in st.session_state:
        renderizar_resultado(st.session_state["diagnostico"])

with tab_trilhas:
    st.subheader("As dez possibilidades de carreira")
    for codigo, dados in TRILHAS.items():
        with st.expander(dados["nome"]):
            st.write(dados["resumo"])
            st.write(f"**Exemplo prático:** {dados['exemplo']}")
            st.write("**Primeiros estudos:** " + ", ".join(dados["aprender"]))

with tab_regras:
    st.subheader("Motor de inferência transparente")
    st.write(
        "A biblioteca **Experta** compara suas respostas a regras do tipo SE–ENTÃO. "
        "Cada regra satisfeita soma pontos a uma trilha e registra uma justificativa. "
        "Ganha a trilha com maior pontuação; empates seguem critérios fixos e públicos."
    )
    st.markdown("**Pesos principais:** atividade (+3), atividade + entrega (+8), atividade + ferramenta (+4), entrega + estilo (+5).")
    st.write("Seis regras complementares reforçam distinções entre áreas próximas.")
    matriz = ler_matriz()
    st.dataframe(matriz, hide_index=True, use_container_width=True)
    with (BASE / "docs" / "matriz_decisao.csv").open("rb") as arq:
        st.download_button("📥 Baixar matriz de decisão CSV", data=arq.read(), file_name="matriz_decisao.csv", mime="text/csv")
    st.caption("A lógica não usa dados pessoais externos, aprendizado de máquina ou serviços pagos.")
