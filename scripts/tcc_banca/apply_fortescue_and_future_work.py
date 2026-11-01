# -*- coding: utf-8 -*-
"""
apply_fortescue_and_future_work.py
Aplica as revisões finais da banca aprovadas pelo usuário:
1. Item 2: Teoria de componentes simétricas de Fortescue e inserção da Figura 2.4
   (diagrama de sistemas girantes e projeção no referencial dq) no §2.4, com
   remissão correspondente no §4.3 (FFT de 120 Hz);
2. Item 3: Complemento dos Trabalhos Futuros abordando o compromisso de controle
   de PLLs com filtragem de sequência negativa (injeção de corrente simétrica vs.
   oscilação de 120 Hz em P e Q sob tensão desbalanceada).
Tudo destacado em AZUL (#0070C0) para o Prof. Rafael.
"""

import os
import shutil
import sys
import time
import zipfile

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"C:\Users\gilbr\OneDrive\UERJ\TCC - Victor e Bruno\Template Modelo TCC\01_TCC_Monografia_Final"
CANONICAL_DOCX = os.path.join(BASE_DIR, "TCC_Victor_Bruno_VFinal.docx")
BACKUP_DIR = os.path.join(BASE_DIR, "_backups", "VF")
TEMP_WORK_DIR = r"C:\Temp\tcc_banca\work_fortescue_tf"

PNG_SRC = r"assets\diagrams\fortescue_componentes_srf_pll.png"

print("=" * 80)
print("APLICANDO COMPONENTES SIMÉTRICAS (FIGURA 2.4) E TRABALHOS FUTUROS NO TCC")
print("=" * 80)

# 1. Conferir canônico e imagem
if not os.path.exists(CANONICAL_DOCX):
    print(f"ERRO: Canônico não encontrado: {CANONICAL_DOCX}")
    sys.exit(1)

if not os.path.exists(PNG_SRC):
    print(f"ERRO: Imagem PNG não encontrada: {PNG_SRC}")
    sys.exit(1)

# 2. Criar backup datado
os.makedirs(BACKUP_DIR, exist_ok=True)
timestamp = time.strftime("%Y%m%d_%H%M%S")
pre_backup = os.path.join(BACKUP_DIR, f"TCC_Victor_Bruno_VFinal_backup_pre_fortescue_{timestamp}.docx")
shutil.copyfile(CANONICAL_DOCX, pre_backup)
print(f"1. Backup prévio salvo em:\n   {pre_backup}")

# 3. Descompactar DOCX
if os.path.exists(TEMP_WORK_DIR):
    shutil.rmtree(TEMP_WORK_DIR)
os.makedirs(TEMP_WORK_DIR, exist_ok=True)

with zipfile.ZipFile(CANONICAL_DOCX, 'r') as z:
    z.extractall(TEMP_WORK_DIR)

# 4. Copiar a imagem para word/media/
media_dir = os.path.join(TEMP_WORK_DIR, "word", "media")
os.makedirs(media_dir, exist_ok=True)
dst_png = os.path.join(media_dir, "fortescue_componentes_srf_pll.png")
shutil.copyfile(PNG_SRC, dst_png)
print(f"2. Imagem copiada para:\n   {dst_png}")

# 5. Adicionar relacionamento rId55 em word/_rels/document.xml.rels
rels_path = os.path.join(TEMP_WORK_DIR, "word", "_rels", "document.xml.rels")
with open(rels_path, "r", encoding="utf-8") as f:
    rels_xml = f.read()

if 'Target="media/fortescue_componentes_srf_pll.png"' not in rels_xml:
    new_rel_entry = '  <Relationship Id="rId55" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fortescue_componentes_srf_pll.png"/>\n</Relationships>'
    rels_xml = rels_xml.replace('</Relationships>', new_rel_entry)
    with open(rels_path, "w", encoding="utf-8") as f:
        f.write(rels_xml)
    print("3. Relacionamento rId55 adicionado em document.xml.rels com sucesso.")
else:
    print("3. Relacionamento rId55 já existente em document.xml.rels.")

# 6. Carregar word/document.xml
doc_xml_path = os.path.join(TEMP_WORK_DIR, "word", "document.xml")
with open(doc_xml_path, "r", encoding="utf-8") as f:
    xml = f.read()

print(f"4. word/document.xml carregado ({len(xml)} bytes).")

# ==============================================================================
# TAREFA A: Inserir a Teoria de Componentes Simétricas e Figura 2.4 no §2.4
# ==============================================================================
# O parágrafo P533 termina a Seção 2.4:
# "Esse é o mecanismo investigado nas seções de modelagem e de resultados."
p533_needle = 'Esse é o mecanismo investigado nas seções de modelagem e de resultados.</w:t></w:r></w:p>'

