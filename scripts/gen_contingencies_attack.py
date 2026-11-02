"""Gera assets/diagrams/contingencies_attack.svg (figura do README).

Uso: python scripts/gen_contingencies_attack.py assets/diagrams/contingencies_attack.svg
"""
import math, sys
W=2*math.pi*60; T0,T1=0.0,0.1; TF,TC=0.03,0.075
X0,X1=40,410
def tx(t): return X0+(t-T0)/(T1-T0)*(X1-X0)
def amps(t,kind):
    if not (TF<=t<TC): return (1,1,1)
    return (0.4,0.4,0.4) if kind=="sim" else (0.3,1,1)
def abc(t,kind):
    a=amps(t,kind); th=W*t
    return [a[0]*math.cos(th), a[1]*math.cos(th-2*math.pi/3), a[2]*math.cos(th+2*math.pi/3)]
def dq(t,kind):
    va,vb,vc=abc(t,kind); th=W*t
    d=2/3*(va*math.cos(th)+vb*math.cos(th-2*math.pi/3)+vc*math.cos(th+2*math.pi/3))
    q=-2/3*(va*math.sin(th)+vb*math.sin(th-2*math.pi/3)+vc*math.sin(th+2*math.pi/3))
    return d,q
N=1200
ts=[T0+i*(T1-T0)/N for i in range(N+1)]
def path(vals,ymap):
    return "M"+" L".join(f"{tx(t):.1f} {ymap(v):.1f}" for t,v in zip(ts,vals))
