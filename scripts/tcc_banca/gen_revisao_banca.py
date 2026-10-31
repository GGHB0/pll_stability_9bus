# -*- coding: utf-8 -*-
"""
gen_revisao_banca.py
Aplica as revisões aprovadas pelo usuário para atender à banca:
- Etapa 1: Padrão UERJ (numeração de seções primárias, introdução/conclusão sem número, renumeração de seções e remissões);
- Etapa 2 (parcial): Lógica do Submódulo 2.10 (inserção da figura do slide 14 e ajuste do texto da rampa);
- Etapa 3: Inclusão das referências bibliográficas faltantes, pontuação de equações, itálicos e correções textuais;
- Etapa 4: Apêndice A do Painel Interativo e eliminação de espaços em branco.
"""

import os
import re
import shutil
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"C:\Temp\tcc_banca\unpacked"
DOC_XML = os.path.join(BASE_DIR, "word", "document.xml")
RELS_XML = os.path.join(BASE_DIR, "word", "_rels", "document.xml.rels")
MEDIA_DIR = os.path.join(BASE_DIR, "word", "media")

with open(DOC_XML, "r", encoding="utf-8") as f:
    xml = f.read()

print(f"Lendo {DOC_XML} ({len(xml)} bytes)...")

# ==============================================================================
# 1. IMAGENS ADICIONAIS (Slide 14 e Dashboard)
# ==============================================================================
os.makedirs(MEDIA_DIR, exist_ok=True)

src_ons = r"assets\diagrams\ons_logica_defesa.png"
dst_ons = os.path.join(MEDIA_DIR, "ons_logica_submodulo210.png")
shutil.copyfile(src_ons, dst_ons)
print(f"Copiada {src_ons} -> {dst_ons}")

src_dash = r"output\verifica_palco\1920x1080\08_sintese.png"
dst_dash = os.path.join(MEDIA_DIR, "dashboard_apendice.png")
shutil.copyfile(src_dash, dst_dash)
print(f"Copiada {src_dash} -> {dst_dash}")

with open(RELS_XML, "r", encoding="utf-8") as f:
    rels_xml = f.read()

if 'Target="media/ons_logica_submodulo210.png"' not in rels_xml:
    new_rels = (
        '  <Relationship Id="rId47" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/ons_logica_submodulo210.png"/>\n'
        '  <Relationship Id="rId48" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/dashboard_apendice.png"/>\n'
        '</Relationships>'
    )
    rels_xml = rels_xml.replace('</Relationships>', new_rels)
    with open(RELS_XML, "w", encoding="utf-8") as f:
        f.write(rels_xml)
    print("Registrados rId47 e rId48 em document.xml.rels com sucesso.")

# ==============================================================================
# 2. PADRÃO UERJ: TÍTULOS DE SEÇÕES PRIMÁRIAS E SUBSEÇÕES
# ==============================================================================
# Títulos primários:
xml = xml.replace("<w:t>Capítulo 1 – Introdução</w:t>", "<w:t>INTRODUÇÃO</w:t>")
xml = xml.replace(
    "<w:t>Capítulo 2 – Desafios à Estabilidade em Redes Dominadas por Inversores</w:t>",
    "<w:t>1  DESAFIOS À ESTABILIDADE EM REDES DOMINADAS POR INVERSORES</w:t>"
)
xml = xml.replace(
    "<w:t>Capítulo 3 – Geração Conectada à Rede por Inversores: Fundamentação Teórica</w:t>",
    "<w:t>2  GERAÇÃO CONECTADA À REDE POR INVERSORES: FUNDAMENTAÇÃO TEÓRICA</w:t>"
)
xml = xml.replace(
    "<w:t>Capítulo 4 – Metodologia de Análise</w:t>",
    "<w:t>3  METODOLOGIA DE ANÁLISE</w:t>"
)
xml = xml.replace(
    "<w:t>Capítulo 5 – Análise e Discussão de Resultados</w:t>",
    "<w:t>4  ANÁLISE E DISCUSSÃO DE RESULTADOS</w:t>"
)
xml = xml.replace(
    "<w:t>Capítulo 6 – Conclusões</w:t>",
    "<w:t>CONCLUSÃO</w:t>"
)

