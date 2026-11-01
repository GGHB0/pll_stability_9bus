# -*- coding: utf-8 -*-
"""
apply_ons_equation.py
Promove o backup do Victor (20261101_042452) para a versão canônica e
converte a restrição de corrente ativa do ONS (Submódulo 2.10) de pseudo-código
inline para uma equação matemática formal numerada (3.1), renumerando
a equação subsequente da teoria p-q (Akagi) de (3.1) para (3.2).
"""

import os
import shutil
import sys
import time
import zipfile
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"C:\Users\gilbr\OneDrive\UERJ\TCC - Victor e Bruno\Template Modelo TCC\01_TCC_Monografia_Final"
CANONICAL_DOCX = os.path.join(BASE_DIR, "TCC_Victor_Bruno_VFinal.docx")
VICTOR_BACKUP = os.path.join(BASE_DIR, "_backups", "VF", "TCC_Victor_Bruno_VFinal_backup_20261101_042452.docx")
TEMP_WORK_DIR = r"C:\Temp\tcc_banca\work_promove_equacao_ons"

print("=" * 80)
print("PROMOVENDO BACKUP DO VICTOR E CONVERTENDO FÓRMULA ONS EM EQUAÇÃO (3.1)")
print("=" * 80)

# 1. Conferir arquivos
if not os.path.exists(VICTOR_BACKUP):
    print(f"ERRO: Backup do Victor não encontrado: {VICTOR_BACKUP}")
    sys.exit(1)

# 2. Fazer backup prévio do canônico atual antes de promover
bk_dir = os.path.join(BASE_DIR, "_backups", "VF")
os.makedirs(bk_dir, exist_ok=True)
timestamp = time.strftime("%Y%m%d_%H%M%S")
pre_backup = os.path.join(bk_dir, f"TCC_Victor_Bruno_VFinal_backup_pre_promocao_{timestamp}.docx")
if os.path.exists(CANONICAL_DOCX):
    shutil.copyfile(CANONICAL_DOCX, pre_backup)
    print(f"1. Backup de segurança do canônico atual gravado:\n   {pre_backup}")

# 3. Descompactar a versão do Victor (ponto de partida com 100% das revisões)
if os.path.exists(TEMP_WORK_DIR):
    shutil.rmtree(TEMP_WORK_DIR)
os.makedirs(TEMP_WORK_DIR, exist_ok=True)

with zipfile.ZipFile(VICTOR_BACKUP, 'r') as z:
    z.extractall(TEMP_WORK_DIR)

doc_xml_path = os.path.join(TEMP_WORK_DIR, "word", "document.xml")
with open(doc_xml_path, "r", encoding="utf-8") as f:
    xml = f.read()

print(f"2. document.xml carregado ({len(xml)} bytes).")

# 4. Substituição do parágrafo P#574 e inserção da tabela da Equação (3.1)
# Texto original:
# Para atender aos Procedimentos de Rede do ONS (Submódulo 2.10, Figura 3.3), a corrente reativa de suporte tem prioridade térmica sobre a ativa, saturando em 1,0 pu para V &lt; 0,5 pu. A corrente ativa remanescente segue a restrição id,ref = min(1.0, sqrt(Imax² - iq,ref²)), anulando-se durante faltas severas para priorizar a sustentação de tensão da rede.

old_p_text = (
    '<w:p w14:paraId="2914F3AD" w14:textId="77777777" w:rsidR="00381505" w:rsidRDefault="00381505">'
    '<w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr></w:pPr>'
    '<w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr>'
    '<w:t>Para atender aos Procedimentos de Rede do ONS (Submódulo 2.10, Figura 3.3), a corrente reativa de suporte tem prioridade térmica sobre a ativa, saturando em 1,0 pu para V &lt; 0,5 pu. A corrente ativa remanescente segue a restrição id,ref = min(1.0, sqrt(Imax² - iq,ref²)), anulando-se durante faltas severas para priorizar a sustentação de tensão da rede.</w:t>'
    '</w:r></w:p>'
)

