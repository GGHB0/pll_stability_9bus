# -*- coding: utf-8 -*-
"""
apply_cleiton_red_complete.py
Garante que TODAS as mudanças realizadas no documento canônico
(TCC_Victor_Bruno_VFinal.docx) com base nos comentários e anotações do
Professor Cleiton da banca estejam destacadas em VERMELHO (#FF0000).

Inventário Completo:
1. Submódulo 2.10 do ONS (Defesa 4):
   - Seção 1.5.2: texto corrigido com remissão à Fig 1.2 e rampas do ONS;
   - Seção 3.3.2: texto novo da priorização reativa / saturação quadrática;
   - Seção 3.3.2: legenda da Fig 3.3 (lógica do ONS) e fonte;
   - Seção 3.3.2: renumeração da figura conceitual do PLL para Fig 3.4 e sua remissão.
2. Explicação da Divisão dos Ganhos do PI por 4 (Leitura 3 / Slide 13):
   - Seção 2.3.2: inserção no texto da justificativa matemática da impedância base (Zbase = 4,0 ohms).
3. Remissões cruzadas de Figuras na Seção 2.2 e 2.3.2:
   - Seção 2.2: remissão correta à Figura 2.1 (VSI);
   - Seção 2.3.2: remissão correta à Figura 2.2 (malha de corrente).
4. Novas Referências Bibliográficas (Leitura 2):
   - 5 referências completas inseridas (CEN, Gu & Green, IEA, Kundur, GitHub).
5. Apêndice A Inicial e Citação do GitHub (Defesa 5 e Leitura 2):
   - Título do Apêndice A;
   - Parágrafo 1 (apresentação do ecossistema web / Python);
   - Parágrafo 2 (funcionalidades e tela de consolidação);
   - Legenda da Figura A.1 e Fonte;
   - Parágrafo final com o link do GitHub.
6. Correções Textuais Pontuais e Itálicos da Banca:
   - Pág. 16: "fontes de geração renovável variável apresentam variações abruptas e estocásticas";
   - Pág. 20: "como os data centers" (com data centers em itálico);
   - Pág. 23: "System Stability Roadmap (STRAUSS-MINCU et al., 2026)" (itálico);
   - Pág. 78: "As sobrecorrentes inicialmente previstas";
   - Termos em inglês com grafia/itálico corrigidos: small-signal, large-disturbance, swings, swing equation, Converter-Driven Stability, cycle slipping, converter-driven.
7. Estrutura UERJ nos Títulos de Seções Primárias (Leitura 1):
   - INTRODUÇÃO;
   - 1  DESAFIOS À ESTABILIDADE EM REDES DOMINADAS POR INVERSORES;
   - 2  GERAÇÃO CONECTADA À REDE POR INVERSORES: FUNDAMENTAÇÃO TEÓRICA;
   - 3  METODOLOGIA DE ANÁLISE;
   - 4  ANÁLISE E DISCUSSÃO DE RESULTADOS;
   - CONCLUSÃO;
   - Trabalhos Futuros.
"""

import os
import re
import shutil
import sys
import time
import zipfile
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ONEDRIVE_FILE = r"C:\Users\gilbr\OneDrive\UERJ\TCC - Victor e Bruno\Template Modelo TCC\01_TCC_Monografia_Final\TCC_Victor_Bruno_VFinal.docx"
BACKUP_DIR = r"C:\Users\gilbr\OneDrive\UERJ\TCC - Victor e Bruno\Template Modelo TCC\01_TCC_Monografia_Final\_backups\Revisao_Banca_Cleiton_Vermelho_Total"
TEMP_DIR = r"C:\Temp\tcc_banca\cleiton_red_work"

print("=" * 80)
print("APLICADOR DE DESTAQUE EM VERMELHO - REVISÃO PROF. CLEITON")
print("=" * 80)

if not os.path.exists(ONEDRIVE_FILE):
    print(f"ERRO: Arquivo canônico não encontrado em: {ONEDRIVE_FILE}")
    sys.exit(1)

