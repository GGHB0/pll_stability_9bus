---
name: tcc-revisao-fragmento-cap4-figuras
description: As 4 figuras inseridas no Cap.4 do fragmento capitulos_4_5_revisados.docx — mapa, renumeração, decisões de redação e as duas pendências de legibilidade
metadata:
  type: project
---

# Cap. 4 do Fragmento — Figuras

Desmembrado de [[tcc-revisao-fragmento-cap4]] em 2026-08-23 pelo limite de
200 linhas. A revisão de texto do capítulo (grupos A e B, remissões à
Seção 5.4) fica lá.

## Figuras do Cap. 4 (2026-08-23, noite)

O capítulo tinha três legendas ("Figura 4.1/4.2/4.3") sem imagem nenhuma, e o
§4.3.1 não tinha figura. Fechado com quatro imagens; a numeração antiga andou
uma casa para abrir espaço para o unifilar.

| Nova | Seção | Arquivo em `assets/diagrams/` | Largura |
|---|---|---|---|
| 4.1 | 4.3.1, rede | `ieee9bus_unifilar.png` | 6,5" |
| 4.2 | 4.3.2.1, filtro LCL | `vsi_lcl_pwm_circuit.png` (era a "Fig. 3.1" do V8) | 6,5" |
| 4.3 | 4.3.2.3, SRF-PLL | `pll_control_loop.png` | 5,5" |
| 4.4 | 4.3.3, cenários | `matriz_cenarios.png` | 5,5" |

Documento passou de 105 para **111 parágrafos e 17 imagens**. A Figura 4.1 é
inteiramente nova (imagem + legenda + frase de chamada); as outras três só
ganharam o parágrafo de imagem acima da legenda que já existia. Nenhuma
menção a figura do Cap. 4 existe fora desses pares, então a renumeração
tocou só 6 parágrafos.

Duas das quatro imagens nasceram nesta sessão:

- `pll_control_loop.svg` foi **refeito**: o `viewBox` caiu de 920×340 para
  680×350 e as fontes subiram para 13-18 px, porque no layout antigo o texto
  chegava à página com 4,9 pt. Junto, `φ̂` virou `θ_PLL` para casar com o
  símbolo usado na Figura 4.2.
- `matriz_cenarios.svg` é **nova**, gerada por `scripts/gen_matriz_cenarios.py`
  lendo `output/results/` direto. Ver [[cenarios-simulados]].

### Decisões de redação que vieram junto

- As três frases de chamada diziam "A Figura X **pode ser utilizada para**
  representar" / "**pode ser empregada para** situar o leitor", linguagem de
  quem ainda não tinha a figura. Viraram afirmação direta.
- A legenda da 4.2 prometia só o estágio de potência, mas a figura traz também
  as malhas dq, o SRF-PLL e o bloco do Submódulo 2.10. Ampliada para
  "Circuito do inversor de dois níveis com filtro LCL, ponto de acoplamento
  com a rede e malhas de controle digital".

### ⚠️ Aberta: as duas figuras herdadas têm rótulo pequeno demais

Texto medido na página (`pt ≈ font_px × L_cm × 28,35 / W`, regra da skill
`svg-diagrams`), já na largura de 6,5":

| Figura | Menor rótulo | Na página |
|---|---|---|
| 4.3 e 4.4 (feitas para o TCC) | 13 px | 6,8 a 7,6 pt |
| 4.1 unifilar | 11,5 px (kV, MW das cargas) | **5,9 pt** |
| 4.2 circuito VSI | 9 px (nomes de sinal) | **4,7 pt** |

Piso da convenção do projeto: ~6,4 pt. Subir a fonte das duas herdadas não é
ajuste, é redesenho: são densas e o texto colide. O usuário optou por inserir
mais largas e decidir o redesenho à parte. O unifilar ainda é usado como
filtro interativo do dashboard ([[ieee9bus-topology]]), o que dá mais um
motivo para não editá-lo por conta própria.

### ⚠️ Aberta: o DOI dentro do unifilar

O subtítulo da figura traz `DOI 10.1109/TPWRS.2024.3469235`, fonte dos
parâmetros de linha. Em figura de TCC isso normalmente vai na linha "Fonte:"
abaixo da legenda, não dentro do desenho. Sinalizado ao usuário, **não
alterado**.
