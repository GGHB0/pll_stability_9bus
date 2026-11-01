"""Áudios da defesa: vozes, limpeza do texto e síntese (edge-tts)."""
import re

import edge_tts

from caminhos import OUTPUT, conteudo_texto

OUT_DIR = OUTPUT / "audios_defesa"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Configuração das vozes neurais
VOICE_NARRADOR = "pt-BR-FranciscaNeural"
VOICE_BRUNO = "pt-BR-AntonioNeural"
VOICE_VICTOR = "pt-BR-AntonioNeural"

PITCH_BRUNO = "+0Hz"
RATE_BRUNO = "+0%"

PITCH_VICTOR = "-6Hz"
RATE_VICTOR = "+3%"

PITCH_NARRADOR = "+0Hz"
RATE_NARRADOR = "+2%"


def clean_html(s: str) -> str:
    """Remove marcações HTML e entidades."""
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("&nbsp;", " ").replace("&#160;", " ").replace("&rarr;", "->")
    s = s.replace("&#8220;", '"').replace("&#8221;", '"')
    s = s.replace("&#178;", " ao quadrado").replace("&#952;", "teta")
    s = s.replace("&#969;", "ômega").replace("&#958;", "ksi")
    s = s.replace("&#8730;", "raiz de ")
    return re.sub(r"\s+", " ", s).strip()


def carregar_diretrizes():
    """Extrai mensagens, perguntas de banca e cuidados do conteudo/ do roteiro de estudo."""
    txt = conteudo_texto()
    
    # Slides 1 a 21
    slide_pattern = re.compile(r'slide\((\d+),\s*"([^"]+)",\s*"([^"]+)"')
    slide_data = {}
    for m in slide_pattern.finditer(txt):
        s_idx = int(m.group(1))
        if s_idx > 21:
            continue
        title = m.group(2)
        bloco = m.group(3)
        pos = m.end()
        
        msg_m = re.search(r'box\("msg",\s*"([^"]+)"', txt[pos:pos+1600])
        msg = clean_html(msg_m.group(1)) if msg_m else ""
        
        banca_m = re.search(r'box\("banca",\s*"([^"]+)"', txt[pos:pos+2500])
        banca = clean_html(banca_m.group(1)) if banca_m else ""
        
        cuid_m = re.search(r'box\("cuidado",\s*"([^"]+)"', txt[pos:pos+2500])
        cuidado = clean_html(cuid_m.group(1)) if cuid_m else ""
        
        slide_data[s_idx] = {
            "titulo": title,
            "bloco": bloco,
            "msg": msg,
            "banca": banca,
            "cuidado": cuidado,
        }
        
    # Capítulos 1 a 8
    cap_pattern = re.compile(r'cap\((\d+),\s*"([^"]+)"')
    cap_data = {}
    for m in cap_pattern.finditer(txt):
        c_idx = int(m.group(1))
        title = m.group(2)
        pos = m.end()
        
        msg_m = re.search(r'box\("msg",\s*"([^"]+)"', txt[pos:pos+1600])
        msg = clean_html(msg_m.group(1)) if msg_m else ""
        
        banca_m = re.search(r'box\("banca",\s*"([^"]+)"', txt[pos:pos+2500])
        banca = clean_html(banca_m.group(1)) if banca_m else ""
        
        cuid_m = re.search(r'box\("cuidado",\s*"([^"]+)"', txt[pos:pos+2500])
        cuidado = clean_html(cuid_m.group(1)) if cuid_m else ""
        
        cap_data[c_idx] = {
            "titulo": title,
            "msg": msg,
            "banca": banca,
            "cuidado": cuidado,
        }
        
    return slide_data, cap_data


SLIDE_META, CAP_META = carregar_diretrizes()


def limpar_texto_para_fala(texto: str) -> str:
    """Limpa rubricas de palco (como '(Seta ->)') para a leitura soar natural."""
    t = texto
    # Remove rubricas entre parênteses como (Seta →) ou (Seta → para o Cap. 2)
    t = re.sub(r"\(\s*Seta\s*[^)]*\)", " ", t, flags=re.IGNORECASE)
    t = re.sub(r"\(\s*Passo\s*\d+[^)]*\)", " ", t, flags=re.IGNORECASE)
    t = re.sub(r"\(\s*Reserva[^)]*\)", " ", t, flags=re.IGNORECASE)
    # Substituições de caracteres especiais
    t = t.replace("→", " ").replace("·", " ").replace("§", "seção ")
    t = clean_html(t)
    return t


async def sintetizar_trecho(texto: str, voz: str, pitch: str = "+0Hz", rate: str = "+0%") -> bytes:
    """Sintetiza um trecho de texto em MP3 com edge-tts e retorna os bytes."""
    texto_limpo = texto.strip()
    if not texto_limpo:
        return b""
    comm = edge_tts.Communicate(texto_limpo, voice=voz, pitch=pitch, rate=rate)
    data = bytearray()
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            data.extend(chunk["data"])
    return bytes(data)


def parse_falas_slide(speech_raw: str):
    """Extrai blocos de fala de um slide formatado como [Bruno] ... [Victor] ..."""
    blocos = []
    padrao = re.compile(r"\[(Bruno|Victor)\]\s*([^\[]+)", re.DOTALL)
    for autor, texto in padrao.findall(speech_raw):
        t = limpar_texto_para_fala(texto)
        if t:
            blocos.append((autor, t))
    return blocos


def parse_falas_palco(cap_entries: list):
    """Extrai blocos de fala de um capítulo do palco."""
    blocos = []
    for quem, texto in cap_entries:
        autor = "Bruno" if quem == "Bruno" else "Victor"
        t = limpar_texto_para_fala(texto)
        if t:
            blocos.append((autor, t))
    return blocos
