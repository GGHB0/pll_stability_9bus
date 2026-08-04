---
name: harmonic-physical-origin-teodorescu
description: Fundamentação bibliográfica (Teodorescu, Liserre & Rodríguez 2011) para a origem física de harmônicos pares vs ímpares em inversores e a genealogia do limite de 1% na 2ª harmônica — não altera nenhum limite aplicado no dashboard
source: Teodorescu, Liserre & Rodríguez (2011) §5.4.3 p.99; §12.3.5.1 p.330-331; Tab.3.6 p.37; Tab.12.1/12.2 p.315
references:
  - "TEODORESCU, Remus; LISERRE, Marco; RODRÍGUEZ, Pedro. Grid Converters for Photovoltaic and Wind Power Systems. Chichester: John Wiley & Sons, Ltd, 2011. ISBN 978-0-470-05751-3."
metadata:
  type: reference
---

# Origem física dos harmônicos (Teodorescu et al., 2011)

Complementa [harmonic_norm_application.md](harmonic_norm_application.md) — aqui fica
a fundamentação bibliográfica de afirmações que já eram usadas nesse arquivo sem
citação. **A regra aplicada no dashboard não muda**: continua exclusivamente
IEEE 519-2014/IEEE 1547-2018 (ver `harmonic_norm_application.md`). Este arquivo é
só o "porquê" físico por trás da tabela de harmônicas, não um limite novo. Para a
derivação formal de por que a checagem por ordem precisa rodar em abc (colisão de
ordens no mesmo bin dq, fundamental dq = DC), ver
[harmonic_dq_frame_mapping.md](harmonic_dq_frame_mapping.md) — este livro chega à
mesma colisão 5ª/7ª→6ª por outro caminho (§12.3.5.1, MSRF), citado lá como
corroboração cruzada da derivação do Yazdani.

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
