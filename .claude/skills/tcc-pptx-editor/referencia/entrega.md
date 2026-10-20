# Staging, finalize e entrega

Continuação de `SKILL.md`. Mesmo desenho da entrega do DOCX
(`tcc-docx-editor/referencia/entrega.md`), adaptado ao PowerPoint.

## Staging

```bash
mkdir -p /c/Temp/defesa_<tema>
cp "<PPTX_SOURCE de config.py>" /c/Temp/defesa_<tema>/deck.pptx
md5sum "<PPTX_SOURCE>"          # vai para o -Md5Staging da entrega
```

- Pasta por tema: o Bruno e outra sessão podem estar mexendo no deck. Nunca
  editar no OneDrive direto, nem com o python-pptx nem pelo COM.
- O `gen_*.py` lê sempre `deck.pptx` do staging e grava `montado.pptx`.
  Reexecutar = recomeçar do staging, nunca encadear sobre a própria saída.

## Finalize

```powershell
powershell -ExecutionPolicy Bypass -File scripts\pptx_finalize.ps1 `
  -In C:\Temp\defesa_<tema>\montado.pptx -Out C:\Temp\defesa_<tema>\final.pptx [-Pdf]
```

Prova que o PowerPoint abre o arquivo **sem pedir reparo** e regrava no
formato dele. O python-pptx grava pacotes que o próprio python-pptx reabre
mas que o PowerPoint recusa (id de forma repetido, relação apontando para
mídia removida). `-Pdf`: cópia de segurança para o dia da defesa.

## Entrega

```powershell
powershell -ExecutionPolicy Bypass -File scripts\entrega.ps1 `
  -Final C:\Temp\defesa_<tema>\final.pptx -Dest "<canônico>" -Md5Staging <md5>
```

Ordem fixa, aborta sem tocar no canônico:

1. Fecha o PowerPoint pelo COM, salvando o que estiver por salvar (nunca
   `Stop-Process`); anota o que estava aberto.
2. Sem lock `~$Defesa_TCC_SRF-PLL.pptx` na pasta.
3. MD5 do canônico = MD5 do staging, conferido **depois** de fechar o
   PowerPoint (o Word regravou o canônico ao sair em 2026-10-03; o PowerPoint
   pode fazer o mesmo).
4. Backup datado em `Template Modelo TCC\_backups\defesa\`.
5. Copia o final, confere o MD5 do destino, reabre o que estava aberto.

Depois, sempre:

```text
python.exe scripts\diff_slides.py "<backup gravado>" "<canônico>"
```

Só pode aparecer o que o plano previa. Diferença a mais → investigar antes
de dizer "entregue".

- "ABORTADO: PowerPoint nao fechou em 30 s" logo depois do finalize
  com `-Pdf`: a instância do finalize ainda estava saindo. Conferir
  `Get-Process POWERPNT`; sem processo, rodar a entrega de novo (o
  canônico não foi tocado). Com processo, é diálogo aberto: avisar o Victor.
- Pastas `C:\Temp\defesa_*` não são apagadas na entrega (o backup que
  vale é o de `_backups\defesa\`); limpar só a pedido do Victor.

## MD5 mudou

- **Antes da entrega** (o Victor ou o Bruno salvaram): refazer o staging e
  rodar o `gen_*.py` de novo sobre o deck atual. Sync do OneDrive chega em
  rajadas: esperar o MD5 parar de mudar.
- **Depois da entrega**: conferir com `find_text.py` uma frase-assinatura
  de cada edição no canônico atual antes de qualquer reaplicação.
