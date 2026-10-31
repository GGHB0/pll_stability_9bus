# -*- coding: utf-8 -*-
"""
apply_enxuto_cleiton_red.py
Reescreve todos os textos novos inseridos com base nos apontamentos do
Prof. Cleiton para torná-los o mais enxutos, diretos e objetivos possível,
mantendo todo o rigor matemático, numérico e o destaque em VERMELHO (#FF0000).
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
BACKUP_DIR = r"C:\Users\gilbr\OneDrive\UERJ\TCC - Victor e Bruno\Template Modelo TCC\01_TCC_Monografia_Final\_backups\Revisao_Banca_Cleiton_Enxuto"
TEMP_DIR = r"C:\Temp\tcc_banca\cleiton_enxuto_work"

print("=" * 80)
print("TORNANDO TEXTOS DA REVISÃO DO PROF. CLEITON MAIS ENXUTOS (EM VERMELHO)")
print("=" * 80)

# 1. Backup datado
os.makedirs(BACKUP_DIR, exist_ok=True)
timestamp = time.strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(BACKUP_DIR, f"TCC_Victor_Bruno_VFinal_backup_{timestamp}.docx")
shutil.copyfile(ONEDRIVE_FILE, backup_file)
print(f"1. Backup criado:\n   {backup_file}")

# 2. Descompactar
if os.path.exists(TEMP_DIR):
    shutil.rmtree(TEMP_DIR)
os.makedirs(TEMP_DIR, exist_ok=True)

with zipfile.ZipFile(ONEDRIVE_FILE, 'r') as z:
    z.extractall(TEMP_DIR)

DOC_XML = os.path.join(TEMP_DIR, "word", "document.xml")
with open(DOC_XML, "r", encoding="utf-8") as f:
    xml = f.read()

print(f"   Tamanho original de document.xml: {len(xml)} bytes")

def make_red_p_xml(para_id, text, is_heading=False):
    # Escapar caracteres especiais XML
    text_xml = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if is_heading:
        return (
            f'<w:p w14:paraId="{para_id}" w14:textId="77777777" w:rsidR="00095F51" w:rsidRDefault="00381505">'
            f'<w:pPr><w:pStyle w:val="Ttulo2"/><w:spacing w:before="360" w:after="180"/><w:jc w:val="both"/><w:rPr><w:color w:val="FF0000"/><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr>'
            f'<w:r><w:rPr><w:color w:val="FF0000"/><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:t>{text_xml}</w:t></w:r></w:p>'
        )
    else:
        return (
            f'<w:p w14:paraId="{para_id}" w14:textId="77777777" w:rsidR="00381505" w:rsidRDefault="00381505">'
            f'<w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr></w:pPr>'
            f'<w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t>{text_xml}</w:t></w:r></w:p>'
        )

def replace_paragraph_text(xml_content, para_id, new_text, is_heading=False):
    pos = xml_content.find(f'paraId="{para_id}"')
    if pos == -1:
        print(f"AVISO: paraId='{para_id}' nao encontrado!")
        return xml_content
    start_p = xml_content.rfind('<w:p ', 0, pos)
    end_p = xml_content.find('</w:p>', pos) + 6
    new_p_xml = make_red_p_xml(para_id, new_text, is_heading=is_heading)
    print(f"Substituído parágrafo {para_id} por versão enxuta.")
    return xml_content[:start_p] + new_p_xml + xml_content[end_p:]

# ==============================================================================
# 1. TEXTOS ENXUTOS
# ==============================================================================

# 1.1 SCR e Scc (2CA00101) na Seção 3.3.1
p_scr_enxuto = (
    "A partir dos parâmetros da rede reduzidos ao PCC (Barra 2, Vb = 20 kV, Sb = 100 MVA, Zbase = 4,0 Ω), "
    "a impedância de Thévenin equivalente é Zth = 0,01004 + j0,4374 Ω (|Zth,pu| ≈ 0,1094 pu). "
    "A potência de curto-circuito simétrica resulta em Scc = Sb / |Zth,pu| ≈ 914,2 MVA, correspondendo a um "
    "SCR = Scc / Pinv,nom = 9,14. Conforme as normas IEEE Std 1204-1997 e CIGRE TB 671, valores de SCR > 3,0 "
    "classificam formalmente o barramento de ensaio como rede forte (strong grid)."
)
xml = replace_paragraph_text(xml, "2CA00101", p_scr_enxuto)

# 1.2 Elo CC como Bateria na Seção 3.3.2 (2CA00102)
p_bat_enxuto = (
    "O elo CC foi modelado como fonte de tensão ideal de 800 V (bateria), desacoplando a resposta dinâmica "
    "do SRF-PLL e do controle de corrente das oscilações de tensão e do algoritmo de MPPT fotovoltaico."
)
xml = replace_paragraph_text(xml, "2CA00102", p_bat_enxuto)

# 1.3 Trabalhos Futuros CC na Conclusão (2CA00103)
p_tf_enxuto = (
    "Como trabalho futuro, sugere-se a modelagem integrada do lado CC, incorporando arranjos fotovoltaicos "
    "com algoritmo de MPPT, regulação do barramento e proteção por chopper de frenagem sob faltas severas."
)
xml = replace_paragraph_text(xml, "2CA00103", p_tf_enxuto)

# 1.4 Transição Barra 6 vs. 7 entre Seções 4.3 e 4.4 (2CA00104)
p_trans_enxuto = (
    "A comparação entre as Barras 6 e 7 ilustra o paradoxo da sintonia: sob falta moderada na Barra 6 "
    "(V ≈ 0,78 pu), a banda estreita atenua a oscilação de 120 Hz; já sob o afundamento severo na Barra 7 "
    "(V < 0,15 pu), a lentidão da malha impede o acompanhamento angular, excedendo ±90° e culminando em perda "
    "de sincronismo por cycle slipping, detalhada a seguir."
)
xml = replace_paragraph_text(xml, "2CA00104", p_trans_enxuto)

# 1.5 Submódulo 2.10 do ONS na Seção 3.3.2 (1FB00320)
p_ons_enxuto = (
    "Para atender aos Procedimentos de Rede do ONS (Submódulo 2.10, Figura 3.3), a corrente reativa de suporte "
    "tem prioridade térmica sobre a ativa, saturando em 1,0 pu para V < 0,5 pu. A corrente ativa remanescente segue "
    "a restrição id,ref = min(1.0, sqrt(Imax² - iq,ref²)), anulando-se durante faltas severas para priorizar a "
    "sustentação de tensão da rede."
)
xml = replace_paragraph_text(xml, "1FB00320", p_ons_enxuto)

# 1.6 Divisão por 4 na Seção 2.3.2
pos_div4 = xml.find("A divisão dos ganhos Kp e Ki por 4")
if pos_div4 != -1:
    old_div4 = "A divisão dos ganhos Kp e Ki por 4 no diagrama de blocos da malha de controle decorre da conversão para grandezas em por unidade (pu), correspondendo exatamente ao valor da impedância base da rede no Ponto de Conexão Comum (Zbase = Vb² / Sb = (20 kV)² / 100 MVA = 4,0 Ω)."
    new_div4 = "A divisão dos ganhos do PI por 4 no diagrama decorre da normalização em pu pela impedância base no PCC (Zbase = Vb² / Sb = (20 kV)² / 100 MVA = 4,0 Ω)."
    xml = xml.replace(old_div4, new_div4, 1)
    print("Divisão por 4 em 2.3.2 tornada enxuta.")

# 1.7 Apêndice A - Parágrafos 1 e 2
p_ap1_enxuto = (
    "Para apoiar a análise dos 28 cenários simulados no MATLAB/Simulink, desenvolveu-se um painel interativo web "
    "em Python e Plotly, automatizando o cálculo dos indicadores de desempenho do SRF-PLL e de conformidade com o ONS."
)
xml = replace_paragraph_text(xml, "1FB00331", p_ap1_enxuto)

p_ap2_enxuto = (
    "A interface permite a comparação direta entre sintonias, visualização dos fasores no plano dq, análise "
    "espectral (FFT) da componente de 120 Hz em faltas assimétricas e verificação das rampas de suporte de reativo (Figura A.1)."
)
xml = replace_paragraph_text(xml, "1FB00332", p_ap2_enxuto)

# 1.8 Apêndice A - GitHub
p_git_enxuto = (
    "O código-fonte da simulação, modelos em Simulink e o painel interativo estão disponíveis em: "
    "https://github.com/bruno-victor-uerj/pll-stability-dashboard."
)
xml = replace_paragraph_text(xml, "1FB00336", p_git_enxuto)

# 1.9 Apêndice A - Detalhe Fig A.1
p_a1_enxuto = (
    "O painel consolidado (Figura A.1) sintetiza a matriz de indicadores para todos os cenários nas Barras 5, 6, 7 e 8, "
    "com filtros por tipo de falta e sintonia para avaliação rápida do tempo de assentamento e conformidade normativa."
)
xml = replace_paragraph_text(xml, "2FB00101", p_a1_enxuto)

# 1.10 Apêndice A - Sec B intro
p_secb_enxuto = (
    "O modo apresentação disponibiliza telas guiadas em alta definição (1920x1080) voltadas à demonstração "
    "didática dos fenômenos transitórios e dos limites de estabilidade do conversor."
)
xml = replace_paragraph_text(xml, "2FB00103", p_secb_enxuto)

# 1.11 Apêndice A - Fig A.2 (Fasor)
p_t1_enxuto = (
    "O módulo fasorial (Figura A.2) reconstrói a trajetória do vetor de tensão no plano direto-quadratura (vd x vq) "
    "sob falta na Barra 6, permitindo reprodução dinâmica ou quadro a quadro para evidenciar a convergência suave na sintonia nominal."
)
xml = replace_paragraph_text(xml, "2FB00104", p_t1_enxuto)

# 1.12 Apêndice A - Fig A.3 (Seq Neg)
p_t2_enxuto = (
    "O módulo espectral (Figura A.3) decompõe a tensão em componentes simétricas e realiza a FFT em tempo real de vq, "
    "isolando a oscilação característica de 120 Hz transmitida ao ângulo estimado pelo PLL sob faltas assimétricas."
)
xml = replace_paragraph_text(xml, "2FB00108", p_t2_enxuto)

# 1.13 Apêndice A - Fig A.4 (Sincronismo)
p_t3_enxuto = (
    "O módulo de sincronismo (Figura A.4) detalha a falta severa na Barra 7 sob sintonia inadequada, evidenciando o erro "
    "de fase além de ±90° e o consequente colapso por escorregamento de polos (cycle slipping)."
)
xml = replace_paragraph_text(xml, "2FB00112", p_t3_enxuto)

# 1.14 Apêndice A - Fig A.5 (ONS)
p_t4_enxuto = (
    "O módulo regulatório (Figura A.5) sobrepõe a corrente reativa injetada (iq) às máscaras do Submódulo 2.10 do ONS, "
    "certificando o suporte dinâmico de tensão e a observância dos limites térmicos do conversor."
)
xml = replace_paragraph_text(xml, "2FB00116", p_t4_enxuto)

# ==============================================================================
# VALIDAÇÃO XML E GRAVAÇÃO
# ==============================================================================
try:
    ET.fromstring(xml)
    print("Validação XML: Sucesso! 100% válido.")
except Exception as e:
    print(f"ERRO DE XML: {e}")
    sys.exit(1)

with open(DOC_XML, "w", encoding="utf-8") as f:
    f.write(xml)

# Reempacotar
temp_zip = os.path.join(TEMP_DIR, "..", "tcc_final_enxuto.docx")
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
print(f"Arquivo oficial gravado no OneDrive:\n   {ONEDRIVE_FILE} ({os.path.getsize(ONEDRIVE_FILE)} bytes)")
print("=" * 80)
print("TODOS OS TEXTOS FORAM TORNADOS ENXUTOS E PRESERVADOS EM VERMELHO!")
print("=" * 80)
