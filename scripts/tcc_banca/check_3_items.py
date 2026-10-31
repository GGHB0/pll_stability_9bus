import zipfile
import sys

sys.stdout.reconfigure(encoding='utf-8')
docx_path = r'C:\Users\gilbr\OneDrive\UERJ\TCC - Victor e Bruno\Template Modelo TCC\01_TCC_Monografia_Final\TCC_Victor_Bruno_VFinal.docx'
with zipfile.ZipFile(docx_path, 'r') as z:
    xml = z.read('word/document.xml').decode('utf-8')

# 1. Trabalhos Futuros
pos = xml.find('Trabalhos Futuros', 740000)
if pos != -1:
    start_p = xml.rfind('<w:p ', 0, pos)
    end_p = xml.find('</w:p>', pos) + 6
    p_xml = xml[start_p:end_p]
    print("TF heading XML:", p_xml)

# 2. Remissao arquitetura do SRF-PLL
pos2 = xml.find('arquitetura do SRF-PLL')
if pos2 != -1:
    start_p = xml.rfind('<w:p ', 0, pos2)
    end_p = xml.find('</w:p>', pos2) + 6
    print("Remissao XML:", xml[start_p:end_p])

# 3. Roadmap
pos3 = xml.find('System Stability Roadmap')
if pos3 != -1:
    start_p = xml.rfind('<w:p ', 0, pos3)
    end_p = xml.find('</w:p>', pos3) + 6
    print("Roadmap XML:", xml[start_p:end_p])

