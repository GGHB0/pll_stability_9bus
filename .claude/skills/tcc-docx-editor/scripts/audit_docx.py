# -*- coding: utf-8 -*-
"""Auditoria estrutural de um .docx antes da entrega.

    python.exe audit_docx.py <arquivo.docx> [--util-in 6.30]

Checa o que o Word tolera ao ABRIR mas reclama ao SALVAR, mais os defeitos
que so aparecem depois (referencia quebrada no sumario, figura estourando a
margem). Sai com codigo 1 se algum item FALHOU.

Motivado por 2026-09-02: um DOCX montado a mao abria e exportava PDF, mas o
Word recusava o upload ("CARREGAMENTO BLOQUEADO"). Esta auditoria e o que
provou que o problema nao era o conteudo. Ver mesclagem_no_canonico.md.
"""
import sys, re, io, zipfile, collections
import xml.etree.ElementTree as ET

BLOCO = r"<w:p\b[^>]*/>|<w:p\b[^>]*>.*?</w:p>|<w:tbl>.*?</w:tbl>"
EMU_POR_TWIP = 635

falhas, avisos = [], []


def ok(cond, msg, grave=True):
    if cond:
        print("  OK    %s" % msg)
    else:
        (falhas if grave else avisos).append(msg)
        print("  %s %s" % ("FALHOU" if grave else "aviso ", msg))