if p533_needle not in xml:
    print("ERRO: Parágrafo P533 não encontrado no XML!")
    sys.exit(1)

# Novo texto explicativo das componentes simétricas e sistema girante
# Bloco XML contendo:
# - Parágrafo explicativo da teoria de Fortescue e batimento de 120 Hz no referencial dq
# - Parágrafo de legenda da Figura 2.4
# - Parágrafo com o drawing (imagem rId55)
# - Parágrafo da fonte
fortescue_xml_block = (
    p533_needle +
    # Parágrafo 1: Teoria de Fortescue e projeção em dq
    '<w:p w14:paraId="5FAF0204" w14:textId="77777777" w:rsidR="009855DD" w:rsidRDefault="009855DD">'
    '<w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:color w:val="0070C0"/><w:szCs w:val="24"/></w:rPr></w:pPr>'
    '<w:r><w:rPr><w:color w:val="0070C0"/><w:szCs w:val="24"/></w:rPr>'
    '<w:t xml:space="preserve">Essa vulnerabilidade decorre da hipótese fundamental do SRF-PLL, concebido estritamente para sistemas trifásicos equilibrados (sequência positiva pura). Diante de contingências assimétricas na rede, o teorema das componentes simétricas de Fortescue estabelece a decomposição das tensões trifásicas em sistemas desacoplados de sequência positiva (v⁺), negativa (v⁻) e zero (v⁰). Enquanto o fasor de sequência positiva gira no sentido anti-horário com velocidade angular síncrona +ω₀ (60 Hz), o fasor de sequência negativa apresenta rotação reversa no sentido horário a −ω₀ devido à inversão da sequência de fases (a-c-b). Como a Transformada de Park empregada no SRF-PLL acompanha o vetor de sequência positiva com velocidade +ω₀, a componente de sequência negativa é observada pelo referencial síncrono dq com velocidade angular relativa de Δω = ω₀ − (−ω₀) = 2ω₀ (120 Hz). Essa rotação relativa projeta uma oscilação senoidal permanente de segunda harmônica sobre as componentes vd e vq. Como a malha do PLL utiliza a condição vq = 0 como sinal de erro angular, o compensador PI interpreta a oscilação de 120 Hz como perturbação de fase, propagando ondulações à frequência estimada ωPLL e ao ângulo θPLL. O diagrama da Figura 2.4 ilustra a rotação dos sistemas fasoriais e a resultante oscilatória no plano direto-quadratura.</w:t>'
    '</w:r></w:p>'
    # Parágrafo 2: Legenda Figura 2.4
    '<w:p w14:paraId="5FAF0205" w14:textId="77777777" w:rsidR="00F4703F" w:rsidRDefault="008B0D95">'
    '<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="60" w:line="240" w:lineRule="auto"/><w:rPr><w:color w:val="0070C0"/><w:sz w:val="20"/></w:rPr></w:pPr>'
    '<w:bookmarkStart w:id="191" w:name="_Toc_Figura_2_4"/>'
    '<w:r><w:rPr><w:color w:val="0070C0"/><w:sz w:val="20"/></w:rPr><w:t>Figura 2.</w:t></w:r>'
    '<w:r><w:rPr><w:color w:val="0070C0"/><w:sz w:val="20"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
    '<w:r><w:rPr><w:color w:val="0070C0"/><w:sz w:val="20"/></w:rPr><w:instrText xml:space="preserve"> SEQ Figura \* ARABIC \s 1 </w:instrText></w:r>'
    '<w:r><w:rPr><w:color w:val="0070C0"/><w:sz w:val="20"/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>'
    '<w:r><w:rPr><w:noProof/><w:color w:val="0070C0"/><w:sz w:val="20"/></w:rPr><w:t>4</w:t></w:r>'
    '<w:r><w:rPr><w:color w:val="0070C0"/><w:sz w:val="20"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>'
    '<w:r><w:rPr><w:color w:val="0070C0"/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve"> – Decomposição em componentes simétricas e projeção da oscilação de 120 Hz no referencial dq.</w:t></w:r>'
    '<w:bookmarkEnd w:id="191"/>'
    '</w:p>'
    # Parágrafo 3: Imagem (Drawing rId55)
    '<w:p w14:paraId="5FAF0207" w14:textId="77777777" w:rsidR="00055498" w:rsidRDefault="00931A4F">'
    '<w:pPr><w:keepNext/><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:jc w:val="center"/></w:pPr>'
    '<w:r><w:rPr><w:noProof/><w:color w:val="1B1C1D"/><w:szCs w:val="24"/></w:rPr>'
    '<w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0" wp14:anchorId="25C1A35C" wp14:editId="4026E5F4">'
    '<wp:extent cx="5760000" cy="2419200"/>'
    '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
    '<wp:docPr id="484168859" name="Imagem 4" descr="Decomposição em componentes simétricas e projeção no referencial dq"/>'
    '<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
    '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
    '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
    '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
    '<pic:nvPicPr><pic:cNvPr id="0" name="Picture 4" descr="Componentes simétricas"/><pic:cNvPicPr><a:picLocks noChangeAspect="1" noChangeArrowheads="1"/></pic:cNvPicPr></pic:nvPicPr>'
    '<pic:blipFill><a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="rId55" cstate="print">'
    '<a:extLst><a:ext uri="{28A0092B-C50C-407E-A947-70E740481C1C}"><a14:useLocalDpi xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main" val="0"/></a:ext></a:extLst>'
    '</a:blip><a:srcRect/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
    '<pic:spPr bwMode="auto"><a:xfrm><a:off x="0" y="0"/><a:ext cx="5760000" cy="2419200"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></pic:spPr>'
    '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing>'
    '</w:r></w:p>'
    # Parágrafo 4: Fonte
    '<w:p w14:paraId="5FAF0208" w14:textId="77777777" w:rsidR="00F4703F" w:rsidRDefault="008B0D95">'
    '<w:pPr><w:spacing w:before="60" w:after="240" w:line="240" w:lineRule="auto"/><w:rPr><w:color w:val="0070C0"/><w:sz w:val="20"/></w:rPr></w:pPr>'
    '<w:r><w:rPr><w:color w:val="0070C0"/><w:sz w:val="20"/></w:rPr><w:t>Fonte: Os autores (2026).</w:t></w:r>'
    '</w:p>'
)

