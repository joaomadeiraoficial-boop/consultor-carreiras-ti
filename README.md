# Consultor Avançado de Carreiras em TI

**UNIPAC Barbacena — Ciência da Computação — Inteligência Artificial**

Sistema especialista em Python com interface Streamlit para mapear afinidades e apresentar as carreiras de tecnologia mais compatíveis com o perfil de cada usuário. Este repositório reúne a **Etapa 1** (motor com 46 regras Experta) e sua evolução progressiva para a **Etapa 2** (inferência ponderada e tratamento de incerteza).

> **Importante:** os percentuais são indicadores heurísticos de afinidade, **não** probabilidades de emprego, sucesso ou aptidão profissional. Os percentuais das carreiras não precisam somar 100%.

## Funcionalidades disponíveis nesta versão (Dia 3 — 25/10/2026)

- **10 trilhas de carreira**: Back-end, Front-end/UX, Ciência de Dados, Engenharia de Dados, Cibersegurança, DevOps/SRE, Cloud, Mobile, QA e Gestão de Produtos.
- Entrevista dividida em **três etapas**: perfil pessoal, 13 afinidades técnicas (de **1 a 5**) e objetivos profissionais.
- Motor independente em `motor_ponderado.py`, que lê a base externa `regras_carreiras.json`, calcula pesos, bônus e penalidades e ordena as **três carreiras com maior aderência**.
- Gráfico comparativo de dez carreiras, motivos da recomendação e relatório exportável em JSON.
- Navegação com possibilidade de voltar às etapas anteriores e ajustar as respostas.
- Código anterior da Etapa 1 preservado em `motor.py` e `conhecimento.py`, com 46 regras `@Rule` da Experta e testes anteriores.

**Em desenvolvimento nos próximos commits:** análise de lacunas para nível Júnior, roadmap de estudos/certificações/portfólio e testes finais da experiência.

## Instalação e execução no Windows

Recomendado: **Python 3.11** (devido às dependências antigas da Experta). O Streamlit e o motor ponderado podem funcionar em outras versões, mas a compatibilidade deve ser testada no computador de execução.

Abra a pasta do projeto no VS Code. No terminal PowerShell:

```powershell
python --version
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

O terminal mostrará um endereço como `http://localhost:8501`. Abra-o no navegador e siga os três passos do questionário. Para encerrar, pressione **Ctrl + C** no terminal.

Também é possível iniciar com `INICIAR_WINDOWS.bat` **se o Python 3.11 estiver instalado** (ele prepara um ambiente virtual).

### Como testar o motor sem navegador

```powershell
python simular_perfil_ponderado.py
python -m unittest discover -s tests -v
```

O primeiro comando demonstra o **Top 3** com um perfil sintético de Ciência de Dados. O segundo verifica o motor antigo, o JSON, a inferência ponderada e as validações da nova entrevista. O teste estrutural da interface não substitui a verificação manual no navegador.

### Como fazer a entrevista no navegador

1. **Perfil pessoal:** indique sua experiência e tecnologias conhecidas (opcionais).
2. **Afinidades:** atribua de 1 a 5 para cada uma das 13 atividades e avance. Pode voltar e ajustar notas.
3. **Objetivos:** informe seu objetivo, tipo de contribuição preferido e horas semanais disponíveis.
4. **Resultado:** veja o Top 3, o gráfico de barras, as explicações e a opção de baixar um diagnóstico JSON.

**Nota sobre a pontuação:** nesta versão, as 13 afinidades definem o ranking. A experiência e os objetivos integram o relatório, mas ainda não influenciam os cálculos; serão aproveitados no roadmap em desenvolvimento.

## Estrutura principal

```text
consultor_carreiras_ti/
├── app.py                       # Streamlit em três etapas; resultado do motor ponderado
├── entrevista_etapa2.py         # Validação e relatório exportável
├── motor_ponderado.py           # Cálculo Top 3 com pesos, bônus e penalidades
├── regras_carreiras.json        # Base externa: dimensões, 10 trilhas, pesos e regras
├── base_conhecimento.py         # Leitura e validação da base JSON
├── simular_perfil_ponderado.py  # Demonstração sem navegador
├── motor.py                     # Motor de 46 regras Experta da Etapa 1 (preservado)
├── conhecimento.py              # Suporte compatível com a Etapa 1
├── personas.json                # Perfis de validação da Etapa 1
├── validar_personas.py          # Validação da Etapa 1
├── docs/
│   ├── matriz_decisao.csv       # Matriz original de regras
│   ├── resumo_matriz.md
│   ├── etapa2_dia1.md            # Modelagem JSON
│   ├── etapa2_dia2.md            # Inferência ponderada
│   └── etapa2_dia3.md            # Interface em três etapas
├── tests/
│   ├── test_motor.py
│   ├── test_base_conhecimento.py
│   ├── test_motor_ponderado.py
│   └── test_entrevista_etapa2.py
├── requirements.txt
├── INICIAR_WINDOWS.bat
└── README.md
```

## Evolução e versionamento

| Dia | Alteração | Referência |
|---|---|---|
| 22/10 | Versão original do Sistema Especialista | `motor.py`, `docs/matriz_decisao.csv` |
| 24/10 | Base externa com pesos e dez carreiras | [`docs/etapa2_dia1.md`](docs/etapa2_dia1.md) |
| 25/10 (Dia 2) | Motor ponderado, penalidades e Top 3 | [`docs/etapa2_dia2.md`](docs/etapa2_dia2.md) |
| 25/10 (Dia 3) | Entrevista graduada e interface wizard | [`docs/etapa2_dia3.md`](docs/etapa2_dia3.md) |

O histórico do Git mostra quais arquivos mudaram em cada evolução. A documentação de cada dia descreve os testes e decisões técnicas. Não é necessário criar outro repositório para a Etapa 2.

## Arquitetura e transparência

Na Etapa 2, os pesos das carreiras, perguntas e condições de ajuste são carregados de **`regras_carreiras.json`**, separados do código Python. O motor calcula a média ponderada das respostas normalizadas e aplica bônus/penalidades às carreiras; o resultado é ordenado por compatibilidade. Em empate, usa menor penalidade e ordem de definição no JSON.

O método é determinístico e usa conhecimento configurado manualmente, não aprendizado de máquina nem diagnóstico vocacional cientificamente validado. O repositório contém também a primeira implementação com Experta, útil para comparar abordagens.

## Autoria e uso acadêmico

Projeto acadêmico da UNIPAC Barbacena. A documentação e os arquivos de teste permitem reproduzir as funcionalidades e compreender as decisões do sistema. O sistema não exige cadastro, nome ou e-mail para avaliar um perfil; o arquivo de diagnóstico é gerado sob solicitação do usuário.
