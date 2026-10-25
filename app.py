"""Interface da Etapa 2 — entrevista em 3 etapas e inferência ponderada.

Executar: python -m streamlit run app.py
Os arquivos motor.py e os testes da Etapa 1 permanecem preservados.
"""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from base_conhecimento import carregar_base
from entrevista_etapa2 import (
    CONHECIMENTOS, ETAPAS, EXPERIENCIAS, IMPACTOS, OBJETIVOS,
    afinidades_iniciais, montar_relatorio, validar_afinidades, validar_contexto,
)
from motor_ponderado import avaliar_ponderado

BASE = Path(__file__).resolve().parent
st.set_page_config(
    page_title="Consultor Avançado de Carreiras em TI",
    page_icon="🧭",
    layout="wide",
)

st.markdown("""
<style>
.block-container {max-width: 1150px; padding-top: 1.7rem;}
h1, h2, h3 {letter-spacing: -0.025em;}
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def base_de_conhecimento():
    return carregar_base()


try:
    base = base_de_conhecimento()
except (OSError, ValueError, json.JSONDecodeError) as erro:
    st.error(f"Não foi possível ler a base externa de carreiras: {erro}")
    st.stop()

# Armazenamento explícito evita perda de respostas ao mudar de etapa.
if "etapa2_passo" not in st.session_state:
    st.session_state["etapa2_passo"] = 0
if "etapa2_perfil" not in st.session_state:
    st.session_state["etapa2_perfil"] = {
        "experiencia": EXPERIENCIAS[0], "conhecimentos": [],
    }
if "etapa2_afinidades" not in st.session_state:
    st.session_state["etapa2_afinidades"] = afinidades_iniciais(base)
if "etapa2_objetivos" not in st.session_state:
    st.session_state["etapa2_objetivos"] = {
        "objetivo": OBJETIVOS[0], "impacto": IMPACTOS[-1], "horas_semanais": 6,
    }


def ir_para(passo: int) -> None:
    st.session_state["etapa2_passo"] = passo
    st.rerun()


def indice_atual(lista: tuple[str, ...], escolhido: str) -> int:
    return lista.index(escolhido) if escolhido in lista else 0


def mostrar_perfil() -> None:
    st.subheader("1. Perfil pessoal")
    st.write("Queremos conhecer seu ponto de partida. Não é necessário informar nome ou e-mail.")
    previo = st.session_state["etapa2_perfil"]
    with st.form("form_etapa2_perfil"):
        experiencia = st.selectbox(
            "Qual sua experiência atual com programação e tecnologia?",
            options=EXPERIENCIAS,
            index=indice_atual(EXPERIENCIAS, previo["experiencia"]),
        )
        conhecimentos = st.multiselect(
            "Com quais tecnologias você já teve algum contato? (opcional)",
            options=CONHECIMENTOS,
            default=previo["conhecimentos"],
        )
        avancar = st.form_submit_button("Próximo: afinidades técnicas", type="primary")
    if avancar:
        st.session_state["etapa2_perfil"] = {
            "experiencia": experiencia, "conhecimentos": conhecimentos,
        }
        ir_para(1)


def mostrar_afinidades() -> None:
    st.subheader("2. Afinidades técnicas")
    st.write("Marque de 1 a 5 o quanto cada atividade desperta seu interesse.")
    escala = base["escala_afinidade"]
    minimo, maximo = escala["minimo"], escala["maximo"]
    st.caption("1 = nenhuma afinidade · 3 = afinidade moderada · 5 = muita afinidade")
    salvas = st.session_state["etapa2_afinidades"]
    notas: dict[str, int] = {}
    with st.form("form_etapa2_afinidades"):
        esquerda, direita = st.columns(2, gap="large")
        for indice, (codigo, info) in enumerate(base["dimensoes"].items()):
            coluna = esquerda if indice % 2 == 0 else direita
            with coluna:
                notas[codigo] = st.slider(
                    info["pergunta"], min_value=minimo, max_value=maximo,
                    value=salvas.get(codigo, 3), step=1, key=f"etapa2_slider_{codigo}",
                )
        voltar = st.form_submit_button("← Voltar ao perfil")
        avancar = st.form_submit_button("Próximo: objetivos profissionais →", type="primary")
    if voltar or avancar:
        try:
            st.session_state["etapa2_afinidades"] = validar_afinidades(notas, base)
        except ValueError as erro:
            st.error(str(erro))
            return
        ir_para(0 if voltar else 2)


def mostrar_objetivos() -> None:
    st.subheader("3. Objetivos de carreira")
    st.write("Esta parte contextualiza o diagnóstico e servirá de base para o roadmap personalizado.")
    previo = st.session_state["etapa2_objetivos"]
    with st.form("form_etapa2_objetivos"):
        objetivo = st.selectbox(
            "Qual seu principal objetivo profissional?", options=OBJETIVOS,
            index=indice_atual(OBJETIVOS, previo["objetivo"]),
        )
        impacto = st.selectbox(
            "Qual tipo de contribuição mais desperta seu interesse?", options=IMPACTOS,
            index=indice_atual(IMPACTOS, previo["impacto"]),
        )
        horas = st.slider(
            "Quantas horas por semana você pretende dedicar aos estudos?",
            min_value=1, max_value=40, value=previo["horas_semanais"], step=1,
        )
        st.caption(
            "O ranking de hoje utiliza as 13 notas de afinidade. "
            "Experiência e objetivos serão usados no módulo de roadmap da próxima etapa."
        )
        voltar = st.form_submit_button("← Voltar às afinidades")
        diagnosticar = st.form_submit_button("🔎 Calcular minha compatibilidade", type="primary")
    if voltar or diagnosticar:
        novos_objetivos = {
            "objetivo": objetivo, "impacto": impacto, "horas_semanais": horas,
        }
        try:
            validar_contexto(st.session_state["etapa2_perfil"], novos_objetivos)
        except ValueError as erro:
            st.error(str(erro))
            return
        st.session_state["etapa2_objetivos"] = novos_objetivos
        if voltar:
            ir_para(1)
        else:
            try:
                notas = validar_afinidades(st.session_state["etapa2_afinidades"], base)
                st.session_state["etapa2_resultado"] = avaliar_ponderado(notas, base)
            except ValueError as erro:
                st.error(f"Não foi possível calcular o diagnóstico: {erro}")
                return
            ir_para(3)


def mostrar_resultado() -> None:
    resultado = st.session_state.get("etapa2_resultado")
    if resultado is None:
        ir_para(0)
        return

    st.subheader("Seu diagnóstico de compatibilidade")
    primeiro = resultado.top3[0]
    st.success(f"Carreira mais compatível com suas respostas: **{primeiro.nome}**")
    colunas = st.columns(3)
    for posicao, (coluna, trilha) in enumerate(zip(colunas, resultado.top3), start=1):
        coluna.metric(f"{posicao}º lugar — {trilha.nome}", f"{trilha.percentual:.2f}%")
    st.caption(
        "Os percentuais são índices heurísticos de aderência, NÃO probabilidades "
        "de conseguir emprego. Os valores não precisam somar 100%."
    )

    st.markdown("#### Comparação de todas as carreiras")
    tabela = [
        {"Carreira": item.nome, "Compatibilidade (%)": item.percentual}
        for item in resultado.ranking
    ]
    st.bar_chart(tabela, x="Carreira", y="Compatibilidade (%)")
    st.dataframe(tabela, hide_index=True)

    st.markdown("#### Por que esta carreira ficou em primeiro?")
    st.write(base["trilhas"][primeiro.identificador]["resumo"])
    positivas = [e for e in primeiro.evidencias if e.impacto > 0]
    negativas = [e for e in primeiro.evidencias if e.impacto < 0]
    for evidencia in positivas[:6]:
        st.write(f"**{evidencia.codigo} (+{evidencia.impacto:.2f})** — {evidencia.motivo}")
    if negativas:
        st.markdown("**Fatores que reduziram a compatibilidade:**")
        for evidencia in negativas[:4]:
            st.write(f"**{evidencia.codigo} ({evidencia.impacto:.2f})** — {evidencia.motivo}")
    st.caption(resultado.criterio_desempate)

    with st.expander("Ver a composição da pontuação das três trilhas"):
        for item in resultado.top3:
            st.write(
                f"**{item.nome}: {item.percentual:.2f}%** — "
                f"base {item.base_percentual:.2f}, bônus +{item.bonus:.2f}, "
                f"penalidade −{item.penalidade:.2f}"
            )
            for evidencia in item.evidencias[:8]:
                st.write(f"{evidencia.codigo}: {evidencia.motivo}")

    relatorio = montar_relatorio(
        base, st.session_state["etapa2_perfil"],
        st.session_state["etapa2_afinidades"],
        st.session_state["etapa2_objetivos"], resultado,
    )
    st.download_button(
        "📥 Baixar diagnóstico em JSON",
        data=json.dumps(relatorio, ensure_ascii=False, indent=2),
        file_name="diagnostico_etapa2.json", mime="application/json",
    )

    a, b, c = st.columns(3)
    if a.button("Editar meu perfil"):
        ir_para(0)
    if b.button("Editar afinidades"):
        ir_para(1)
    if c.button("Editar objetivos"):
        ir_para(2)


with st.sidebar:
    st.header("🧭 Consultor de Carreiras")
    st.write("**Etapa 2:** diagnóstico por pesos e tratamento de incerteza.")
    st.write("**10 carreiras · 13 afinidades · Top 3**")
    st.caption("Python + Streamlit · base de conhecimento JSON externa")
    st.info("Ferramenta acadêmica e exploratória; não substitui orientação profissional.")
    st.caption("UNIPAC Barbacena — Inteligência Artificial")

st.title("🧭 Consultor Avançado de Carreiras em TI")
st.write("Descubra carreiras compatíveis com seus interesses por meio de regras e pontuação ponderada.")

aba_entrevista, aba_carreiras, aba_metodo = st.tabs(
    ["🎯 Entrevista", "💻 Dez carreiras", "🧠 Como funciona"]
)

with aba_entrevista:
    passo = st.session_state["etapa2_passo"]
    if passo < len(ETAPAS):
        st.progress((passo + 1) / len(ETAPAS))
        st.caption(f"Etapa {passo + 1} de {len(ETAPAS)}: {ETAPAS[passo]}")
    else:
        st.progress(1.0)
        st.caption("Entrevista concluída — resultados")

    if passo == 0:
        mostrar_perfil()
    elif passo == 1:
        mostrar_afinidades()
    elif passo == 2:
        mostrar_objetivos()
    else:
        mostrar_resultado()

with aba_carreiras:
    st.subheader("As dez trilhas de tecnologia")
    for codigo, dados in base["trilhas"].items():
        with st.expander(dados["nome"]):
            st.write(dados["resumo"])
            st.write(f"**Exemplo de projeto:** {dados['exemplo']}")
            st.write("**Tecnologias iniciais:** " + ", ".join(dados["aprender"]))

with aba_metodo:
    st.subheader("Como o motor calcula a compatibilidade")
    st.write(
        "As 13 notas variam de 1 a 5. Cada nota é normalizada e multiplicada "
        "pelo peso da carreira descrito em `regras_carreiras.json`. O motor soma "
        "as contribuições, aplica regras extras de bônus ou penalidade e limita "
        "o resultado ao intervalo de 0% a 100%."
    )
    st.write(
        "Empates são resolvidos por menor penalidade e, persistindo, "
        "pela ordem fixa das carreiras no JSON. O código da Etapa 1, incluindo "
        "as regras Experta, permanece no repositório."
    )
    st.info(
        "**Próximos módulos:** identificação das lacunas para nível Júnior "
        "e geração de um roadmap de estudos individualizado."
    )
    with st.expander("Mostrar as 13 dimensões avaliadas"):
        st.dataframe(
            [{"Dimensão": d["titulo"], "Pergunta": d["pergunta"]}
             for d in base["dimensoes"].values()],
            hide_index=True,
        )
