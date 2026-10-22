# Consultor Inteligente de Carreiras em TI

**Trabalho acadêmico — Centro Universitário Presidente Antônio Carlos (UNIPAC), Barbacena.**

Sistema especialista baseado em regras que entrevista o usuário e recomenda uma **entre dez trilhas de carreira em TI**, com pontuação e justificativas transparentes.

## Funcionalidades

- Interface web interativa com **Streamlit** e cinco perguntas objetivas.
- **46 regras explícitas** `@Rule` da biblioteca **Experta**, com inferência por encadeamento para frente.
- Base de conhecimento com dez carreiras, regras cruzadas e critérios explícitos de desempate.
- Diagnóstico detalhado com pontuação, justificativa, ranking e sugestões de estudo.
- Download do diagnóstico em JSON e da matriz em CSV.
- Dez personas de validação e testes automatizados `unittest`.

## Carreiras

1. Desenvolvimento Back-end
2. Desenvolvimento Front-end & UI/UX
3. Ciência de Dados e Machine Learning
4. Engenharia de Dados
5. Cibersegurança (Security / Pentesting)
6. DevOps & SRE
7. Computação em Nuvem (Cloud Architecture)
8. Desenvolvimento Mobile
9. Engenharia de Qualidade e Testes (QA)
10. Gestão de Produtos (Product Management)

## Requisitos

- **Python 3.11** recomendado. O enunciado aceita Python 3.10+, mas a biblioteca Experta foi publicada em 2019 e tem dependências antigas. A aplicação inclui um ajuste para `collections.Mapping` necessário nas versões atuais do Python.
- Internet apenas para **instalar as dependências** pela primeira vez.

## Como instalar e executar no Windows (VS Code ou terminal)

Se o **Python 3.11** já estiver instalado, você pode dar dois cliques em `INICIAR_WINDOWS.bat` para criar o ambiente e iniciar a interface.

Ou abra a pasta do projeto no VS Code. No terminal **PowerShell** execute:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Se o PowerShell bloquear a ativação, abra o **Prompt de Comando (cmd)** e execute:

```bat
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

**Importante:** no Windows, `py -3.11` requer Python 3.11 instalado. Se usar somente `python`, primeiro confira `python --version`.

O aplicativo abre normalmente em `http://localhost:8501` no navegador. Para parar, use **Ctrl + C**.

## Como validar

Execute na raiz do projeto com o ambiente virtual ativado:

```powershell
python validar_personas.py
python -m unittest discover -s tests -v
```

`validar_personas.py` percorre dez perfis hipotéticos, **um por carreira**, compara a recomendação à esperada e informa acertos. Os testes também validam pontuação, entradas inválidas e reinicialização de estado.

## Estrutura do projeto

```text
consultor_carreiras_ti/
├── INICIAR_WINDOWS.bat         # Iniciar com dois cliques no Windows
├── app.py                      # Interface Streamlit
├── conhecimento.py             # Trilhas e opções válidas da entrevista
├── motor.py                    # Classe Fact, KnowledgeEngine e 46 @Rule
├── personas.json               # Dez perfis hipotéticos
├── validar_personas.py         # Validação de personas no terminal
├── docs/
│   ├── matriz_decisao.csv      # Regras, condições, pontuação e motivos
│   └── resumo_matriz.md        # Engenharia de conhecimento e desempate
├── tests/
│   └── test_motor.py           # Testes de unidade
├── requirements.txt            # Dependências Python
├── runtime.txt                 # Versão recomendada para hospedagem
└── README.md
```

## Como funciona a decisão

O usuário informa: **afinidade matemática**, **atividade desejada**, **ferramenta favorita**, **entrega preferida** e **estilo de trabalho**. O sistema transforma as respostas em um objeto `Perfil(Fact)`, declara esse fato no motor Experta e executa `run()`, ativando todas as regras compatíveis.

| Tipo de regra | Pontos | Exemplo |
|---|---:|---|
| Afinidade com a atividade | +3 | Preferir construir APIs → Back-end |
| Atividade + entrega | +8 | Explorar modelos + fazer previsões → Ciência de Dados |
| Atividade + ferramenta | +4 | Construir pipelines + SQL → Engenharia de Dados |
| Entrega + estilo | +5 | Proteger sistemas + investigar falhas → Cibersegurança |
| Diferenciação especializada (6 regras) | +2 ou +3 | Escalabilidade + operação → Cloud |

**Empates:** mais regras disparadas → afinidade diária → entrega pretendida → ordem fixa das trilhas. A pontuação **não é** probabilidade nem garantia de adequação profissional.

### Ciência de Dados x Engenharia de Dados

- **Ciência de Dados:** busca *interpretar dados e prever fenômenos* com estatística e modelos.
- **Engenharia de Dados:** busca *preparar, disponibilizar e transportar dados* via ETL/ELT, integrações e infraestrutura.

### DevOps x Cloud

- **DevOps/SRE:** foco no *processo de entrega*, automação CI/CD e confiabilidade.
- **Cloud:** foco em *arquiteturas e infraestrutura escalável* na nuvem.

## Matriz de decisão e personas

A matriz completa está em [`docs/matriz_decisao.csv`](docs/matriz_decisao.csv). Sua versão explicativa está em [`docs/resumo_matriz.md`](docs/resumo_matriz.md). As dez entradas de teste ficam em [`personas.json`](personas.json).

## Etapas do trabalho

- [x] **Fase 1:** Engenharia de conhecimento e matriz de decisão.
- [x] **Fase 2:** Classe `Perfil(Fact)` e regras `@Rule` com Experta.
- [x] **Fase 3:** Interface de entrevista e apresentação do diagnóstico via Streamlit.
- [x] **Fase 4:** Dez personas e testes de validação automatizáveis.
- [x] **Fase 5:** Documentação pronta para publicar em repositório GitHub.

## Publicar no GitHub

Crie um repositório vazio e, na pasta do projeto, rode (substitua `SEU_USUARIO`):

```bash
git init
git add .
git commit -m "Projeto de sistema especialista para carreiras em TI"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/consultor-carreiras-ti.git
git push -u origin main
```

Nenhuma publicação no GitHub é feita automaticamente por este projeto.

## Nota técnica sobre a Experta

A Experta 1.9.4 depende de `frozendict==1.2`, que referencia `collections.Mapping` (removido do namespace de `collections` no Python 3.10). O início de `motor.py` estabelece um alias de compatibilidade para `collections.abc.Mapping` **antes** da importação de `experta`, evitando ter que editar arquivos em `site-packages`.

**Limitação:** trata-se de um sistema determinístico baseado em conhecimento codificado manualmente, não de um questionário psicológico validado cientificamente.
