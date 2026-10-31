# -*- coding: utf-8 -*-
"""
test_apendice_setup.py
Testa copia das 4 imagens e preparacao dos relacionamentos.
"""

import os
import shutil

BASE_DIR = r"C:\Temp\tcc_banca\unpacked"
MEDIA_DIR = os.path.join(BASE_DIR, "word", "media")
SOURCE_DIR = r"c:\pll_stability_9bus\output\verifica_palco\1920x1080"

images = [
    ("03_local_p2_fasor_mouse.png", "image36.png", "rId49"),
    ("04_seqneg_p2.png", "image37.png", "rId50"),
    ("06_sinc_p2.png", "image38.png", "rId51"),
    ("07_ons_p5.png", "image39.png", "rId52"),
]

for src_name, dst_name, rid in images:
    src_path = os.path.join(SOURCE_DIR, src_name)
    dst_path = os.path.join(MEDIA_DIR, dst_name)
    shutil.copyfile(src_path, dst_path)
    print(f"Copiado {src_name} -> {dst_name} ({os.path.getsize(dst_path)} bytes)")

print("Imagens copiadas com sucesso!")

