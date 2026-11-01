# -*- coding: utf-8 -*-
"""
apply_banca_pendencias.py
Aplica as revisões aprovadas pelo usuário:
1. Item 5: Correção de remissão cruzada no Cap. 4 (Figuras 4.12 e 5.13 -> 4.12 e 4.13);
2. Item 4: Harmonização do §3.3.2 / Seção 2.5 com a Seção 2.3.2 e Figura 2.2 (filtro LCL e PI com notch, sem desacoplamento ativo);
3. Item 1: Inclusão da justificativa da escolha do SRF-PLL perante DSOGI-PLL e DDSRF-PLL (Prof. Rafael, comentário 4), em azul (#0070C0), no §2.4 e sigla DSOGI-PLL.
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
TEMP_WORK_DIR = r"C:\Temp\tcc_banca\work_pendencias"

print("=" * 80)
print("APLICANDO ITENS 1, 4 E 5 DA BANCA NO DOCUMENTO CANÔNICO")
print("=" * 80)

# 1. Conferir canônico
if not os.path.exists(CANONICAL_DOCX):
    print(f"ERRO: Canônico não encontrado: {CANONICAL_DOCX}")
    sys.exit(1)

# 2. Criar backup datado
os.makedirs(BACKUP_DIR, exist_ok=True)
timestamp = time.strftime("%Y%m%d_%H%M%S")
pre_backup = os.path.join(BACKUP_DIR, f"TCC_Victor_Bruno_VFinal_backup_pre_pendencias_{timestamp}.docx")
shutil.copyfile(CANONICAL_DOCX, pre_backup)
print(f"1. Backup de segurança prévio salvo em:\n   {pre_backup}")

# 3. Descompactar para pasta temporária
if os.path.exists(TEMP_WORK_DIR):
    shutil.rmtree(TEMP_WORK_DIR)
os.makedirs(TEMP_WORK_DIR, exist_ok=True)

with zipfile.ZipFile(CANONICAL_DOCX, 'r') as z:
    z.extractall(TEMP_WORK_DIR)

doc_xml_path = os.path.join(TEMP_WORK_DIR, "word", "document.xml")
with open(doc_xml_path, "r", encoding="utf-8") as f:
    xml = f.read()

print(f"2. word/document.xml carregado ({len(xml)} bytes).")

# ==============================================================================
# TAREFA 1: Item 5 - Correção de Remissão Cruzada (Figuras 4.12 e 5.13 -> 4.12 e 4.13)
# ==============================================================================
old_remissao = "As Figuras 4.12 e 5.13 isolam o efeito da parametrização do SRF-PLL"
new_remissao = "As Figuras 4.12 e 4.13 isolam o efeito da parametrização do SRF-PLL"

if old_remissao not in xml:
    print(f"ERRO: Trecho '{old_remissao}' não encontrado!")
    sys.exit(1)

xml = xml.replace(old_remissao, new_remissao, 1)
print("3. Item 5 aplicado: Remissão corrigida para 'Figuras 4.12 e 4.13'.")

# ==============================================================================
# TAREFA 2: Item 4 - Harmonização da Seção 2.5 com Seção 2.3.2 (sem desacoplamento)
# ==============================================================================
# P535 antigo
p535_tag = 'w14:paraId="35938431"'
pos_p535 = xml.find(p535_tag)
if pos_p535 == -1:
    print(f"ERRO: Parágrafo P535 ({p535_tag}) não encontrado!")
    sys.exit(1)

start_p535 = xml.rfind('<w:p ', 0, pos_p535)
end_p535 = xml.find('</w:p>', pos_p535) + 6
old_p535 = xml[start_p535:end_p535]

new_p535 = (
    '<w:p w14:paraId="35938431" w14:textId="77777777" w:rsidR="00AF35EC" w:rsidRDefault="00AF35EC">'
    '<w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:szCs w:val="24"/></w:rPr></w:pPr>'
    '<w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve">A arquitetura de controle de corrente apresentada na Seção </w:t></w:r>'
    '<w:r><w:rPr><w:color w:val="0070C0"/><w:szCs w:val="24"/></w:rPr><w:t>2.3.2</w:t></w:r>'
    '<w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve"> emprega controladores PI independentes nos eixos d e q associados a filtros notch sintonizados na frequência de ressonância do filtro LCL. Como as tensões da rede e o acoplamento cruzado atuam como perturbações rejeitadas pela ação integral dos compensadores, a dinâmica de cada eixo pode ser aproximada por uma planta puramente indutiva para fins de sintonia. Isso permite que os ganhos do compensador sejam projetados pela mesma metodologia empregada no laço de sincronismo (Seção 2.4): a comparação direta com a forma canônica de um sistema de segunda ordem.</w:t></w:r>'
    '</w:p>'
)

xml = xml[:start_p535] + new_p535 + xml[end_p535:]
print("4. Item 4 (P535) aplicado: Texto harmonizado com Seção 2.3.2 (filtro LCL e PI com notch).")

# P536 antigo
p536_tag = 'w14:paraId="77431F0B"'
pos_p536 = xml.find(p536_tag)
if pos_p536 == -1:
    print(f"ERRO: Parágrafo P536 ({p536_tag}) não encontrado!")
    sys.exit(1)

start_p536 = xml.rfind('<w:p ', 0, pos_p536)
end_p536 = xml.find('</w:p>', pos_p536) + 6
old_p536 = xml[start_p536:end_p536]

new_p536 = (
    '<w:p w14:paraId="77431F0B" w14:textId="77777777" w:rsidR="00AF35EC" w:rsidRDefault="00AF35EC">'
    '<w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:szCs w:val="24"/></w:rPr></w:pPr>'
    '<w:r><w:rPr><w:szCs w:val="24"/></w:rPr><w:t>Modelo da planta de corrente equivalente por eixo para projeto dos ganhos:</w:t></w:r>'
    '</w:p>'
)

xml = xml[:start_p536] + new_p536 + xml[end_p536:]
print("5. Item 4 (P536) aplicado: Legenda introdutória da Equação (2.21) harmonizada.")

# ==============================================================================
# TAREFA 3: Item 1 - Justificativa do SRF-PLL perante outros métodos (Prof. Rafael)
# ==============================================================================
# 3.1. Inserir parágrafo explicativo logo após P484 (Seção 2.4), em AZUL (#0070C0)
p484_tag = 'w14:paraId="6B6578B6"'
pos_p484 = xml.find(p484_tag)
if pos_p484 == -1:
    print(f"ERRO: Parágrafo P484 ({p484_tag}) não encontrado!")
    sys.exit(1)

end_p484 = xml.find('</w:p>', pos_p484) + 6

p_srf_choice = (
    '<w:p w14:paraId="5FAF0401" w14:textId="77777777" w:rsidR="009855DD" w:rsidRDefault="009855DD">'
    '<w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:color w:val="0070C0"/><w:szCs w:val="24"/></w:rPr></w:pPr>'
    '<w:r><w:rPr><w:color w:val="0070C0"/><w:szCs w:val="24"/></w:rPr>'
    '<w:t>Embora técnicas modernas como o DSOGI-PLL (Dual Second-Order Generalized Integrator) e o DDSRF-PLL (Decoupled Double Synchronous Reference Frame) permitam desacoplar as componentes de sequência positiva e negativa sob desequilíbrios, a priorização da técnica SRF-PLL neste trabalho fundamenta-se em sua ampla consolidação comercial como o padrão dominante na indústria de inversores grid-following e em sua reduzida demanda computacional. Ademais, a topologia convencional atua como linha de base (baseline) indispensável para investigar os limites de estabilidade angular frente a afundamentos severos e variações de banda passante, sem que filtros adicionais mascarem a dinâmica fundamental do laço de sincronismo.</w:t>'
    '</w:r></w:p>'
)

xml = xml[:end_p484] + p_srf_choice + xml[end_p484:]
print("6. Item 1 (Seção 2.4) aplicado: Parágrafo de escolha do SRF-PLL inserido em AZUL (#0070C0).")

# 3.2. Inserir a sigla DSOGI-PLL na Lista de Abreviaturas e Siglas após P206 (DDSRF-PLL)
p206_tag = 'w14:paraId="5718BFDB"'
pos_p206 = xml.find(p206_tag)
if pos_p206 == -1:
    print(f"ERRO: Parágrafo P206 ({p206_tag}) não encontrado!")
    sys.exit(1)

end_p206 = xml.find('</w:p>', pos_p206) + 6

p_dsogi_sigla = (
    '<w:p w14:paraId="5FAF0206" w14:textId="77777777" w:rsidR="007B189F" w:rsidRDefault="00C10CED">'
    '<w:pPr><w:tabs><w:tab w:val="left" w:pos="1701"/></w:tabs><w:spacing w:after="60" w:line="240" w:lineRule="auto"/><w:ind w:left="1701" w:hanging="1701"/><w:rPr><w:color w:val="0070C0"/><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr></w:pPr>'
    '<w:r><w:rPr><w:color w:val="0070C0"/><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr><w:t>DSOGI-PLL</w:t></w:r>'
    '<w:r><w:rPr><w:color w:val="0070C0"/><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr><w:tab/><w:t>Dual Second-Order Generalized Integrator Phase-Locked Loop</w:t></w:r>'
    '</w:p>'
)

xml = xml[:end_p206] + p_dsogi_sigla + xml[end_p206:]
print("7. Item 1 (Siglas) aplicado: Sigla DSOGI-PLL inserida na lista em AZUL (#0070C0).")

# 4. Salvar document.xml
with open(doc_xml_path, "w", encoding="utf-8") as f:
    f.write(xml)

print(f"8. word/document.xml gravado ({len(xml)} bytes).")

# 5. Reempacotar DOCX
output_docx = os.path.join(TEMP_WORK_DIR, "repacked.docx")
with zipfile.ZipFile(output_docx, 'w', compression=zipfile.ZIP_DEFLATED) as zip_out:
    for foldername, subfolders, filenames in os.walk(TEMP_WORK_DIR):
        for filename in filenames:
            if filename == "repacked.docx":
                continue
            filepath = os.path.join(foldername, filename)
            arcname = os.path.relpath(filepath, TEMP_WORK_DIR)
            zip_out.write(filepath, arcname)

print(f"9. DOCX reempacotado com sucesso ({os.path.getsize(output_docx)} bytes).")

# 6. Atualizar arquivo canônico
shutil.copyfile(output_docx, CANONICAL_DOCX)
print(f"10. Canônico atualizado com sucesso:\n    {CANONICAL_DOCX}")

# 7. Backup pós-modificação
post_backup = os.path.join(BACKUP_DIR, f"TCC_Victor_Bruno_VFinal_backup_{timestamp}.docx")
shutil.copyfile(CANONICAL_DOCX, post_backup)
print(f"11. Backup datado oficial pós-modificação gravado:\n    {post_backup}")

print("=" * 80)
print("OPERAÇÃO CONCLUÍDA COM SUCESSO!")
print("=" * 80)

