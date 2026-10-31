# -*- coding: utf-8 -*-
"""
apply_apendice_palco.py
Insere a Sequencia de Telas do Modo Apresentacao (Palco) no Apendice A:
- Copia as 4 imagens 1080p para word/media/ (image36 a image39);
- Adiciona os relacionamentos rId49 a rId52 em document.xml.rels;
- Insere a narrativa tecnica e as Figuras A.2 a A.5 com legendas e fontes no document.xml;
- Todos os novos textos e legendas destacados em VERMELHO (#FF0000).
"""

import os
import shutil
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"C:\Temp\tcc_banca\unpacked"
DOC_XML = os.path.join(BASE_DIR, "word", "document.xml")
RELS_XML = os.path.join(BASE_DIR, "word", "_rels", "document.xml.rels")
MEDIA_DIR = os.path.join(BASE_DIR, "word", "media")
SOURCE_DIR = r"c:\pll_stability_9bus\output\verifica_palco\1920x1080"

# 1. Copiar as 4 imagens para media/
images = [
    ("03_local_p2_fasor_mouse.png", "image36.png", "rId49"),
    ("04_seqneg_p2.png", "image37.png", "rId50"),
    ("06_sinc_p2.png", "image38.png", "rId51"),
    ("07_ons_p5.png", "image39.png", "rId52"),
]

for src_name, dst_name, rid in images:
    src_path = os.path.join(SOURCE_DIR, src_name)
    dst_path = os.path.join(MEDIA_DIR, dst_name)
    shutil.copyfile(src_path, dst_path)
    print(f"Copiado {src_name} -> {dst_name} ({os.path.getsize(dst_path)} bytes)")

# 2. Atualizar document.xml.rels
with open(RELS_XML, "r", encoding="utf-8") as f:
    rels = f.read()

new_rels = ""
for _, dst_name, rid in images:
    rel_tag = f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{dst_name}"/>'
    if rel_tag not in rels:
        new_rels += rel_tag

if new_rels:
    rels = rels.replace("</Relationships>", new_rels + "</Relationships>")
    with open(RELS_XML, "w", encoding="utf-8") as f:
        f.write(rels)
    print(f"document.xml.rels atualizado com rId49 a rId52.")
else:
    print("Relacionamentos ja presentes em document.xml.rels.")

# 3. Atualizar document.xml
with open(DOC_XML, "r", encoding="utf-8") as f:
    xml = f.read()

# Helper para construir bloco de imagem
def make_image_xml(para_id, docpr_id, rid, name):
    return (
        f'<w:p w14:paraId="{para_id}" w14:textId="77777777" w:rsidR="00381505" w:rsidRDefault="00381505">'
        f'<w:pPr><w:keepNext/><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/><w:jc w:val="center"/><w:rPr><w:szCs w:val="24"/></w:rPr></w:pPr>'
        f'<w:r><w:rPr><w:noProof/></w:rPr>'
        f'<w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0" wp14:anchorId="04A8139C" wp14:editId="3F049AF3">'
        f'<wp:extent cx="5760720" cy="3240405"/>'
        f'<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{docpr_id}" name="{name}"/>'
        f'<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
        f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        f'<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr><pic:cNvPr id="{docpr_id + 10000000}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="5760720" cy="3240405"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        f'</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'
    )

def make_caption_xml(para_id, caption_text):
    return (
        f'<w:p w14:paraId="{para_id}" w14:textId="77777777" w:rsidR="00095F51" w:rsidRDefault="00381505">'
        f'<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="60" w:line="240" w:lineRule="auto"/><w:rPr><w:color w:val="FF0000"/><w:sz w:val="20"/></w:rPr></w:pPr>'
        f'<w:r><w:rPr><w:color w:val="FF0000"/><w:sz w:val="20"/></w:rPr><w:t>{caption_text}</w:t></w:r></w:p>'
    )

def make_source_xml(para_id, source_text="Fonte: Os autores (2026)."):
    return (
        f'<w:p w14:paraId="{para_id}" w14:textId="77777777" w:rsidR="00095F51" w:rsidRDefault="00381505">'
        f'<w:pPr><w:spacing w:before="60" w:after="240" w:line="240" w:lineRule="auto"/><w:rPr><w:color w:val="FF0000"/><w:sz w:val="20"/></w:rPr></w:pPr>'
        f'<w:r><w:rPr><w:color w:val="FF0000"/><w:sz w:val="20"/></w:rPr><w:t>{source_text}</w:t></w:r></w:p>'
    )

