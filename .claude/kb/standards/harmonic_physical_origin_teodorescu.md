---
name: harmonic-physical-origin-teodorescu
description: Fundamentação bibliográfica (Teodorescu, Liserre & Rodríguez 2011) para por que a checagem normativa por ordem harmônica precisa rodar em abc e não em dq, e a origem física de harmônicos pares vs ímpares em inversores — não altera nenhum limite aplicado no dashboard
source: Teodorescu, Liserre & Rodríguez (2011) §5.4.3 p.99; §12.3.5.1 p.330-331; Tab.3.6 p.37; Tab.12.1/12.2 p.315
references:
  - "TEODORESCU, Remus; LISERRE, Marco; RODRÍGUEZ, Pedro. Grid Converters for Photovoltaic and Wind Power Systems. Chichester: John Wiley & Sons, Ltd, 2011. ISBN 978-0-470-05751-3."
metadata:
  type: reference
---

# Origem física dos harmônicos e por que dq não separa 5ª de 7ª

Complementa [harmonic_norm_application.md](harmonic_norm_application.md) — aqui fica
a fundamentação bibliográfica de duas afirmações que já eram usadas nesse arquivo
sem citação. **A regra aplicada no dashboard não muda**: continua exclusivamente
IEEE 519-2014/IEEE 1547-2018 (ver `harmonic_norm_application.md`). Este arquivo é
só o "porquê" por trás da arquitetura da checagem, não um limite novo.

## Colisão 5ª/7ª no mesmo bin dq (§12.3.5.1, p.330-331)

Num referencial síncrono girando a `ω` (velocidade da fundamental), a transformada
de Park desloca cada harmônico de ordem `n` por `∓ω` conforme a sequência:
sequência negativa desloca por `−(n+1)ω`, sequência positiva por `(n−1)ω`. O livro
mostra o caso da 5ª (negativa) e da 7ª (positiva) caindo exatamente na mesma ordem
6 no referencial dq:

```
5ª (sequência negativa): −5ω − ω = −6ω
7ª (sequência positiva):  7ω − ω =  6ω
```

Citação literal: "they generate six-order harmonics of different sequences" — ou
seja, um único filtro/observador sintonizado em 6ω não consegue distinguir se o
que está vendo é 5ª ou 7ª, porque as duas produzem o mesmo componente de 6ª ordem
no dq (360 Hz na base de 60 Hz deste projeto). O mesmo raciocínio se aplica à
11ª (negativa) e 13ª (positiva), que colidem em 12ª ordem (720 Hz).

Essa é a fundamentação formal da frase já existente em
`harmonic_norm_application.md` ("5ª negativa + 7ª positiva → ambas em
6f₁ = 360 Hz"), que até 2026-08-03 não tinha citação — o raciocínio era nosso,
sem fonte. Agora tem.

## Origem física dos harmônicos pares (§5.4.3, p.99)

O livro discute isso no capítulo de detecção de ilhamento, não no de qualidade de
energia — mas a classificação por origem é geral. Segundo o texto: harmônicos de
alta ordem vêm do chaveamento PWM; harmônicos **pares** vêm de tempo morto
("dead-time") e queda de tensão nos semicondutores; harmônicos **ímpares** vêm do
ripple do barramento CC. A 3ª, 5ª, 7ª, 9ª e 11ª são citadas como "as mais
importantes".

Isso explica, em termos físicos, por que a tabela de harmônicas do dashboard tem
uma coluna de ordens pares (2ª/4ª/6ª) com limites mais apertados (1%/2%/3%) além
da faixa ímpar (4%): pares e ímpares não são a mesma classe de fenômeno, têm
origem distinta no conversor.

## Genealogia do limite de 1% na 2ª harmônica (Tab.3.6, p.37)

A Tabela 3.6 do livro (limites pré-2018, IEEE 1547/IEC 61727 da época) já trazia
a banda ímpar 4,0%/2,0%/1,5%/0,6%/0,3% e a nota explícita: *"even harmonics are
limited to 25% of the odd harmonic limits above"*. `25% × 4% = 1%` — é exatamente
o valor que este projeto usa para a 2ª harmônica. A revisão de 2018 do IEEE 1547
(base atual deste projeto, ver `harmonic_norm_application.md`) manteve a 2ª em 1%
e relaxou só a 4ª/6ª (para 2%/3%); esse relaxamento **não está** no livro de 2011,
que é anterior à revisão — vem da tabela do próprio IEEE 1547-2018/1547.2-2023 já
citada no KB.

## Por que as Tabelas 12.1/12.2 do livro não substituem IEEE 519/1547 aqui

O capítulo 12 do livro (p.315) traz duas tabelas de limite de distorção que à
primeira vista parecem alternativa aos limites já usados no dashboard:

- **Tab.12.1** — limites por faixa de ordem ímpar, "como percentual da
  fundamental" (não de `I_rated`/`IL`).
- **Tab.12.2** — limites individuais por ordem para sistemas eólicos conforme
  IEC (5ª: 5-6%, 7ª: 3-4%, 11ª: 1,5-3%, 13ª: 1-2,5%).

Nenhuma das duas é usada neste projeto: ambas são de 2011 (pré-revisão 2018 do
IEEE 1547, que é a base normativa atual aqui) e usam base de normalização
diferente ("percentual da fundamental", não `I_rated` — ver a tabela de notação
única em `harmonic_norm_application.md`). Misturar essa base reintroduziria
exatamente a ambiguidade de normalização que a reformulação da legenda do
dashboard resolveu em 2026-08-02. Conclusão: o livro fica só como fonte da
fundamentação acima; os limites aplicados continuam exclusivamente
IEEE 519-2014/IEEE 1547-2018.