xml = xml.replace(p533_needle, fortescue_xml_block, 1)
print("5. Teoria de Fortescue e Figura 2.4 inseridas na Seção 2.4 em AZUL (#0070C0).")

# ==============================================================================
# TAREFA B: Inserir a Figura 2.4 na Lista de Ilustrações (após Figura 2.3)
# ==============================================================================
toc_needle = 'Figura 2.3 – Diagrama de blocos funcionais do SRF-PLL.</w:t></w:r>'
pos_toc = xml.find(toc_needle)
if pos_toc != -1:
    pos_p_end = xml.find('</w:p>', pos_toc) + 6
    toc_fig24_entry = (
        '<w:p w14:paraId="5FAF0162" w14:textId="77777777" w:rsidR="00BE6084" w:rsidRDefault="00000000">'
        '<w:pPr><w:pStyle w:val="ndicedeilustraes"/><w:rPr><w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorEastAsia" w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi"/><w:noProof/><w:kern w:val="2"/><w:szCs w:val="24"/><w14:ligatures w14:val="standardContextual"/></w:rPr></w:pPr>'
        '<w:hyperlink w:anchor="_Toc_Figura_2_4" w:history="1">'
        '<w:r w:rsidR="00BE6084" w:rsidRPr="00405CBB"><w:rPr><w:rStyle w:val="Hyperlink"/><w:noProof/></w:rPr><w:t>Figura 2.4 – Decomposição em componentes simétricas e projeção da oscilação de 120 Hz no referencial dq.</w:t></w:r>'
        '<w:r w:rsidR="00BE6084"><w:rPr><w:noProof/><w:webHidden/></w:rPr><w:tab/></w:r>'
        '<w:r w:rsidR="00BE6084"><w:rPr><w:noProof/><w:webHidden/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
        '<w:r w:rsidR="00BE6084"><w:rPr><w:noProof/><w:webHidden/></w:rPr><w:instrText xml:space="preserve"> PAGEREF _Toc_Figura_2_4 \h </w:instrText></w:r>'
        '<w:r w:rsidR="00BE6084"><w:rPr><w:noProof/><w:webHidden/></w:rPr></w:r>'
        '<w:r w:rsidR="00BE6084"><w:rPr><w:noProof/><w:webHidden/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>'
        '<w:r w:rsidR="00BE6084"><w:rPr><w:noProof/><w:webHidden/></w:rPr><w:t>47</w:t></w:r>'
        '<w:r w:rsidR="00BE6084"><w:rPr><w:noProof/><w:webHidden/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>'
        '</w:hyperlink></w:p>'
    )
    xml = xml[:pos_p_end] + toc_fig24_entry + xml[pos_p_end:]
    print("6. Figura 2.4 adicionada à Lista de Ilustrações com sucesso.")
else:
    print("AVISO: Ponto da Figura 2.3 na Lista de Ilustrações não encontrado exatamente.")

