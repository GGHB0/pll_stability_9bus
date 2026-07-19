# Exemplos de Uso — pdf-kb-updater

## Modo dirigido (tópico específico)

```
"Busca no Kundur o critério das áreas iguais"
0. Listar PDFs → Kundur__Power_System_Stability_and_Control.pdf
1. TOC → Cap. 3 p.130 "Equal Area Criterion"
2. Extrair p.130-155 → ~/pdfext/secao.txt
3. Checar kb/power-system/ → não existe equal_area_criterion.md
4. Criar kb/power-system/equal_area_criterion.md com frontmatter
5. Adicionar entrada no MEMORY.md
```

```
"Busca no artigo IEEE 7767 o método de estimativa de inércia por CoI"
0. Usuário fornece caminho ou listar bibliografia
1. Sem sumário → extrair p.1-4 para estrutura
2. Buscar seção "Center of Inertia" → extrair páginas relevantes
3. Checar kb/power-system/inertia_estimation.md → existe, verificar linhas
4. Append ou criar inertia_estimation_2.md se >200 linhas
```

## Modo exploratório (sem tópico definido)

```
"Dá uma olhada nesse relatório novo e vê o que vale extrair"
0. Usuário fornece caminho (ou listar bibliografia e confirmar)
1. Delegar ao pdf-extractor: TOC + varredura (skim_*.txt + _index.txt)
2. Ler _index.txt; ler skim_*.txt das seções promissoras
3. Cruzar com KBs existentes e escopo do TCC → propor lista priorizada:
   seção → páginas → por que interessa → KB alvo (novo ou append)
4. AGUARDAR aprovação do usuário
5. Aprovado → extrair na íntegra as seções escolhidas e seguir Passos 3–4
```
