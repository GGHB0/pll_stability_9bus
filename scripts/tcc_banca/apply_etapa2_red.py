# -*- coding: utf-8 -*-
"""
apply_etapa2_red.py
Aplica as alterações aprovadas para a Etapa 2 com os novos textos destacados em VERMELHO:
- Ponto A: Deslocamento da subseção 2.1.4 para 2.3.2 (Arquitetura de Controle Baseada em Corrente);
- Ponto B: Explicação matemática e normativa do SCR = 9,14 e Scc = 914,2 MVA na Seção 3.3.1;
- Ponto E: Premissa do elo CC como bateria na Seção 3.3.2 e menção em Trabalhos Futuros;
- Ponto F: Texto de transição sobre o paradoxo Barra 6 vs. Barra 7 entre as Seções 4.3 e 4.4.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"C:\Temp\tcc_banca\unpacked"
DOC_XML = os.path.join(BASE_DIR, "word", "document.xml")

with open(DOC_XML, "r", encoding="utf-8") as f:
    xml = f.read()

print(f"Lendo {DOC_XML} ({len(xml)} bytes)...")

# ==============================================================================
# 1. PONTO A: DESLOCAMENTO DA SUBSEÇÃO 2.1.4 PARA 2.3.2 (EM VERMELHO)
# ==============================================================================
idx_heading_214 = xml.find("2.1.4. Arquitetura de Controle Baseada em Corrente", 300000)
if idx_heading_214 == -1:
    print("ERRO: Subseção 2.1.4 não encontrada no corpo!")
    sys.exit(1)

p_start_214 = xml.rfind("<w:p ", 0, idx_heading_214)
idx_heading_22 = xml.find("2.2. Geração", p_start_214)
p_end_214 = xml.rfind("<w:p ", 0, idx_heading_22)

bloco_214 = xml[p_start_214:p_end_214]
print(f"Bloco 2.1.4 extraído ({len(bloco_214)} bytes).")

# Remove o bloco de sua posição original em 2.1
xml = xml[:p_start_214] + xml[p_end_214:]

# Atualiza o título de 2.1.4 para 2.3.2
bloco_232 = bloco_214.replace(
    "2.1.4. Arquitetura de Controle Baseada em Corrente",
    "2.3.2. Arquitetura de Controle Baseada em Corrente"
)

# Adiciona <w:color w:val="FF0000"/> nos runs de texto (<w:rPr>) do bloco deslocado
def color_red_runs(block_xml):
    def add_red(match):
        rPr_content = match.group(1)
        if 'w:color' not in rPr_content:
            return f'<w:rPr><w:color w:val="FF0000"/>{rPr_content}</w:rPr>'
        else:
            return re.sub(r'<w:color [^>]*/>', '<w:color w:val="FF0000"/>', match.group(0))
    
    # Substitui rPr existentes
    res = re.sub(r'<w:rPr>(.*?)</w:rPr>', add_red, block_xml, flags=re.DOTALL)
    # Onde não havia rPr antes de w:t
    res = re.sub(r'(<w:r(?: [^>]*)?>)(?!<w:rPr>)', r'\1<w:rPr><w:color w:val="FF0000"/></w:rPr>', res)
    return res

bloco_232_red = color_red_runs(bloco_232)

# Destino: inserir após o último parágrafo de 2.3.1 (antes de 2.4. O Sistema de Sincronismo SRF-PLL)
idx_heading_24 = xml.find("2.4. O Sistema de Sincronismo SRF-PLL", 300000)
p_start_24 = xml.rfind("<w:p ", 0, idx_heading_24)

xml = xml[:p_start_24] + bloco_232_red + xml[p_start_24:]
print("Subseção 2.3.2 inserida com sucesso antes da Seção 2.4.")

# Troca das remissões cruzadas de figuras no texto (Figura 2.1 <-> Figura 2.2):
remissao_antiga_21 = "A Figura 2.1 mostra a malha de corrente im"
remissao_nova_21 = '<w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t>A Figura 2.2 mostra a malha de corrente im</w:t></w:r>'

remissao_antiga_22 = "A Figura 2.2 ilustra esse arranjo em diagr"
remissao_nova_22 = '<w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t>A Figura 2.1 ilustra esse arranjo em diagr</w:t></w:r>'

if remissao_antiga_21 in xml:
    xml = xml.replace(f"<w:t>{remissao_antiga_21}", remissao_nova_21[:-10])
    print("Remissão da malha de corrente atualizada para Figura 2.2 (em vermelho).")

if remissao_antiga_22 in xml:
    xml = xml.replace(f"<w:t>{remissao_antiga_22}", remissao_nova_22[:-10])
    print("Remissão do VSI atualizada para Figura 2.1 (em vermelho).")

# ==============================================================================
# 2. PONTO B: CÁLCULO DE SCC E SCR NA SEÇÃO 3.3.1 (EM VERMELHO)
# ==============================================================================
target_fonte_31 = "<w:t>Fonte: Adaptado de Anderson e Fouad (2003) e MathWorks (2025).</w:t></w:r></w:p>"

paragrafo_scr_red = """<w:p w14:paraId="2CA00101" w14:textId="77777777" w:rsidR="00381505" w:rsidRDefault="00381505"><w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t>A partir dos parâmetros das linhas de transmissão, transformadores e geradores síncronos do sistema IEEE 9 barras reduzidos ao Ponto de Conexão Comum (PCC - Barra 2), determinou-se a impedância equivalente de Thévenin da rede como Zth = 0,01004 + j0,4374 Ω. Adotando-se os valores de base do sistema (Vb = 20 kV e Sb = 100 MVA, correspondente à potência nominal da central fotovoltaica), tem-se a impedância base Zbase = Vb² / Sb = 4,0 Ω. Em valores normalizados por unidade, a impedância equivalente resulta em |Zth,pu| = |0,00251 + j0,10935| ≈ 0,10938 pu. A potência de curto-circuito trifásica simétrica no PCC é dada por Scc = Sb / |Zth,pu| = 100 MVA / 0,10938 ≈ 914,2 MVA. Consequentemente, a Relação de Curto-Circuito (Short-Circuit Ratio - SCR) no barramento de conexão da UFV é calculada como SCR = Scc / Pinv,nom = 914,2 MVA / 100 MVA = 9,14. De acordo com as diretrizes normativas internacionais (IEEE Std 1204-1997 e CIGRE Technical Brochure 671), sistemas elétricos com SCR &gt; 3,0 são formalmente classificados como redes fortes (strong grids), confirmando quantitativamente que o barramento de ensaio apresenta elevada robustez de tensão frente à potência injetada pelo conversor.</w:t></w:r></w:p>"""

if target_fonte_31 in xml:
    xml = xml.replace(target_fonte_31, target_fonte_31 + "\n" + paragrafo_scr_red, 1)
    print("Ponto B: Parágrafo de SCR = 9,14 e Scc inserido com sucesso (em vermelho).")
else:
    print("AVISO: Âncora da Figura 3.1 não encontrada para o Ponto B.")

# ==============================================================================
# 3. PONTO E: PREMISSA DO ELO CC (SEÇÃO 3.3.2) E TRABALHOS FUTUROS (EM VERMELHO)
# ==============================================================================
target_vsi_desc = "O inversor foi modelado como um VSI trifásico de dois níveis com frequência de chaveamento de 5 kHz."

paragrafo_bateria_red = """<w:p w14:paraId="2CA00102" w14:textId="77777777" w:rsidR="00381505" w:rsidRDefault="00381505"><w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t>O barramento de corrente contínua (elo CC) foi representado por uma fonte de tensão ideal de 800 V (bateria). Essa simplificação metodológica é amplamente adotada em estudos de estabilidade transitória de sincronismo, pois permite isolar as dinâmicas de rastreamento de ângulo do SRF-PLL e do controle de corrente CA, desacoplando-as das oscilações de tensão do elo CC decorrentes do algoritmo de seguimento de ponto de máxima potência (MPPT) dos módulos fotovoltaicos.</w:t></w:r></w:p>"""

if target_vsi_desc in xml:
    pos_vsi = xml.find(target_vsi_desc)
    end_p_vsi = xml.find("</w:p>", pos_vsi) + len("</w:p>")
    xml = xml[:end_p_vsi] + "\n" + paragrafo_bateria_red + xml[end_p_vsi:]
    print("Ponto E: Parágrafo da premissa de bateria inserido na Seção 3.3.2 (em vermelho).")

# Ponto E em Trabalhos Futuros:
target_tf_p2 = "que a literatura ainda trata como questão em aberto (STRAUSS-MINCU et al., 2026)."

paragrafo_tf_red = """<w:p w14:paraId="2CA00103" w14:textId="77777777" w:rsidR="00381505" w:rsidRDefault="00381505"><w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t>Uma terceira linha de investigação é a modelagem integrada do lado CC da planta fotovoltaica, substituindo a fonte de tensão ideal por arranjos de módulos fotovoltaicos operando com algoritmo de MPPT, controle dinâmico da tensão do barramento CC e sistema de proteção por resistor de frenagem (chopper CC) durante faltas assimétricas e simétricas profundas.</w:t></w:r></w:p>"""

if target_tf_p2 in xml:
    pos_tf = xml.find(target_tf_p2)
    end_p_tf = xml.find("</w:p>", pos_tf) + len("</w:p>")
    xml = xml[:end_p_tf] + "\n" + paragrafo_tf_red + xml[end_p_tf:]
    print("Ponto E: Nova linha de investigação inserida em Trabalhos Futuros (em vermelho).")
else:
    print("AVISO: Âncora de Trabalhos Futuros não encontrada!")

# ==============================================================================
# 4. PONTO F: TEXTO DE TRANSIÇÃO BARRA 6 VS. BARRA 7 (EM VERMELHO)
# ==============================================================================
target_fim_43 = "o inversor prolonga o período em que injeta potência de forma descoordenada justamente na etapa de restabelecimento, quando a rede depende da contribuição estável dos recursos conectados."

paragrafo_transicao_red = """<w:p w14:paraId="2CA00104" w14:textId="77777777" w:rsidR="00381505" w:rsidRDefault="00381505"><w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t>A comparação entre as faltas aplicadas na Barra 6 e na Barra 7 sintetiza esse paradoxo de controle: sob a falta bifásica moderada e distante na Barra 6, a tensão remanescente no PCC é de aproximadamente 0,78 pu, permitindo que a banda estreita da sintonia inadequada atue favoravelmente como filtro da componente de 120 Hz de sequência negativa. Todavia, sob a contingência severa da Barra 7 (V &lt; 0,15 pu), essa mesma lentidão impede o acompanhamento do salto angular do vetor de tensão. O erro ultrapassa os limites lineares (±90°), o ganho da malha inverte-se e o conversor perde o sincronismo por escorregamento de ciclos (cycle slipping), como detalhado a seguir.</w:t></w:r></w:p>"""

if target_fim_43 in xml:
    pos_fim_43 = xml.find(target_fim_43)
    end_p_fim_43 = xml.find("</w:p>", pos_fim_43) + len("</w:p>")
    xml = xml[:end_p_fim_43] + "\n" + paragrafo_transicao_red + xml[end_p_fim_43:]
    print("Ponto F: Texto de transição Barra 6 vs. Barra 7 inserido (em vermelho).")

# ==============================================================================
# 5. MARCAÇÃO DO TOC COM DIRTY=TRUE E VALIDAÇÃO XML
# ==============================================================================
if '<w:fldSimple w:instr="TOC ' in xml:
    xml = xml.replace('<w:fldSimple w:instr="TOC ', '<w:fldSimple w:dirty="true" w:instr="TOC ', 1)
elif 'TOC \\o' in xml:
    xml = re.sub(r'(<w:fldChar w:fldCharType="begin"\/?>)', r'<w:fldChar w:dirty="true" w:fldCharType="begin"/>', xml, count=1)

try:
    ET.fromstring(xml)
    print("VALIDAÇÃO XML: Sucesso! O XML gerado está perfeitamente bem-formado.")
except Exception as e:
    print(f"ERRO DE XML: {e}")
    sys.exit(1)

with open(DOC_XML, "w", encoding="utf-8") as f:
    f.write(xml)

print(f"Arquivo {DOC_XML} regravado com sucesso ({len(xml)} bytes).")