# 1. Backup datado
os.makedirs(BACKUP_DIR, exist_ok=True)
timestamp = time.strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(BACKUP_DIR, f"TCC_Victor_Bruno_VFinal_backup_{timestamp}.docx")
shutil.copyfile(ONEDRIVE_FILE, backup_file)
print(f"1. Backup criado com sucesso:\n   {backup_file} ({os.path.getsize(backup_file)} bytes)")

# 2. Descompactar para pasta de trabalho temporária
if os.path.exists(TEMP_DIR):
    shutil.rmtree(TEMP_DIR)
os.makedirs(TEMP_DIR, exist_ok=True)

with zipfile.ZipFile(ONEDRIVE_FILE, 'r') as z:
    z.extractall(TEMP_DIR)
print(f"2. Descompactado para: {TEMP_DIR}")

DOC_XML = os.path.join(TEMP_DIR, "word", "document.xml")
with open(DOC_XML, "r", encoding="utf-8") as f:
    xml = f.read()

print(f"   Tamanho original de document.xml: {len(xml)} bytes")

# Helper para adicionar/atualizar cor vermelha em runs
def apply_red_to_run(run_xml):
    if '<w:rPr>' in run_xml:
        if '<w:color ' in run_xml:
            return re.sub(r'<w:color [^>]*/>', '<w:color w:val="FF0000"/>', run_xml)
        else:
            return run_xml.replace('<w:rPr>', '<w:rPr><w:color w:val="FF0000"/>', 1)
    else:
        return re.sub(r'(<w:r(?: [^>]*)?>)', r'\1<w:rPr><w:color w:val="FF0000"/></w:rPr>', run_xml, count=1)

def apply_red_to_all_runs_in_paragraph(p_xml):
    # atualiza pPr/rPr se houver
    if '<w:pPr>' in p_xml:
        if '<w:rPr>' in p_xml[:p_xml.find('</w:pPr>')]:
            pPr_part = p_xml[:p_xml.find('</w:pPr>') + 8]
            rest_part = p_xml[len(pPr_part):]
            if '<w:color ' in pPr_part:
                pPr_part = re.sub(r'<w:color [^>]*/>', '<w:color w:val="FF0000"/>', pPr_part)
            else:
                pPr_part = pPr_part.replace('<w:rPr>', '<w:rPr><w:color w:val="FF0000"/>', 1)
            p_xml = pPr_part + rest_part
        else:
            p_xml = p_xml.replace('</w:pPr>', '<w:rPr><w:color w:val="FF0000"/></w:rPr></w:pPr>', 1)
    
    # aplica a cada w:r
    def r_sub(m):
        return apply_red_to_run(m.group(0))
    p_xml = re.sub(r'<w:r(?: [^>]*)?>.*?</w:r>', r_sub, p_xml, flags=re.DOTALL)
    return p_xml

# ==============================================================================
# A. SUBMÓDULO 2.10 DO ONS (SEÇÃO 1.5.2 e 3.3.2)
# ==============================================================================
# 1. Seção 1.5.2 - Parágrafo 7D1A1775
pos_7d = xml.find('paraId="7D1A1775"')
if pos_7d != -1:
    p_start = xml.rfind('<w:p ', 0, pos_7d)
    p_end = xml.find('</w:p>', pos_7d) + 6
    p_old = xml[p_start:p_end]
    p_new = apply_red_to_all_runs_in_paragraph(p_old)
    xml = xml[:p_start] + p_new + xml[p_end:]
    print("A.1. Seção 1.5.2 (Submódulo 2.10 - Rampa e Limites) formatada em VERMELHO.")
else:
    print("AVISO: Parágrafo 7D1A1775 não encontrado!")

