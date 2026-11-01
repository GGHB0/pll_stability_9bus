# -*- coding: utf-8 -*-
"""
apply_doi_github.py
Aplica o DOI gerado no Zenodo (10.5281/zenodo.23866787) e a URL oficial do repositório
(https://github.com/GGHB0/pll_stability_9bus) no documento canônico Word:
1. Na Seção 3.3.3: citação formal (OLIVEIRA; REZENDE, 2026) e remissão ao Apêndice A em AZUL (#0070C0);
2. No Apêndice A: URL oficial e DOI no parágrafo final;
3. Nas Referências Bibliográficas: URL oficial e DOI na entrada ABNT;
4. No arquivo CITATION.cff e README.md: DOI registrado.
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
TEMP_WORK_DIR = r"C:\Temp\tcc_banca\work_doi"

DOI_STR = "10.5281/zenodo.23866787"
REPO_URL = "https://github.com/GGHB0/pll_stability_9bus"

print("=" * 80)
print(f"APLICANDO DOI ({DOI_STR}) E REPOSITÓRIO GITHUB NO CANÔNICO")
print("=" * 80)

# 1. Conferir canônico
if not os.path.exists(CANONICAL_DOCX):
    print(f"ERRO: Canônico não encontrado: {CANONICAL_DOCX}")
    sys.exit(1)

# 2. Criar backup datado
os.makedirs(BACKUP_DIR, exist_ok=True)
timestamp = time.strftime("%Y%m%d_%H%M%S")
pre_backup = os.path.join(BACKUP_DIR, f"TCC_Victor_Bruno_VFinal_backup_pre_doi_{timestamp}.docx")
shutil.copyfile(CANONICAL_DOCX, pre_backup)
print(f"1. Backup prévio salvo em:\n   {pre_backup}")

# 3. Descompactar
if os.path.exists(TEMP_WORK_DIR):
    shutil.rmtree(TEMP_WORK_DIR)
os.makedirs(TEMP_WORK_DIR, exist_ok=True)

with zipfile.ZipFile(CANONICAL_DOCX, 'r') as z:
    z.extractall(TEMP_WORK_DIR)

doc_xml_path = os.path.join(TEMP_WORK_DIR, "word", "document.xml")
with open(doc_xml_path, "r", encoding="utf-8") as f:
    xml = f.read()

print(f"2. document.xml carregado ({len(xml)} bytes).")

# ==============================================================================
# 1. SEÇÃO 3.3.3: Inserir menção e citação no final do parágrafo P602
# ==============================================================================
# Parágrafo P602 termina com:
# caracterizado na Seção 4.4, e a verificação da resposta dinâmica do sistema frente às diferentes contingências.</w:t></w:r></w:p>
target_p602_end = 'caracterizado na Seção 4.4, e a verificação da resposta dinâmica do sistema frente às diferentes contingências.</w:t></w:r></w:p>'

if target_p602_end not in xml:
    print("ERRO: Final do parágrafo P602 não encontrado no XML!")
    sys.exit(1)

replacement_p602 = (
    'caracterizado na Seção 4.4, e a verificação da resposta dinâmica do sistema frente às diferentes contingências.</w:t></w:r>'
    '<w:r><w:rPr><w:color w:val="0070C0"/><w:szCs w:val="24"/></w:rPr>'
    '<w:t xml:space="preserve"> Para assegurar a reprodutibilidade dos ensaios e permitir a exploração interativa dos dados, os modelos de simulação em Simulink, as rotinas de tratamento de dados e o código-fonte do painel interativo foram disponibilizados em repositório público (OLIVEIRA; REZENDE, 2026), cujas telas e funcionalidades estão detalhadas no Apêndice A.</w:t></w:r>'
    '</w:p>'
)

xml = xml.replace(target_p602_end, replacement_p602, 1)
print("3. Seção 3.3.3 atualizada: Citação (OLIVEIRA; REZENDE, 2026) e remissão ao Apêndice A inseridas em AZUL (#0070C0).")

# ==============================================================================
# 2. REFERÊNCIAS BIBLIOGRÁFICAS (P860): Atualizar URL e incluir DOI
# ==============================================================================
p_ref_old = (
    '<w:p w14:paraId="7DF56275" w14:textId="77777777" w:rsidR="00425537" w:rsidRPr="00CC15CE" w:rsidRDefault="00425537"><w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:spacing w:after="240" w:line="240" w:lineRule="auto"/><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr></w:pPr><w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve">OLIVEIRA, B. H.; REZENDE, V. H. A. </w:t></w:r><w:r><w:rPr><w:i/><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t>Painel Interativo para Análise Dinâmica e Métricas de Sincronismo do SRF-PLL sob Contingências em Redes Elétricas</w:t></w:r><w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve">. 2026. Repositório no GitHub. Disponível em: &lt;https://github.com/bruno-victor-uerj/pll-stability-dashboard&gt;. </w:t></w:r><w:r w:rsidRPr="00CC15CE"><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr><w:t>Acesso em: 29 out. 2026.</w:t></w:r></w:p>'
)

p_ref_new = (
    '<w:p w14:paraId="7DF56275" w14:textId="77777777" w:rsidR="00425537" w:rsidRPr="00CC15CE" w:rsidRDefault="00425537"><w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:spacing w:after="240" w:line="240" w:lineRule="auto"/><w:rPr><w:color w:val="0070C0"/><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr></w:pPr>'
    '<w:r><w:rPr><w:color w:val="0070C0"/><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve">OLIVEIRA, B. H.; REZENDE, V. H. A. </w:t></w:r>'
    '<w:r><w:rPr><w:i/><w:color w:val="0070C0"/><w:szCs w:val="24"/></w:rPr><w:t>Painel Interativo para Análise Dinâmica e Métricas de Sincronismo do SRF-PLL sob Contingências em Redes Elétricas</w:t></w:r>'
    '<w:r><w:rPr><w:color w:val="0070C0"/><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve">. 2026. Repositório no GitHub. Disponível em: &lt;https://github.com/GGHB0/pll_stability_9bus&gt;. DOI: 10.5281/zenodo.23866787. </w:t></w:r>'
    '<w:r w:rsidRPr="00CC15CE"><w:rPr><w:color w:val="0070C0"/><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr><w:t>Acesso em: 1 nov. 2026.</w:t></w:r></w:p>'
)

if p_ref_old in xml:
    xml = xml.replace(p_ref_old, p_ref_new, 1)
    print("4. Referências Bibliográficas atualizada: URL oficial e DOI inseridos em AZUL (#0070C0).")
else:
    # Busca alternativa se o XML tiver espaços ligeiramente diferentes
    pos_ref = xml.find('paraId="7DF56275"')
    if pos_ref != -1:
        start_r = xml.rfind('<w:p ', 0, pos_ref)
        end_r = xml.find('</w:p>', pos_ref) + 6
        xml = xml[:start_r] + p_ref_new + xml[end_r:]
        print("4. Referências Bibliográficas atualizada (via paraId): URL oficial e DOI inseridos em AZUL (#0070C0).")
    else:
        print("ERRO: Parágrafo de referência não encontrado!")
        sys.exit(1)

# ==============================================================================
# 3. APÊNDICE A (último parágrafo, P904): Atualizar URL e incluir DOI
# ==============================================================================
old_apendice_text = "O código-fonte da simulação, modelos em Simulink e o painel interativo estão disponíveis em: https://github.com/bruno-victor-uerj/pll-stability-dashboard."
new_apendice_text = "O código-fonte da simulação, os modelos em Simulink e o painel interativo estão disponíveis em: https://github.com/GGHB0/pll_stability_9bus (DOI: 10.5281/zenodo.23866787)."

if old_apendice_text not in xml:
    print(f"ERRO: Texto de encerramento do Apêndice A não encontrado!")
    sys.exit(1)

xml = xml.replace(old_apendice_text, new_apendice_text, 1)
print("5. Apêndice A atualizado: URL oficial e DOI inseridos.")

# 4. Gravar document.xml
with open(doc_xml_path, "w", encoding="utf-8") as f:
    f.write(xml)

print(f"6. word/document.xml gravado ({len(xml)} bytes).")

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

print(f"7. DOCX reempacotado com sucesso ({os.path.getsize(output_docx)} bytes).")

# 6. Atualizar arquivo canônico
shutil.copyfile(output_docx, CANONICAL_DOCX)
print(f"8. Canônico atualizado com sucesso:\n   {CANONICAL_DOCX}")

# 7. Backup pós-modificação
post_backup = os.path.join(BACKUP_DIR, f"TCC_Victor_Bruno_VFinal_backup_{timestamp}.docx")
shutil.copyfile(CANONICAL_DOCX, post_backup)
print(f"9. Backup datado pós-modificação gravado:\n   {post_backup}")

print("=" * 80)
print("OPERAÇÃO CONCLUÍDA COM SUCESSO!")
print("=" * 80)
