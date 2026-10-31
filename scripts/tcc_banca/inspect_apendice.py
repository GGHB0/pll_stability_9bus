# -*- coding: utf-8 -*-
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"C:\Temp\tcc_banca\unpacked"
DOC_XML = os.path.join(BASE_DIR, "word", "document.xml")
RELS_XML = os.path.join(BASE_DIR, "word", "_rels", "document.xml.rels")

with open(DOC_XML, "r", encoding="utf-8") as f:
    xml = f.read()

draw_idx = xml.find("<w:drawing>")
if draw_idx != -1:
    print("SAMPLE DRAWING:")
    print(xml[draw_idx:draw_idx+1200])

docpr_ids = [int(m.group(1)) for m in re.finditer(r'<wp:docPr\s+id="(\d+)"', xml)]
print("Max docPr id:", max(docpr_ids) if docpr_ids else "None")

with open(RELS_XML, "r", encoding="utf-8") as f:
    rels = f.read()

r_ids = [int(m.group(1)) for m in re.finditer(r'rId(\d+)', rels)]
print("Max rId:", max(r_ids) if r_ids else "None")

# Check images in media folder
media_dir = os.path.join(BASE_DIR, "word", "media")
if os.path.exists(media_dir):
    media_files = os.listdir(media_dir)
    print(f"Total media files: {len(media_files)}")
    print("Sample media files:", media_files[:5])