# Capítulo 7 no corpo vira subseção Trabalhos Futuros dentro de Conclusão:
pos = xml.find('w:val="Ttulo1"')
while pos != -1:
    end_p = xml.find('</w:p>', pos)
    p_text = xml[pos:end_p]
    if 'Capítulo 7 – Trabalhos Futuros' in p_text:
        p_start = xml.rfind('<w:p ', 0, pos)
        p_end = end_p + 6
        cap7_p = xml[p_start:p_end]
        new_cap7_p = cap7_p.replace('w:val="Ttulo1"', 'w:val="Ttulo2"') \
                           .replace('<w:pageBreakBefore/>', '') \
                           .replace('w:sz w:val="48"', 'w:sz w:val="36"') \
                           .replace('w:szCs w:val="48"', 'w:szCs w:val="36"') \
                           .replace('<w:lastRenderedPageBreak/>', '') \
                           .replace('Capítulo 7 – Trabalhos Futuros', 'Trabalhos Futuros')
        xml = xml[:p_start] + new_cap7_p + xml[p_end:]
        print("Capítulo 7 no corpo transformado em subseção Trabalhos Futuros.")
        break
    pos = xml.find('w:val="Ttulo1"', end_p)

# Subseções (headings): 2.x -> 1.x, 3.x -> 2.x, 4.x -> 3.x, 5.x -> 4.x
def renum_heading_t(m):
    tag_prefix = m.group(1)
    sec = m.group(2)
    parts = sec.split('.')
    first = int(parts[0])
    new_first = first - 1
    new_sec = f"{new_first}." + ".".join(parts[1:])
    return f"{tag_prefix}{new_sec} "

xml = re.sub(r'(<w:t(?: xml:space="preserve")?>)([2-5]\.\d+(?:\.\d+)*\.)\s+', renum_heading_t, xml)
print("Subseções (headings) renumeradas com sucesso.")

# ==============================================================================
# 3. PREFIXOS DE FIGURAS E TABELAS NAS LEGENDAS
# ==============================================================================
xml = xml.replace("<w:t>Figura 2.</w:t>", "<w:t>Figura 1.</w:t>")
xml = xml.replace("<w:t>Figura 3.</w:t>", "<w:t>Figura 2.</w:t>")
xml = xml.replace("<w:t>Figura 4.</w:t>", "<w:t>Figura 3.</w:t>")
xml = xml.replace("<w:t>Figura 5.</w:t>", "<w:t>Figura 4.</w:t>")
xml = xml.replace("<w:t>Tabela 4.</w:t>", "<w:t>Tabela 3.</w:t>")
xml = xml.replace("<w:t>Tabela 5.</w:t>", "<w:t>Tabela 4.</w:t>")
print("Prefixos de legendas renumerados.")

# ==============================================================================
# 4. REMISSÕES NO CORPO DO TEXTO (PASSAGEM ÚNICA SEM CASCATA)
# ==============================================================================
# Figuras citadas no texto:
def renum_fig_match(m):
    prefix = m.group(1)
    cap = int(m.group(2))
    num = int(m.group(3))
    if cap == 2:
        return f"{prefix} 1.{num}"
    elif cap == 3:
        return f"{prefix} 2.{num}"
    elif cap == 4:
        if num <= 2:
            return f"{prefix} 3.{num}"
        else:
            return f"{prefix} 3.{num+1}"
    elif cap == 5:
        return f"{prefix} 4.{num}"
    return m.group(0)

xml = re.sub(r'\b(Figuras?)\s+([2-5])\.(\d+)\b', renum_fig_match, xml)

# Tabelas citadas no texto:
def renum_tab_match(m):
    prefix = m.group(1)
    cap = int(m.group(2))
    num = int(m.group(3))
    if cap == 4:
        return f"{prefix} 3.{num}"
    elif cap == 5:
        return f"{prefix} 4.{num}"
    return m.group(0)

xml = re.sub(r'\b(Tabelas?)\s+([4-5])\.(\d+)\b', renum_tab_match, xml)

# Seções citadas no texto:
def renum_sec_match(m):
    prefix = m.group(1)
    sec = m.group(2)
    parts = sec.split('.')
    first = int(parts[0])
    if first in (2, 3, 4, 5):
        new_first = first - 1
        return f"{prefix} {new_first}." + ".".join(parts[1:])
    return m.group(0)

xml = re.sub(r'\b(Seç(?:ão|ões))\s+([2-5]\.\d+(?:\.\d+)*)\b', renum_sec_match, xml)

