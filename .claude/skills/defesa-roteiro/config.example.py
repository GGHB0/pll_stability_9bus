"""Caminhos pessoais da skill defesa-roteiro.

Copiar para config.py (gitignored) só se a busca automática de scripts/caminhos.py
não achar a pasta do TCC no OneDrive desta máquina. Sem config.py, a skill tenta:
  ~/OneDrive/Meus Bagulhos/Arquivos/UERJ/TCC - Victor e Bruno   (Victor)
  ~/OneDrive/UERJ/TCC - Victor e Bruno                          (Bruno)
"""

# Pasta "TCC - Victor e Bruno" do OneDrive (contém "Template Modelo TCC" e "Bibliografia")
TCC_DIR = r"C:\Users\<usuario>\OneDrive\UERJ\TCC - Victor e Bruno"

# Miniaturas dos slides (s01.png...), geradas pelo render.ps1 da skill tcc-pptx-editor
SLIDES_PNG = r"C:\Temp\defesa_roteiro\png"