def make_text_p_xml(para_id, text, is_heading=False):
    if is_heading:
        return (
            f'<w:p w14:paraId="{para_id}" w14:textId="77777777" w:rsidR="00095F51" w:rsidRDefault="00381505">'
            f'<w:pPr><w:pStyle w:val="Ttulo2"/><w:spacing w:before="360" w:after="180"/><w:jc w:val="both"/><w:rPr><w:color w:val="FF0000"/><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr>'
            f'<w:r><w:rPr><w:color w:val="FF0000"/><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:t>{text}</w:t></w:r></w:p>'
        )
    else:
        return (
            f'<w:p w14:paraId="{para_id}" w14:textId="77777777" w:rsidR="00BE4CBD" w:rsidRDefault="00BE4CBD">'
            f'<w:pPr><w:ind w:firstLine="708"/><w:jc w:val="both"/><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr></w:pPr>'
            f'<w:r><w:rPr><w:color w:val="FF0000"/><w:szCs w:val="24"/></w:rPr><w:t>{text}</w:t></w:r></w:p>'
        )

# Localiza o paragrafo da Fonte da Figura A.1 (1FB00335)
target_fonte_a1 = '<w:p w14:paraId="1FB00335"'
idx_target = xml.find(target_fonte_a1)
if idx_target == -1:
    print("ERRO: Paragrafo 1FB00335 nao encontrado!")
    sys.exit(1)

p_end_target = xml.find("</w:p>", idx_target) + 6

# Montagem do conteudo novo do Apendice A
novo_conteudo_apendice = []

# Texto de detalhamento da Figura A.1
p_a1_desc = (
    "A tela de consolidação de cenários (Figura A.1) apresenta o painel executivo com a matriz completa de indicadores dinâmicos do SRF-PLL "
    "para todos os pontos de contingência simulados no sistema IEEE 9 Barras (Barras 5, 6, 7 e 8). A interface disponibiliza filtros interativos "
    "por tipo de falta (simétrica e assimétrica), tempo de eliminação da falta e perfil de sintonia, calculando de forma automatizada o tempo de "
    "assentamento angular, o pico de sobretensão transitória e a conformidade regulatória com os Procedimentos de Rede do ONS."
)
novo_conteudo_apendice.append(make_text_p_xml("2FB00101", p_a1_desc))

# Titulo da Secao B
novo_conteudo_apendice.append(make_text_p_xml("2FB00102", "B. Sequência de Telas do Modo Apresentação no Texto", is_heading=True))

# Texto introdutorio da Secao B
p_sec_b_intro = (
    "Além da navegação interativa livre, o painel dispõe de um modo de apresentação estruturado em telas guiadas de alta definição (1920x1080), "
    "concebido para apoiar a exploração pedagógica dos fenômenos transitórios e evidenciar os limites de estabilidade do inversor conectado à rede. "
    "As telas a seguir ilustram os quatro módulos fundamentais desenvolvidos na ferramenta."
)
novo_conteudo_apendice.append(make_text_p_xml("2FB00103", p_sec_b_intro))

# ------------------------------------------------------------------------------
# Tela 1: Modulo Fasorial Dinamico (image36, rId49)
p_t1_desc = (
    "O módulo de animação fasorial no referencial síncrono (Figura A.2) reconstrói em tempo real a trajetória do vetor espacial de tensão da rede "
    "no plano direto-quadratura (vd x vq). O usuário pode reproduzir o evento por meio de animação contínua (play) ou inspecionar o comportamento "
    "quadro a quadro com o cursor temporal do mouse. Na contingência ilustrada na Barra 6, o gráfico evidencia a contração abrupta da amplitude da tensão "
    "durante o curto-circuito e o retorno suave ao círculo unitário na sintonia nominal, comprovando o amortecimento ótimo do laço de controle."
)
novo_conteudo_apendice.append(make_text_p_xml("2FB00104", p_t1_desc))
novo_conteudo_apendice.append(make_caption_xml("2FB00105", "Figura A.2 – Módulo de animação fasorial no referencial síncrono dq sob falta na Barra 6."))
novo_conteudo_apendice.append(make_image_xml("2FB00106", 900000049, "rId49", "dashboard_palco_fasor"))
novo_conteudo_apendice.append(make_source_xml("2FB00107"))

