"""Caminhos da skill: repo, saídas e pastas pessoais (OneDrive) de cada máquina.

A pasta "TCC - Victor e Bruno" do OneDrive muda de lugar entre o PC do Victor e o
do Bruno. Ordem de busca: `config.py` da skill (gitignored, copiado de
`config.example.py`), depois os caminhos conhecidos dos dois.
"""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
ROOT = SKILL.parents[2]
sys.path.insert(0, str(SKILL))
sys.path.insert(0, str(ROOT / "scripts" / "notas"))  # pdfnote.py

try:
    import config  # noqa: E402
except ImportError:
    config = None

_CANDIDATOS = [
    Path.home() / "OneDrive" / "Meus Bagulhos" / "Arquivos" / "UERJ" / "TCC - Victor e Bruno",
    Path.home() / "OneDrive" / "UERJ" / "TCC - Victor e Bruno",
]


def _tcc_dir() -> Path:
    if config is not None and getattr(config, "TCC_DIR", None):
        return Path(config.TCC_DIR)
    for p in _CANDIDATOS:
        if p.exists():
            return p
    return _CANDIDATOS[-1]


TCC_DIR = _tcc_dir()
TEMPLATE_DIR = TCC_DIR / "Template Modelo TCC"  # onde as cópias dos .docx são entregues
RAP_PDF = TCC_DIR / "Bibliografia" / "RAP 2023.08.15 08h030min versão final.pdf"

# Miniaturas dos slides (s01.png...): render.ps1 da skill tcc-pptx-editor sobre uma cópia do deck
SLIDES_PNG = Path(getattr(config, "SLIDES_PNG", None) or r"C:\Temp\defesa_roteiro\png")
PALCO_PNG = ROOT / "output" / "verifica_palco" / "1920x1080"  # scripts/verifica_palco.py
CACHE = SLIDES_PNG.parent / "jpg"
OUTPUT = ROOT / "output"
CONTEUDO = SKILL / "conteudo"
ENTREGAR = "--sem-onedrive" not in sys.argv  # gerar.py ... --sem-onedrive: só output/


def conteudo_texto() -> str:
    """Texto do roteiro de estudo, na ordem dos arquivos de conteudo/."""
    return "\n".join(p.read_text(encoding="utf-8") for p in sorted(CONTEUDO.glob("*.py")))


def entregar(origem: Path, nome: str):
    """Copia o .docx para a pasta do template no OneDrive (com sufixo se estiver aberto)."""
    import shutil
    if not ENTREGAR:
        return
    destino = TEMPLATE_DIR / nome
    try:
        shutil.copy2(origem, destino)
        print(f"[OK] Cópia no OneDrive: {destino}")
    except PermissionError:
        alt = destino.with_name(destino.stem + "_atualizado" + destino.suffix)
        shutil.copy2(origem, alt)
        print(f"[OK] Original aberto no Word; cópia em: {alt}")
    except OSError as e:
        print(f"[AVISO] Não foi possível copiar para o OneDrive ({e}).")


def salvar(doc, saida: Path) -> Path:
    """Salva o .docx em output/; se o arquivo estiver aberto no Word, salva com sufixo."""
    saida.parent.mkdir(parents=True, exist_ok=True)
    try:
        doc.save(str(saida))
    except PermissionError:
        saida = saida.with_name(saida.stem + "_atualizado" + saida.suffix)
        doc.save(str(saida))
    print(f"[OK] Salvo em: {saida} ({saida.stat().st_size:,} bytes)")
    return saida