if old_p_text not in xml:
    print("ERRO: Parágrafo P#574 exato não encontrado!")
    sys.exit(1)

# Novo parágrafo de texto (introduzindo a Equação 3.1)
new_p_text = (
    '<w:p w14:paraId="2914F3AD" w14:textId="77777777" w:rsidR="00381505" w:rsidRDefault="00381505">'
    '<w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr></w:pPr>'
    '<w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr>'
    '<w:t>Para atender aos Procedimentos de Rede do ONS (Submódulo 2.10, Figura 3.3), a corrente reativa de suporte tem prioridade térmica sobre a ativa, saturando em 1,0 pu para V &lt; 0,5 pu. A corrente ativa remanescente segue a restrição estabelecida na Equação (3.1), anulando-se durante faltas severas para priorizar a sustentação de tensão da rede:</w:t>'
    '</w:r></w:p>'
)

# Tabela sem bordas com a Equação (3.1) em OMML
eq31_table = (
    '<w:tbl>'
    '<w:tblPr>'
    '<w:tblW w:w="9072" w:type="dxa"/>'
    '<w:tblBorders>'
    '<w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/>'
    '</w:tblBorders>'
    '<w:tblLayout w:type="fixed"/>'
    '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
    '</w:tblPr>'
    '<w:tblGrid><w:gridCol w:w="7087"/><w:gridCol w:w="1985"/></w:tblGrid>'
    '<w:tr w:rsidR="00381505" w14:paraId="3A14F3AE" w14:textId="77777777">'
    '<w:tc>'
    '<w:tcPr><w:tcW w:w="7087" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
    '<w:p w14:paraId="4B25F4BF" w14:textId="77777777" w:rsidR="00381505" w:rsidRDefault="00381505">'
    '<w:pPr><w:spacing w:before="120" w:after="120"/><w:jc w:val="center"/><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr></w:pPr>'
    '<m:oMathPara>'
    '<m:oMath>'
    '<m:sSub>'
    '<m:sSubPr><m:ctrlPr><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:i/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr></m:ctrlPr></m:sSubPr>'
    '<m:e><m:r><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><m:t>i</m:t></m:r></m:e>'
    '<m:sub><m:r><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><m:t>d,ref</m:t></m:r></m:sub>'
    '</m:sSub>'
    '<m:r><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><m:t>=min</m:t></m:r>'
    '<m:d>'
    '<m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/><m:ctrlPr><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr></m:ctrlPr></m:dPr>'
    '<m:e>'
    '<m:r><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><m:t>1,0;&#160;</m:t></m:r>'
    '<m:rad>'
    '<m:radPr><m:degHide m:val="1"/><m:ctrlPr><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr></m:ctrlPr></m:radPr>'
    '<m:deg><m:ctrlPr><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:i/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr></m:ctrlPr></m:deg>'
    '<m:e>'
    '<m:sSubSup>'
    '<m:sSubSupPr><m:ctrlPr><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:i/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr></m:ctrlPr></m:sSubSupPr>'
    '<m:e><m:r><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><m:t>I</m:t></m:r></m:e>'
    '<m:sub><m:r><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><m:t>max</m:t></m:r></m:sub>'
    '<m:sup><m:r><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><m:t>2</m:t></m:r></m:sup>'
    '</m:sSubSup>'
    '<m:r><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><m:t>-</m:t></m:r>'
    '<m:sSubSup>'
    '<m:sSubSupPr><m:ctrlPr><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:i/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr></m:ctrlPr></m:sSubSupPr>'
    '<m:e><m:r><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><m:t>i</m:t></m:r></m:e>'
    '<m:sub><m:r><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><m:t>q,ref</m:t></m:r></m:sub>'
    '<m:sup><m:r><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><m:t>2</m:t></m:r></m:sup>'
    '</m:sSubSup>'
    '</m:e>'
    '</m:rad>'
    '</m:e>'
    '</m:d>'
    '<m:r><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><m:t>,</m:t></m:r>'
    '</m:oMath>'
    '</m:oMathPara>'
    '</w:p>'
    '</w:tc>'
    '<w:tc>'
    '<w:tcPr><w:tcW w:w="1985" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
    '<w:p w14:paraId="5C36F5D0" w14:textId="77777777" w:rsidR="00381505" w:rsidRDefault="00381505">'
    '<w:pPr><w:jc w:val="right"/><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr></w:pPr>'
    '<w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t>(3.1)</w:t></w:r>'
    '</w:p>'
    '</w:tc>'
    '</w:tr>'
    '</w:tbl>'
)