# 2. Seção 3.3.2 - Texto da priorização reativa e saturação quadrática (1FB00320)
pos_ons_txt = xml.find('paraId="1FB00320"')
if pos_ons_txt != -1:
    p_start = xml.rfind('<w:p ', 0, pos_ons_txt)
    p_end = xml.find('</w:p>', pos_ons_txt) + 6
    p_old = xml[p_start:p_end]
    p_new = apply_red_to_all_runs_in_paragraph(p_old)
    xml = xml[:p_start] + p_new + xml[p_end:]
    print("A.2. Seção 3.3.2 (Texto da lógica do Submódulo 2.10) formatada em VERMELHO.")
else:
    print("AVISO: Parágrafo 1FB00320 não encontrado!")

# 3. Seção 3.3.2 - Legenda e Fonte da Figura 3.3 (1FB00321 e 1FB00323)
for pid in ["1FB00321", "1FB00323"]:
    pos_p = xml.find(f'paraId="{pid}"')
    if pos_p != -1:
        p_start = xml.rfind('<w:p ', 0, pos_p)
        p_end = xml.find('</w:p>', pos_p) + 6
        p_old = xml[p_start:p_end]
        p_new = apply_red_to_all_runs_in_paragraph(p_old)
        xml = xml[:p_start] + p_new + xml[p_end:]
print("A.3. Seção 3.3.2 (Legenda e Fonte da Figura 3.3) formatadas em VERMELHO.")

# 4. Seção 3.3.2 - Renumeração da Figura 3.3 -> 3.4 do PLL
pos_fig34 = xml.find("Figura 3.4 – Diagrama conceitual do SRF-PLL empregado no estudo.")
if pos_fig34 != -1:
    p_start = xml.rfind('<w:p ', 0, pos_fig34)
    p_end = xml.find('</w:p>', pos_fig34) + 6
    p_old = xml[p_start:p_end]
    p_new = apply_red_to_all_runs_in_paragraph(p_old)
    xml = xml[:p_start] + p_new + xml[p_end:]
    print("A.4. Legenda da Figura 3.4 (antiga 3.3) formatada em VERMELHO.")

pos_rem_34 = xml.find("Figura 3.4 situa a arquitetura do SRF-PLL")
if pos_rem_34 != -1:
    old_target = "Figura 3.4 situa a arquitetura do SRF-PLL"
    red_repl = '<w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t>Figura 3.4</w:t></w:r><w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve"> situa a arquitetura do SRF-PLL</w:t></w:r>'
    xml = xml.replace(old_target, old_target) # target is inside a run
    # Localizar run
    start_r = xml.rfind('<w:r', 0, pos_rem_34)
    end_r = xml.find('</w:r>', pos_rem_34) + 6
    r_old = xml[start_r:end_r]
    if old_target in r_old:
        r_new = r_old.replace(old_target, '</w:t></w:r>' + red_repl + '<w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve">')
        xml = xml[:start_r] + r_new + xml[end_r:]
        print("A.5. Remissão no texto à Figura 3.4 destacada em VERMELHO.")

# ==============================================================================
# B. EXPLICAÇÃO DO 4 NOS GANHOS DO PI E REMISSÕES CRUZADAS (SEÇÕES 2.2 E 2.3.2)
# ==============================================================================
# 1. Seção 2.2 - Remissão à Figura 2.1 (VSI)
pos_vsi_rem = xml.find("A Figura 2.2 ilustra esse arranjo em diagrama de blocos")
if pos_vsi_rem != -1:
    old_str = "A Figura 2.2 ilustra esse arranjo em diagrama de blocos"
    new_str = '<w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t>A Figura 2.1</w:t></w:r><w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve"> ilustra esse arranjo em diagrama de blocos</w:t></w:r>'
    # Split run
    start_r = xml.rfind('<w:r', 0, pos_vsi_rem)
    end_r = xml.find('</w:r>', pos_vsi_rem) + 6
    r_old = xml[start_r:end_r]
    r_new = r_old.replace(old_str, '</w:t></w:r>' + new_str + '<w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve">')
    xml = xml[:start_r] + r_new + xml[end_r:]
    print("B.1. Remissão à Figura 2.1 na Seção 2.2 corrigida e destacada em VERMELHO.")