# Adequação terminológica e gramatical (Capítulo -> Seção):
xml = xml.replace("Resumo e conclusões do capítulo", "Resumo e conclusões da seção")
xml = xml.replace("no capítulo anterior", "na seção anterior")
xml = xml.replace("no capítulo seguinte", "na seção seguinte")
xml = xml.replace("nos capítulos seguintes", "nas seções seguintes")
xml = xml.replace("nos capítulos subsequentes", "nas seções subsequentes")
xml = xml.replace("nos capítulos de modelagem e de resultados", "nas seções de modelagem e de resultados")
xml = xml.replace("Este capítulo ", "Esta seção ")
xml = xml.replace("este capítulo ", "esta seção ")
xml = xml.replace("o capítulo ", "a seção ")
xml = xml.replace("O capítulo ", "A seção ")
xml = xml.replace("do capítulo ", "da seção ")
xml = xml.replace("no capítulo ", "na seção ")
xml = xml.replace("nos capítulos ", "nas seções ")

xml = xml.replace("ao longo do Capítulo 5", "ao longo da Seção 4")
xml = xml.replace("no Capítulo 2", "na Seção 1")
xml = xml.replace("no Capítulo 3", "na Seção 2")
xml = xml.replace("no Capítulo 4", "na Seção 3")
xml = xml.replace("no Capítulo 5", "na Seção 4")
xml = xml.replace("do Capítulo 2", "da Seção 1")
xml = xml.replace("do Capítulo 3", "da Seção 2")
xml = xml.replace("do Capítulo 4", "da Seção 3")
xml = xml.replace("do Capítulo 5", "da Seção 4")
xml = xml.replace("o Capítulo 2", "a Seção 1")
xml = xml.replace("o Capítulo 3", "a Seção 2")
xml = xml.replace("o Capítulo 4", "a Seção 3")
xml = xml.replace("o Capítulo 5", "a Seção 4")
xml = xml.replace("O Capítulo 2", "A Seção 1")
xml = xml.replace("O Capítulo 3", "A Seção 2")
xml = xml.replace("O Capítulo 4", "A Seção 3")
xml = xml.replace("O Capítulo 5", "A Seção 4")
xml = xml.replace("Capítulo 2,", "Seção 1,")
xml = xml.replace("Capítulo 3 ", "Seção 2 ")
xml = xml.replace("Capítulo 4 ", "Seção 3 ")
xml = xml.replace("Capítulo 5 ", "Seção 4 ")
xml = xml.replace("no Capítulo 6", "na Conclusão")
xml = xml.replace("do Capítulo 6", "da Conclusão")
xml = xml.replace("Capítulo 6 ", "Conclusão ")
xml = xml.replace("Capítulo 7", "seção de Trabalhos Futuros")

# Split run específico do Capítulo 3 com quebra de página:
xml = xml.replace(
    'no Capítulo </w:t></w:r><w:r><w:lastRenderedPageBreak/><w:t>3:',
    'na Seção </w:t></w:r><w:r><w:lastRenderedPageBreak/><w:t>2:'
)
print("Remissões no corpo do texto atualizadas.")

# ==============================================================================
# 5. CORREÇÕES TEXTUAIS PONTUAIS DA BANCA
# ==============================================================================
# Pág. 16: "fontes de geração renovável variável"
old_p16 = 'os sistemas de geraç</w:t></w:r><w:r w:rsidR="007018F7"><w:rPr><w:szCs w:val="24"/></w:rPr><w:t>ão centralizada</w:t></w:r><w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve"> apresentam variações abruptas.'
new_p16 = 'as fontes de geração renovável variável apresentam variações abruptas e estocásticas.'
if old_p16 in xml:
    xml = xml.replace(old_p16, new_p16)
    print("Pág. 16: 'geração renovável variável' corrigida.")

# Pág. 20: "como os centros de dados" -> "como os data centers"
xml = xml.replace(
    "<w:t>como os centros de dados.</w:t>",
    "<w:t xml:space=\"preserve\">como os </w:t></w:r><w:r><w:rPr><w:i/><w:color w:val=\"1B1C1D\"/><w:szCs w:val=\"24\"/></w:rPr><w:t>data centers</w:t></w:r><w:r><w:rPr><w:color w:val=\"1B1C1D\"/><w:szCs w:val=\"24\"/></w:rPr><w:t>.</w:t>"
)

