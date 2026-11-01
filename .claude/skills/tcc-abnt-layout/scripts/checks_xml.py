"""Conferencias ABNT sobre o document.xml. Usadas pelo check_abnt.py.

Cada funcao imprime o seu bloco e registra em FALHAS/AVISOS. Read-only.
"""
import re
import html
import collections

FALHAS = []
AVISOS = []


def ok(msg):
    print(f"  OK    {msg}")


def falha(msg):
    FALHAS.append(msg)
    print(f"  FALHA {msg}")


def aviso(msg):
    AVISOS.append(msg)
    print(f"  aviso {msg}")


def texto(frag):
    return html.unescape(re.sub(r'<[^>]+>', '', frag)).strip()


def paragrafos(body):
    return re.findall(r'<w:p\b[^>]*>.*?</w:p>|<w:p\b[^>]*/>', body, re.S)


def corpo(paras):
    """Do titulo do Cap. 1 ate REFERENCIAS. Pre-texto tem brasao sem legenda
    e resumo sem recuo por norma; referencia nao leva recuo."""
    ini = next((i for i, p in enumerate(paras) if 'w:val="Ttulo1"' in p and texto(p)), 0)
    fim = next((i for i, p in enumerate(paras) if i > ini and texto(p) == 'REFERÊNCIAS'), len(paras))
    return paras[ini:fim]


def paginacao(x):
    print("\n-- paginacao --")
    sects = re.findall(r'<w:sectPr\b.*?</w:sectPr>', x, re.S)
    print(f"  ({len(sects)} secao(oes))")
    for i, s in enumerate(sects, 1):
        htypes = re.findall(r'<w:headerReference[^>]*w:type="(\w+)"', s)
        ftypes = re.findall(r'<w:footerReference[^>]*w:type="(\w+)"', s)
        start = re.findall(r'<w:pgNumType[^>]*w:start="(\d+)"', s)
        print(f"  secao {i}: headers={htypes or '-'} footers={ftypes or '-'} "
              f"pgNumType start={start or '-'}")
        if i > 1 and not ftypes:
            falha(f"secao {i} nao declara nenhum footerReference — herda o "
                  f"rodape (possivelmente numerado) da secao anterior")
        elif i > 1 and 'even' not in ftypes:
            aviso(f"secao {i} declara footer default mas nao 'even' — "
                  f"herda o rodape da secao anterior nas paginas pares "
                  f"(so importa com evenAndOddHeaders ligado)")


def evenodd(settings_path):
    print("\n-- evenAndOddHeaders --")
    if not settings_path:
        # sem isso lia o proprio XML e dava falso "desligado" (2026-09-13)
        aviso("settings.xml nao informado — passe --settings quando o XML "
              "nao se chamar document.xml")
        return
    try:
        s = open(settings_path, encoding='utf-8').read()
    except OSError:
        aviso(f"settings.xml nao encontrado em {settings_path} — pulei")
        return
    if 'evenAndOddHeaders' in s:
        aviso("evenAndOddHeaders LIGADO: toda secao precisa dos 4 pares "
              "header/footer (even+default) ou herda o que sobrou")
    else:
        ok("evenAndOddHeaders desligado")


CAP = re.compile(r'^(Figura|Quadro|Tabela|Gr[áa]fico)\s*\d')


def _legendas(paras):
    return [p for p in paras if CAP.match(texto(p))]


def _imagens(paras):
    return [p for p in paras if '<a:blip' in p or '<w:drawing>' in p]


def keepnext(paras):
    print("\n-- keepNext em legenda e imagem --")
    legs, imgs = _legendas(paras), _imagens(paras)
    print(f"  keepNext no corpo: {sum(1 for p in paras if '<w:keepNext/>' in p)}")
    for nome, grupo, risco in (
            ("legenda", legs, "podem se separar da imagem"),
            ("imagem", imgs, "o 'Fonte:' pode cair sozinho na folha seguinte")):
        sem = [p for p in grupo if '<w:keepNext/>' not in p]
        if sem:
            falha(f"{len(sem)}/{len(grupo)} {nome}(s) sem keepNext — {risco}")
        elif grupo:
            ok(f"todas as {len(grupo)} {nome}s com keepNext")


