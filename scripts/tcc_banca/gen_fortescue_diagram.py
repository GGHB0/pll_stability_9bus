# -*- coding: utf-8 -*-
"""
gen_fortescue_diagram.py
Gera o diagrama vetorial dos sistemas girantes de Fortescue e projeção no
referencial dq do SRF-PLL (assets/diagrams/fortescue_componentes_srf_pll.svg).
"""

import math
import os

svg_path = r"assets\diagrams\fortescue_componentes_srf_pll.svg"
os.makedirs(os.path.dirname(svg_path), exist_ok=True)

width, height = 1000, 420

def pol2cart(cx, cy, r, angle_deg):
    rad = math.radians(angle_deg)
    return cx + r * math.cos(rad), cy - r * math.sin(rad)

# Painéis
# (a) Sequência Positiva: cx=170, cy=240
# (b) Sequência Negativa: cx=500, cy=240
# (c) Referencial dq: cx=830, cy=240

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" font-family="Arial, Helvetica, sans-serif" width="{width}" height="{height}">')
svg.append('<defs>')
# Marcadores de seta
svg.append('  <marker id="arr_pos" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1.5 L8 5 L0 8.5 z" fill="#1D4ED8"/></marker>')
svg.append('  <marker id="arr_neg" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1.5 L8 5 L0 8.5 z" fill="#DC2626"/></marker>')
svg.append('  <marker id="arr_dq" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1.5 L8 5 L0 8.5 z" fill="#0F172A"/></marker>')
svg.append('  <marker id="arr_rot" viewBox="0 0 10 10" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L7 4 L0 8 z" fill="#475569"/></marker>')
svg.append('  <marker id="arr_rot_red" viewBox="0 0 10 10" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L7 4 L0 8 z" fill="#DC2626"/></marker>')
svg.append('</defs>')

# Fundo geral
svg.append(f'<rect width="{width}" height="{height}" fill="#FFFFFF"/>')

# Caixas dos painéis
panels = [
    (15, 12, 310, 396, "(a) Sequência Positiva (v⁺)", "Sequência de fase a-b-c • Rotação a +ω₀ (60 Hz)", "#EFF6FF", "#BFDBFE"),
    (345, 12, 310, 396, "(b) Sequência Negativa (v⁻)", "Sequência de fase a-c-b • Rotação a −ω₀ (60 Hz)", "#FEF2F2", "#FECACA"),
    (675, 12, 310, 396, "(c) Projeção no Referencial dq", "Referencial gira a +ω₀ • Batimento a 2ω₀ (120 Hz)", "#F8FAFC", "#CBD5E1")
]

for x, y, w, h, title, sub, bg, border in panels:
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{bg}" stroke="{border}" stroke-width="1.5"/>')
    svg.append(f'<text x="{x + w/2}" y="{y + 26}" text-anchor="middle" font-size="16" font-weight="bold" fill="#0F172A">{title}</text>')
    svg.append(f'<text x="{x + w/2}" y="{y + 44}" text-anchor="middle" font-size="11" fill="#475569">{sub}</text>')

# -------------------------------------------------------------
# PAINEL (a): Sequência Positiva
# -------------------------------------------------------------
cxa, cya, ra = 170, 240, 85
# Círculo pontilhado de referência
svg.append(f'<circle cx="{cxa}" cy="{cya}" r="{ra}" fill="none" stroke="#93C5FD" stroke-width="1.2" stroke-dasharray="4 3"/>')
svg.append(f'<circle cx="{cxa}" cy="{cya}" r="3" fill="#1D4ED8"/>')

# Fasores va+, vb+, vc+ (ângulos 90, 90-120=-30, 90+120=210)
angles_pos = [('a', 90, '#1D4ED8', 'v_a⁺'), ('b', -30, '#1E40AF', 'v_b⁺'), ('c', 210, '#1E40AF', 'v_c⁺')]
for name, ang, color, lbl in angles_pos:
    x2, y2 = pol2cart(cxa, cya, ra, ang)
    svg.append(f'<line x1="{cxa}" y1="{cya}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2.8" marker-end="url(#arr_pos)"/>')
    xl, yl = pol2cart(cxa, cya, ra + 18, ang)
    svg.append(f'<text x="{xl}" y="{yl+5}" text-anchor="middle" font-size="14" font-weight="bold" fill="{color}">{lbl}</text>')

