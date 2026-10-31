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

def apply_red_to_run(run_xml):
    if '<w:rPr>' in run_xml:
        if '<w:color ' in run_xml:
            return re.sub(r'<w:color [^>]*/>', '<w:color w:val="FF0000"/>', run_xml)
        else:
            return run_xml.replace('<w:rPr>', '<w:rPr><w:color w:val="FF0000"/>', 1)
    else:
        return re.sub(r'(<w:r(?: [^>]*)?>)', r'\1<w:rPr><w:color w:val="FF0000"/></w:rPr>', run_xml, count=1)

def apply_red_to_all_runs_in_paragraph(p_xml):
    if '<w:pPr>' in p_xml:
        idx_pPr_end = p_xml.find('</w:pPr>')
        pPr_part = p_xml[:idx_pPr_end + 8]
        rest_part = p_xml[len(pPr_part):]
        if '<w:rPr>' in pPr_part:
            if '<w:color ' in pPr_part:
                pPr_part = re.sub(r'<w:color [^>]*/>', '<w:color w:val="FF0000"/>', pPr_part)
            else:
                pPr_part = pPr_part.replace('<w:rPr>', '<w:rPr><w:color w:val="FF0000"/>', 1)
        else:
            pPr_part = pPr_part.replace('</w:pPr>', '<w:rPr><w:color w:val="FF0000"/></w:rPr></w:pPr>', 1)
        p_xml = pPr_part + rest_part
    
    p_xml = re.sub(r'<w:r(?: [^>]*)?>.*?</w:r>', lambda m: apply_red_to_run(m.group(0)), p_xml, flags=re.DOTALL)
    return p_xml

# 1. HEADINGS (INTRODUÇÃO, 1, 2, 3, 4, CONCLUSÃO, Trabalhos Futuros)
# Procuramos os parágrafos que contêm Ttulo1 ou Ttulo2 e o texto exato
primary_headings = [
    "INTRODUÇÃO",
    "1  DESAFIOS À ESTABILIDADE EM REDES DOMINADAS POR INVERSORES",
    "2  GERAÇÃO CONECTADA À REDE POR INVERSORES: FUNDAMENTAÇÃO TEÓRICA",
    "3  METODOLOGIA DE ANÁLISE",
    "4  ANÁLISE E DISCUSSÃO DE RESULTADOS",
    "CONCLUSÃO",
    "Trabalhos Futuros",
    "2.3.2. Arquitetura de Controle Baseada em Corrente",
    "APÊNDICE A – PAINEL INTERATIVO DE ANÁLISE DINÂMICA",
    "B. Sequência de Telas do Modo Apresentação no Texto"
]

for h in primary_headings:
    # Apenas ocorrências fora do sumário (após posição 180000)
    pos = xml.find(h, 180000)
    if pos != -1:
        start_p = xml.rfind('<w:p ', 0, pos)
        end_p = xml.find('</w:p>', pos) + 6
        p_slice = xml[start_p:end_p]
        if 'FF0000' not in p_slice.upper():
            p_red = apply_red_to_all_runs_in_paragraph(p_slice)
            xml = xml[:start_p] + p_red + xml[end_p:]
            print(f"Heading '{h}' formatado em VERMELHO.")
        else:
            print(f"Heading '{h}' já estava em VERMELHO.")
    else:
        print(f"AVISO: Heading '{h}' não encontrado após pos 180000.")

# 2. CEN (2025)
pos_cen = xml.find("COORDINADOR ELÉCTRICO NACIONAL", 700000)
if pos_cen != -1:
    start_p = xml.rfind('<w:p ', 0, pos_cen)
    end_p = xml.find('</w:p>', pos_cen) + 6
    p_slice = xml[start_p:end_p]
    if 'FF0000' not in p_slice.upper():
        p_red = apply_red_to_all_runs_in_paragraph(p_slice)
        xml = xml[:start_p] + p_red + xml[end_p:]
        print("Ref CEN (2025) formatada em VERMELHO.")

# 3. Legenda da Figura 2.2
pos_fig22 = xml.find("Diagrama de blocos do controle de corrente no referencial dq", 400000)
if pos_fig22 != -1:
    start_p = xml.rfind('<w:p ', 0, pos_fig22)
    end_p = xml.find('</w:p>', pos_fig22) + 6
    p_slice = xml[start_p:end_p]
    if 'FF0000' not in p_slice.upper():
        p_red = apply_red_to_all_runs_in_paragraph(p_slice)
        xml = xml[:start_p] + p_red + xml[end_p:]
        print("Legenda Figura 2.2 formatada em VERMELHO.")

# 4. Fonte da Figura 3.3
pos_f33 = xml.find("Fonte: Adaptado de ONS (2022).", 500000)
if pos_f33 != -1:
    start_p = xml.rfind('<w:p ', 0, pos_f33)
    end_p = xml.find('</w:p>', pos_f33) + 6
    p_slice = xml[start_p:end_p]
    if 'FF0000' not in p_slice.upper():
        p_red = apply_red_to_all_runs_in_paragraph(p_slice)
        xml = xml[:start_p] + p_red + xml[end_p:]
        print("Fonte da Figura 3.3 formatada em VERMELHO.")

# 5. Legenda da Figura 3.4
pos_f34 = xml.find("Diagrama conceitual do SRF-PLL", 500000)
if pos_f34 != -1:
    start_p = xml.rfind('<w:p ', 0, pos_f34)
    end_p = xml.find('</w:p>', pos_f34) + 6
    p_slice = xml[start_p:end_p]
    if 'FF0000' not in p_slice.upper():
        p_red = apply_red_to_all_runs_in_paragraph(p_slice)
        xml = xml[:start_p] + p_red + xml[end_p:]
        print("Legenda da Figura 3.4 formatada em VERMELHO.")

# Validação XML
ET.fromstring(xml)
print("Validação XML: OK!")

with open(DOC_XML, "w", encoding="utf-8") as f:
    f.write(xml)

temp_zip = os.path.join(TEMP_DIR, "..", "tcc_final_red.docx")
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
print("Arquivo canônico regravado com sucesso.")

