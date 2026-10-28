# -*- coding: utf-8 -*-
"""
Gera todos os áudios neurais de estudo e ensaio da defesa de TCC (Slides 1 a 21 + Palco Capítulos 1 a 8).
Utiliza a biblioteca edge-tts com vozes neurais brasileiras calibradas:
  - Narradora (Guia do Slide / Dicas de Banca): pt-BR-FranciscaNeural
  - Bruno: pt-BR-AntonioNeural (pitch normal)
  - Victor: pt-BR-AntonioNeural (pitch -6Hz, rate +3% para distinção de timbre)

Gera:
  1. output/audios_defesa/Slide_XX_com_guia.mp3 e Palco_Cap_XX_com_guia.mp3 (Modo Estudo com Diretrizes)
  2. output/audios_defesa/Slide_XX_fala_pura.mp3 e Palco_Cap_XX_fala_pura.mp3 (Modo Ensaio Cronometrado)
  3. output/audios_defesa/Defesa_Completa_Ensaio_Continuo.mp3 (Podcast de 30 min da apresentação contínua)
"""
import asyncio
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import edge_tts
from gerar_guia_estudos_word import SLIDE_SPEECHES, PALCO_SPEECHES

OUT_DIR = ROOT / "output" / "audios_defesa"
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
    """Extrai mensagens, perguntas de banca e cuidados do gen_roteiro_estudo_defesa.py."""
    txt = (ROOT / "scripts" / "notas" / "gen_roteiro_estudo_defesa.py").read_text(encoding="utf-8")
    
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
    for tag, texto, _ in cap_entries:
        autor = "Bruno" if "[Bruno]" in tag else "Victor"
        t = limpar_texto_para_fala(texto)
        if t:
            blocos.append((autor, t))
    return blocos


async def gerar_item(identificador: str, titulo: str, meta: dict, blocos_fala: list, incluir_guia: bool = True):
    """Gera áudio para um slide ou capítulo."""
    partes = []
    
    # 1. Introdução de Diretrizes do Slide/Capítulo (Modo Estudo)
    if incluir_guia and meta:
        bloco_nome = f" ({meta.get('bloco')})" if meta.get("bloco") else ""
        texto_guia = f"Orientações para {identificador}{bloco_nome}: {titulo}. "
        if meta.get("msg"):
            texto_guia += f"Objetivo e mensagem central: {meta['msg']}. "
        if meta.get("banca"):
            texto_guia += f"Pergunta e ponto de atenção da banca: {meta['banca']}. "
        if meta.get("cuidado"):
            texto_guia += f"Cuidado conceitual: {meta['cuidado']}. "
        texto_guia += "A seguir, a simulação de ensaio da fala dos apresentadores:"
        
        audio_guia = await sintetizar_trecho(
            texto_guia, 
            VOICE_NARRADOR, 
            pitch=PITCH_NARRADOR, 
            rate=RATE_NARRADOR
        )
        if audio_guia:
            partes.append(audio_guia)
            
    # 2. Falas dos apresentadores
    for autor, texto in blocos_fala:
        if autor == "Bruno":
            voz = VOICE_BRUNO
            pitch = PITCH_BRUNO
            rate = RATE_BRUNO
        else:
            voz = VOICE_VICTOR
            pitch = PITCH_VICTOR
            rate = RATE_VICTOR
            
        audio_bloco = await sintetizar_trecho(texto, voz, pitch=pitch, rate=rate)
        if audio_bloco:
            partes.append(audio_bloco)
            
    sufixo = "_com_guia" if incluir_guia else "_fala_pura"
    prefixo = identificador.replace(" ", "_")
    nome_arquivo = f"{prefixo}{sufixo}.mp3"
    caminho_final = OUT_DIR / nome_arquivo
    
    dados_totais = b"".join(partes)
    caminho_final.write_bytes(dados_totais)
    return caminho_final, dados_totais