# Arco de rotação +w0 (anti-horário)
# arco de 40 a 80 graus em raio 110
r_arc = 108
x_arc1, y_arc1 = pol2cart(cxa, cya, r_arc, 40)
x_arc2, y_arc2 = pol2cart(cxa, cya, r_arc, 85)
svg.append(f'<path d="M {x_arc1} {y_arc1} A {r_arc} {r_arc} 0 0 0 {x_arc2} {y_arc2}" fill="none" stroke="#1D4ED8" stroke-width="2.2" marker-end="url(#arr_pos)"/>')
svg.append(f'<text x="{cxa + 95}" y="{cya - 85}" font-size="13" font-weight="bold" fill="#1D4ED8">+ω₀</text>')

# Rodapé Painel (a)
svg.append(f'<rect x="25" y="348" width="290" height="48" rx="6" fill="#DBEAFE" stroke="#93C5FD"/>')
svg.append(f'<text x="170" y="367" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#1E3A8A">Gira no sentido anti-horário (+ω₀)</text>')
svg.append(f'<text x="170" y="384" text-anchor="middle" font-size="11" fill="#1E40AF">Simétrico: alinha-se ao eixo d do PLL</text>')

# -------------------------------------------------------------
# PAINEL (b): Sequência Negativa
# -------------------------------------------------------------
cxb, cyb, rb = 500, 240, 85
svg.append(f'<circle cx="{cxb}" cy="{cyb}" r="{rb}" fill="none" stroke="#FCA5A5" stroke-width="1.2" stroke-dasharray="4 3"/>')
svg.append(f'<circle cx="{cxb}" cy="{cyb}" r="3" fill="#DC2626"/>')

# Fasores va-, vb-, vc- (sequência invertida: va em 90, vb em 210, vc em -30)
angles_neg = [('a', 90, '#DC2626', 'v_a⁻'), ('b', 210, '#B91C1C', 'v_b⁻'), ('c', -30, '#B91C1C', 'v_c⁻')]
for name, ang, color, lbl in angles_neg:
    x2, y2 = pol2cart(cxb, cyb, rb, ang)
    svg.append(f'<line x1="{cxb}" y1="{cyb}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2.8" marker-end="url(#arr_neg)"/>')
    xl, yl = pol2cart(cxb, cyb, rb + 18, ang)
    svg.append(f'<text x="{xl}" y="{yl+5}" text-anchor="middle" font-size="14" font-weight="bold" fill="{color}">{lbl}</text>')

# Arco de rotação -w0 (horário)
x_arc1b, y_arc1b = pol2cart(cxb, cyb, r_arc, 85)
x_arc2b, y_arc2b = pol2cart(cxb, cyb, r_arc, 40)
svg.append(f'<path d="M {x_arc1b} {y_arc1b} A {r_arc} {r_arc} 0 0 1 {x_arc2b} {y_arc2b}" fill="none" stroke="#DC2626" stroke-width="2.2" marker-end="url(#arr_neg)"/>')
svg.append(f'<text x="{cxb + 95}" y="{cyb - 85}" font-size="13" font-weight="bold" fill="#DC2626">−ω₀</text>')

# Rodapé Painel (b)
svg.append(f'<rect x="355" y="348" width="290" height="48" rx="6" fill="#FEE2E2" stroke="#FCA5A5"/>')
svg.append(f'<text x="500" y="367" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#991B1B">Gira no sentido horário (−ω₀)</text>')
svg.append(f'<text x="500" y="384" text-anchor="middle" font-size="11" fill="#B91C1C">Surge exclusivamente em faltas assimétricas</text>')

