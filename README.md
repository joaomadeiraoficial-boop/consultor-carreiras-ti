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
- Permite revisar respostas e baixar o diagnóstico em **JSON**.

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

Ao concluir, o consultor apresenta o ranking, o gráfico comparativo e as regras que ajudam a explicar o resultado. O diagnóstico pode ser exportado em JSON.

**Nota de transparência:** nesta versão, **as 13 afinidades determinam o ranking**. Experiência e objetivos são registrados no relatório, mas **ainda não alteram a pontuação**. Eles serão utilizados no módulo posterior de análise de competências e plano de estudos.

## O que acontece nos bastidores?

O funcionamento da **Etapa 2** segue uma sequência simples de explicar, embora mais cuidadosa de programar:

1. O usuário atribui notas às afinidades técnicas.
2. `base_conhecimento.py` lê e valida o arquivo `regras_carreiras.json`.
3. `motor_ponderado.py` aplica os pesos de cada carreira, calcula a pontuação e considera bônus ou penalidades.
4. O sistema ordena os resultados, resolve empates pelos critérios definidos e apresenta as três carreiras mais compatíveis.
5. `app.py` exibe os resultados; `entrevista_etapa2.py` valida as respostas e organiza o relatório exportável.

As regras ficam fora do código do motor, de modo que a base de conhecimento possa ser estudada e ajustada sem misturar conceitos de carreira à lógica da aplicação. **Há método por trás do resultado, não magia por trás da tela.**

A **Etapa 1**, preservada em `motor.py`, utiliza fatos e regras da Experta. Ela permite observar a passagem de uma recomendação por regras tradicionais para uma abordagem com graus de afinidade e pontuação ponderada.

## Organização do projeto

```text
consultor_carreiras_ti/
├── app.py                       # Interface Streamlit em três etapas
├── entrevista_etapa2.py         # Validação e relatório da entrevista
├── motor_ponderado.py           # Pesos, bônus, penalidades e Top 3
├── regras_carreiras.json        # Conhecimento externo das dez trilhas
├── base_conhecimento.py         # Leitura e validação do JSON
├── simular_perfil_ponderado.py  # Demonstração do novo motor
├── motor.py                     # Motor original: 46 regras Experta
├── conhecimento.py              # Dados de apoio da Etapa 1
├── personas.json                # Perfis de validação originais
├── validar_personas.py          # Testes das personas da Etapa 1
├── docs/                        # Matriz e diário técnico das etapas
├── tests/                       # Testes automatizados
├── requirements.txt             # Bibliotecas necessárias
├── INICIAR_WINDOWS.bat          # Inicialização assistida no Windows
└── README.md                    # Este pequeno mapa
```

## Testes: porque confiar é bom, verificar é melhor

Para executar a demonstração do motor ponderado e os testes automatizados:

```powershell
python simular_perfil_ponderado.py
python -m unittest discover -s tests -v
```

Os testes cobrem carregamento da base, validação de entradas, regras ponderadas, diferenciação de carreiras, perfis ambíguos e componentes de validação da entrevista. A aplicação também deve ser conferida manualmente no navegador: avançar pelas três etapas, voltar, modificar respostas e verificar o diagnóstico.

Os documentos na pasta [`docs/`](docs/) registram as decisões e os testes realizados em cada incremento. O código, por sua vez, oferece ao leitor a oportunidade de não depender apenas da palavra do autor.

## Diário de desenvolvimento

| Data | Evolução | Registro |
|---|---|---|
| **22/10/2026** | Sistema original com regras Experta e entrevista objetiva | `motor.py` e [`docs/resumo_matriz.md`](docs/resumo_matriz.md) |
| **24/10/2026** | Separação do conhecimento em JSON | [`docs/etapa2_dia1.md`](docs/etapa2_dia1.md) |
| **25/10/2026 — Dia 2** | Inferência ponderada, bônus, penalidades e Top 3 | [`docs/etapa2_dia2.md`](docs/etapa2_dia2.md) |
| **25/10/2026 — Dia 3** | Entrevista em três etapas integrada ao Streamlit | [`docs/etapa2_dia3.md`](docs/etapa2_dia3.md) |

O histórico de commits registra a evolução do projeto. Cada mudança funcional deve ser testada antes de ser publicada — uma disciplina que se aprende melhor praticando do que prometendo.

## Próximos capítulos

A Etapa 2 ainda prevê:

- **Análise de lacunas (*skill gaps*):** comparar os conhecimentos informados com competências esperadas de um profissional Júnior.
- **Roadmap personalizado:** organizar estudos, tecnologias, certificações pertinentes e projetos para portfólio.
- **Validação final:** ampliar os testes de robustez e revisar a experiência completa.

Essas funcionalidades **ainda não estão prontas nesta versão**. O README será atualizado conforme forem implementadas e testadas.

## Considerações finais

Este é um projeto **acadêmico e exploratório**, construído sobre regras definidas manualmente. Não utiliza aprendizado de máquina para descobrir aptidões, não substitui orientação profissional e não oferece qualquer garantia sobre o mercado de trabalho.

Ferramentas de inteligência artificial foram utilizadas como apoio ao desenvolvimento, especialmente na elaboração da interface e na organização de textos. O funcionamento do sistema deve ser avaliado por suas regras, seus testes e pelos resultados que é capaz de reproduzir.

Se o programa ajudar alguém a formular uma pergunta melhor sobre a própria carreira, já terá cumprido uma parte importante de sua missão. Às vezes, escolher um caminho começa simplesmente por compreender as opções.
