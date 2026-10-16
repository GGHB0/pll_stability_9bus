# Roteiro de fala (notas do apresentador)

Continuação de `SKILL.md`. Cada slide tem nas notas o roteiro dividido entre
os dois autores, com o marcador no início de cada trecho:

```text
[Bruno] Começamos pelo cenário global. ...

[Victor] Essa mudança não é só de quantidade. ...
```

## Regras

- **Tempo**: defesa de **30 min** (Victor, 2026-10-16). Só o corpo conta
  (slides antes do DIVIDER "Apêndice"); o apêndice é para as perguntas.
  `tempo_fala.py` estima a 130 palavras/min e sai com código 1 acima do
  limite. Mirar ~27 min no roteiro: a fala real escorrega e a banca interrompe.
- **Divisão**: entre 40/60 e 60/40 no total; o script avisa fora disso.
  Alternar dentro do slide é o padrão do deck; não concentrar um orador
  em vários slides seguidos sem combinar.
- **Marcador obrigatório** em todo trecho: texto sem `[Bruno]`/`[Victor]`
  sai como "?" no script.
- **Redação falada**: frases curtas, número por extenso do jeito que se
  fala ("cento e quarenta e cinco radianos por segundo" pode ficar
  "145,5 rad/s", mas sem fórmula com símbolo que não se lê em voz alta).
  O roteiro explica o slide; não repete o texto da tela palavra por palavra.
- Mesmas regras do TCC: sem travessão, sem nome de código ("sintonia
  inadequada", não "BAD_PLL"), sem RoCoF, sem "reaquisitar".
- Toda mudança de número no slide → mesma mudança nas notas
  (`find_text.py --notas`).

## Editar notas no gen_*.py

```python
tf = slide.notes_slide.notes_text_frame      # cria se não houver
tf.text = "[Bruno] ...\n\n[Victor] ..."      # parágrafos por \n
```

Notas não têm formatação que valha preservar: substituir o texto inteiro é
seguro aqui (ao contrário dos slides, ver `referencia/armadilhas.md`).
Depois: `tempo_fala.py` e reportar ao Victor o tempo antes × depois.

## Ensaio

Para treinar, um PDF com slide + notas sai pelo PowerPoint (Imprimir →
Anotações). Não gerar por script sem o Victor pedir.