# Pág. 78: "As sobrecorrentes antecipadas" -> "As sobrecorrentes inicialmente previstas"
xml = xml.replace("As sobrecorrentes antecipadas", "As sobrecorrentes inicialmente previstas")

# Termos em inglês em itálico:
termos_italico = [
    ("(small-signal)", "(", "small-signal", ")"),
    ("(large-disturbance)", "(", "large-disturbance", ")"),
    ("(swings)", "(", "swings", ")"),
    ("(swing equation)", "(", "swing equation", ")"),
    ("(Converter-Driven Stability)", "(", "Converter-Driven Stability", ")"),
    ("(cycle slipping)", "(", "cycle slipping", ")"),
    ("(converter-driven)", "(", "converter-driven", ")"),
    ("ou cycle slipping,", "ou ", "cycle slipping", ","),
]
for full, pre, term, post in termos_italico:
    replacement = f"{pre}</w:t></w:r><w:r><w:rPr><w:i/><w:szCs w:val=\"24\"/></w:rPr><w:t>{term}</w:t></w:r><w:r><w:rPr><w:szCs w:val=\"24\"/></w:rPr><w:t>{post}"
    if full in xml:
        xml = xml.replace(full, replacement, 1)
        print(f"Itálico aplicado a: {term}")

# Pág. 23: System Stability Roadmap em itálico + citação de Strauss-Mincu et al. (2026)
old_roadmap = "<w:t>O System Stability Roadmap estabelece,"
new_roadmap = "<w:t xml:space=\"preserve\">O </w:t></w:r><w:r><w:rPr><w:i/><w:szCs w:val=\"24\"/></w:rPr><w:t>System Stability Roadmap</w:t></w:r><w:r><w:rPr><w:szCs w:val=\"24\"/></w:rPr><w:t xml:space=\"preserve\"> (STRAUSS-MINCU et al., 2026) estabelece,</w:t>"
if old_roadmap in xml:
    xml = xml.replace(old_roadmap, new_roadmap, 1)
    print("System Stability Roadmap formatado em itálico com citação.")

# Ajuste dimensional da Imagem 2 (antiga Fig 3.2, agora Fig 2.2) para caber na área útil (6.30 in)
xml = xml.replace('cx="5892800" cy="1911985"', 'cx="5760720" cy="1869123"')
print("Imagem 2 ajustada para caber na área útil de 6.30 in.")

# ==============================================================================
# 6. SUBMÓDULO 2.10: AJUSTE DO TEXTO NA SEÇÃO 1.5.2 E FIGURA DO SLIDE 14
# ==============================================================================
# Na Seção 1.5.2, parágrafo com a referência quebrada à figura do ONS:
old_p_ons = (
    '<w:p w14:paraId="7D1A1775" w14:textId="140A21B0" w:rsidR="00A41C58" w:rsidRDefault="002C0A25" w:rsidP="004442B0">'
    '<w:pPr><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:szCs w:val="24"/></w:rPr></w:pPr>'
    '<w:r><w:t>A observância desses requisitos depende inteiramente da atuação coordenada das malhas de controle do inversor. '
    'o ONS impõe rampas e limites específicos para a resposta de corrente durante e logo após a eliminação da falta</w:t></w:r>'
    '<w:r w:rsidR="00F20DBB"><w:t xml:space="preserve">, como </w:t></w:r>'
    '<w:r w:rsidR="00AC0A0F"><w:t xml:space="preserve">na figura </w:t></w:r>'
    '<w:r w:rsidR="000E49BF"><w:t>2.2,</w:t></w:r>'
    '<w:r><w:t xml:space="preserve"> a estimação correta do ângulo da tensão no PCC pelo SRF-PLL mostra-se indispensável. '
    'Falhas ou lentidão no sincronismo impossibilitam o correto direcionamento dos vetores de corrente nas coordenadas '
    'síncronas (d e q), comprometendo o atendimento aos critérios exigidos pelo operador nacional.</w:t></w:r></w:p>'
)