xml = xml.replace(old_p_text, new_p_text + eq31_table)
print("3. Parágrafo P#574 atualizado e Equação (3.1) inserida.")

# 5. Renumeração da equação Akagi de (3.1) para (3.2)
# Menção no texto:
old_akagi_mention = "conforme a Equação (3.1):"
new_akagi_mention = "conforme a Equação (3.2):"

if old_akagi_mention not in xml:
    print("ERRO: Menção à Equação (3.1) no texto de Akagi não encontrada!")
    sys.exit(1)

xml = xml.replace(old_akagi_mention, new_akagi_mention)

# Rótulo na tabela de Akagi:
old_akagi_label = '<w:p w14:paraId="651A60DB" w14:textId="77777777" w:rsidR="00DC4EFB" w:rsidRDefault="001452AF"><w:pPr><w:jc w:val="right"/><w:rPr><w:szCs w:val="24"/></w:rPr></w:pPr><w:r><w:rPr><w:color w:val="0070C0"/><w:szCs w:val="24"/></w:rPr><w:t>(3.1)</w:t></w:r></w:p>'
new_akagi_label = '<w:p w14:paraId="651A60DB" w14:textId="77777777" w:rsidR="00DC4EFB" w:rsidRDefault="001452AF"><w:pPr><w:jc w:val="right"/><w:rPr><w:szCs w:val="24"/></w:rPr></w:pPr><w:r><w:rPr><w:color w:val="0070C0"/><w:szCs w:val="24"/></w:rPr><w:t>(3.2)</w:t></w:r></w:p>'

if old_akagi_label not in xml:
    print("ERRO: Rótulo da Equação (3.1) na tabela de Akagi não encontrado!")
    sys.exit(1)

xml = xml.replace(old_akagi_label, new_akagi_label)
print("4. Equação de Akagi renumerada com sucesso: (3.1) -> (3.2).")

# 6. Validação estrita do XML
try:
    ET.fromstring(xml)
    print("5. Validação XML: Sucesso! Estrutura 100% íntegra.")
except Exception as e:
    print(f"ERRO DE XML: {e}")
    sys.exit(1)

with open(doc_xml_path, "w", encoding="utf-8") as f:
    f.write(xml)

# 7. Reempacotar
temp_output_docx = os.path.join(TEMP_WORK_DIR, "..", "tcc_promovido_com_equacao.docx")
if os.path.exists(temp_output_docx):
    os.remove(temp_output_docx)

with zipfile.ZipFile(temp_output_docx, 'w', zipfile.ZIP_DEFLATED) as zout:
    for foldername, subfolders, filenames in os.walk(TEMP_WORK_DIR):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            arcname = os.path.relpath(filepath, TEMP_WORK_DIR)
            zout.write(filepath, arcname)

# 8. Gravar backup oficial pós-equação e atualizar o Canônico no OneDrive
pos_backup = os.path.join(bk_dir, f"TCC_Victor_Bruno_VFinal_backup_{timestamp}.docx")
shutil.copyfile(temp_output_docx, pos_backup)
shutil.copyfile(temp_output_docx, CANONICAL_DOCX)

print(f"6. Backup oficial gravado:\n   {pos_backup} ({os.path.getsize(pos_backup)} bytes)")
print(f"7. Arquivo canônico promovido e atualizado com sucesso:\n   {CANONICAL_DOCX} ({os.path.getsize(CANONICAL_DOCX)} bytes)")
print("=" * 80)
print("PROMOÇÃO E FORMATAÇÃO DA EQUAÇÃO CONCLUÍDAS COM SUCESSO!")
print("=" * 80)