async def main():
    print("=" * 70)
    print("GERANDO TODOS OS ÁUDIOS DA APRESENTAÇÃO DE TCC (SLIDES 1-21 + PALCO 1-8)")
    print("=" * 70)
    
    arquivos_fala_pura_ordenados = []
    
    # =========================================================================
    # PARTE I: Slides 1 a 19 (PowerPoint - Contexto, Fundamentos e Metodologia)
    # =========================================================================
    print("\n--- PARTE I: Slides 1 a 19 (PowerPoint) ---")
    for s_idx in range(1, 20):
        speech = SLIDE_SPEECHES.get(s_idx, "")
        meta = SLIDE_META.get(s_idx, {})
        titulo = meta.get("titulo", f"Slide {s_idx}")
        blocos = parse_falas_slide(speech)
        ident = f"Slide_{s_idx:02d}"
        
        print(f"[{s_idx:02d}/29] Processando {ident}: {titulo}...")
        # 1. Versão com guia
        c_guia, _ = await gerar_item(ident, titulo, meta, blocos, incluir_guia=True)
        # 2. Versão fala pura
        c_pura, bytes_pura = await gerar_item(ident, titulo, meta, blocos, incluir_guia=False)
        arquivos_fala_pura_ordenados.append(bytes_pura)
        print(f"       -> OK: {c_guia.name} ({c_guia.stat().st_size/1024:.1f} KB) | {c_pura.name}")
        
    # =========================================================================
    # PARTE II: Palco Capítulos 1 a 8 (Painel Interativo ao Vivo)
    # =========================================================================
    print("\n--- PARTE II: Painel Interativo (Capítulos 1 a 8 do Palco) ---")
    for c_idx in range(1, 9):
        cap_entries = PALCO_SPEECHES.get(c_idx, [])
        meta = CAP_META.get(c_idx, {})
        titulo = meta.get("titulo", f"Capítulo {c_idx}")
        blocos = parse_falas_palco(cap_entries)
        ident = f"Palco_Cap_{c_idx:02d}"
        
        print(f"[{19+c_idx:02d}/29] Processando {ident}: {titulo}...")
        # 1. Versão com guia
        c_guia, _ = await gerar_item(ident, titulo, meta, blocos, incluir_guia=True)
        # 2. Versão fala pura
        c_pura, bytes_pura = await gerar_item(ident, titulo, meta, blocos, incluir_guia=False)
        arquivos_fala_pura_ordenados.append(bytes_pura)
        print(f"       -> OK: {c_guia.name} ({c_guia.stat().st_size/1024:.1f} KB) | {c_pura.name}")

    # =========================================================================
    # PARTE III: Slides 20 e 21 (PowerPoint - Síntese, Trabalhos Futuros e Fim)
    # =========================================================================
    print("\n--- PARTE III: Conclusão e Encerramento (Slides 20 e 21) ---")
    for s_idx in [20, 21]:
        speech = SLIDE_SPEECHES.get(s_idx, "")
        meta = SLIDE_META.get(s_idx, {})
        titulo = meta.get("titulo", f"Slide {s_idx}")
        blocos = parse_falas_slide(speech)
        ident = f"Slide_{s_idx:02d}"
        
        print(f"[{8+s_idx:02d}/29] Processando {ident}: {titulo}...")
        c_guia, _ = await gerar_item(ident, titulo, meta, blocos, incluir_guia=True)
        c_pura, bytes_pura = await gerar_item(ident, titulo, meta, blocos, incluir_guia=False)
        arquivos_fala_pura_ordenados.append(bytes_pura)
        print(f"       -> OK: {c_guia.name} ({c_guia.stat().st_size/1024:.1f} KB) | {c_pura.name}")

    # =========================================================================
    # ÁUDIO CONSOLIDADO: Defesa Completa Contínua (30 minutos)
    # =========================================================================
    print("\n--- Gerando Áudio Consolidado (Ensaio Contínuo da Apresentação) ---")
    arquivo_consolidado = OUT_DIR / "Defesa_Completa_Ensaio_Continuo.mp3"
    arquivo_consolidado.write_bytes(b"".join(arquivos_fala_pura_ordenados))
    tam_mb = arquivo_consolidado.stat().st_size / (1024 * 1024)
    print(f"[CONCLUÍDO] Áudio contínuo gerado: {arquivo_consolidado.name} ({tam_mb:.2f} MB)")
    print(f"\nTodos os arquivos estão prontos em:\n{OUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