new_p_ons = (
    '<w:p w14:paraId="7D1A1775" w14:textId="140A21B0" w:rsidR="00A41C58" w:rsidRDefault="002C0A25" w:rsidP="004442B0">'
    '<w:pPr><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:szCs w:val="24"/></w:rPr></w:pPr>'
    '<w:r><w:rPr><w:szCs w:val="24"/></w:rPr>'
    '<w:t>A observância desses requisitos depende inteiramente da atuação coordenada das malhas de controle do inversor. '
    'Como o ONS impõe rampas e limites específicos para a resposta de corrente durante e logo após a eliminação da falta '
    '(conforme ilustrado na Figura 1.2), a estimação precisa do ângulo da tensão no PCC pelo SRF-PLL mostra-se indispensável. '
    'Falhas ou lentidão no sincronismo impossibilitam o correto direcionamento dos vetores de corrente nas coordenadas '
    'síncronas (d e q), comprometendo o atendimento aos critérios exigidos pelo operador nacional.</w:t></w:r></w:p>'
)

if old_p_ons in xml:
    xml = xml.replace(old_p_ons, new_p_ons)
    print("Parágrafo da Seção 1.5.2 (Submódulo 2.10) corrigido.")
else:
    print("AVISO: Parágrafo exato do Submódulo 2.10 não casou por string completa, verificando substituição pontual...")
    xml = xml.replace(
        '<w:r><w:t>A observância desses requisitos depende inteiramente da atuação coordenada das malhas de controle do inversor. o ONS impõe rampas e limites específicos para a resposta de corrente durante e logo após a eliminação da falta</w:t></w:r><w:r w:rsidR="00F20DBB"><w:t xml:space="preserve">, como </w:t></w:r><w:r w:rsidR="00AC0A0F"><w:t xml:space="preserve">na figura </w:t></w:r><w:r w:rsidR="000E49BF"><w:t>2.2,</w:t></w:r><w:r><w:t xml:space="preserve"> a estimação correta do ângulo da tensão no PCC pelo SRF-PLL mostra-se indispensável.',
        '<w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t>A observância desses requisitos depende inteiramente da atuação coordenada das malhas de controle do inversor. Como o ONS impõe rampas e limites específicos para a resposta de corrente durante e logo após a eliminação da falta (conforme ilustrado na Figura 1.2), a estimação precisa do ângulo da tensão no PCC pelo SRF-PLL mostra-se indispensável.'
    )

# Inclusão da Figura do Slide 14 na Metodologia (Seção 3.3.2 - Projeto do conversor)
bloco_ons_logica = """<w:p w14:paraId="1FB00320" w14:textId="77777777" w:rsidR="00381505" w:rsidRDefault="00381505"><w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:szCs w:val="24"/></w:rPr></w:pPr><w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t>Para implementar o suporte dinâmico de tensão exigido pelos Procedimentos de Rede do ONS (Submódulo 2.10), as referências de corrente interna são geradas dinamicamente a partir da tensão eficaz medida no PCC, segundo o diagrama funcional da Figura 3.3. A corrente reativa de suporte tem prioridade térmica absoluta sobre a corrente ativa, saturando no limite de 1,0 pu para afundamentos severos (V &lt; 0,5 pu). A margem de capacidade dos semicondutores remanescente é então alocada à injeção de corrente ativa pela relação quadrática id,ref = min(1.0, sqrt(Imax² - iq,ref²)). Com isso, a potência ativa injetada cai a zero durante as faltas mais profundas, garantindo que a capacidade do conversor seja integralmente dedicada à recuperação dos níveis de tensão da rede.</w:t></w:r></w:p>
<w:p w14:paraId="1FB00321" w14:textId="77777777" w:rsidR="00095F51" w:rsidRDefault="00381505"><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="60" w:line="240" w:lineRule="auto"/><w:rPr><w:sz w:val="20"/></w:rPr></w:pPr><w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>Figura 3.3 – Lógica de controle e priorização de corrente reativa do Submódulo 2.10 do ONS.</w:t></w:r></w:p>
<w:p w14:paraId="1FB00322" w14:textId="77777777" w:rsidR="00381505" w:rsidRDefault="00381505"><w:pPr><w:keepNext/><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:jc w:val="center"/><w:rPr><w:szCs w:val="24"/></w:rPr></w:pPr><w:r><w:rPr><w:noProof/></w:rPr><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0" wp14:anchorId="04A8139B" wp14:editId="3F049AF2"><wp:extent cx="5303520" cy="1767840"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:docPr id="900000047" name="ons_logica_submodulo210"/><wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="910000047" name="ons_logica_submodulo210"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="rId47"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="5303520" cy="1767840"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>
<w:p w14:paraId="1FB00323" w14:textId="77777777" w:rsidR="00095F51" w:rsidRDefault="00381505"><w:pPr><w:spacing w:before="60" w:after="240" w:line="240" w:lineRule="auto"/><w:rPr><w:sz w:val="20"/></w:rPr></w:pPr><w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>Fonte: Adaptado de ONS (2022).</w:t></w:r></w:p>"""