def legendas(paras):
    print("\n-- legenda e fonte --")
    legs = _legendas(paras)
    fontes = [p for p in paras if texto(p).startswith('Fonte:')]
    imgs = _imagens(paras)
    print(f"  {len(legs)} legenda(s), {len(fontes)} linha(s) 'Fonte:', {len(imgs)} imagem(ns)")
    if len(legs) != len(fontes):
        aviso(f"legendas ({len(legs)}) e fontes ({len(fontes)}) nao batem — a "
              f"ABNT pede fonte mesmo quando a figura e do proprio autor")
    seq = sum(1 for p in legs if 'SEQ' in p)
    if legs and not seq:
        aviso("nenhuma legenda usa campo SEQ — a Lista de Ilustracoes nao "
              "pode ser gerada pelo Word")
    elif legs:
        ok(f"{seq}/{len(legs)} legendas com campo SEQ")
    for nome, grupo in (("legenda", legs), ("fonte", fontes)):
        centr = sum(1 for p in grupo if 'w:jc w:val="center"' in p)
        if centr:
            aviso(f"{centr} {nome}(s) centralizada(s) — ABNT alinha a esquerda")
    if len(legs) < len(imgs):
        falha(f"{len(imgs) - len(legs)} imagem(ns) sem legenda")


def recuo(paras, alvo):
    print(f"\n-- recuo de primeira linha (alvo {alvo} twips) --")
    c = collections.Counter()
    for p in paras:
        t = texto(p)
        if len(t) < 120 or re.match(r'^(Figura|Quadro|Tabela|Gr[áa]fico|Fonte:)', t):
            continue
        pr = re.search(r'<w:pPr>.*?</w:pPr>', p, re.S)
        pr = pr.group(0) if pr else ''
        if re.search(r'w:pStyle w:val="(Ttulo|Sumrio|PargrafodaLista)|<w:numPr>|'
                     r'w:left="[1-9]|w:jc w:val="(center|right)"', pr):
            continue
        ind = re.findall(r'w:firstLine="(\d+)"', pr)
        c[ind[0] if ind else 'sem recuo'] += 1
    for k, v in c.most_common():
        print(f"  {v:>4} paragrafo(s): {k}")
    fora = sum(v for k, v in c.items() if k != str(alvo))
    falha(f"{fora} paragrafo(s) de corpo fora do recuo de {alvo} twips") if fora \
        else ok("recuo uniforme")


def titulos(paras):
    print("\n-- titulos --")
    niveis = collections.defaultdict(collections.Counter)
    for p in paras:
        st = re.findall(r'w:pStyle w:val="(Ttulo\d)"', p)
        if not st or not texto(p):
            continue
        if st[0] == 'Ttulo1' and not re.match(r'(Cap[íi]tulo|\d)', texto(p)):
            st = ['Ttulo1 sem indicativo']  # REFERENCIAS, ANEXOS: centralizados pela NBR 14724
        sz = (re.findall(r'<w:sz w:val="(\d+)"', p) or ['herdado'])[0]
        jc = (re.findall(r'<w:jc w:val="(\w+)"', p) or ['herdado'])[0]
        fonte = (re.findall(r'w:ascii="([^"]+)"', p) or ['herdado'])[0]
        niveis[st[0]][(sz, jc, fonte)] += 1
    for nivel in sorted(niveis):
        var = niveis[nivel]
        det = ", ".join(f"sz={k[0]}/jc={k[1]}/{k[2]}x{v}" for k, v in var.items())
        falha(f"{nivel} com {len(var)} formatacoes diferentes: {det}") if len(var) > 1 \
            else ok(f"{nivel} uniforme ({det})")


def equacoes(x):
    print("\n-- equacoes --")
    caixa = re.findall(r'EQUA[ÇC][ÃA]O\s*[\d.]+', x)
    paren = re.findall(r'\(\d+\.\d+\)', x)
    print(f"  rotulo 'EQUACAO N' em caixa alta: {len(caixa)} | '(N.N)': {len(paren)}")
    falha(f"{len(caixa)} equacao(oes) com rotulo em caixa alta — ABNT usa "
          f"'(3.1)' alinhado a direita") if caixa \
        else ok("nenhum rotulo de equacao em caixa alta")


PLACEHOLDERS = [r'\[INSERIR[^\]]*\]', r'\[FIGURA[^\]]*\]', r'\[A CONFIRMAR\]',
                r'\[ANO A CONFIRMAR\]', r'Acervo da biblioteca', r'\bXX\s*f\.']
# texto que os autores ainda vao escrever: aviso, nao falha. "A ser elaborada
# pela Biblioteca" nao entra: e a instrucao real da UERJ para a ficha.
AUTORAIS = [r'Frase opcional', r'Dedicatória opcional']


def placeholders(x):
    print("\n-- residuos de template --")
    plano = html.unescape(re.sub(r'<[^>]+>', '', x))
    achou = 0
    for pat in PLACEHOLDERS:
        for m in sorted(set(re.findall(pat, plano))):
            print(f"    {m[:90]}")
            achou += 1
    falha(f"{achou} residuo(s) de template/placeholder no texto") if achou \
        else ok("sem residuo de template")
    for pat in AUTORAIS:
        if re.search(pat, plano):
            aviso(f"'{pat}' ainda no texto — conteudo a escrever pelos autores")