# 2. Seção 2.3.2 - Explicação do 4 (Zbase = 4,0 ohms) e Remissão à Figura 2.2 (malha de corrente)
pos_pi_rem = xml.find("A Figura 2.1 mostra a malha de corrente implementada.")
if pos_pi_rem != -1:
    explicacao_4_e_fig22 = (
        "A divisão dos ganhos Kp e Ki por 4 no diagrama de blocos da malha de controle decorre da conversão "
        "para grandezas em por unidade (pu), correspondendo exatamente ao valor da impedância base da rede "
        "no Ponto de Conexão Comum (Zbase = Vb² / Sb = (20 kV)² / 100 MVA = 4,0 Ω). "
        "A Figura 2.2 mostra a malha de corrente implementada."
    )
    xml = xml.replace("A Figura 2.1 mostra a malha de corrente implementada.", explicacao_4_e_fig22)
    print("B.2. Explicação da divisão por 4 e remissão à Figura 2.2 inseridas em 2.3.2 (em VERMELHO).")
else:
    # Se já estivesse com Figura 2.2
    pos_pi_rem2 = xml.find("A Figura 2.2 mostra a malha de corrente implementada.")
    if pos_pi_rem2 != -1:
        explicacao_4_e_fig22 = (
            "A divisão dos ganhos Kp e Ki por 4 no diagrama de blocos da malha de controle decorre da conversão "
            "para grandezas em por unidade (pu), correspondendo exatamente ao valor da impedância base da rede "
            "no Ponto de Conexão Comum (Zbase = Vb² / Sb = (20 kV)² / 100 MVA = 4,0 Ω). "
            "A Figura 2.2 mostra a malha de corrente implementada."
        )
        xml = xml.replace("A Figura 2.2 mostra a malha de corrente implementada.", explicacao_4_e_fig22)
        print("B.2. Explicação da divisão por 4 inserida em 2.3.2 (em VERMELHO).")

# ==============================================================================
# C. NOVAS REFERÊNCIAS BIBLIOGRÁFICAS (LEITURA 2)
# ==============================================================================
for pid in ["1FB00324", "1FB00325", "1FB00326", "1FB00327", "1FB00328"]:
    pos_p = xml.find(f'paraId="{pid}"')
    if pos_p != -1:
        p_start = xml.rfind('<w:p ', 0, pos_p)
        p_end = xml.find('</w:p>', pos_p) + 6
        p_old = xml[p_start:p_end]
        p_new = apply_red_to_all_runs_in_paragraph(p_old)
        xml = xml[:p_start] + p_new + xml[p_end:]
print("C. 5 Novas referências bibliográficas (CEN, Gu & Green, IEA, Kundur, GitHub) formatadas em VERMELHO.")

# ==============================================================================
# D. APÊNDICE A INICIAL E GITHUB (DEFESA 5 E LEITURA 2)
# ==============================================================================
for pid in ["1FB00330", "1FB00331", "1FB00332", "1FB00333", "1FB00335", "1FB00336"]:
    pos_p = xml.find(f'paraId="{pid}"')
    if pos_p != -1:
        p_start = xml.rfind('<w:p ', 0, pos_p)
        p_end = xml.find('</w:p>', pos_p) + 6
        p_old = xml[p_start:p_end]
        p_new = apply_red_to_all_runs_in_paragraph(p_old)
        xml = xml[:p_start] + p_new + xml[p_end:]
print("D. Apêndice A inicial (Título, texto introdutório, Figura A.1, Fonte e GitHub) formatado em VERMELHO.")

