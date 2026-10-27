# Etapa 2 — Dia 5: painel comparativo e validação de casos-limite

**Data da preparação:** 26/10/2026  
**Mensagem sugerida do commit:** `feat: aprimora graficos e valida perfis ambiguos`

## 1. Propósito

A fase anterior já oferecia diagnóstico ponderado e roadmap. Esta evolução
**não troca o motor** nem a base de carreiras; melhora a leitura dos resultados
e acrescenta testes de robustez para entradas difíceis de interpretar.

## 2. Arquivos da mudança

| Arquivo | Finalidade |
| --- | --- |
| `painel_resultados.py` | Prepara dados dos gráficos e identifica empates/proximidade entre 1º e 2º. |
| `app.py` | Apresenta barras horizontais das dez carreiras, composição do Top 3 e comparação de critérios. |
| `simular_casos_limite.py` | Executa cinco perfis de demonstração no terminal. |
| `tests/test_robustez_etapa2.py` | 15 testes de extremos, ambiguidade, integridade do ranking, cálculos e dados dos gráficos. |
| `docs/etapa2_dia5.md` | Registro técnico deste desenvolvimento. |

## 3. Visualizações

1. **Ranking em barras horizontais** — compara as dez carreiras em ordem do motor.
2. **Alerta de resultados próximos** — considera uma diferença de até **5 pontos percentuais** entre os dois primeiros como decisão próxima; diferença zero é explicitamente descrita como empate.
3. **Composição da pontuação** — mostra, para cada carreira do Top 3, a base ponderada, bônus, penalidades negativas e o resultado final limitado a 0–100%.
4. **Pesos das principais afinidades** — compara os pesos das dimensões mais relevantes nas três carreiras, sem confundi-los com notas declaradas pelo usuário.

O limiar de 5 pontos é um **critério pedagógico de apresentação**, e não uma probabilidade nem um limiar estatístico validado. O desempate continua sendo feito pelo motor, com menor penalidade e, persistindo, ordem fixa declarada na base externa.

## 4. Testes de robustez

Os testes verificam:

- Todas as 13 afinidades no mínimo (1) e no máximo (5).
- Empates e diferenças pequenas entre o primeiro e o segundo lugar.
- Perfil misto de desenvolvimento web/mobile e execução determinística.
- Cem perfis sintéticos reproduzíveis para validar ordenação, limites e ausência de duplicatas.
- Integridade dos dados dos gráficos frente aos resultados do motor.
- Confirmação de que a comparação de pesos utiliza a base JSON externa.
- Rejeição de limites inválidos nos módulos de apresentação.
- Sintaxe do `app.py` e preservação da integração com roadmap.

**Observação:** perfis de fronteira avaliam estabilidade do algoritmo; não demonstram, por si só, que o diagnóstico psicológico/profissional seja correto no mundo real.

## 5. Comandos para validar

```powershell
python simular_casos_limite.py
python -m unittest discover -s tests -p "test_robustez_etapa2.py" -v
python -m unittest discover -s tests -v
python -m streamlit run app.py
```

No navegador: conclua as três etapas, observe as barras e a composição do Top 3, teste um perfil pouco definido e confirme que a autoavaliação e o roadmap da fase anterior continuam acessíveis.

## 6. Próximos passos

A etapa final prevista antes da entrega é revisar o README, comprovar a execução com capturas reais, executar a suíte completa, checar o repositório remoto e enviar a atividade até **29/10/2026, 19h (BRT)**.
