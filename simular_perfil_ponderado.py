"""Demonstra o Top 3 ponderado no terminal, antes da interface do Dia 3.

Uso: python simular_perfil_ponderado.py
"""
from base_conhecimento import carregar_base
from motor_ponderado import avaliar_ponderado

base = carregar_base()
# Caso ilustrativo: interesse elevado em estatística e previsões.
perfil = {dimensao: 2 for dimensao in base["dimensoes"]}
perfil.update({
    "logica": 4,
    "matematica_estatistica": 5,
    "modelagem_preditiva": 5,
    "bancos_dados": 3,
    "pipelines_dados": 1,
    "comunicacao": 3,
})

resultado = avaliar_ponderado(perfil, base)
print("DIAGNÓSTICO DE DEMONSTRAÇÃO — ETAPA 2 / DIA 2")
print("Top 3 (afinidade ponderada, não probabilidade de sucesso):")
for posicao, item in enumerate(resultado.top3, start=1):
    print(f"{posicao}º {item.nome}: {item.percentual:.2f}% "
          f"(base {item.base_percentual:.2f}; bônus +{item.bonus:.2f}; "
          f"penalidade -{item.penalidade:.2f})")
print("\nPrincipais justificativas da trilha vencedora:")
for evidencia in resultado.top3[0].evidencias[:5]:
    print(f"  {evidencia.codigo}: {evidencia.motivo}")
