# -*- coding: utf-8 -*-
"""
apply_ponto_c.py
Aplica a fundamentacao analitica e os calculos numericos de largura de banda
do SRF-PLL segundo Teodorescu, Liserre e Rodriguez (2011):
- Secao 2.4: Expressao analitica da largura de banda a -3 dB (em vermelho);
- Secao 3.3.2.3: Largura de banda nominal (106,5 Hz) e inadequada (38,5 Hz) (em vermelho).
"""

import os
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"C:\Temp\tcc_banca\unpacked"
DOC_XML = os.path.join(BASE_DIR, "word", "document.xml")

with open(DOC_XML, "r", encoding="utf-8") as f:
    xml = f.read()

print(f"Lendo {DOC_XML} ({len(xml)} bytes)...")

# Estilos de runs em vermelho
red_rpr = '<w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr>'
red_sub_rpr = '<w:rPr><w:color w:val="FF0000"/><w:vertAlign w:val="subscript"/><w:szCs w:val="24"/></w:rPr>'

# ==============================================================================
# 1. SECAO 2.4 - FORMULACAO ANALITICA DE LARGURA DE BANDA (TEODORESCU)
# ==============================================================================
text24_red = (
    '<w:r>' + red_rpr + '<w:t xml:space="preserve"> Conforme a modelagem analítica de Teodorescu, Liserre e Rodríguez (2011, §4.2.2.3, p. 56), o critério de 1% para o tempo de acomodação (</w:t></w:r>'
    '<w:r>' + red_rpr + '<w:t>t</w:t></w:r>'
    '<w:r>' + red_sub_rpr + '<w:t>s</w:t></w:r>'
    '<w:r>' + red_rpr + '<w:t xml:space="preserve"> = 4,6 / (ξω</w:t></w:r>'
    '<w:r>' + red_sub_rpr + '<w:t>n</w:t></w:r>'
    '<w:r>' + red_rpr + '<w:t xml:space="preserve">)) fundamenta o projeto dos ganhos e estabelece analiticamente a largura de banda de malha fechada a -3 dB do laço de sincronismo: ω</w:t></w:r>'
    '<w:r>' + red_sub_rpr + '<w:t>-3dB</w:t></w:r>'
    '<w:r>' + red_rpr + '<w:t xml:space="preserve"> = ω</w:t></w:r>'
    '<w:r>' + red_sub_rpr + '<w:t>n</w:t></w:r>'
    '<w:r>' + red_rpr + '<w:t xml:space="preserve"> · √[1 + 2ξ² + √((1 + 2ξ²)² + 1)] ≈ 2,06·ω</w:t></w:r>'
    '<w:r>' + red_sub_rpr + '<w:t>n</w:t></w:r>'
    '<w:r>' + red_rpr + '<w:t xml:space="preserve"> (para ξ = 0,707).</w:t></w:r>'
)

old_run_24 = 'frequência da rede. Adota-se t'
new_run_24 = 'frequência da rede.</w:t></w:r>' + text24_red + '<w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve"> Adota-se t'

if old_run_24 in xml:
    xml = xml.replace(old_run_24, new_run_24, 1)
    print("Sucesso: Expressão analítica da largura de banda inserida na Seção 2.4 (em vermelho).")
else:
    print("ERRO: Trecho da Seção 2.4 não encontrado!")
    sys.exit(1)

# ==============================================================================
# 2. SECAO 3.3.2.3 - VALORES NUMERICOS DE LARGURA DE BANDA
# ==============================================================================
# Insercao 1: Apos "ξ = 0,707)."
old_3323_nom = '<w:t xml:space="preserve"> = 325,3 rad/s, ξ = 0,707). A sintonia inadequada'

new_3323_nom = (
    '<w:t xml:space="preserve"> = 325,3 rad/s, ξ = 0,707).</w:t></w:r>'
    '<w:r>' + red_rpr + '<w:t xml:space="preserve"> A partir da formulação de Teodorescu, Liserre e Rodríguez (2011), essa sintonia nominal (</w:t></w:r>'
    '<w:r>' + red_rpr + '<w:t>t</w:t></w:r>'
    '<w:r>' + red_sub_rpr + '<w:t>s</w:t></w:r>'
    '<w:r>' + red_rpr + '<w:t xml:space="preserve"> = 20 ms) resulta em uma largura de banda de malha fechada a -3 dB de ω</w:t></w:r>'
    '<w:r>' + red_sub_rpr + '<w:t>-3dB</w:t></w:r>'
    '<w:r>' + red_rpr + '<w:t xml:space="preserve"> = 669,5 rad/s (f</w:t></w:r>'
    '<w:r>' + red_sub_rpr + '<w:t>-3dB</w:t></w:r>'
    '<w:r>' + red_rpr + '<w:t xml:space="preserve"> ≈ 106,5 Hz).</w:t></w:r>'
    '<w:r><w:t xml:space="preserve"> A sintonia inadequada'
)

if old_3323_nom in xml:
    xml = xml.replace(old_3323_nom, new_3323_nom, 1)
    print("Sucesso: Largura de banda nominal inserida na Seção 3.3.2.3 (em vermelho).")
else:
    print("ERRO: Trecho nominal da Seção 3.3.2.3 não encontrado!")
    sys.exit(1)

# Insercao 2: Apos "ξ = 0,316)."
old_3323_inad = '<w:t xml:space="preserve"> = 145,5 rad/s, ξ = 0,316). As consequências'

new_3323_inad = (
    '<w:t xml:space="preserve"> = 145,5 rad/s, ξ = 0,316)</w:t></w:r>'
    '<w:r>' + red_rpr + '<w:t xml:space="preserve">, o que reduz a largura de banda de malha fechada a -3 dB para ω</w:t></w:r>'
    '<w:r>' + red_sub_rpr + '<w:t>-3dB</w:t></w:r>'
    '<w:r>' + red_rpr + '<w:t xml:space="preserve"> = 241,8 rad/s (f</w:t></w:r>'
    '<w:r>' + red_sub_rpr + '<w:t>-3dB</w:t></w:r>'
    '<w:r>' + red_rpr + '<w:t xml:space="preserve"> ≈ 38,5 Hz).</w:t></w:r>'
    '<w:r><w:t xml:space="preserve"> As consequências'
)

if old_3323_inad in xml:
    xml = xml.replace(old_3323_inad, new_3323_inad, 1)
    print("Sucesso: Largura de banda inadequada inserida na Seção 3.3.2.3 (em vermelho).")
else:
    print("ERRO: Trecho inadequado da Seção 3.3.2.3 não encontrado!")
    sys.exit(1)

# Salvar o document.xml modificado
with open(DOC_XML, "w", encoding="utf-8") as f:
    f.write(xml)

print(f"Arquivo {DOC_XML} atualizado com sucesso ({len(xml)} bytes).")

# Validacao de bem-formacao XML
tree = ET.parse(DOC_XML)
print("Validacao XML: document.xml eh 100% bem-formado!")