# ==============================================================================
# TAREFA C: Amarrar o mecanismo no §4.3 (FFT de 120 Hz, P716)
# ==============================================================================
# No §4.3, o parágrafo termina com:
# "a sequência negativa é refletida no referencial síncrono como uma oscilação de frequência dupla, superposta às componentes contínuas de eixo direto e de quadratura.</w:t></w:r></w:p>"
p716_needle = 'a sequência negativa é refletida no referencial síncrono como uma oscilação de frequência dupla, superposta às componentes contínuas de eixo direto e de quadratura.</w:t></w:r></w:p>'

if p716_needle in xml:
    p716_replacement = (
        'a sequência negativa é refletida no referencial síncrono como uma oscilação de frequência dupla, superposta às componentes contínuas de eixo direto e de quadratura.</w:t></w:r>'
        '<w:r><w:rPr><w:color w:val="0070C0"/><w:szCs w:val="24"/></w:rPr>'
        '<w:t xml:space="preserve"> Conforme fundamentado na Seção 2.4 e ilustrado no sistema girante da Figura 2.4, essa expressiva raia de 120 Hz observada no espectro é a manifestação física direta da velocidade relativa de 2ω₀ induzida pela componente de sequência negativa sobre o referencial síncrono dq do SRF-PLL.</w:t></w:r>'
        '</w:p>'
    )
    xml = xml.replace(p716_needle, p716_replacement, 1)
    print("7. Seção 4.3 (§4.3) atualizada com remissão direta à Figura 2.4 em AZUL (#0070C0).")
else:
    print("AVISO: Parágrafo P716 no §4.3 não encontrado exatamente.")

# ==============================================================================
# TAREFA D: Complemento dos Trabalhos Futuros (§6.1, P844)
# ==============================================================================
# P844 termina com:
# "medir quanto se ganha em imunidade e quanto se perde em tempo de retomada do sincronismo.</w:t></w:r></w:p>"
p844_needle = 'medir quanto se ganha em imunidade e quanto se perde em tempo de retomada do sincronismo.</w:t></w:r></w:p>'

if p844_needle in xml:
    p844_replacement = (
        'medir quanto se ganha em imunidade e quanto se perde em tempo de retomada do sincronismo.</w:t></w:r>'
        '<w:r><w:rPr><w:color w:val="0070C0"/><w:szCs w:val="24"/></w:rPr>'
        '<w:t xml:space="preserve"> Cumpre notar, contudo, que a utilização de técnicas com filtragem de sequência negativa para a injeção de correntes puramente equilibradas impõe um compromisso operacional: sob tensões desbalanceadas no ponto de acoplamento, correntes simétricas resultam inevitavelmente em potências ativa e reativa oscilantes a 120 Hz, o que pode estressar o barramento CC e a estabilidade da malha. Sugere-se, portanto, investigar em trabalhos futuros o balanço sistêmico entre a simetria de correntes injetadas e a oscilação das potências sob contingências severas.</w:t></w:r>'
        '</w:p>'
    )
    xml = xml.replace(p844_needle, p844_replacement, 1)
    print("8. Trabalhos Futuros (§6.1) atualizado com o compromisso de correntes simétricas vs. potências oscilantes em AZUL (#0070C0).")
else:
    print("AVISO: Parágrafo P844 nos Trabalhos Futuros não encontrado exatamente.")

# 7. Gravar document.xml
with open(doc_xml_path, "w", encoding="utf-8") as f:
    f.write(xml)

print(f"9. word/document.xml gravado ({len(xml)} bytes).")

# 8. Reempacotar DOCX
output_docx = os.path.join(TEMP_WORK_DIR, "repacked.docx")
with zipfile.ZipFile(output_docx, 'w', compression=zipfile.ZIP_DEFLATED) as zip_out:
    for foldername, subfolders, filenames in os.walk(TEMP_WORK_DIR):
        for filename in filenames:
            if filename == "repacked.docx":
                continue
            filepath = os.path.join(foldername, filename)
            arcname = os.path.relpath(filepath, TEMP_WORK_DIR)
            zip_out.write(filepath, arcname)

print(f"10. DOCX reempacotado com sucesso ({os.path.getsize(output_docx)} bytes).")

# 9. Atualizar arquivo canônico
shutil.copyfile(output_docx, CANONICAL_DOCX)
print(f"11. Canônico atualizado com sucesso:\n    {CANONICAL_DOCX}")

# 10. Backup pós-modificação
post_backup = os.path.join(BACKUP_DIR, f"TCC_Victor_Bruno_VFinal_backup_{timestamp}.docx")
shutil.copyfile(CANONICAL_DOCX, post_backup)
print(f"12. Backup datado oficial pós-modificação gravado:\n    {post_backup}")

print("=" * 80)
print("OPERAÇÃO CONCLUÍDA COM SUCESSO!")
print("=" * 80)
