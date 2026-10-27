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
from modulo_roadmap import carregar_roteiros, gerar_roadmap
from painel_resultados import (
    analisar_proximidade, tabela_ranking, tabela_composicao_top3, pesos_destaque_top3,
)

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
if "etapa2_autoavaliacoes" not in st.session_state:
    st.session_state["etapa2_autoavaliacoes"] = {}
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
    st.write("Esta parte contextualiza o diagnóstico e ajuda a personalizar o roteiro de estudos.")
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
            "O objetivo e as horas disponíveis ajudam a orientar o roadmap; a experiência contextualiza seu perfil."
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

    st.markdown("#### As dez carreiras, lado a lado")
    tabela = tabela_ranking(resultado)
    st.bar_chart(
        tabela, x="Carreira", y="Compatibilidade (%)",
        horizontal=True, sort=False, height=430,
    )
    with st.expander("Ver ranking completo em tabela"):
        st.dataframe(tabela, hide_index=True)

    proximidade = analisar_proximidade(resultado)
    st.markdown("#### A decisão foi apertada?")
    if proximidade.muito_proximas:
        st.warning(proximidade.mensagem)
    else:
        st.info(proximidade.mensagem)
    st.caption("Critério didático: diferença de até 5 pontos percentuais indica perfis próximos.")

    st.markdown("#### De onde vêm os pontos do Top 3?")
    composicao = tabela_composicao_top3(resultado)
    st.bar_chart(
        composicao, x="Carreira",
        y=["Base (p.p.)", "Bônus (p.p.)", "Penalidades (p.p.)"],
        horizontal=True, stack=False,
    )
    st.dataframe(composicao, hide_index=True)
    st.caption(
        "Base ponderada + bônus − penalidades, com resultado limitado a 0–100%. "
        "As parcelas são mostradas separadamente para facilitar a auditoria."
    )

    with st.expander("Comparar os critérios mais valorizados pelas três trilhas"):
        pesos = pesos_destaque_top3(resultado, base)
        st.bar_chart(
            pesos, x="Afinidade", y=[item.nome for item in resultado.top3],
            horizontal=True, stack=False,
        )
        st.dataframe(pesos, hide_index=True)
        st.caption(
            "Os valores são pesos extraídos de regras_carreiras.json, "
            "não novas notas atribuídas ao usuário."
        )

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

    st.divider()
    st.markdown("#### Seu próximo passo: competências para Júnior")
    st.write(
        "Gostar de uma área é diferente de conhecer suas ferramentas. "
        "Avalie o que você **já consegue fazer**, de 0 (nunca estudei) a 5 "
        "(consigo aplicar com autonomia). A referência acadêmica aqui é o nível 3."
    )

    chave_carreira = primeiro.identificador
    competencias = base["trilhas"][chave_carreira]["competencias_junior"]
    avaliacoes_salvas = st.session_state["etapa2_autoavaliacoes"].get(chave_carreira, {})
    respostas_novas = {}
    with st.form(f"form_lacunas_{chave_carreira}"):
        for competencia in competencias:
            codigo = competencia["id"]
            respostas_novas[codigo] = st.slider(
                f"{competencia['nome']} (meta de referência: {competencia['nivel_requerido']}/5)",
                min_value=0, max_value=5,
                value=avaliacoes_salvas.get(codigo, 0), step=1,
                key=f"lacuna_{codigo}",
            )
        gerar = st.form_submit_button("📚 Gerar meu plano de estudos", type="primary")
    if gerar:
        st.session_state["etapa2_autoavaliacoes"][chave_carreira] = respostas_novas

    plano = None
    niveis_atuais = st.session_state["etapa2_autoavaliacoes"].get(chave_carreira)
    if niveis_atuais is not None:
        try:
            plano = gerar_roadmap(
                carreira_id=chave_carreira, niveis=niveis_atuais,
                horas_semanais=st.session_state["etapa2_objetivos"]["horas_semanais"],
                objetivo=st.session_state["etapa2_objetivos"]["objetivo"],
                base=base, roteiros=carregar_roteiros(base=base),
            )
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as erro:
            st.error(f"Não foi possível montar o roadmap: {erro}")
        else:
            st.markdown("#### Lacunas de competências (skill gaps)")
            a, b = st.columns(2)
            a.metric("Índice orientativo de preparo", f"{plano.preparo_estimado:.1f}%")
            b.metric("Semanas estimadas para cobrir lacunas", str(plano.total_semanas))
            st.dataframe([
                {"Competência": h.nome, "Seu nível": h.nivel_atual,
                 "Meta Júnior": h.nivel_junior, "Faltam níveis": h.lacuna,
                 "Situação": h.situacao} for h in plano.avaliacoes
            ], hide_index=True)
            st.caption(plano.aviso)

            st.markdown("#### Roadmap personalizado")
            st.write(
                f"Disponibilidade informada: **{plano.horas_semanais} h/semana**. "
                f"Objetivo: **{plano.objetivo}**. "
                "O planejamento prioriza suas maiores lacunas."
            )
            if not plano.etapas:
                st.success(
                    "Você informou ter atingido as metas desta referência inicial. "
                    "O próximo passo é praticar, validar suas habilidades e aprofundar os temas."
                )
            for etapa in plano.etapas:
                with st.expander(
                    f"{etapa.ordem}. {etapa.competencia} — "
                    f"semana(s) {etapa.inicio_semana} a {etapa.fim_semana}",
                    expanded=etapa.ordem == 1,
                ):
                    st.write(f"Estudo aproximado: **{etapa.horas_estimadas} horas**.")
                    for topico in etapa.topicos:
                        st.write(f"• {topico}")
                    st.write(f"**Prática:** {etapa.atividade_pratica}")
            st.markdown("**Projeto para o portfólio no GitHub**")
            st.write(plano.projeto_portfolio)
            st.markdown("**Certificações ou formações opcionais**")
            for certificacao in plano.certificacoes_opcionais:
                st.write(f"• {certificacao}")
            st.caption("Certificações não são obrigatórias; verifique disponibilidade e custos atuais.")
    else:
        st.info("Preencha os níveis acima e clique em **Gerar meu plano de estudos**.")

    relatorio = montar_relatorio(
        base, st.session_state["etapa2_perfil"],
        st.session_state["etapa2_afinidades"],
        st.session_state["etapa2_objetivos"], resultado,
        plano=plano,
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
    st.write("**10 carreiras · 13 afinidades · Top 3 · Skill gaps**")
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
        "**Orientação profissional:** após o Top 3, o usuário autoavalia "
        "as competências da trilha principal. O sistema compara as notas com "
        "os requisitos Júnior do JSON e gera um roteiro por lacunas."
    )
    with st.expander("Mostrar as 13 dimensões avaliadas"):
        st.dataframe(
            [{"Dimensão": d["titulo"], "Pergunta": d["pergunta"]}
             for d in base["dimensoes"].values()],
            hide_index=True,
        )
