# Etapa 2 — Dia 4: Lacunas profissionais e roadmap individualizado

**Data do desenvolvimento:** 26/10/2026  
**Commit sugerido:** `feat: adiciona skill gaps e roadmap personalizado`

## Propósito

O diagnóstico da Etapa 2 já devolvia um Top 3 fundamentado em afinidades ponderadas.
Nesta entrega, o usuário poderá **autoavaliar seus conhecimentos** na carreira em primeiro lugar e receber um plano de estudos baseado no que falta para atingir uma **referência acadêmica de competências Júnior**.

## Arquitetura

- `roteiros_carreiras.json`: base externa com tópicos, exercícios de fixação, carga horária orientativa por nível de lacuna e sugestões de certificações/formações opcionais, cobrindo as 10 carreiras.
- `modulo_roadmap.py`: valida essa base, cruza competências com os níveis informados e produz passos ordenados por lacuna, com estimativa de semanas a partir das horas disponíveis.
- `app.py`: apresenta formulário de **autoavaliação de 0 a 5** dentro da página de resultados, após o Top 3, exibindo tabela de lacunas, roadmap, projeto GitHub e formações opcionais.
- `entrevista_etapa2.py`: acrescenta o roteiro ao JSON exportado sem quebrar os relatórios anteriores.
- `tests/test_roadmap.py`: cobre perfis iniciantes, usuários que declararam já atingir as metas, empates, prazos de estudo, JSON inválido, cobertura das carreiras e serialização do relatório.

## Regra de cálculo

Para cada competência da carreira recomendada:

`lacuna = max(0, nivel_junior - nivel_autodeclarado)`

Índice de preparo **orientativo**:

`100 × soma(min(nivel_autodeclarado, nivel_junior)) / soma(nivel_junior)`

As competências com maiores lacunas são sugeridas primeiro. Para cada lacuna, as horas estimadas são `lacuna × horas_por_nivel` do JSON. A duração aproximada é o teto das horas necessárias divididas pela disponibilidade semanal informada na entrevista.

O resultado **não comprova** formação, proficiência ou empregabilidade: são notas de autoavaliação e parâmetros didáticos, não avaliações oficiais. As certificações são opcionais, dependem de verificação de disponibilidade e **não são tratadas como requisito obrigatório**.

## Exemplo

Se uma pessoa interessada em Back-end declara nível 3 em lógica, 1 em APIs REST e 2 em SQL, as lacunas serão respectivamente 0, 2 e 1. O roadmap começa por APIs REST e depois SQL. A carga horária informada altera o número de semanas, não a necessidade de aprender os tópicos.

## Como validar

```powershell
python -m unittest discover -s tests -p "test_roadmap.py" -v
python -m unittest discover -s tests -v
python -m streamlit run app.py
```

No navegador: complete as três etapas, obtenha o Top 3, preencha a autoavaliação de competências, gere o roteiro e baixe o JSON. Edite a disponibilidade semanal e confira se a estimativa de duração é atualizada.

## Limites e continuidade

- O nível Júnior adotado é uma referência acadêmica simplificada de três competências essenciais por carreira.
- Não há prova prática que valide as notas autodeclaradas.
- As estimativas de tempo são heurísticas e podem variar muito na prática.
- O projeto original da Etapa 1 e as regras Experta permanecem disponíveis no repositório.
