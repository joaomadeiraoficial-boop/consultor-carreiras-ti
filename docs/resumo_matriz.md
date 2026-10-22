# Fase 1 — Engenharia de conhecimento

## Matriz de decisão

A tabela completa, linha por linha, está no arquivo `matriz_decisao.csv` (46 regras). Cada linha contém os fatos **SE**, os pontos adicionados **ENTÃO**, e a explicação mostrada ao usuário.

| Trilha | Preferência diária | Entrega esperada | Ferramentas afins | Estilo de trabalho |
|---|---|---|---|---|
| Desenvolvimento Back-end | Programar regras de negócio, APIs e serviços | Funcionalidades e serviços funcionando | Python, SQL / bancos de dados | Escrever e depurar código |
| Desenvolvimento Front-end & UI/UX | Criar interfaces e melhorar a navegação | Uma experiência bonita e fácil de usar | JavaScript / TypeScript, Figma / CSS | Prototipar e ajustar elementos visuais |
| Ciência de Dados e Machine Learning | Treinar modelos e interpretar padrões | Descobertas e previsões extraídas de dados | Python, SQL / bancos de dados | Explorar dados e testar hipóteses |
| Engenharia de Dados | Organizar e transportar dados entre sistemas | Dados organizados e disponíveis para análise | SQL / bancos de dados, Python | Estruturar fluxos e integrações |
| Cibersegurança (Security / Pentesting) | Investigar falhas e proteger sistemas | Menos riscos e ataques a sistemas | Linux / redes, Python | Investigar riscos, causas e vulnerabilidades |
| DevOps & SRE | Automatizar deploys e monitorar serviços | Publicações rápidas e sistemas confiáveis | Linux / redes, AWS / Azure / GCP | Automatizar tarefas repetitivas |
| Computação em Nuvem (Cloud Architecture) | Planejar servidores e infraestrutura na nuvem | Infraestrutura que aguenta crescer | AWS / Azure / GCP, Linux / redes | Planejar e manter infraestrutura |
| Desenvolvimento Mobile | Criar aplicativos para celular | Aplicativos que as pessoas usam no celular | Flutter / Kotlin / Swift, JavaScript / TypeScript | Escrever e depurar código |
| Engenharia de Qualidade e Testes (QA) | Procurar defeitos e automatizar testes | Software testado e sem defeitos críticos | Selenium / Playwright / Pytest, Python | Validar requisitos e cenários de testes |
| Gestão de Produtos (Product Management) | Definir prioridades e coordenar necessidades | Valor para usuários e objetivos de negócio | Jira / Trello / documentação, Figma / CSS | Conversar com equipes e definir prioridades |

## Pesos e resolução de conflitos

- Regra de atividade: **+3** pontos; vale para todas as dez trilhas, garantindo pelo menos uma hipótese.
- Atividade **e** entrega compatíveis: **+8** pontos.
- Atividade **e** ferramenta compatíveis: **+4** pontos.
- Entrega **e** estilo compatíveis: **+5** pontos.
- Regras adicionais **R41 a R46**: de +2 a +3 pontos para sinais específicos e desempates úteis.

O resultado é uma **pontuação explicável**, e **não** uma probabilidade, um teste psicométrico ou um modelo de machine learning. O mecanismo da Experta dispara as regras que correspondem aos fatos. Em empate, usa número de regras disparadas, atividade, entrega e, por último, ordem estável das trilhas.

### Distinções importantes

- **Ciência de Dados x Engenharia de Dados:** prever e interpretar padrões, com matemática, difere de preparar fluxos, ETL e dados disponíveis.
- **DevOps x Cloud:** automatizar entrega, deploy e confiabilidade operacional difere de desenhar infraestrutura e capacidade de escala.
- **Front-end x Mobile:** interfaces web são distintas de apps Android/iOS.
- **QA x Cibersegurança:** detectar bugs e validar software difere de investigar ataques e vulnerabilidades.
- **Produto x Interface:** definir prioridades e valor de negócio difere de criar a experiência visual.