def card(kind,ox):
    sim = kind=="sim"
    out=[f'<g transform="translate({ox},52)">',
         '<rect x="0" y="0" width="430" height="452" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>',
         '<circle cx="26" cy="28" r="13" fill="#c92a2a"/>',
         f'<text x="26" y="33" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">{1 if sim else 2}</text>',
         f'<text x="48" y="27" font-size="16" font-weight="700" fill="#0B132B">Afundamento {"simétrico" if sim else "assimétrico"}</text>',
         f'<text x="48" y="45" font-size="12" fill="#6b7280">{"falta trifásica: as três fases caem juntas" if sim else "falta monofásica ou bifásica: fases desequilibradas"}</text>']
    # fault band in both plots
    for y0,h in ((86,92),(242,92)):
        out.append(f'<rect x="{tx(TF):.1f}" y="{y0}" width="{tx(TC)-tx(TF):.1f}" height="{h}" fill="#fde2e2"/>')
    out.append(f'<text x="{(tx(TF)+tx(TC))/2:.1f}" y="98" text-anchor="middle" font-size="11" font-weight="700" fill="#c92a2a">falta</text>')
    # plot 1 abc
    out.append('<text x="40" y="78" font-size="12" font-weight="700" fill="#475569">Tensões no PCC (abc)</text>')
    yc=134; A=34
    out.append(f'<line x1="{X0}" y1="{yc}" x2="{X1}" y2="{yc}" stroke="#cbd5e1" stroke-width="1"/>')
    cols=["#c92a2a","#2f9e44","#1971c2"]
    V=[abc(t,kind) for t in ts]
    for k in range(3):
        out.append(f'<path d="{path([v[k] for v in V],lambda v:yc-A*v)}" fill="none" stroke="{cols[k]}" stroke-width="1.6"/>')
    out.append(f'<text x="{X1+4}" y="{yc-24}" font-size="11" fill="#c92a2a" font-style="italic">a</text>')
    out.append(f'<text x="{X1+4}" y="{yc+4}" font-size="11" fill="#2f9e44" font-style="italic">b</text>')
    out.append(f'<text x="{X1+4}" y="{yc+30}" font-size="11" fill="#1971c2" font-style="italic">c</text>')
    # arrow Park
    out.append('<line x1="225" y1="184" x2="225" y2="210" stroke="#0B132B" stroke-width="1.8" marker-end="url(#ar)"/>')
    out.append('<text x="236" y="202" font-size="12" fill="#0B132B">Park com θ<tspan baseline-shift="sub" font-size="75%">PLL</tspan></text>')
    # plot 2 dq
    out.append('<text x="40" y="234" font-size="12" font-weight="700" fill="#475569">Eixos dq: o que o PLL enxerga</text>')
    y0=318; S=62  # y = y0 - S*v ; v range [-0.3, 1.15]
    out.append(f'<line x1="{X0}" y1="{y0}" x2="{X1}" y2="{y0}" stroke="#cbd5e1" stroke-width="1"/>')
    out.append(f'<text x="{X0-6}" y="{y0+4}" text-anchor="end" font-size="10" fill="#6b7280">0</text>')
    out.append(f'<text x="{X0-6}" y="{y0-S+4}" text-anchor="end" font-size="10" fill="#6b7280">1</text>')
    out.append(f'<line x1="{X0-3}" y1="{y0-S}" x2="{X0}" y2="{y0-S}" stroke="#6b7280"/>')
    D=[dq(t,kind) for t in ts]
    out.append(f'<path d="{path([d for d,q in D],lambda v:y0-S*v)}" fill="none" stroke="#0B132B" stroke-width="2"/>')
    out.append(f'<path d="{path([q for d,q in D],lambda v:y0-S*v)}" fill="none" stroke="#F97316" stroke-width="2"/>')
    out.append(f'<text x="{X1+4}" y="{y0-S+4}" font-size="12" font-style="italic" fill="#0B132B">v<tspan baseline-shift="sub" font-size="75%">d</tspan></text>')
    out.append(f'<text x="{X1+4}" y="{y0+4}" font-size="12" font-style="italic" fill="#F97316">v<tspan baseline-shift="sub" font-size="75%">q</tspan></text>')
    # note on dq plot
    if sim:
        out.append(f'<text x="{(tx(TF)+tx(TC))/2:.1f}" y="{y0-S*0.4-8:.1f}" text-anchor="middle" font-size="11" fill="#0B132B">v<tspan baseline-shift="sub" font-size="75%">d</tspan> = U</text>')
    else:
        out.append(f'<text x="{(tx(TF)+tx(TC))/2:.1f}" y="{y0+30:.1f}" text-anchor="middle" font-size="11" font-weight="700" fill="#c2410c">oscilação de 120 Hz</text>')
    # effect box
    lines = (["v<tspan baseline-shift='sub' font-size='75%'>d</tspan> cai para U e v<tspan baseline-shift='sub' font-size='75%'>q</tspan> segue em zero.",
              "O ganho do laço é proporcional a U: ω<tspan baseline-shift='sub' font-size='75%'>n</tspan> e ξ",
              "caem com √U e o PLL fica mais lento.",
              "Com U = 0,2 pu, vira a sintonia lenta."] if sim else
             ["A sequência negativa gira no sentido oposto",
              "e aparece em dq como oscilação de 120 Hz.",
              "Como v<tspan baseline-shift='sub' font-size='75%'>q</tspan> é a entrada do PI, o PLL corrige",
              "um erro que não existe e θ<tspan baseline-shift='sub' font-size='75%'>PLL</tspan> oscila."])
    out.append('<rect x="16" y="356" width="398" height="82" rx="8" fill="#fff7ed" stroke="#F97316" stroke-width="1.2"/>')
    for i,l in enumerate(lines):
        out.append(f'<text x="30" y="{376+i*18}" font-size="12.5" fill="#0B132B">{l}</text>')
    out.append('</g>')
    return "\n  ".join(out)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 520" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif">
  <defs>
    <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#0B132B"/></marker>
  </defs>
  <!-- Gerado por script (formas de onda calculadas: Park invariante em amplitude, θ = ωt, 60 Hz).
       Simétrico: as três fases a 0,4 pu. Assimétrico: fase a a 0,3 pu, b e c a 1 pu. -->
  <rect width="920" height="520" fill="#ffffff"/>
  <text x="460" y="32" text-anchor="middle" font-size="17" font-weight="700" fill="#0B132B">Onde cada contingência ataca o laço do SRF-PLL</text>
  {card("sim",20)}
  {card("asim",470)}
</svg>
'''
open(sys.argv[1],"w",encoding="utf-8").write(svg)
