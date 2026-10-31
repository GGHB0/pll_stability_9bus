# -*- coding: utf-8 -*-
"""
organize_onedrive_folders.py
Organiza a pasta 'Template Modelo TCC' da UERJ no OneDrive:
- Cria categorias numeradas limpas para cada tela;
- Move arquivos intermediarios e obsoletos para subpastas '_versoes_anteriores' e '_arquivo_historico';
- Mantem juncao/link de compatibilidade para 'comentado'.
"""

import os
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r"C:\Users\gilbr\OneDrive\UERJ\TCC - Victor e Bruno\Template Modelo TCC"

print(f"Iniciando organizacao em: {BASE}")

def safe_move(src, dst):
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)
        print(f"MOVIDO: {os.path.basename(src)} -> {os.path.relpath(dst, BASE)}")
    else:
        print(f"AVISO: {src} nao encontrado (pulando)")

# ------------------------------------------------------------------------------
# 1. 01_TCC_Monografia_Final
# ------------------------------------------------------------------------------
dir_tcc = os.path.join(BASE, "01_TCC_Monografia_Final")
dir_comentado = os.path.join(BASE, "comentado")

if os.path.exists(dir_comentado) and not os.path.islink(dir_comentado):
    os.rename(dir_comentado, dir_tcc)
    print("RENOMEADO: comentado -> 01_TCC_Monografia_Final")

dir_tcc_antigos = os.path.join(dir_tcc, "_versoes_anteriores")
os.makedirs(dir_tcc_antigos, exist_ok=True)

obsoletos_tcc = [
    "TCC_Victor_Bruno_V10.docx",
    "TCC_Victor_Bruno_V10.pdf",
    "TCC_Victor_Bruno_VF.docx",
    "TCC_Victor_Bruno_VF - Copia.docx",
]

for f in obsoletos_tcc:
    p = os.path.join(dir_tcc, f)
    if os.path.exists(p):
        safe_move(p, os.path.join(dir_tcc_antigos, f))

# Criar juncao de compatibilidade comentado -> 01_TCC_Monografia_Final
try:
    if not os.path.exists(dir_comentado):
        subprocess.run(f'cmd /c mklink /J "{dir_comentado}" "{dir_tcc}"', shell=True, check=True)
        print("CRIADA JUNCAO: comentado -> 01_TCC_Monografia_Final (compatibilidade total)")
except Exception as e:
    print(f"Aviso ao criar juncao (nao critico): {e}")

# ------------------------------------------------------------------------------
# 2. 02_Slides_Apresentacao
# ------------------------------------------------------------------------------
dir_slides = os.path.join(BASE, "02_Slides_Apresentacao")
dir_slides_antigos = os.path.join(dir_slides, "_versoes_anteriores")
os.makedirs(dir_slides_antigos, exist_ok=True)

safe_move(os.path.join(BASE, "Defesa_TCC_SRF-PLL.pptx"), os.path.join(dir_slides, "Defesa_TCC_SRF-PLL.pptx"))
safe_move(os.path.join(BASE, "Defesa_TCC_SRF-PLL.pdf"), os.path.join(dir_slides, "Defesa_TCC_SRF-PLL.pdf"))
safe_move(os.path.join(BASE, "Falas_Defesa_TCC.pptx"), os.path.join(dir_slides, "Falas_Defesa_TCC.pptx"))
safe_move(os.path.join(BASE, "Falas_Defesa_TCC_atualizado.pptx"), os.path.join(dir_slides_antigos, "Falas_Defesa_TCC_atualizado.pptx"))

# ------------------------------------------------------------------------------
# 3. 03_Roteiros_e_Guias_de_Estudo
# ------------------------------------------------------------------------------
dir_roteiros = os.path.join(BASE, "03_Roteiros_e_Guias_de_Estudo")
dir_roteiros_antigos = os.path.join(dir_roteiros, "_versoes_anteriores")
os.makedirs(dir_roteiros_antigos, exist_ok=True)

safe_move(os.path.join(BASE, "Roteiro_e_Guia_de_Estudos_Defesa_TCC.docx"), os.path.join(dir_roteiros, "Roteiro_e_Guia_de_Estudos_Defesa_TCC.docx"))
safe_move(os.path.join(BASE, "roteiro_estudo_defesa.pdf"), os.path.join(dir_roteiros, "roteiro_estudo_defesa.pdf"))
safe_move(os.path.join(BASE, "Roteiro_Falas_e_Tempo_Defesa_TCC.docx"), os.path.join(dir_roteiros, "Roteiro_Falas_e_Tempo_Defesa_TCC.docx"))
safe_move(os.path.join(BASE, "Roteiro_Falas_e_Tempo_Defesa_TCC_atualizado.docx"), os.path.join(dir_roteiros_antigos, "Roteiro_Falas_e_Tempo_Defesa_TCC_atualizado.docx"))

# ------------------------------------------------------------------------------
# 4. 04_Audios_Defesa
# ------------------------------------------------------------------------------
dir_audios = os.path.join(BASE, "04_Audios_Defesa")
os.makedirs(dir_audios, exist_ok=True)

safe_move(os.path.join(BASE, "audios_defesa"), os.path.join(dir_audios, "audios_defesa"))
safe_move(os.path.join(BASE, "audios_defesa.zip"), os.path.join(dir_audios, "audios_defesa.zip"))
safe_move(os.path.join(BASE, "audios_teste"), os.path.join(dir_audios, "_testes", "audios_teste"))

# ------------------------------------------------------------------------------
# 5. 05_Templates_Originais_UERJ
# ------------------------------------------------------------------------------
dir_templates = os.path.join(BASE, "05_Templates_Originais_UERJ")
os.makedirs(dir_templates, exist_ok=True)

safe_move(os.path.join(BASE, "Modelo TCCs e Monografias_Engenharia.doc"), os.path.join(dir_templates, "Modelo TCCs e Monografias_Engenharia.doc"))
safe_move(os.path.join(BASE, "Modelo TCCs e Monografias_Engenharia1.doc"), os.path.join(dir_templates, "Modelo TCCs e Monografias_Engenharia1.doc"))
safe_move(os.path.join(BASE, "Link template TCC em Overleaf.docx"), os.path.join(dir_templates, "Link template TCC em Overleaf.docx"))

# ------------------------------------------------------------------------------
# 6. _Arquivo_Historico
# ------------------------------------------------------------------------------
dir_historico = os.path.join(BASE, "_Arquivo_Historico")
os.makedirs(dir_historico, exist_ok=True)

safe_move(os.path.join(BASE, "Fragmentos"), os.path.join(dir_historico, "Fragmentos"))
safe_move(os.path.join(BASE, "Versoes antigas"), os.path.join(dir_historico, "Versoes antigas"))
safe_move(os.path.join(BASE, "_backups"), os.path.join(dir_historico, "_backups_defesa_antigos"))

print("\n--- ORGANIZACAO CONCLUIDA COM SUCESSO! ---")

