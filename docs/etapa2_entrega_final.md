# Etapa 2 — Fechamento e validação final

**UNIPAC Barbacena — Inteligência Artificial**  
**Prazo informado para entrega:** 29/10/2026, 19h (horário de Brasília).  
**Mensagem proposta do commit:** `docs: finaliza README, verificacao integrada e guia de entrega`

## 1. Objetivo

Concluir a segunda etapa do Consultor de Carreiras em TI. A proposta é transformar as respostas graduais do usuário em uma comparação ponderada de dez carreiras, apresentar um Top 3 explicável e orientar o aprendizado para uma referência inicial de nível Júnior.

Este commit final atualiza a documentação, acrescenta testes de integração e oferece o script `verificar_entrega.py`. **Não modifica os pesos nem as regras de decisão**, preservando a rastreabilidade das etapas anteriores.

## 2. Relação dos requisitos com a implementação

| Requisito da Etapa 2 | Arquivos responsáveis | Como verificar |
|---|---|---|
| Dez trilhas e pesos em base externa | `regras_carreiras.json`, `base_conhecimento.py` | Testes de carregamento; `verificar_entrega.py` |
| Escalas graduais de 1 a 5 | `app.py`, `entrevista_etapa2.py` | Navegar na etapa de afinidades e alterar notas |
| Pontuação ponderada e penalidades | `motor_ponderado.py` | `simular_perfil_ponderado.py`; testes de motor |
| Ranking Top 3 e porcentagens | `motor_ponderado.py`, `app.py` | Diagnóstico e testes de ordenação |
| Skill gaps para referência Júnior | `modulo_roadmap.py`, `roteiros_carreiras.json` | Autoavaliação no resultado; testes de roadmap |
| Tecnologias, certificações e portfólio | `roteiros_carreiras.json`, `modulo_roadmap.py` | Gerar plano na carreira recomendada |
| Interface de três etapas e gráficos | `app.py`, `painel_resultados.py` | Teste visual do fluxo completo |
| Perfis ambíguos, empates e limites | `simular_casos_limite.py`, `tests/test_robustez_etapa2.py` | Simulação e suíte automatizada |
| Relatório JSON exportável | `entrevista_etapa2.py`, `app.py` | Baixar diagnóstico após gerar roadmap |
| Reprodutibilidade/documentação | `README.md`, `docs/`, `verificar_entrega.py` | Comandos abaixo e histórico Git |

## 3. Desenho simplificado da arquitetura

`regras_carreiras.json` → `base_conhecimento.py` → `motor_ponderado.py` → `painel_resultados.py` → `app.py`.

`roteiros_carreiras.json` + autoavaliação → `modulo_roadmap.py` → `app.py` e `entrevista_etapa2.py` (exportação).

O motor de regras original da Etapa 1 (`motor.py`, Experta) foi mantido como referência histórica. A Etapa 2 utiliza motor próprio de soma ponderada, **alternativa expressamente prevista no enunciado**.

## 4. Critério de pontuação e limitações

A nota de cada afinidade é normalizada a partir da escala de 1 a 5, multiplicada pelo peso correspondente da carreira e combinada às demais dimensões. Regras declaradas no JSON podem acrescentar bônus ou impor penalidades. Os índices são limitados a 0–100% e ordenados do maior para o menor. Os valores **não precisam somar 100%**: são índices heurísticos, não probabilidades de contratação ou aptidão.

A experiência e o objetivo declarados não interferem no ranking de afinidades. A orientação de estudos utiliza a autoavaliação das competências, a disponibilidade semanal e o objetivo informado. O nível Júnior é uma **referência didática** baseada no JSON, não certificação ou norma profissional. Estimativas de tempo não garantem empregabilidade.

## 5. Como reproduzir os testes

Na raiz do projeto, em um ambiente com as dependências instaladas:

```powershell
python verificar_entrega.py
python simular_perfil_ponderado.py
python simular_casos_limite.py
python -m unittest discover -s tests -v
python -m streamlit run app.py
```

As verificações automatizadas exercitam os módulos Python. **Elas não substituem o teste manual da interface no navegador**, que deve incluir navegação entre telas, gráfico, autoavaliação, roadmap e download do diagnóstico.

## 6. Registro das evidências

O documento [`guia_evidencias.md`](guia_evidencias.md) indica quais imagens reais do navegador e do terminal devem ser registradas. Não são fornecidas capturas fabricadas: as evidências precisam refletir a execução no computador do aluno.

## 7. Git e entrega

Depois de testar, registre apenas as alterações reais deste incremento, publique na branch `main` e confirme o histórico remoto. Antes de enviar a atividade, abra o link do GitHub em janela anônima para garantir que o repositório é acessível sem autenticação. Verifique se o professor solicitou **link e imagens anexadas no ambiente da disciplina**; imagens presentes só no repositório podem não substituir anexos exigidos pelo formulário.

> A evolução do projeto é documentada pelos commits e pelos arquivos `docs/etapa2_dia*.md`. O objetivo é tornar as decisões rastreáveis, não inflar artificialmente a contagem de commits.
