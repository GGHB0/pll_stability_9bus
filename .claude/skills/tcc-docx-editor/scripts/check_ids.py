# -*- coding: utf-8 -*-
"""Estado dos IDs do documento (rodar SEMPRE antes de inserir elementos novos —
o Word renumera IDs ao salvar, o registro do KB pode estar obsoleto).

Uso: python.exe check_ids.py <document.xml>
"""
import re, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

xml = open(sys.argv[1], encoding='utf-8').read()

bm = [int(x) for x in re.findall(r'<w:bookmarkStart w:id="(\d+)"', xml)]
print(f'bookmarkStart: max={max(bm)} count={len(bm)} -> proximo livre: {max(bm)+1}')

ins = [int(x) for x in re.findall(r'<w:ins w:id="(\d+)"', xml)]
dele = [int(x) for x in re.findall(r'<w:del w:id="(\d+)"', xml)]
allrev = ins + dele
print(f'w:ins ids: {sorted(set(ins))[:20]}{"..." if len(set(ins)) > 20 else ""} | '
      f'w:del count={len(dele)} -> proximo livre: {max(allrev)+1 if allrev else 1}')

fb = sorted(int(x, 16) for x in re.findall(r'w14:paraId="(1FB[0-9A-Fa-f]{5})"', xml))
ours = [x for x in fb if x < 0x1FB01000]
print(f'paraId 1FB0xxxx (nossos): max={hex(max(ours)) if ours else None} '
      f'-> proximo livre: {hex(max(ours)+1) if ours else "0x1FB00000"}')

toc = re.search(r'<w:fldChar w:fldCharType="begin"([^>]*)/>', xml)
print(f'TOC dirty flag: {"SIM" if toc and "w:dirty" in toc.group(1) else "NAO (marcar antes de entregar)"}')

tocn = [int(x) for x in re.findall(r'_Toc235351(\d+)"', xml)]
print(f'bookmarks _Toc235351NNN: max NNN={max(tocn) if tocn else None} '
      f'-> proximo livre: {max(tocn)+1 if tocn else None}')