# Como inserimos a Figura 3.3 para a lógica do ONS, a antiga Figura 4.3 (Diagrama conceitual do SRF-PLL) passa a ser Figura 3.4
xml = xml.replace(
    "Figura 3.3 – Diagrama conceitual do SRF-PLL empregado no estudo.",
    "Figura 3.4 – Diagrama conceitual do SRF-PLL empregado no estudo."
)
xml = xml.replace("Figura 3.3 situa a arquitetura do SRF-PLL", "Figura 3.4 situa a arquitetura do SRF-PLL")

# Insere a nova figura após o bloco da Figura 3.2 (antiga 4.2)
target_fig32 = "<w:t>Fonte: Adaptado de Alves (2022).</w:t></w:r></w:p>"
if target_fig32 in xml:
    xml = xml.replace(target_fig32, target_fig32 + "\n" + bloco_ons_logica, 1)
    print("Figura 3.3 (Lógica do Submódulo 2.10) inserida com sucesso.")

# ==============================================================================
# 7. NOVAS REFERÊNCIAS BIBLIOGRÁFICAS
# ==============================================================================
novas_referencias = """<w:p w14:paraId="1FB00324" w14:textId="77777777" w:rsidR="00425537" w:rsidRDefault="00425537"><w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:spacing w:after="240" w:line="240" w:lineRule="auto"/><w:rPr><w:szCs w:val="24"/><w:lang w:val="es-CL"/></w:rPr></w:pPr><w:r><w:rPr><w:szCs w:val="24"/><w:lang w:val="es-CL"/></w:rPr><w:t xml:space="preserve">COORDINADOR ELÉCTRICO NACIONAL. </w:t></w:r><w:r><w:rPr><w:i/><w:szCs w:val="24"/><w:lang w:val="es-CL"/></w:rPr><w:t>Resumen Ejecutivo: Estudio para Análisis de Falla del 25 de febrero de 2025 (EAF 089/2025)</w:t></w:r><w:r><w:rPr><w:szCs w:val="24"/><w:lang w:val="es-CL"/></w:rPr><w:t>. Santiago de Chile: CEN, 2025.</w:t></w:r></w:p>
<w:p w14:paraId="1FB00325" w14:textId="77777777" w:rsidR="00425537" w:rsidRDefault="00425537"><w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:spacing w:after="240" w:line="240" w:lineRule="auto"/><w:rPr><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr></w:pPr><w:r><w:rPr><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr><w:t xml:space="preserve">GU, Y.; GREEN, T. C. Power System Stability With a High Penetration of Inverter-Based Resources. </w:t></w:r><w:r><w:rPr><w:i/><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr><w:t>Proceedings of the IEEE</w:t></w:r><w:r><w:rPr><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr><w:t>, v. 111, n. 7, p. 832-853, jul. 2023. DOI 10.1109/JPROC.2022.3179826.</w:t></w:r></w:p>
<w:p w14:paraId="1FB00326" w14:textId="77777777" w:rsidR="00425537" w:rsidRDefault="00425537"><w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:spacing w:after="240" w:line="240" w:lineRule="auto"/><w:rPr><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr></w:pPr><w:r><w:rPr><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr><w:t xml:space="preserve">INTERNATIONAL ENERGY AGENCY (IEA). </w:t></w:r><w:r><w:rPr><w:i/><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr><w:t>Global Energy Review 2026: Electricity Demand and Inverter-Based Integration</w:t></w:r><w:r><w:rPr><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr><w:t>. Paris: IEA, 2026.</w:t></w:r></w:p>
<w:p w14:paraId="1FB00327" w14:textId="77777777" w:rsidR="00425537" w:rsidRDefault="00425537"><w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:spacing w:after="240" w:line="240" w:lineRule="auto"/><w:rPr><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr></w:pPr><w:r><w:rPr><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr><w:t xml:space="preserve">KUNDUR, P. et al. Definition and Classification of Power System Stability of IEEE/CIGRE Joint Task Force on Power System Stability. </w:t></w:r><w:r><w:rPr><w:i/><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr><w:t>IEEE Transactions on Power Systems</w:t></w:r><w:r><w:rPr><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr><w:t>, v. 19, n. 3, p. 1387-1401, ago. 2004. DOI 10.1109/TPWRS.2004.825981.</w:t></w:r></w:p>
<w:p w14:paraId="1FB00328" w14:textId="77777777" w:rsidR="00425537" w:rsidRDefault="00425537"><w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:spacing w:after="240" w:line="240" w:lineRule="auto"/><w:rPr><w:szCs w:val="24"/></w:rPr></w:pPr><w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve">OLIVEIRA, B. H.; REZENDE, V. H. A. </w:t></w:r><w:r><w:rPr><w:i/><w:szCs w:val="24"/></w:rPr><w:t>Painel Interativo para Análise Dinâmica e Métricas de Sincronismo do SRF-PLL sob Contingências em Redes Elétricas</w:t></w:r><w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t>. 2026. Repositório no GitHub. Disponível em: &lt;https://github.com/bruno-victor-uerj/pll-stability-dashboard&gt;. Acesso em: 29 out. 2026.</w:t></w:r></w:p>"""

