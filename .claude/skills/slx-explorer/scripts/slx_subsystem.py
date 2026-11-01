# -*- coding: utf-8 -*-
"""Lista blocos, parâmetros e ligações de um subsistema do .slx, sem MATLAB.

Uso: python slx_subsystem.py <SID | nome> [--slx caminho.slx] [--all-params]

  <SID>   número do subsistema (abre simulink/systems/system_<SID>.xml)
  <nome>  nome do bloco SubSystem (busca em todos os systems; parcial,
          sem diferenciar maiúsculas). Ambíguo → lista os candidatos.

Saída: blocos com tipo, nome, SID e os parâmetros que definem comportamento
(Gain, Numerator, Inputs, GotoTag...), depois o grafo de ligações
"origem → destino" com nomes resolvidos. É o grafo que responde perguntas do
tipo "existe desacoplamento ωL?" ou "o que vem depois do PI?".
"""
import io, re, sys, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DEFAULT_SLX = Path(__file__).resolve().parents[4] / 'pll_stability_9bus.slx'
# Parâmetros de layout/aparência: nunca interessam para entender o modelo.
SKIP = {'Position', 'ZOrder', 'Ports', 'BackgroundColor', 'ForegroundColor',
        'NamePlacement', 'ShowName', 'FontSize', 'IconDisplay', 'Orientation',
        'BlockMirror', 'LibraryVersion', 'DropShadow', 'ShowPortLabels',
        'ContentPreviewEnabled', 'HideAutomaticName'}


def args():
    a = sys.argv[1:]
    if not a or a[0] in ('-h', '--help'):
        print(__doc__); sys.exit(0)
    slx = Path(a[a.index('--slx') + 1]) if '--slx' in a else DEFAULT_SLX
    return a[0], slx, '--all-params' in a


def find_sid(z, target):
    if target.isdigit():
        return target
    hits = []
    for n in z.namelist():
        if not n.startswith('simulink/systems/system_'):
            continue
        root = ET.fromstring(z.read(n))
        for b in root.iter('Block'):
            if b.get('BlockType') == 'SubSystem' and target.lower() in b.get('Name', '').lower():
                hits.append((b.get('SID'), b.get('Name').replace('\n', ' '), n))
    if len(hits) == 1:
        return hits[0][0]
    print('Nenhum subsistema com esse nome.' if not hits else 'Ambíguo:')
    for sid, name, n in hits:
        print(f'  SID {sid:>5}  {name}  (dentro de {n.split("/")[-1]})')
    sys.exit(1)


def endpoints(line):
    """Origem e todos os destinos de uma <Line>, incluindo <Branch> aninhados."""
    src = next((p.text for p in line.findall('P') if p.get('Name') == 'Src'), None)
    dsts = [p.text for p in line.iter('P') if p.get('Name') == 'Dst']
    return src, dsts


def main():
    target, slx, all_params = args()
    with zipfile.ZipFile(slx) as z:
        sid = find_sid(z, target)
        name = f'simulink/systems/system_{sid}.xml'
        if name not in z.namelist():
            sys.exit(f'{name} não existe (SID de bloco que não é subsistema?)')
        root = ET.fromstring(z.read(name))

    names = {}
    print(f'== system_{sid}.xml ({slx.name}) ==\n')
    for b in root.findall('Block'):
        bt, bn, bs = b.get('BlockType'), b.get('Name', '').replace('\n', ' '), b.get('SID')
        names[bs] = bn
        ps = {p.get('Name'): (p.text or '').strip() for p in b.findall('P')}
        ps.update({p.get('Name'): (p.text or '').strip() for p in b.findall('InstanceData/P')})
        if not all_params:
            ps = {k: v for k, v in ps.items() if k not in SKIP and v}
        extra = '  ' + '; '.join(f'{k}={v}' for k, v in ps.items()) if ps else ''
        print(f'[{bt}] {bn} (SID {bs}){extra}')

    def label(ep):
        m = re.match(r'(\d+)#(\w+):(\d+)', ep or '')
        if not m:
            return ep
        port = '' if m.group(3) == '1' else f':{m.group(2)}{m.group(3)}'
        return names.get(m.group(1), m.group(1)) + port

    print('\n== ligações ==')
    for line in root.findall('Line'):
        src, dsts = endpoints(line)
        print(f'{label(src)} → {", ".join(label(d) for d in dsts)}')


if __name__ == '__main__':
    main()
