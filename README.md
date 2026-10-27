# Consultor Inteligente de Carreiras em TI 🧭

*Um sistema especialista para quem deseja escolher uma direção sem precisar consultar uma bola de cristal.*

**Centro Universitário Presidente Antônio Carlos — UNIPAC Barbacena**  
**Curso:** Ciência da Computação · **Disciplina:** Inteligência Artificial

O universo da tecnologia tem uma virtude e um pequeno defeito: oferece caminhos em abundância. Entre algoritmos, interfaces, servidores e dados, não é raro que alguém descubra dez áreas interessantes e, ao final, continue sem saber por qual começar.

Este projeto nasceu para tornar essa escolha um pouco menos nebulosa. Por meio de uma entrevista e de um motor de inferência baseado em regras, o sistema compara as afinidades do usuário com **dez trilhas de carreira em TI**, organiza os resultados e explica os motivos da recomendação. Não pretende decidir o futuro de ninguém — até porque seria uma responsabilidade excessiva para um programa em Python.

## O que o consultor sabe fazer

Na versão atual, o sistema:

- Conduz uma entrevista em **três etapas**: perfil pessoal, afinidades técnicas e objetivos de carreira.
- Avalia **13 afinidades** em uma escala de **1 a 5**, sem exigir do usuário uma resposta absoluta para tudo.
- Consulta uma base de conhecimento externa, `regras_carreiras.json`, com critérios, pesos e regras de ajuste.
- Calcula compatibilidades por **pontuação ponderada**, com bônus e penalidades para situações específicas.
- Apresenta um **Top 3 de carreiras**, além do ranking completo das dez opções.
- Exibe gráficos e justificativas para que o resultado não pareça um palpite revestido de porcentagens.
- Identifica **lacunas de competências para uma referência inicial de nível Júnior** com autoavaliação de 0 a 5.
- Gera **roadmap personalizado** com estudos, projetos de portfólio, certificações opcionais e estimativas didáticas de tempo.
- Permite revisar respostas e baixar o diagnóstico, incluindo o roadmap, em **JSON**.

O motor original da primeira etapa, com **46 regras `@Rule` da biblioteca Experta**, permanece no repositório para consulta e comparação.

> **Uma ressalva necessária:** os percentuais representam índices *heurísticos de afinidade*. Não são probabilidades de emprego, talento ou sucesso, e **não precisam somar 100%**. Uma carreira promissora ainda exige estudo — infelizmente, essa etapa não pôde ser automatizada.

## As dez trilhas do mapa

| Trilha | Território principal |
|---|---|
| **Desenvolvimento Back-end** | Lógica de servidores, APIs e bancos de dados |
| **Desenvolvimento Front-end & UI/UX** | Interfaces, interação e experiência do usuário |
| **Ciência de Dados e Machine Learning** | Estatística, modelos e previsões |
| **Engenharia de Dados** | Pipelines, integração e infraestrutura de dados |
| **Cibersegurança** | Proteção de sistemas e análise de vulnerabilidades |
| **DevOps & SRE** | Automação, entrega contínua e confiabilidade |
| **Computação em Nuvem** | Arquitetura e serviços escaláveis |
| **Desenvolvimento Mobile** | Aplicativos para dispositivos móveis |
| **Engenharia de Qualidade e Testes (QA)** | Testes, prevenção de falhas e qualidade |
| **Gestão de Produtos** | Negócio, prioridades e evolução de produtos |

## Colocando a bússola para funcionar

**Requisitos:** Python instalado (preferencialmente **3.11**, em razão das dependências antigas da Experta) e acesso à internet para instalar as bibliotecas. **Não é necessário XAMPP**: o próprio Streamlit inicia o servidor local.

No VS Code, abra a pasta do projeto, acesse o terminal e execute:

