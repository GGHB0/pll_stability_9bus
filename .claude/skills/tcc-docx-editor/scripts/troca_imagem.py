# -*- coding: utf-8 -*-
"""Troca o PNG de uma figura que já está no DOCX, mantendo a largura.

Uso: python.exe troca_imagem.py <staging.docx> <novo.png> <saida.docx>
                                (--rid rIdN | --apos "trecho de texto")

--apos: pega o primeiro desenho depois do trecho (ex.: "Figura 4.2 – Circuito",
a legenda fica acima da imagem, D3). --rid: o r:embed direto.

Substitui o arquivo de mídia e recalcula o cy (wp:extent + a:ext daquele
desenho) pela proporção do PNG novo; cx fica. O document.xml é editado como
texto bruto (nunca ET.write no documento inteiro). Depois: word_finalize.ps1
→ audit_docx.py → entrega.ps1, como qualquer edição.

Nasceu da troca das Figuras 4.1 (2026-10-02) e 4.2 (2026-10-03), as duas
feitas à mão com o mesmo zip reescrito.
"""
import argparse, io, re, struct, sys, zipfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ap = argparse.ArgumentParser()
ap.add_argument('docx'); ap.add_argument('png'); ap.add_argument('saida')
g = ap.add_mutually_exclusive_group(required=True)
g.add_argument('--rid'); g.add_argument('--apos')
a = ap.parse_args()

zin = zipfile.ZipFile(a.docx)
xml = zin.read('word/document.xml').decode('utf-8')
rels = zin.read('word/_rels/document.xml.rels').decode('utf-8')

if a.apos:
    # A legenda se repete na Lista de Ilustrações: vale só a ocorrência com
    # um desenho até 2 parágrafos depois (legenda → imagem). Em 2026-10-03 a
    # 1ª ocorrência era a da lista e o desenho seguinte, outra figura.
    # O número da legenda é campo SEQ partido em runs: comparar pelo texto
    # juntado de cada parágrafo, não pelo XML bruto.
    paras = list(re.finditer(r'<w:p[ >].*?</w:p>', xml, re.S))
    texto = lambda p: ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', p.group(0)))
    achados = []
    for j, p in enumerate(paras):
        if a.apos in texto(p):
            for q in paras[j + 1:j + 3]:
                e = re.search(r'r:embed="(rId\d+)"', q.group(0))
                if e:
                    achados.append(e.group(1)); break
    assert len(achados) == 1, f'{len(achados)} legendas com desenho logo abaixo: {achados}'
    rid = achados[0]
else:
    rid = a.rid

alvo = re.search(r'Id="%s"[^>]*Target="([^"]+)"' % rid, rels) or \
       re.search(r'Target="([^"]+)"[^>]*Id="%s"' % rid, rels)
media = 'word/' + alvo.group(1)

# o <w:drawing> que contém esse r:embed
k = xml.index(f'r:embed="{rid}"')
ini = xml.rfind('<w:drawing>', 0, k); fim = xml.index('</w:drawing>', k)
d = xml[ini:fim]
cx, cy = map(int, re.search(r'<wp:extent cx="(\d+)" cy="(\d+)"', d).groups())

png = open(a.png, 'rb').read()
assert png[:8] == b'\x89PNG\r\n\x1a\n', 'não é PNG'
w, h = struct.unpack('>II', png[16:24])
ow, oh = struct.unpack('>II', zin.read(media)[16:24])
cy_novo = round(cx * h / w)

d2 = d.replace(f'cx="{cx}" cy="{cy}"', f'cx="{cx}" cy="{cy_novo}"')
assert d2.count(f'cy="{cy_novo}"') == 2, 'esperava wp:extent + a:ext'
xml = xml[:ini] + d2 + xml[fim:]

with zipfile.ZipFile(a.saida, 'w', zipfile.ZIP_DEFLATED) as zout:
    for it in zin.infolist():
        data = zin.read(it.filename)
        if it.filename == 'word/document.xml':
            data = xml.encode('utf-8')
        elif it.filename == media:
            data = png
        zout.writestr(it, data)

print(f'{rid} → {media}')
print(f'PNG antigo {ow}x{oh} → novo {w}x{h}')
print(f'cy {cy} → {cy_novo} (cx {cx} = {cx/914400:.2f} in)')
