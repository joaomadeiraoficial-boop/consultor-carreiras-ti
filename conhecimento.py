"""Vocabulário da entrevista e descrição das dez carreiras."""

from base_conhecimento import carregar_trilhas

TRILHAS = carregar_trilhas()

OPCOES = {'matematica': [('baixa', 'Baixa: evito estatística e cálculos'), ('media', 'Média: consigo lidar com cálculos pontuais'), ('alta', 'Alta: gosto de estatística e matemática')], 'atividade': [('backend', 'Programar regras de negócio, APIs e serviços'), ('frontend', 'Criar interfaces e melhorar a navegação'), ('ciencia', 'Treinar modelos e interpretar padrões'), ('engenharia', 'Organizar e transportar dados entre sistemas'), ('seguranca', 'Investigar falhas e proteger sistemas'), ('devops', 'Automatizar deploys e monitorar serviços'), ('cloud', 'Planejar servidores e infraestrutura na nuvem'), ('mobile', 'Criar aplicativos para celular'), ('qa', 'Procurar defeitos e automatizar testes'), ('produto', 'Definir prioridades e coordenar necessidades')], 'ferramenta': [('python', 'Python'), ('javascript', 'JavaScript / TypeScript'), ('sql', 'SQL / bancos de dados'), ('linux', 'Linux / redes'), ('cloud', 'AWS / Azure / GCP'), ('mobile', 'Flutter / Kotlin / Swift'), ('testes', 'Selenium / Playwright / Pytest'), ('design', 'Figma / CSS'), ('gestao', 'Jira / Trello / documentação'), ('nenhuma', 'Nenhuma / sou iniciante')], 'entrega': [('funcionalidades', 'Funcionalidades e serviços funcionando'), ('experiencia', 'Uma experiência bonita e fácil de usar'), ('previsoes', 'Descobertas e previsões extraídas de dados'), ('dados', 'Dados organizados e disponíveis para análise'), ('protecao', 'Menos riscos e ataques a sistemas'), ('entrega_continua', 'Publicações rápidas e sistemas confiáveis'), ('escala', 'Infraestrutura que aguenta crescer'), ('aplicativos', 'Aplicativos que as pessoas usam no celular'), ('qualidade', 'Software testado e sem defeitos críticos'), ('negocio', 'Valor para usuários e objetivos de negócio')], 'estilo': [('programar', 'Escrever e depurar código'), ('criar', 'Prototipar e ajustar elementos visuais'), ('analisar', 'Explorar dados e testar hipóteses'), ('estruturar', 'Estruturar fluxos e integrações'), ('investigar', 'Investigar riscos, causas e vulnerabilidades'), ('automatizar', 'Automatizar tarefas repetitivas'), ('operar', 'Planejar e manter infraestrutura'), ('testar', 'Validar requisitos e cenários de testes'), ('coordenar', 'Conversar com equipes e definir prioridades')]}

VALIDOS = {campo: {codigo for codigo, _ in alternativas} for campo, alternativas in OPCOES.items()}

ROTULOS = {campo: dict(alternativas) for campo, alternativas in OPCOES.items()}

ORDEM = tuple(TRILHAS)