anchor_cigre = "CIGRE. Suitable Classification of Power System Stability Phenomena."
idx_cigre = xml.find(anchor_cigre)
if idx_cigre != -1:
    end_p_cigre = xml.find("</w:p>", idx_cigre) + len("</w:p>")
    xml = xml[:end_p_cigre] + "\n" + novas_referencias + xml[end_p_cigre:]
    print("5 novas referências inseridas com sucesso.")
else:
    print("AVISO: Âncora CIGRE não encontrada para referências.")

# ==============================================================================
# 8. PONTUAÇÃO NAS EQUAÇÕES
# ==============================================================================
pontuacoes = [
    ("Kpd=Vm", "Kpd=Vm."),
    ("θrefs-θPLLs", "θrefs-θPLLs,"),
    ("KpPLL+KiPLLs", "KpPLL+KiPLLs."),
    ("KpdKpPLLs+KiPLLs2", "KpdKpPLLs+KiPLLs2,"),
    ("s2+KpdKpPLLs+KpdKiPLL", "s2+KpdKpPLLs+KpdKiPLL."),
    ("Es=11+Lsθrefs", "Es=11+Lsθrefs,"),
    ("vqs=Kpd11+Lsθrefs", "vqs=Kpd11+Lsθrefs."),
    ("s2+2ξωns+ωn2", "s2+2ξωns+ωn2,"),
    ("KpPLL=2ξωn", "KpPLL=2ξωn."),
    ("KpPLL=9,2ts", "KpPLL=9,2ts."),
    ("1s·Lest", "1s·Lest,"),
    ("s2+KpLests+KiLest=0", "s2+KpLests+KiLest=0."),
    ("Ki=ωn2·Lest", "Ki=ωn2·Lest."),
]

for old_m, new_m in pontuacoes:
    if f"<m:t>{old_m}</m:t>" in xml:
        xml = xml.replace(f"<m:t>{old_m}</m:t>", f"<m:t>{new_m}</m:t>", 1)
    elif old_m in xml:
        xml = xml.replace(old_m, new_m, 1)

print("Pontuação nas equações aplicada.")

