---
name: vsc-topology-and-transforms
description: Fundamentos de topologia VSC (half-bridge, full-bridge, dois níveis) e formalismo de fasor espacial para as transformadas Clarke/Park — Yazdani & Iravani, Cap. 1-2, 4
source: Yazdani & Iravani, Voltage-Sourced Converters in Power Systems, 2010, Cap.1 (p.23-46), Cap.4 (p.69-125)
---

# Topologia VSC e Formalismo de Fasor Espacial (Yazdani & Iravani, Cap. 1-4)

Base para as seções 3.1 (Transformadas de Referência) e 3.2/3.3 (GD/VSI,
PWM) do TCC — complementa [[vsc-reference]] (que cobre o Cap. 8, controle
em dq-frame) com os capítulos fundacionais do livro (topologia e
transformadas), ainda não mapeados no KB.

## Topologia VSC (Cap. 1, §1.6-1.7)

Um conversor eletrônico de potência é definido como um circuito multiporta
de chaves semicondutoras (+ componentes auxiliares — capacitores, indutores,
transformadores) cuja função é trocar energia entre subsistemas de forma
controlada. Classificação por tipo de subsistema interfaceado: DC/AC
(retificador se o fluxo médio de potência vai de CA→CC; inversor se
CC→CA), DC/DC, AC/AC.

**Progressão de topologias (todas construídas a partir da célula de
chaveamento half-bridge):**
1. **Half-bridge (2 níveis)** — célula básica: chave superior + chave
   inferior, cada uma com diodo antiparalelo (reverse-conducting switch,
   tipicamente IGBT). A tensão AC comutada está sempre no nó `p` ou `n` —
   por isso "conversor de dois níveis".
2. **Full-bridge / H-bridge** — 2 half-bridges em paralelo pelo lado CC;
   tensão AC sintetizada é o dobro do half-bridge para a mesma tensão CC
   (melhor aproveitamento).
3. **VSC trifásico de dois níveis (3 fios)** — extensão direta do
   half-bridge: 3 pernas, uma por fase, interfaceadas à rede tipicamente via
   transformador trifásico. **Esta é a topologia do inversor do TCC.**
4. Configurações multinível/multimódulo (H-bridge em cascata, NPC) — fora do
   escopo deste TCC, mas mencionadas no livro como extensão para aplicações
   de tensão mais alta.

**Aplicações de IBR citadas pelo livro** (2010, já antecipava o cenário de
transição energética hoje descrito em [[energy-transition-iea2026]]):
integração de fontes renováveis de larga escala, geração distribuída,
maximização de penetração de renováveis — motivação praticamente idêntica
à do Cap. 2.1 deste TCC.

## Modulação PWM (Cap. 2 e 3)

A tensão fundamental do lado CA é controlada por PWM (pulse-width
modulation) — sinal modulante `m(t)` gera a tensão de saída `Vt = (VDC/2)·m`.
O modelo médio (averaged model) do half-bridge é a base para análise
dinâmica/projeto de controle (Fig. 2.17), distinto do modelo comutado
(chaveamento discreto), usado apenas para perdas de comutação com maior
precisão.

**Controle do half-bridge (Cap. 3)** — precursor conceitual do controle de
corrente trifásico do Cap. 8 (já em [[vsc-reference]]): compensador PI
`K(s) = (kp·s + ki)/s`, cancelamento do polo da planta `ki/kp = (R+ron)/L`,
constante de tempo de malha fechada `τi` escolhida tipicamente 10× menor
que o período de chaveamento. Mesma lógica de projeto (pole-zero
cancellation) reaparece de forma independente em [[agp-current-control-theory]]
(tese do coorientador) — duas fontes convergentes para a mesma técnica.

## Formalismo de Fasor Espacial (Cap. 4) — base rigorosa de Clarke/Park

Yazdani introduz Clarke/Park não como matrizes trigonométricas isoladas
(abordagem mais comum em outros livros, já usada no texto atual do TCC —
ver `full_cap2.md`), mas via o conceito mais geral de **fasor espacial**:

```
f⃗(t) = (2/3)·[e^(j0)·fa(t) + e^(j2π/3)·fb(t) + e^(j4π/3)·fc(t)]
```

Para um sinal trifásico equilibrado `fa,b,c = f̂·cos(ωt + θ0 − k·2π/3)`,
o fasor espacial se reduz a `f⃗(t) = f̂·e^(jθ0)·e^(jωt)` — um fasor clássico
girando a `ω`. A forma generalizada `f⃗(t) = f̂(t)·e^(jθ(t))` acomoda
amplitude e frequência variáveis no tempo — útil para descrever
diretamente o sinal de saída de um PLL rastreando uma rede com RoCoF.

### αβ-frame — decomposição em partes real/imaginária

```
f⃗(t) = fα(t) + j·fβ(t)
```
```
[fa]   [ 1      0    ]
[fb] = [-1/2  √3/2 ] · [fα]
[fc]   [-1/2 -√3/2 ]   [fβ]
```

Matriz de transformação inversa (abc→αβ) é a transposta escalada — mesma
matriz `C` citada de forma equivalente em [[srf-pll-theory]] (Karimi-
Ghartemani) e no texto atual do TCC (`full_cap2.md`, "Transformada de
Clarke").

### dq-frame — rotação sobre o αβ

```
fd + j·fq = (fα + j·fβ)·e^(-jε(t))
```

Em forma matricial real (Eq. 4.68-4.69 do livro):

```
[fd]   [ cos ε(t)   sin ε(t) ]   [fα]
[fq] = [-sin ε(t)   cos ε(t) ] · [fβ]
```

Se `ε(t) = ε0 + ∫ω(τ)dτ` acompanha exatamente a frequência do fasor
espacial, `fd + j·fq` torna-se **estacionário** (constante em regime) — as
componentes trifásicas viram grandezas CC, a propriedade central que
justifica o uso de controladores PI no referencial síncrono (mesmo
argumento já presente no texto atual do TCC, seção "Transformada de Park").
A matriz de rotação `R[ε(t)]` é ortogonal: `R⁻¹[ε] = Rᵀ[ε] = R[-ε]`.

## Uso no TCC

Este material dá uma segunda fonte, mais formal (fasor espacial → αβ → dq
por rotação), para a seção 3.1, complementando a apresentação trigonométrica
direta já redigida. Também fundamenta 3.2 (identificação do VSI trifásico
de dois níveis como a topologia do inversor UFV do projeto) e 3.3 (PWM como
elo funcional entre referência dq e o estágio de potência, já delimitado
como fora do escopo de análise detalhada). Ver [[vsc-reference]] para a
continuação no Cap. 8 (controle de corrente dq, critério de VDC, base pu).
