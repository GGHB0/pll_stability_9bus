# -*- coding: utf-8 -*-
"""
apply_eq_punct_and_fig34.py
1. Aplica pontuacao correta (. e ,) em VERMELHO (#FF0000) no final das equacoes (3.1) a (3.23);
2. Atualiza a legenda da Figura conceitual do PLL (paraId="19FE71A9") para Figura 3.4 em VERMELHO;
3. Reempacota e atualiza o arquivo canonico no OneDrive e backup local.
"""

import os
import re
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ONEDRIVE_FILE = r"C:\Users\gilbr\OneDrive\UERJ\TCC - Victor e Bruno\Template Modelo TCC\01_TCC_Monografia_Final\TCC_Victor_Bruno_VFinal.docx"
TEMP_DIR = r"C:\Temp\tcc_banca\cleiton_red_work"

print("Lendo document.xml...")
DOC_XML = os.path.join(TEMP_DIR, "word", "document.xml")
with open(DOC_XML, "r", encoding="utf-8") as f:
    xml = f.read()

# 1. PONTUAÇÃO NAS EQUAÇÕES (3.1) a (3.23)
eq_punct = {
    1: ",",
    2: ",",
    3: ".",
    4: ",",
    5: ",",
    6: ",",
    7: ".",
    8: ",",
    9: ".",
    10: ".",
    11: ",",
    12: ".",
    13: ",",
    14: ",",
    15: ".",
    16: ",",
    17: ".",
    18: ",",
    19: ".",
    20: ".",
    21: ",",
    22: ".",
    23: "."
}

def punct_repl(m):
    full_row = m.group(0)
    num = int(m.group(2))
    punct_char = eq_punct.get(num, ".")
    punct_xml = f'<m:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><m:t>{punct_char}</m:t></m:r>'
    
    # Inserir antes de </m:oMath> se já não tiver
    idx_close = full_row.rfind('</m:oMath>')
    if idx_close != -1:
        # verifica se já tem pontuação antes de </m:oMath>
        prev_slice = full_row[max(0, idx_close-100):idx_close]
        if '<m:t>.</m:t>' not in prev_slice and '<m:t>,</m:t>' not in prev_slice:
            full_row = full_row[:idx_close] + punct_xml + full_row[idx_close:]
            print(f"Eq (3.{num}) pontuada com '{punct_char}' em VERMELHO.")
    return full_row

pattern = r'(<w:tr [^>]*>.*?<m:oMath>.*?</m:oMath>.*?<w:t>\(3\.(\d+)\)</w:t>.*?</w:tr>)'
xml = re.sub(pattern, punct_repl, xml, flags=re.DOTALL)

# 2. ATUALIZAR PARÁGRAFO 19FE71A9 PARA FIGURA 3.4 EM VERMELHO
pos_p = xml.find('paraId="19FE71A9"')
if pos_p != -1:
    p_start = xml.rfind('<w:p ', 0, pos_p)
    p_end = xml.find('</w:p>', pos_p) + 6
    p_old = xml[p_start:p_end]
    
    # Atualiza cached value de 3 para 4
    p_new = p_old.replace('<w:t>3</w:t>', '<w:t>4</w:t>')
    
    # Adiciona cor vermelha a todos os w:r do parágrafo
    def apply_red_to_run(run_xml):
        if '<w:rPr>' in run_xml:
            if '<w:color ' in run_xml:
                return re.sub(r'<w:color [^>]*/>', '<w:color w:val="FF0000"/>', run_xml)
            else:
                return run_xml.replace('<w:rPr>', '<w:rPr><w:color w:val="FF0000"/>', 1)
        else:
            return re.sub(r'(<w:r(?: [^>]*)?>)', r'\1<w:rPr><w:color w:val="FF0000"/></w:rPr>', run_xml, count=1)
    
    p_new = re.sub(r'<w:r(?: [^>]*)?>.*?</w:r>', lambda m: apply_red_to_run(m.group(0)), p_new, flags=re.DOTALL)
    
    xml = xml[:p_start] + p_new + xml[p_end:]
    print("Legenda da Figura 3.4 (antiga 3.3) atualizada para 4 e formatada em VERMELHO.")

# Validação XML
try:
    ET.fromstring(xml)
    print("Validação XML: Sucesso! 100% válido.")
except Exception as e:
    print(f"Erro XML: {e}")
    sys.exit(1)

with open(DOC_XML, "w", encoding="utf-8") as f:
    f.write(xml)

# Reempacotar
temp_zip = os.path.join(TEMP_DIR, "..", "tcc_updated2.docx")
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
print(f"OneDrive atualizado: {ONEDRIVE_FILE} ({os.path.getsize(ONEDRIVE_FILE)} bytes).")

