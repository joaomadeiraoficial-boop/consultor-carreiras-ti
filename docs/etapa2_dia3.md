# Etapa 2 — Dia 3: entrevista gradual no Streamlit

**Data do desenvolvimento:** 25/10/2026  
**Mensagem sugerida para o commit:** `feat: integra entrevista gradual ao Streamlit`

## Objetivo

Integrar o motor de inferência ponderado (`motor_ponderado.py`) à aplicação web, que agora realiza a entrevista em **três etapas** e coleta **13 afinidades de 1 a 5**. A base de conhecimento e os pesos continuam em `regras_carreiras.json`.

## Mudanças

1. `app.py` — reformula a interface para um **wizard** (formulário dividido em passos):
   - **Perfil pessoal:** experiência atual e tecnologias já conhecidas;
   - **Afinidades técnicas:** 13 controles graduais, com perguntas carregadas do JSON;
   - **Objetivos de carreira:** objetivo principal, tipo de contribuição e horas semanais de estudo;
   - **Resultado:** Top 3, ranking das dez carreiras, gráfico de barras, explicações, ajustes e exportação de diagnóstico em JSON.
2. `entrevista_etapa2.py` — adiciona validações de entrada, valores iniciais e a estrutura do relatório exportado, sem depender da interface web.
3. `tests/test_entrevista_etapa2.py` — adiciona **10 testes** para etapas, limites das respostas, integração com o motor, relatório serializável e verificações estruturais da interface.
4. `README.md` — documenta como iniciar e utilizar a nova entrevista, separando a Etapa 2 do sistema anterior.

## Decisões técnicas

- As afinidades e respostas ficam em `st.session_state` para que o usuário possa voltar e editar sem perdê-las.
- As 13 perguntas são criadas a partir do **JSON**, evitando fixar a lista de dimensões no código da interface.
- A compatibilidade utiliza o motor implementado no Dia 2; ele aplica pesos, ajustes e penalidades e calcula Top 3. Os percentuais não são probabilidades e não precisam somar 100%.
- A interface original da Etapa 1 foi substituída em `app.py`, mas seus módulos `motor.py`, `conhecimento.py` e testes foram preservados no projeto e no histórico do Git.
- Experiência e objetivos são guardados e exibidos no relatório; **ainda não mudam a pontuação**. Eles servirão à análise de gaps e ao roadmap, previstos para o Dia 4. Isso impede que a interface sugira influência que o algoritmo ainda não possui.

## Como testar

No terminal da raiz do projeto:

```powershell
python -m unittest discover -s tests -v
python -m streamlit run app.py
```

No navegador, executar o seguinte roteiro manual:

1. Preencher o perfil e avançar.
2. Alterar pelo menos duas notas de afinidade e voltar ao perfil; retornar e conferir que as notas foram preservadas.
3. Escolher o objetivo e clicar em **Calcular minha compatibilidade**.
4. Conferir Top 3, gráfico, justificativas e exportação do JSON.
5. Editar as afinidades, gerar novo diagnóstico e observar a mudança no ranking.

## Limitações e próximas etapas

- O teste estrutural da interface não substitui a execução real no navegador. Uma verificação visual/manual deve ser feita antes do commit.
- As avaliações das competências para atingir o nível Júnior (**skill gaps**) e o roadmap de estudos ainda serão implementados.
- O resultado expressa afinidade definida por regras acadêmicas, não aptidão validada cientificamente.