```powershell
python --version
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Abra o endereço indicado pelo terminal, normalmente **http://localhost:8501**. Para encerrar a aplicação, pressione **Ctrl + C** no terminal.

No Windows, quem tiver Python 3.11 instalado também pode executar `INICIAR_WINDOWS.bat`, que prepara um ambiente virtual para o projeto.

### A entrevista, em três capítulos

1. **Perfil pessoal:** informe sua experiência e as tecnologias com as quais já teve contato.
2. **Afinidades técnicas:** dê notas de 1 a 5 às 13 atividades propostas; é possível voltar e alterar as respostas.
3. **Objetivos de carreira:** indique seu propósito profissional, o tipo de contribuição que prefere e suas horas disponíveis para estudo.

Ao concluir, o consultor apresenta o ranking, gráficos comparativos e os fatores que justificam o resultado. Em seguida, a pessoa autoavalia o que já sabe sobre a trilha recomendada e recebe uma sequência de estudos com exemplos de prática, portfólio e formações opcionais. O diagnóstico pode ser exportado em JSON.

**Nota de transparência:** as **13 afinidades determinam o ranking**. Experiência e objetivos não modificam essa pontuação. Já a autoavaliação de conhecimentos, as horas semanais e o objetivo declarado orientam o roadmap. Interesse por uma área e domínio técnico são aspectos diferentes — convém não confundi-los.

## O que acontece nos bastidores?

O funcionamento da **Etapa 2** segue uma sequência simples de explicar, embora mais cuidadosa de programar:

1. O usuário atribui notas às afinidades técnicas.
2. `base_conhecimento.py` lê e valida o arquivo `regras_carreiras.json`.
3. `motor_ponderado.py` aplica os pesos de cada carreira, calcula a pontuação e considera bônus ou penalidades.
4. O sistema ordena os resultados, resolve empates pelos critérios definidos e apresenta as três carreiras mais compatíveis.
5. `painel_resultados.py` prepara gráficos, sinaliza empates e explica a composição da pontuação.
6. `modulo_roadmap.py` compara os conhecimentos declarados às competências Júnior e consulta `roteiros_carreiras.json` para gerar o plano de estudos.
7. `app.py` exibe a entrevista e os resultados; `entrevista_etapa2.py` valida as respostas e organiza o relatório exportável.

As regras ficam fora do código do motor, de modo que a base de conhecimento possa ser estudada e ajustada sem misturar conceitos de carreira à lógica da aplicação. **Há método por trás do resultado, não magia por trás da tela.**

A **Etapa 1**, preservada em `motor.py`, utiliza fatos e regras da Experta. Ela permite observar a passagem de uma recomendação por regras tradicionais para uma abordagem com graus de afinidade e pontuação ponderada.

## Organização do projeto

```text
consultor_carreiras_ti/
├── app.py                       # Interface Streamlit com entrevista e resultados
├── entrevista_etapa2.py         # Validação das respostas e relatório JSON
├── motor_ponderado.py           # Pesos, bônus, penalidades e Top 3
├── base_conhecimento.py         # Carregamento da base externa
├── regras_carreiras.json        # Dez carreiras, dimensões e regras ponderadas
├── modulo_roadmap.py            # Skill gaps, prioridades e plano de estudos
├── roteiros_carreiras.json      # Conteúdos e projetos para as dez trilhas
├── painel_resultados.py         # Gráficos e interpretação dos resultados
├── verificar_entrega.py         # Verificação integrada da Etapa 2
├── simular_perfil_ponderado.py  # Demonstração do diagnóstico no terminal
├── simular_casos_limite.py      # Perfis ambíguos e situações de fronteira
├── motor.py                     # Motor original: 46 regras da Experta
├── conhecimento.py              # Apoio à Etapa 1
├── docs/                        # Matriz, decisões técnicas e guia de evidências
├── tests/                       # Testes automatizados
├── requirements.txt             # Dependências
├── INICIAR_WINDOWS.bat          # Inicialização assistida no Windows
└── README.md                    # Este pequeno mapa
```

## Testes: porque confiar é bom, verificar é melhor

No terminal da pasta do projeto:

```powershell
python verificar_entrega.py
python simular_perfil_ponderado.py
python simular_casos_limite.py
python -m unittest discover -s tests -v
```

O primeiro comando examina a integração das dez carreiras, a entrevista, o motor, os dados para gráficos, os roadmaps e a exportação JSON. O último executa os testes automatizados de todos os módulos, incluindo o motor da primeira etapa com Experta. Veja [`docs/etapa2_entrega_final.md`](docs/etapa2_entrega_final.md) para a relação entre critérios do enunciado e arquivos.

**A interface precisa de uma conferência no navegador:** complete as três etapas, volte para alterar uma resposta, veja o Top 3, gere o roadmap e baixe o relatório. Nenhum teste de terminal deve ser confundido com essa inspeção visual.

Para facilitar a correção, use o [`guia de capturas de tela`](docs/guia_evidencias.md). O professor pode examinar o trabalho sem precisar iniciar a aplicação — um gesto de civilidade em meio a dezenas de repositórios.

## Diário de desenvolvimento

| Data | Evolução | Registro |
|---|---|---|
| **22/10/2026** | Sistema original com 46 regras Experta | [`docs/resumo_matriz.md`](docs/resumo_matriz.md) |
| **24/10/2026** | Conhecimento separado em JSON | [`docs/etapa2_dia1.md`](docs/etapa2_dia1.md) |
| **25/10/2026** | Inferência ponderada e ranking Top 3 | [`docs/etapa2_dia2.md`](docs/etapa2_dia2.md) |
| **25/10/2026** | Entrevista gradual em três etapas | [`docs/etapa2_dia3.md`](docs/etapa2_dia3.md) |
| **26/10/2026** | Skill gaps e roadmap personalizado | [`docs/etapa2_dia4.md`](docs/etapa2_dia4.md) |
| **26/10/2026** | Gráficos comparativos e casos-limite | [`docs/etapa2_dia5.md`](docs/etapa2_dia5.md) |
| **27/10/2026** | Revisão, verificações de integração e preparação da entrega | [`docs/etapa2_entrega_final.md`](docs/etapa2_entrega_final.md) |

A tabela descreve a sequência de desenvolvimento planejada e documentada; o histórico real de alterações e horários deve ser conferido na aba de commits do GitHub. Registrar mudanças claras vale mais do que produzir uma quantidade teatral de commits.

## A reta final

Antes de entregar, execute a suíte de testes no seu computador e produza **capturas reais** da interface, do roadmap, dos gráficos e dos resultados dos testes. A documentação não incorpora imagens fictícias. Se a atividade pedir capturas anexadas na plataforma da faculdade, envie-as juntamente com o link público; tê-las só no GitHub pode não bastar.

**Prazo informado:** 29 de outubro de 2026, às 19h (horário de Brasília).

## Considerações finais

Este é um projeto **acadêmico e exploratório**, construído sobre regras definidas manualmente. Não utiliza aprendizado de máquina para descobrir aptidões, não substitui orientação profissional e não oferece qualquer garantia sobre o mercado de trabalho.

Ferramentas de inteligência artificial foram utilizadas como apoio ao desenvolvimento, especialmente na elaboração da interface e na organização de textos. O funcionamento do sistema deve ser avaliado por suas regras, seus testes e pelos resultados que é capaz de reproduzir.

Se o programa ajudar alguém a formular uma pergunta melhor sobre a própria carreira, já terá cumprido uma parte importante de sua missão. Às vezes, escolher um caminho começa simplesmente por compreender as opções.