def main(caminho, util_in=None):
    z = zipfile.ZipFile(caminho)
    partes = [i.filename for i in z.infolist()]
    doc = z.read("word/document.xml").decode("utf-8")

    print("\n== %s (%d partes) ==" % (caminho, len(partes)))

    print("\n-- XML --")
    try:
        ET.fromstring(doc.encode("utf-8"))
        ok(True, "document.xml bem-formado")
    except Exception as e:
        ok(False, "document.xml NAO e bem-formado: %s" % e)
    dup = [k for k, v in collections.Counter(partes).items() if v > 1]
    ok(not dup, "sem partes duplicadas no zip (%s)" % (dup or "-"))

    print("\n-- comentarios --")
    if "word/comments.xml" in partes:
        cm = z.read("word/comments.xml").decode("utf-8")
        defs = set(re.findall(r'<w:comment [^>]*w:id="(\d+)"', cm))
        pares = {}
        for tag in ("commentRangeStart", "commentRangeEnd", "commentReference"):
            ids = set(re.findall(r'<w:%s w:id="(\d+)"' % tag, doc))
            pares[tag] = ids
            orf = sorted(ids - defs)
            ok(not orf, "%s sem definicao em comments.xml (%s)" % (tag, orf or "-"))
        ok(pares["commentRangeStart"] == pares["commentRangeEnd"],
           "commentRangeStart casa com commentRangeEnd")
        # partes auxiliares nao podem apontar para comentario que saiu
        vivos = set(x.upper() for x in
                    re.findall(r'w14:paraId="([0-9A-Fa-f]+)"', cm))
        for aux in ("word/commentsExtended.xml", "word/commentsIds.xml"):
            if aux in partes:
                s = z.read(aux).decode("utf-8")
                refs = set(x.upper() for x in
                           re.findall(r'paraId="([0-9A-Fa-f]+)"', s))
                orf = sorted(refs - vivos)
                ok(not orf, "%s sem orfaos (%s)" % (aux.split("/")[-1], orf or "-"))
    else:
        print("  (documento sem comentarios)")

    print("\n-- bookmarks --")
    bs = re.findall(r'<w:bookmarkStart w:id="(\d+)"[^>]*w:name="([^"]*)"', doc)
    be = set(re.findall(r'<w:bookmarkEnd w:id="(\d+)"', doc))
    sids = [a for a, _ in bs]
    nomes = [n for _, n in bs]
    ok(not (set(sids) - be), "todo bookmarkStart tem End (%s)"
       % (sorted(set(sids) - be) or "-"))
    ok(not (be - set(sids)), "todo bookmarkEnd tem Start (%s)"
       % (sorted(be - set(sids)) or "-"))
    ok(len(set(sids)) == len(sids), "ids de bookmark unicos")
    ok(len(set(nomes)) == len(nomes), "nomes de bookmark unicos")

    print("\n-- campos --")
    b = doc.count('w:fldCharType="begin"')
    s_ = doc.count('w:fldCharType="separate"')
    e = doc.count('w:fldCharType="end"')
    ok(b == e, "fldChar begin(%d) == end(%d)" % (b, e))
    ok(s_ <= b, "separate(%d) <= begin(%d)" % (s_, b))
    refs = set(re.findall(r"PAGEREF (_\w+)", doc))
    orf = sorted(refs - set(nomes))
    ok(not orf, "PAGEREF sem bookmark (viraria 'Erro! Indicador nao definido'): %s"
       % (orf[:8] if orf else "-"))
    d = doc.count('w:dirty="true"')
    ok(d == 0, "nenhum campo marcado dirty (%d) — arquivo abre sem pedir "
                "atualizacao e sem ficar modificado na hora" % d, grave=False)

    print("\n-- imagens --")
    rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
    alvo = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
    emb = sorted(set(re.findall(r'r:embed="(rId\d+)"', doc)),
                 key=lambda x: int(x[3:]))
    semrel = [x for x in emb if x not in alvo]
    ok(not semrel, "todo r:embed tem relationship (%s)" % (semrel or "-"))
    faltando = [alvo[x] for x in emb
                if x in alvo and "word/" + alvo[x].lstrip("./") not in partes]
    ok(not faltando, "todo alvo de imagem existe no zip (%s)" % (faltando or "-"))
    ids = re.findall(r'<wp:docPr id="(\d+)"', doc)
    rep = [k for k, v in collections.Counter(ids).items() if v > 1]
    ok(not rep, "docPr unicos (%d) (%s)" % (len(ids), rep or "-"))

    if util_in is None:
        mp = re.search(r'<w:pgSz w:w="(\d+)"', doc)
        mm = re.search(r'<w:pgMar w:top="\d+" w:right="(\d+)"'
                       r' w:bottom="\d+" w:left="(\d+)"', doc)
        if mp and mm:
            tw = int(mp.group(1)) - int(mm.group(1)) - int(mm.group(2))
            util_in = tw / 1440.0
    if util_in:
        lim = int(round(util_in * 1440 * EMU_POR_TWIP))
        larg = [int(a) for a, _ in
                re.findall(r'<wp:extent cx="(\d+)" cy="(\d+)"/>', doc)]
        est = [w for w in larg if w > lim]
        ok(not est, "nenhuma imagem passa da area util de %.2f in (%s)"
           % (util_in, ["%.2f in" % (w / 914400.0) for w in est] or "-"))

    print("\n-- content types e rels --")
    ct = z.read("[Content_Types].xml").decode("utf-8")
    ov = set(re.findall(r'PartName="/([^"]+)"', ct))
    ext = set(x.lower() for x in re.findall(r'Extension="([^"]+)"', ct))
    sem = [n for n in partes if n != "[Content_Types].xml" and n not in ov
           and n.rsplit(".", 1)[-1].lower() not in ext]
    ok(not sem, "toda parte tem content-type (%s)" % (sem or "-"))

    print("\n-- convencoes do TCC --")
    ok("—" not in doc, "sem em-dash (—) no texto")
    cod = [w for w in ("params.m", "FAULT_TYPE", "export_sim_data", "app.py",
                       ".csv", ".slx")
           if re.search(r"<w:t[^>]*>[^<]*%s" % re.escape(w), doc)]
    ok(not cod, "sem linguagem de codigo no corpo (%s)" % (cod or "-"), grave=False)

    print("\n== %d falha(s), %d aviso(s) ==" % (len(falhas), len(avisos)))
    for f in falhas:
        print("  FALHOU: %s" % f)
    return 1 if falhas else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    u = None
    if "--util-in" in sys.argv:
        u = float(sys.argv[sys.argv.index("--util-in") + 1])
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                  errors="replace")
    sys.exit(main(sys.argv[1], u))
