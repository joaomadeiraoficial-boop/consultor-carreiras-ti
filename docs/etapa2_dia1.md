# Etapa 2 — Dia 1: engenharia do conhecimento

**Objetivo:** introduzir dados carregados de um arquivo JSON externo sem quebrar o consultor da Etapa 1.

## Arquivos deste incremento

- `regras_carreiras.json`: contém 10 trilhas, 13 dimensões avaliadas numa escala de 1 a 5, pesos por trilha e competências de referência para Júnior.
- `base_conhecimento.py`: abre e valida o JSON e fornece os dados descritivos usados pela interface.
- `conhecimento.py`: passa a montar `TRILHAS` a partir do JSON; as opções do questionário anterior continuam iguais.
- `tests/test_base_conhecimento.py`: confere quantidade de trilhas, pesos e compatibilidade dos dados.

## O que ainda NÃO foi implementado

O questionário da Etapa 1 e suas 46 regras da Experta permanecem em funcionamento. A **pontuação ponderada**, percentuais, penalidades de conflito, Top 3, gaps e roadmap **ainda não utilizam o novo JSON**. Isso faz parte dos próximos dias; os pesos do arquivo já estão prontos para serem consumidos pelo novo motor.

## Testar no terminal do VS Code

```powershell
python -m unittest tests.test_base_conhecimento -v
python -m unittest discover -s tests -v
python -m streamlit run app.py
```

Se o comando `tests.test_base_conhecimento` não encontrar o módulo (dependendo da configuração do Python), use:

```powershell
python -m unittest discover -s tests -p "test_base_conhecimento.py" -v
```

## Commit somente após conferir

```powershell
git status
git add regras_carreiras.json base_conhecimento.py conhecimento.py tests/test_base_conhecimento.py docs/etapa2_dia1.md
git commit -m "feat: estrutura base de conhecimento em JSON"
git push origin main
```

**Nota:** pesos são hipóteses didáticas e não representam probabilidade de sucesso profissional. 