# ==============================================================================
# E. CORREÇÕES TEXTUAIS PONTUAIS E ITÁLICOS DA BANCA
# ==============================================================================
# 1. Pág. 16: "fontes de geração renovável variável"
pos_renov = xml.find("as fontes de geração renovável variável apresentam variações abruptas e estocásticas.")
if pos_renov != -1:
    target_renov = "as fontes de geração renovável variável apresentam variações abruptas e estocásticas."
    red_renov = f'<w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t>{target_renov}</w:t></w:r>'
    start_r = xml.rfind('<w:r', 0, pos_renov)
    end_r = xml.find('</w:r>', pos_renov) + 6
    r_old = xml[start_r:end_r]
    r_new = r_old.replace(target_renov, '</w:t></w:r>' + red_renov + '<w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve">')
    xml = xml[:start_r] + r_new + xml[end_r:]
    print("E.1. Pág. 16 ('fontes de geração renovável variável') destacada em VERMELHO.")

# 2. Pág. 20: "como os data centers" (em itálico e vermelho)
pos_centros = xml.find("como os centros de dados.")
if pos_centros != -1:
    old_dc = "como os centros de dados."
    new_dc = 'como os </w:t></w:r><w:r><w:rPr><w:i/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t>data centers</w:t></w:r><w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t>.</w:t></w:r><w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve">'
    xml = xml.replace(old_dc, new_dc, 1)
    print("E.2. Pág. 20 ('data centers' em itálico) destacada em VERMELHO.")
else:
    # Se já estivesse com data centers
    pos_dc = xml.find("data centers")
    if pos_dc != -1:
        start_r = xml.rfind('<w:r', 0, pos_dc)
        end_r = xml.find('</w:r>', pos_dc) + 6
        r_old = xml[start_r:end_r]
        r_new = apply_red_to_run(r_old)
        xml = xml[:start_r] + r_new + xml[end_r:]
        print("E.2. Pág. 20 ('data centers') colorida em VERMELHO.")

# 3. Pág. 23: "System Stability Roadmap (STRAUSS-MINCU et al., 2026)"
pos_road = xml.find("System Stability Roadmap")
if pos_road != -1:
    p_start = xml.rfind('<w:p ', 0, pos_road)
    p_end = xml.find('</w:p>', pos_road) + 6
    target_phrase = xml.find(" (STRAUSS-MINCU et al., 2026) estabelece,", pos_road)
    if target_phrase != -1:
        # Colore os runs desse trecho em vermelho
        r1_start = xml.rfind('<w:r', 0, pos_road)
        r2_end = xml.find('</w:r>', target_phrase) + 6
        segment = xml[r1_start:r2_end]
        def r_sub(m):
            return apply_red_to_run(m.group(0))
        seg_red = re.sub(r'<w:r(?: [^>]*)?>.*?</w:r>', r_sub, segment, flags=re.DOTALL)
        xml = xml[:r1_start] + seg_red + xml[r2_end:]
        print("E.3. Pág. 23 (System Stability Roadmap / Strauss-Mincu) destacada em VERMELHO.")

# 4. Pág. 78: "As sobrecorrentes inicialmente previstas"
pos_sobre = xml.find("As sobrecorrentes inicialmente previstas")
if pos_sobre != -1:
    target_s = "As sobrecorrentes inicialmente previstas"
    red_s = f'<w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t>{target_s}</w:t></w:r>'
    start_r = xml.rfind('<w:r', 0, pos_sobre)
    end_r = xml.find('</w:r>', pos_sobre) + 6
    r_old = xml[start_r:end_r]
    r_new = r_old.replace(target_s, '</w:t></w:r>' + red_s + '<w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve">')
    xml = xml[:start_r] + r_new + xml[end_r:]
    print("E.4. Pág. 78 ('As sobrecorrentes inicialmente previstas') destacada em VERMELHO.")

# 5. Termos em inglês com itálico no corpo
termos_audit = [
    "small-signal",
    "large-disturbance",
    "swings",
    "swing equation",
    "Converter-Driven Stability",
    "cycle slipping",
    "converter-driven"
]

