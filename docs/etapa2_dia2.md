# Etapa 2 — Dia 2 (25/10/2026): Motor de inferência ponderada

## Objetivo

Implementar **a lógica de compatibilidade ponderada** para as 10 trilhas, preservando o motor Experta e a interface Streamlit da Etapa 1. A integração de um questionário em escala 1–5 com a interface está planejada para o Dia 3.

## Arquivos deste incremento

- `regras_carreiras.json` — atualização dos parâmetros de cálculo e inclusão de 6 regras de ajuste transparentes (A01 a A06).
- `motor_ponderado.py` — leitura da base externa, validação, pontuação, penalidades, regras de contraste, top 3 e justificativas.
- `simular_perfil_ponderado.py` — demonstração executável, sem interface web.
- `tests/test_motor_ponderado.py` — 10 testes automatizados para condições normais e limite.
- `docs/etapa2_dia2.md` — este documento.

## Cálculo utilizado

Para uma trilha com pesos `w_i` e respostas `r_i` na escala inteira de **1 a 5**:

```
base (%) = 100 * soma[ w_i * (r_i - 1) / 4 ] / soma[w_i]
compatibilidade (%) = limitar(base + bonus_regras - penalidades, 0, 100)
```

- **Peso**: relevância da dimensão para a carreira (de 0 a 5).
- **Penalidade**: menos 6 pontos percentuais por dimensão com peso 4 ou 5 e afinidade 1 ou 2.
- **Regras de ajuste**: condições explícitas no JSON; algumas combinações relevantes ganham bônus de 4 ou 5 pontos.
- **Empate**: compatibilidade maior; se houver empate, menor penalidade; persistindo empate, ordem das trilhas declarada no JSON.

Os pesos e limiares são parâmetros didáticos, **não uma avaliação psicométrica validada nem uma probabilidade de emprego**. Os percentuais não precisam somar 100.

### Exemplos de diferenciação

- Ciência de Dados: estatística/modelagem preditiva altas + pipelines baixos.
- Engenharia de Dados: pipelines/bancos de dados altos + modelagem preditiva baixa.
- DevOps: automação/qualidade/nuvem altas.
- Cloud: nuvem alta com menor interesse em automação.

## Como executar no VS Code (terminal na raiz do projeto)

```powershell
python simular_perfil_ponderado.py
python -m unittest discover -s tests -p "test_motor_ponderado.py" -v
python -m unittest discover -s tests -p "test_base_conhecimento.py" -v
```

A primeira linha mostra Top 3, percentuais e explicações de um perfil demonstrativo. A segunda verifica o motor novo e a terceira confere a base JSON do Dia 1. Testes antigos que usam Experta também podem ser executados quando as dependências estiverem instaladas:

```powershell
python -m unittest discover -s tests -v
```

## Limitações e próximos incrementos

- **Dia 2:** motor novo funcional pelo terminal e isolado da interface antiga.
- **Dia 3:** questionário gradual de 1 a 5, navegação em etapas e integração Streamlit com `avaliar_ponderado`.
- **Dia 4:** gaps e plano de estudos para o nível Júnior.
- **Dia 5:** gráficos mais completos e testes adicionais para perfis ambíguos.
- **Dia 6:** README, evidências e revisão para entrega.

## Registro de versionamento

Mensagem sugerida para registrar as mudanças **após os testes**:

```
feat: implementa motor ponderado e ranking top 3
```
