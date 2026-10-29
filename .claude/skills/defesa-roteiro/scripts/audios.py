"""Áudios de estudo e ensaio da defesa (slides 1-21 e palco 1-8), com edge-tts.

Gera em output/audios_defesa/: <item>_com_guia.mp3 (orientações + fala),
<item>_fala_pura.mp3 e Defesa_Completa_Ensaio_Continuo.mp3. Texto em falas/.
"""
import asyncio

from au_voz import *  # noqa: F401,F403
from falas import PALCO_FALAS, SLIDE_SPEECHES


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
        cap_entries = PALCO_FALAS.get(c_idx, [])
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
