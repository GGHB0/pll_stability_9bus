"""Guia de estudos: ambiente em que o conteudo/ roda, desviando cada bloco para o Word.

Os arquivos de conteudo/ chamam box(), slide(), cap(), tab()... como no PDF; aqui
cada chamada vira o bloco equivalente no WordRoteiroBuilder, e as falas completas
entram logo depois da mensagem (slides) ou dos passos (capítulos).
"""
from caminhos import CACHE, PALCO_PNG, SLIDES_PNG
from falas import FALAS
from gw_cronograma import inject_30min_schedule_and_tcc_map
from gw_reserva import inject_defesa_qa_and_hidden_slides
from gw_util import *  # noqa: F401,F403


def ambiente(wb):
    """Dicionário de nomes para o exec() do conteudo/."""
    CACHE.mkdir(parents=True, exist_ok=True)

    def jpg(src: Path, largura=1300) -> Path:
        dst = CACHE / (src.parent.name + "_" + src.stem + ".jpg")
        if not dst.exists() or (src.exists() and dst.stat().st_mtime < src.stat().st_mtime):
            with PILImage.open(src) as im:
                im = im.convert("RGB")
                if im.width > largura:
                    im = im.resize((largura, round(im.height * largura / im.width)), PILImage.LANCZOS)
                im.save(dst, "JPEG", quality=86, optimize=True)
        return dst

    def rap_fig(nome, pagina, clip) -> Path:
        dst = CACHE / f"rap_{nome}.jpg"
        return dst

    current_context = {"type": None, "num": None, "injected_schedule": False}

    class NoteProxy:
        def h(self, text):
            wb.h(text)
            if text == "Folha de números":
                # Antes da Folha de números final, injetamos os slides ocultos 25-30 e o Q&A completo!
                pass

        def p(self, text):
            wb.p(text)

        def table(self, header, rows, widths):
            wb.table(header, rows, widths)

        def note(self, text):
            wb.note(text)
            # Logo após a nota das "Convenções que valem para tudo", injetamos o Cronograma de 30 min e o Mapa do TCC!
            if "Sem RoCoF" in text and not current_context["injected_schedule"]:
                current_context["injected_schedule"] = True
                inject_30min_schedule_and_tcc_map(wb)

        def gap(self, h=6):
            wb.gap(h)

        def pagebreak(self):
            wb.pagebreak()

    n_proxy = NoteProxy()

    def box_hook(kind, *paras, titulo=None):
        wb.box(kind, *paras, titulo=titulo)
        # Se acabamos de colocar a MENSAGEM de um slide que NÃO tem `fala(num)` (ex.: slides 1-4, 18-22),
        # injetamos a caixa de fala completa logo abaixo da MENSAGEM!
        if kind == "msg":
            if current_context["type"] == "slide":
                s_num = current_context["num"]
                if s_num not in range(5, 16):
                    wb.add_slide_speech_box(s_num)
            elif current_context["type"] == "cap":
                c_num = current_context["num"]
                # Nos capítulos 1 e 8 (que não têm box("passo")), injetamos a fala do palco logo após a MENSAGEM
                if c_num in (1, 8):
                    wb.add_palco_speech_box(c_num)
        elif kind == "passo" and current_context["type"] == "cap":
            # Nos capítulos 2 a 7 (que têm box("passo")), injetamos a fala passo a passo logo após os PASSOS!
            wb.add_palco_speech_box(current_context["num"])

    def fala_hook(num):
        wb.box("fala", *[f"<b>{quem}:</b> {texto}" for quem, texto in FALAS[num]])
        # E logo abaixo dos tópicos do Victor nos slides 5 a 15, colocamos o texto completo cronometrado!
        wb.add_slide_speech_box(num)

    def slide_hook(num, titulo, bloco, quem, tcc):
        current_context["type"] = "slide"
        current_context["num"] = num
        wb.faixa(
            "SLIDE",
            num,
            titulo,
            f"{bloco} &#160;·&#160; Fala: {quem} &#160;·&#160; No TCC: {tcc}",
            imagem=jpg(SLIDES_PNG / f"s{num:02d}.png"),
        )

    def cap_hook(num, titulo, ref, png, legenda):
        current_context["type"] = "cap"
        current_context["num"] = num
        wb.faixa(
            "PAINEL",
            num,
            titulo,
            ref,
            imagem=jpg(PALCO_PNG / png),
            legenda=legenda,
        )

    def imagem_palco_hook(png, legenda, alt=8.6):
        wb.figura(jpg(PALCO_PNG / png), legenda=legenda, largura_cm=15.0)

    def parte_hook(titulo, *paras):
        wb.h(titulo)
        for x in paras:
            wb.p(x)

    def tab_hook(header, rows, widths):
        wb.table(header, rows, widths)
        # Se acabamos de colocar a tabela "Outros materiais" na Parte V, injetamos os Slides Ocultos 23-28 e o Q&A!
        if header == ["Material", "Para quê"]:
            inject_defesa_qa_and_hidden_slides(wb, lambda s_n: jpg(SLIDES_PNG / f"s{s_n:02d}.png"))

    def nums_hook(rows):
        wb.table(["Número", "O que é"], rows, [3.9, 10.8])

    def figura_hook(caminho, legenda, largura=14.7):
        wb.figura(caminho, legenda=legenda, largura_cm=largura * 16.5 / 14.7)

    exec_env = {
        "n": n_proxy,
        "W": 14.7,
        "S_BUL": "bul",
        "Paragraph": lambda txt, style, bulletText=None: txt,
        "box": box_hook,
        "sub": wb.sub,
        "bul": wb.bul,
        "eq": wb.eq,
        "tab": tab_hook,
        "nums": nums_hook,
        "figura": figura_hook,
        "instante": wb.instante,
        "ponte": wb.ponte,
        "parte": parte_hook,
        "slide": slide_hook,
        "cap": cap_hook,
        "imagem_palco": imagem_palco_hook,
        "rap_fig": rap_fig,
        "FALAS": FALAS,
        "fala": fala_hook,
    }
    return exec_env