# ==============================================================================
# 9. APÊNDICE A: PAINEL INTERATIVO DE ANÁLISE DINÂMICA
# ==============================================================================
apendice_xml = """
<w:p w14:paraId="1FB00330" w14:textId="77777777" w:rsidR="00055498" w:rsidRDefault="00055498" w:rsidP="00055498"><w:pPr><w:pStyle w:val="Ttulo1"/><w:pageBreakBefore/><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:spacing w:after="360"/><w:jc w:val="both"/><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="48"/><w:szCs w:val="48"/></w:rPr></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="48"/><w:szCs w:val="48"/></w:rPr><w:t>APÊNDICE A – PAINEL INTERATIVO DE ANÁLISE DINÂMICA</w:t></w:r></w:p>
<w:p w14:paraId="1FB00331" w14:textId="77777777" w:rsidR="00BE4CBD" w:rsidRDefault="00BE4CBD"><w:pPr><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:szCs w:val="24"/></w:rPr></w:pPr><w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t>Como ferramenta de apoio à análise e visualização dos 28 cenários simulados no MATLAB/Simulink, foi desenvolvido um painel interativo (dashboard) em ambiente web utilizando a linguagem Python e a biblioteca gráfica Plotly. O ecossistema processa os dados transitórios com alta taxa de amostragem exportados em formato CSV, calculando automaticamente as métricas de desempenho do SRF-PLL e de conformidade com os Procedimentos de Rede do ONS.</w:t></w:r></w:p>
<w:p w14:paraId="1FB00332" w14:textId="77777777" w:rsidR="00BE4CBD" w:rsidRDefault="00BE4CBD"><w:pPr><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:szCs w:val="24"/></w:rPr></w:pPr><w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t>A interface gráfica permite a inspeção lado a lado da sintonia nominal e inadequada, a visualização vetorial dos fasores de tensão no referencial síncrono dq, o espectro de frequências de Fourier com isolamento da componente de segunda harmônica (120 Hz) sob faltas assimétricas, e a verificação do cumprimento das rampas de corrente reativa do Submódulo 2.10. A Figura A.1 ilustra a interface de consolidação dos cenários e métricas do painel.</w:t></w:r></w:p>
<w:p w14:paraId="1FB00333" w14:textId="77777777" w:rsidR="00095F51" w:rsidRDefault="00381505"><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="60" w:line="240" w:lineRule="auto"/><w:rPr><w:sz w:val="20"/></w:rPr></w:pPr><w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>Figura A.1 – Interface do painel interativo de métricas e análise dinâmica do SRF-PLL.</w:t></w:r></w:p>
<w:p w14:paraId="1FB00334" w14:textId="77777777" w:rsidR="00381505" w:rsidRDefault="00381505"><w:pPr><w:keepNext/><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:jc w:val="center"/><w:rPr><w:szCs w:val="24"/></w:rPr></w:pPr><w:r><w:rPr><w:noProof/></w:rPr><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0" wp14:anchorId="04A8139C" wp14:editId="3F049AF3"><wp:extent cx="5760720" cy="3240405"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:docPr id="900000048" name="dashboard_apendice"/><wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="910000048" name="dashboard_apendice"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="rId48"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="5760720" cy="3240405"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>
<w:p w14:paraId="1FB00335" w14:textId="77777777" w:rsidR="00095F51" w:rsidRDefault="00381505"><w:pPr><w:spacing w:before="60" w:after="240" w:line="240" w:lineRule="auto"/><w:rPr><w:sz w:val="20"/></w:rPr></w:pPr><w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>Fonte: Os autores (2026).</w:t></w:r></w:p>
<w:p w14:paraId="1FB00336" w14:textId="77777777" w:rsidR="00BE4CBD" w:rsidRDefault="00BE4CBD"><w:pPr><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:szCs w:val="24"/></w:rPr></w:pPr><w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t>O código-fonte completo da plataforma de simulação, os modelos em Simulink, os notebooks analíticos e o visualizador interativo estão hospedados e disponíveis publicamente no repositório do projeto no GitHub: https://github.com/bruno-victor-uerj/pll-stability-dashboard.</w:t></w:r></w:p>
"""

idx_body_close = xml.rfind("</w:body>")
if idx_body_close != -1:
    xml = xml[:idx_body_close] + apendice_xml + "\n" + xml[idx_body_close:]
    print("Apêndice A inserido com sucesso antes do fechamento do corpo.")

# ==============================================================================
# 10. MARCAÇÃO DO TOC COM DIRTY=TRUE
# ==============================================================================
if '<w:fldSimple w:instr="TOC ' in xml:
    xml = xml.replace('<w:fldSimple w:instr="TOC ', '<w:fldSimple w:dirty="true" w:instr="TOC ', 1)
    print("TOC marcado com w:dirty=\"true\" no fldSimple.")
elif 'TOC \\o' in xml:
    xml = re.sub(r'(<w:fldChar w:fldCharType="begin"\/?>)', r'<w:fldChar w:dirty="true" w:fldCharType="begin"/>', xml, count=1)
    print("TOC marcado com dirty no fldChar.")

# ==============================================================================
# 11. VALIDAÇÃO XML E GRAVAÇÃO
# ==============================================================================
try:
    ET.fromstring(xml)
    print("VALIDAÇÃO XML: Sucesso! O XML gerado está perfeitamente bem-formado.")
except Exception as e:
    print(f"ERRO DE XML: {e}")
    sys.exit(1)

with open(DOC_XML, "w", encoding="utf-8") as f:
    f.write(xml)

print(f"Arquivo {DOC_XML} regravado com sucesso ({len(xml)} bytes).")
