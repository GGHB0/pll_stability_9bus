# -*- coding: utf-8 -*-
import zipfile
import re
import os
import shutil
import xml.etree.ElementTree as ET

ONEDRIVE_FILE = r"C:\Users\gilbr\OneDrive\UERJ\TCC - Victor e Bruno\Template Modelo TCC\01_TCC_Monografia_Final\TCC_Victor_Bruno_VFinal.docx"
TEMP_DIR = r"C:\Temp\tcc_banca\cleiton_red_work"

with zipfile.ZipFile(ONEDRIVE_FILE, 'r') as z:
    z.extractall(TEMP_DIR)

DOC_XML = os.path.join(TEMP_DIR, "word", "document.xml")
with open(DOC_XML, "r", encoding="utf-8") as f:
    xml = f.read()

# 1. Heading Trabalhos Futuros (5E98674D)
pos_tf = xml.find('paraId="5E98674D"')
if pos_tf != -1:
    start_p = xml.rfind('<w:p ', 0, pos_tf)
    end_p = xml.find('</w:p>', pos_tf) + 6
    p_slice = xml[start_p:end_p]
    p_red = p_slice.replace(
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="36"/><w:szCs w:val="36"/><w:lang w:val="pt-BR"/></w:rPr>',
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="FF0000"/><w:sz w:val="36"/><w:szCs w:val="36"/><w:lang w:val="pt-BR"/></w:rPr>'
    )
    xml = xml[:start_p] + p_red + xml[end_p:]
    print("1. Heading Trabalhos Futuros formatado em VERMELHO.")

# 2. German System Stability Roadmap e Strauss-Mincu (55BEC2C4)
target_road = "German System Stability Roadmap, este último formulado para subsidiar a transição da rede alemã rumo a uma operação segura sob 100% de geração renovável até 2030 (STRAUSS-MINCU et al., 2026)"
if target_road in xml:
    red_road = (
        '</w:t></w:r>'
        '<w:r><w:rPr><w:i/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t>German System Stability Roadmap</w:t></w:r>'
        '<w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve">, este último formulado para subsidiar a transição da rede alemã rumo a uma operação segura sob 100% de geração renovável até 2030 (STRAUSS-MINCU et al., 2026)</w:t></w:r>'
        '<w:r w:rsidRPr="00D575EC"><w:rPr><w:color w:val="1B1C1D"/><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve">'
    )
    xml = xml.replace(target_road, red_road, 1)
    print("2. German System Stability Roadmap e Strauss-Mincu formatados em VERMELHO.")

# Validação XML
ET.fromstring(xml)
print("Validação XML: 100% válida!")

with open(DOC_XML, "w", encoding="utf-8") as f:
    f.write(xml)

temp_zip = os.path.join(TEMP_DIR, "..", "tcc_final_red2.docx")
if os.path.exists(temp_zip):
    os.remove(temp_zip)

with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zip_out:
    for foldername, subfolders, filenames in os.walk(TEMP_DIR):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            arcname = os.path.relpath(filepath, TEMP_DIR)
            zip_out.write(filepath, arcname)

shutil.copyfile(temp_zip, ONEDRIVE_FILE)
shutil.copyfile(temp_zip, r"C:\Temp\tcc_banca\tcc_final.docx")
print("Arquivo canônico atualizado com sucesso no OneDrive.")

