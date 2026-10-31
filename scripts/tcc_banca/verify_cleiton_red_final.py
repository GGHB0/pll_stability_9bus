# -*- coding: utf-8 -*-
"""
verify_cleiton_red_final.py
Auditoria automatizada completa de conformidade do documento canônico:
Verifica se cada uma das alterações atribuídas ao Professor Cleiton está
devidamente formatada com destaque em VERMELHO (#FF0000).
"""

import sys
import zipfile
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ONEDRIVE_FILE = r"C:\Users\gilbr\OneDrive\UERJ\TCC - Victor e Bruno\Template Modelo TCC\01_TCC_Monografia_Final\TCC_Victor_Bruno_VFinal.docx"

print("=" * 80)
print("AUDITORIA FINAL DE ALTERAÇÕES EM VERMELHO - PROF. CLEITON")
print("=" * 80)

with zipfile.ZipFile(ONEDRIVE_FILE, 'r') as z:
    xml = z.read('word/document.xml').decode('utf-8')

checklist = [
    # 1. Estrutura UERJ (Leitura 1)
    ("1.1", "Título INTRODUÇÃO", "INTRODUÇÃO"),
    ("1.2", "Título Seção 1 (1  DESAFIOS...)", "1  DESAFIOS À ESTABILIDADE"),
    ("1.3", "Título Seção 2 (2  GERAÇÃO...)", "2  GERAÇÃO CONECTADA À REDE"),
    ("1.4", "Título Seção 3 (3  METODOLOGIA...)", "3  METODOLOGIA DE ANÁLISE"),
    ("1.5", "Título Seção 4 (4  ANÁLISE...)", "4  ANÁLISE E DISCUSSÃO DE RESULTADOS"),
    ("1.6", "Título CONCLUSÃO", "CONCLUSÃO"),
    ("1.7", "Subseção Trabalhos Futuros", "Trabalhos Futuros"),

    # 2. Novas Referências (Leitura 2)
    ("2.1", "Ref: CEN (2025)", "COORDINADOR ELÉCTRICO NACIONAL"),
    ("2.2", "Ref: Gu & Green (2023)", "GU, Y.; GREEN, T. C."),
    ("2.3", "Ref: IEA (2026)", "INTERNATIONAL ENERGY AGENCY (IEA)"),
    ("2.4", "Ref: Kundur (2004)", "KUNDUR, P. et al."),
    ("2.5", "Ref: Repositório GitHub (2026)", "OLIVEIRA, B. H.; REZENDE, V. H. A."),

    # 3. Justificativa do 4 e Remissões de Figuras (Leitura 3 e 4)
    ("3.1", "Subseção 2.3.2 título", "2.3.2. Arquitetura de Controle Baseada em Corrente"),
    ("3.2", "Explicação da divisão por 4 (Zbase = 4,0 Ω)", "Zbase = Vb² / Sb = (20 kV)² / 100 MVA = 4,0 Ω"),
    ("3.3", "Remissão à Figura 2.1 na Seção 2.2", "A Figura 2.1"),
    ("3.4", "Remissão à Figura 2.2 na Seção 2.3.2", "A Figura 2.2 mostra a malha de corrente"),
    ("3.5", "Legenda da Figura 2.2", "Diagrama de blocos do controle de corrente no referencial dq"),

    # 4. Pontuação nas Equações (Leitura 5)
    ("4.1", "Pontuação Eq (3.1) a (3.23)", 'w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><m:t>.</m:t></m:r></m:oMath>'),

    # 5. Potência de Curto-Circuito e SCR (Leitura 6)
    ("5.1", "Cálculo Scc = 914,2 MVA e SCR = 9,14", "SCR = Scc / Pinv,nom = 9,14"),
    ("5.2", "Normas IEEE Std 1204 e CIGRE TB 671", "IEEE Std 1204-1997 e CIGRE TB 671"),

    # 6. Elo CC como Bateria (Defesa 1)
    ("6.1", "Premissa de bateria ideal 800 V (Seção 3.3.2)", "fonte de tensão ideal de 800 V (bateria)"),
    ("6.2", "Trabalhos Futuros: MPPT e lado CC", "modelagem integrada do lado CC"),

    # 7. Largura de Banda do PLL (Defesa 3)
    ("7.1", "Fórmula analítica de Teodorescu (Seção 2.4)", "Teodorescu, Liserre e Rodríguez (2011, §4.2.2.3, p. 56)"),
    ("7.2", "Largura de banda nominal 106,5 Hz (Seção 3.3.2.3)", "106,5 Hz"),
    ("7.3", "Largura de banda inadequada 38,5 Hz (Seção 3.3.2.3)", "38,5 Hz"),

    # 8. Submódulo 2.10 do ONS (Defesa 4)
    ("8.1", "Texto contextualizado na Seção 1.5.2", "Como o ONS impõe rampas e limites específicos"),
    ("8.2", "Texto da priorização reativa / saturação quadrática (Seção 3.3.2)", "id,ref = min(1.0, sqrt(Imax² - iq,ref²))"),
    ("8.3", "Legenda da Figura 3.3 (Lógica do ONS)", "Figura 3.3 – Lógica de controle e priorização de corrente reativa"),
    ("8.4", "Fonte da Figura 3.3", "Fonte: Adaptado de ONS (2022)."),
    ("8.5", "Legenda da Figura 3.4 (Diagrama conceitual)", "Diagrama conceitual do SRF-PLL"),
    ("8.6", "Remissão no texto à Figura 3.4", "situa a arquitetura do SRF-PLL"),

    # 9. Apêndice A (Defesa 5)
    ("9.1", "Título do Apêndice A", "APÊNDICE A – PAINEL INTERATIVO DE ANÁLISE DINÂMICA"),
    ("9.2", "Texto introdutório do ecossistema Python / Plotly", "desenvolveu-se um painel interativo web em Python e Plotly"),
    ("9.3", "Legenda da Figura A.1 e Fonte", "Figura A.1 – Interface do painel interativo de métricas"),
    ("9.4", "Subseção B (Sequência de Telas do Modo Apresentação)", "B. Sequência de Telas do Modo Apresentação no Texto"),
    ("9.5", "Figuras A.2 a A.5 com narrativas e legendas", "Figura A.2 – Módulo de animação fasorial"),
    ("9.6", "Citação do Repositório GitHub", "https://github.com/bruno-victor-uerj/pll-stability-dashboard"),

    # 10. Transição Barra 6 vs Barra 7 (Leitura/Defesa)
    ("10.1", "Texto do paradoxo de controle Barra 6 vs 7", "A comparação entre as Barras 6 e 7 ilustra o paradoxo da sintonia"),

    # 11. Correções do PDF / Tablet
    ("11.1", "Pág. 16: geração renovável variável", "fontes de geração renovável variável apresentam"),
    ("11.2", "Pág. 20: data centers (em itálico)", "data centers"),
    ("11.3", "Pág. 23: German System Stability Roadmap", "German System Stability Roadmap"),
    ("11.4", "Pág. 78: sobrecorrentes inicialmente previstas", "As sobrecorrentes inicialmente previstas"),
    ("11.5", "Termo itálico small-signal", "small-signal"),
    ("11.6", "Termo itálico large-disturbance", "large-disturbance"),
    ("11.7", "Termo itálico swings", "swings"),
    ("11.8", "Termo itálico swing equation", "swing equation"),
    ("11.9", "Termo itálico Converter-Driven Stability", "Converter-Driven Stability"),
    ("11.10", "Termo itálico cycle slipping", "cycle slipping"),
    ("11.11", "Termo itálico converter-driven", "converter-driven"),
]

all_passed = True
for code, desc, needle in checklist:
    # Busca a ocorrência no corpo do texto (usando rfind para evitar o sumário TOC)
    pos = xml.rfind(needle)
    if pos == -1:
        print(f"[{code}] {desc}: FALHA - Texto não encontrado!")
        all_passed = False
        continue
    
    start_p = xml.rfind('<w:p ', 0, pos)
    end_p = xml.find('</w:p>', pos) + 6
    p_slice = xml[start_p:end_p]
    is_red = ('FF0000' in p_slice.upper() or 'RED' in p_slice.upper())
    
    if not is_red:
        print(f"[{code}] {desc}: FALHA - Não está em vermelho no corpo!")
        all_passed = False
    else:
        print(f"[{code:5}] {desc:60} : OK (Presente e em VERMELHO)")

print("=" * 80)
if all_passed:
    print("RESULTADO DA AUDITORIA: 100% DAS ALTERAÇÕES DO PROF. CLEITON ESTÃO EM VERMELHO!")
else:
    print("RESULTADO DA AUDITORIA: FORAM DETECTADAS PENDÊNCIAS!")
print("=" * 80)