# ------------------------------------------------------------------------------
# Tela 2: Decomposicao em Sequencia Negativa e FFT (image37, rId50)
p_t2_desc = (
    "Durante faltas desbalanceadas na rede (curtos-circuitos monofásicos e bifásicos), a presença de componentes de sequência negativa projeta uma "
    "ondulação oscilatória com frequência de 120 Hz (2ω0) nas componentes de eixo síncrono. O módulo de decomposição espectral (Figura A.3) decompõe "
    "a tensão nas componentes de sequência positiva e negativa e realiza a Transformada Rápida de Fourier (FFT) em tempo real da tensão vq, revelando o "
    "pico pronunciado em 120 Hz transmitido ao ângulo estimado pelo SRF-PLL convencional quando desprovido de filtros desacoplados adicionais."
)
novo_conteudo_apendice.append(make_text_p_xml("2FB00108", p_t2_desc))
novo_conteudo_apendice.append(make_caption_xml("2FB00109", "Figura A.3 – Módulo de decomposição de sequência negativa e análise espectral de Fourier (120 Hz)."))
novo_conteudo_apendice.append(make_image_xml("2FB00110", 900000050, "rId50", "dashboard_palco_seqneg"))
novo_conteudo_apendice.append(make_source_xml("2FB00111"))

# ------------------------------------------------------------------------------
# Tela 3: Perda de Sincronismo e Cycle Slipping (image38, rId51)
p_t3_desc = (
    "A contingência mais severa avaliada no trabalho (falta trifásica franca na Barra 7) é examinada em detalhes no módulo de sincronismo angular (Figura A.4). "
    "Sob parametrização inadequada do SRF-PLL, a severidade do afundamento associada à redução excessiva dos ganhos de malha provoca uma defasagem "
    "angular que excede o limite estático de 90° (1,57 rad). Sem torque restaurador linear, o integrador do VCO perde a capacidade de rastreamento "
    "e opera em escorregamento sucessivo de polos (cycle slipping), ilustrado pelas descontinuidades angulares que culminam no colapso do sincronismo."
)
novo_conteudo_apendice.append(make_text_p_xml("2FB00112", p_t3_desc))
novo_conteudo_apendice.append(make_caption_xml("2FB00113", "Figura A.4 – Módulo de caracterização de perda de sincronismo e cycle slipping sob falta na Barra 7."))
novo_conteudo_apendice.append(make_image_xml("2FB00114", 900000051, "rId51", "dashboard_palco_sinc"))
novo_conteudo_apendice.append(make_source_xml("2FB00115"))

# ------------------------------------------------------------------------------
# Tela 4: Suporte de Reativo ONS Submodulo 2.10 (image39, rId52)
p_t4_desc = (
    "A resposta dinâmica do conversor frente aos requisitos normativos é certificada no módulo regulatório do Submódulo 2.10 do ONS (Figura A.5). "
    "O painel sobrepõe o oscilograma temporal da corrente reativa injetada (iq) às máscaras de suporte de tensão estabelecidas pela legislação brasileira. "
    "A ferramenta verifica automaticamente se a planta atende ao patamar de sustentação de corrente reativa proporcional à retenção de tensão no PCC, "
    "restringindo dinamicamente a corrente ativa para respeitar o círculo de limite térmico dos semicondutores de potência do inversor."
)
novo_conteudo_apendice.append(make_text_p_xml("2FB00116", p_t4_desc))
novo_conteudo_apendice.append(make_caption_xml("2FB00117", "Figura A.5 – Módulo de validação normativa de suporte dinâmico de potência reativa (ONS Submódulo 2.10)."))
novo_conteudo_apendice.append(make_image_xml("2FB00118", 900000052, "rId52", "dashboard_palco_ons"))
novo_conteudo_apendice.append(make_source_xml("2FB00119"))

# Insere todo o bloco novo apos a Fonte da Figura A.1
xml_novo = xml[:p_end_target] + "".join(novo_conteudo_apendice) + xml[p_end_target:]

with open(DOC_XML, "w", encoding="utf-8") as f:
    f.write(xml_novo)

print(f"document.xml atualizado com sucesso ({len(xml_novo)} bytes).")

# Validacao de bem-formacao XML
tree = ET.parse(DOC_XML)
print("Validacao XML: document.xml eh 100% bem-formado!")