# -------------------------------------------------------------
# PAINEL (c): Referencial dq do SRF-PLL
# -------------------------------------------------------------
cxc, cyc = 830, 240
# Eixos dq síncronos
# Eixo d apontando na horizontal/ligeiramente inclinado (ângulo 20 graus)
theta_dq = 20
l_axis = 105
xd, yd = pol2cart(cxc, cyc, l_axis, theta_dq)
xq, yq = pol2cart(cxc, cyc, l_axis, theta_dq + 90)
svg.append(f'<line x1="{cxc - 20}" y1="{cyc}" x2="{xd}" y2="{yd}" stroke="#0F172A" stroke-width="2" marker-end="url(#arr_dq)"/>')
svg.append(f'<line x1="{cxc}" y1="{cyc + 20}" x2="{xq}" y2="{yq}" stroke="#0F172A" stroke-width="2" marker-end="url(#arr_dq)"/>')
svg.append(f'<text x="{xd + 8}" y="{yd + 4}" font-size="15" font-weight="bold" fill="#0F172A">d</text>')
svg.append(f'<text x="{xq - 4}" y="{yq - 8}" font-size="15" font-weight="bold" fill="#0F172A">q</text>')

# Vetor de Sequência Positiva V+ alinhado com o eixo d (Magnitude CC constante)
rv_pos = 75
xv_pos, yv_pos = pol2cart(cxc, cyc, rv_pos, theta_dq)
svg.append(f'<line x1="{cxc}" y1="{cyc}" x2="{xv_pos}" y2="{yv_pos}" stroke="#1D4ED8" stroke-width="3.5" marker-end="url(#arr_pos)"/>')
svg.append(f'<text x="{xv_pos - 15}" y="{yv_pos - 10}" font-size="13" font-weight="bold" fill="#1D4ED8">V⁺ (CC)</text>')

# Órbita da Sequência Negativa V- ao redor da ponta de V+
rv_neg = 32
svg.append(f'<circle cx="{xv_pos}" cy="{yv_pos}" r="{rv_neg}" fill="none" stroke="#DC2626" stroke-width="1.3" stroke-dasharray="3 3"/>')
# Vetor V- rotacionando a 2w0 no sentido horário relativo
ang_vneg = theta_dq - 65
xv_neg, yv_neg = pol2cart(xv_pos, yv_pos, rv_neg, ang_vneg)
svg.append(f'<line x1="{xv_pos}" y1="{yv_pos}" x2="{xv_neg}" y2="{yv_neg}" stroke="#DC2626" stroke-width="2.5" marker-end="url(#arr_neg)"/>')
svg.append(f'<text x="{xv_neg + 6}" y="{yv_neg + 14}" font-size="12" font-weight="bold" fill="#DC2626">V⁻ (2ω₀)</text>')

# Seta indicando a rotação de 2w0 ao redor de V+
x_rot1, y_rot1 = pol2cart(xv_pos, yv_pos, rv_neg + 12, ang_vneg + 50)
x_rot2, y_rot2 = pol2cart(xv_pos, yv_pos, rv_neg + 12, ang_vneg - 10)
svg.append(f'<path d="M {x_rot1} {y_rot1} A {rv_neg+12} {rv_neg+12} 0 0 1 {x_rot2} {y_rot2}" fill="none" stroke="#DC2626" stroke-width="1.8" marker-end="url(#arr_rot_red)"/>')
svg.append(f'<text x="{xv_pos + 26}" y="{yv_pos - 32}" font-size="11.5" font-weight="bold" fill="#DC2626">2ω₀ (120 Hz)</text>')

# Projeções pontilhadas sobre o eixo d e q mostrando o ripple
svg.append(f'<circle cx="{cxc}" cy="{cyc}" r="3" fill="#0F172A"/>')

# Rodapé Painel (c)
svg.append(f'<rect x="685" y="348" width="290" height="48" rx="6" fill="#F1F5F9" stroke="#CBD5E1"/>')
svg.append(f'<text x="830" y="367" text-anchor="middle" font-size="11" font-weight="bold" fill="#0F172A">Velocidade relativa: Δω = ω₀ − (−ω₀) = 2ω₀</text>')
svg.append(f'<text x="830" y="384" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#B91C1C">Ondulação de 120 Hz induzida em vd e vq</text>')

svg.append('</svg>')

with open(svg_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(svg))

print(f"SVG gerado com sucesso: {svg_path}")