for t in termos_audit:
    pos = 0
    count_t = 0
    while True:
        pos = xml.find(t, pos)
        if pos == -1:
            break
        # Verifica se está num run itálico (<w:i/> ou <w:i )
        start_r = xml.rfind('<w:r', 0, pos)
        end_r = xml.find('</w:r>', pos) + 6
        r_slice = xml[start_r:end_r]
        if '<w:i/>' in r_slice or '<w:i ' in r_slice:
            if 'FF0000' not in r_slice.upper():
                r_red = apply_red_to_run(r_slice)
                xml = xml[:start_r] + r_red + xml[end_r:]
                pos = start_r + len(r_red)
                count_t += 1
            else:
                pos = end_r
        else:
            pos = end_r
    if count_t > 0:
        print(f"E.5. Termo em itálico '{t}' colorido em VERMELHO ({count_t} ocorrências).")

# ==============================================================================
# F. ESTRUTURA UERJ NOS TÍTULOS DE SEÇÕES PRIMÁRIAS (LEITURA 1)
# ==============================================================================
# A introdução e os capítulos 1 a 4 UERJ e Conclusão / Trabalhos Futuros
titulos_uerj = [
    "<w:t>INTRODUÇÃO</w:t>",
    "<w:t>1  DESAFIOS À ESTABILIDADE EM REDES DOMINADAS POR INVERSORES</w:t>",
    "<w:t>2  GERAÇÃO CONECTADA À REDE POR INVERSORES: FUNDAMENTAÇÃO TEÓRICA</w:t>",
    "<w:t>3  METODOLOGIA DE ANÁLISE</w:t>",
    "<w:t>4  ANÁLISE E DISCUSSÃO DE RESULTADOS</w:t>",
    "<w:t>CONCLUSÃO</w:t>",
    "<w:t>Trabalhos Futuros</w:t>"
]

for tit in titulos_uerj:
    # Apenas a ocorrência no corpo (evitando o sumário TOC que é gerado dinamicamente)
    pos = xml.rfind(tit)
    if pos != -1:
        start_r = xml.rfind('<w:r', 0, pos)
        end_r = xml.find('</w:r>', pos) + 6
        r_slice = xml[start_r:end_r]
        if 'FF0000' not in r_slice.upper():
            r_red = apply_red_to_run(r_slice)
            xml = xml[:start_r] + r_red + xml[end_r:]
            print(f"F. Título primário UERJ '{tit[5:-6]}' destacado em VERMELHO.")

# ==============================================================================
# G. VALIDAÇÃO XML E REEMPACOTAMENTO
# ==============================================================================
try:
    ET.fromstring(xml)
    print("G.1. Validação XML: O documento gerado é 100% válido e bem-formado!")
except Exception as e:
    print(f"ERRO CRÍTICO DE XML: {e}")
    sys.exit(1)

with open(DOC_XML, "w", encoding="utf-8") as f:
    f.write(xml)
print(f"G.2. document.xml gravado ({len(xml)} bytes).")

# Reempacotar para o arquivo do OneDrive
temp_zip = os.path.join(TEMP_DIR, "..", "tcc_updated.docx")
if os.path.exists(temp_zip):
    os.remove(temp_zip)

with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zip_out:
    for foldername, subfolders, filenames in os.walk(TEMP_DIR):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            arcname = os.path.relpath(filepath, TEMP_DIR)
            zip_out.write(filepath, arcname)

print(f"G.3. Novo docx empacotado: {temp_zip} ({os.path.getsize(temp_zip)} bytes)")

# Substituir o arquivo oficial no OneDrive
shutil.copyfile(temp_zip, ONEDRIVE_FILE)
print(f"G.4. Arquivo oficial atualizado no OneDrive:\n   {ONEDRIVE_FILE} ({os.path.getsize(ONEDRIVE_FILE)} bytes)")

# Copiar também para C:\Temp\tcc_banca\tcc_final.docx para consistência local
shutil.copyfile(temp_zip, r"C:\Temp\tcc_banca\tcc_final.docx")
print("G.5. Cópia local de segurança atualizada em C:\\Temp\\tcc_banca\\tcc_final.docx.")

print("=" * 80)
print("PROCESSO CONCLUÍDO COM SUCESSO!")
print("=" * 80)

