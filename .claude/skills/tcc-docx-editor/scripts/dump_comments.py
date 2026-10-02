# -*- coding: utf-8 -*-
"""Lista os comentários do DOCX com o trecho que cada um marca.

Uso: python.exe dump_comments.py <arquivo.docx> [--grep padrão] [--autor nome] [--abertos]
                                  [--blocos ini-fim]

  --grep   filtra por regex (sem diferenciar maiúsculas) no texto do
           comentário OU no trecho ancorado
  --autor  filtra pelo autor (parcial)
  --abertos  esconde comentários marcados como resolvidos
  --blocos   só os comentários cuja âncora começa nesse intervalo de blocos
             (inclusivo): é o mapa de comentários do passo 3 do workflow,
             para decidir quais recebem "Feito." e reancorar os que caem
             em parágrafo substituído

Lê o .docx direto, inclusive com o Word aberto: se o lock impedir a leitura,
copia pela API do Windows (CopyFileW, que o lock não bloqueia) para C:\\Temp.
Saída por comentário: id, autor, data, estado, índice de bloco do parágrafo
(mesma numeração de dump_blocks/find_text), trecho ancorado e texto. Respostas
aparecem recuadas sob o comentário-pai.
"""
import ctypes, io, os, re, sys, zipfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def opt(name):
    a = sys.argv
    return a[a.index(name) + 1] if name in a else None


def open_docx(path):
    try:
        return zipfile.ZipFile(path)
    except PermissionError:
        tmp = r'C:\Temp\_dump_comments_copy.docx'
        os.makedirs(r'C:\Temp', exist_ok=True)
        if not ctypes.windll.kernel32.CopyFileW(os.path.abspath(path), tmp, False):
            raise
        return zipfile.ZipFile(tmp)


def text_of(x):
    return ''.join(m.group(1) if m.group(1) is not None else ' '
                   for m in re.finditer(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>|<w:tab/>|<w:br/>', x))


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print(__doc__); sys.exit(0)
    z = open_docx(sys.argv[1])
    names = z.namelist()
    if 'word/comments.xml' not in names:
        print('Documento sem comentários.'); return
    doc = z.read('word/document.xml').decode('utf-8')
    com = z.read('word/comments.xml').decode('utf-8')
    ext = z.read('word/commentsExtended.xml').decode('utf-8') if 'word/commentsExtended.xml' in names else ''

    # paraId do último parágrafo de cada comentário → id; estado/pai vêm do commentsExtended
    comments, para2id = {}, {}
    for m in re.finditer(r'<w:comment\b([^>]*)>(.*?)</w:comment>', com, re.S):
        attrs, body = m.groups()
        cid = re.search(r'w:id="(\d+)"', attrs).group(1)
        get = lambda k: (re.search(rf'w:{k}="([^"]*)"', attrs) or [None, ''])[1]
        paras = re.findall(r'w14:paraId="([0-9A-F]+)"', body)
        if paras:
            para2id[paras[-1]] = cid
        comments[cid] = dict(autor=get('author'), data=get('date')[:10],
                             texto=' / '.join(t for t in (text_of(p) for p in
                                   re.findall(r'<w:p\b.*?</w:p>', body, re.S)) if t))
    done, parent = {}, {}
    for m in re.finditer(r'<w15:commentEx\b([^>]*)/>', ext):
        a = m.group(1)
        pid = re.search(r'w15:paraId="([0-9A-F]+)"', a).group(1)
        cid = para2id.get(pid)
        if not cid:
            continue
        done[cid] = 'w15:done="1"' in a
        pp = re.search(r'w15:paraIdParent="([0-9A-F]+)"', a)
        if pp and pp.group(1) in para2id:
            parent[cid] = para2id[pp.group(1)]

    # trecho ancorado: texto entre commentRangeStart e commentRangeEnd; bloco do início
    body = doc[doc.index('<w:body>'):]
    blocks = [(b.start(), b.end()) for b in re.finditer(
        r'<w:tbl>.*?</w:tbl>|<w:p\b[^>]*>.*?</w:p>|<w:p\b[^>]*/>', body, re.S)]
    for cid, c in comments.items():
        s = re.search(rf'<w:commentRangeStart w:id="{cid}"/>', body)
        e = re.search(rf'<w:commentRangeEnd w:id="{cid}"/>', body)
        c['trecho'] = text_of(body[s.end():e.start()]) if s and e else ''
        c['bloco'] = next((i for i, (a, b) in enumerate(blocks) if s and a <= s.start() < b), '?')

    pat, autor, abertos = opt('--grep'), opt('--autor'), '--abertos' in sys.argv
    faixa = tuple(int(v) for v in opt('--blocos').split('-')) if opt('--blocos') else None

    def keep(cid):
        c = comments[cid]
        if autor and autor.lower() not in c['autor'].lower():
            return False
        if abertos and done.get(cid):
            return False
        if faixa and not (isinstance(c['bloco'], int) and faixa[0] <= c['bloco'] <= faixa[1]):
            return False
        return not pat or re.search(pat, c['texto'] + ' ' + c['trecho'], re.I)

    roots = [cid for cid in comments if cid not in parent]
    shown = 0
    for cid in roots:
        replies = [r for r in comments if parent.get(r) == cid]
        if not (keep(cid) or any(keep(r) for r in replies)):
            continue
        c = comments[cid]; shown += 1
        estado = 'resolvido' if done.get(cid) else 'aberto'
        trecho = c['trecho'] if len(c['trecho']) <= 220 else c['trecho'][:220] + '…'
        print(f"#{cid} [{c['autor']} {c['data']} {estado}] bloco {c['bloco']}")
        print(f"  trecho: «{trecho}»")
        print(f"  {c['texto']}")
        for r in replies:
            print(f"    ↳ #{r} [{comments[r]['autor']}] {comments[r]['texto']}")
        print()
    print(f'{shown} comentário(s) de {len(roots)}')


if __name__ == '__main__':
    main()
