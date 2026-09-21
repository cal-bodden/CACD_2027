#!/usr/bin/env python3
"""Regera a nota 'Conteúdo Programático — íntegra oficial.md' a partir dos CSVs.
Uso, a partir da pasta '01 - Edital e Documentos Oficiais':
    python3 _dados/mapear2.py _dados/edital_itens.csv _dados/cobertura_edital.csv
    python3 _dados/gerar_conteudo_programatico.py
"""
import csv, collections, datetime, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
rows=list(csv.DictReader(open('_dados/edital_itens.csv',encoding='utf-8')))
cob={r['id']:r for r in csv.DictReader(open('_dados/cobertura_edital.csv',encoding='utf-8'))}
ORD=["LP","ING","HB","HM","PI","GEO","ECO","DIR","ESP","FRA"]
NOME={"LP":"Língua Portuguesa","ING":"Língua Inglesa","HB":"História do Brasil","HM":"História Mundial",
      "PI":"Política Internacional","GEO":"Geografia","ECO":"Economia","DIR":"Direito",
      "ESP":"Língua Espanhola","FRA":"Língua Francesa"}
ICON={"consolidado":"🟩","parcial":"🟨","esboco":"🟧","coberto-no-pai":"↳","ausente":"🟥"}
hoje=datetime.date.today().isoformat()
L=[f"""---
title: Conteúdo Programático — íntegra oficial
area: Edital e Documentos Oficiais
subarea: GESTÃO & METADADOS
tags:
  - cacd-2027
  - edital
  - conteudo-programatico
fonte: Edital nº 1, de 28/1/2026 (CACD 2026), Anexo III — Dos Objetos de Avaliação
atualizado: {hoje}
---

# Conteúdo Programático — íntegra oficial

Transcrição integral e numerada do **Anexo III do Edital nº 1, de 28/1/2026**, com um identificador estável por item (`PI-13.4`, `DIR-27`, …) para uso nas notas e nos relatórios de cobertura.

> Esta nota é **gerada automaticamente**. Para atualizá-la depois de mexer no vault:
> ```
> cd "00 - GESTÃO & METADADOS/01 - Edital e Documentos Oficiais"
> python3 _dados/mapear2.py _dados/edital_itens.csv _dados/cobertura_edital.csv
> python3 _dados/gerar_conteudo_programatico.py
> ```

Estado de cada item no vault:

| Marca | Significado |
|:--:|---|
| 🟩 | consolidado — ≥ 20 KB de nota própria |
| 🟨 | parcial — 4 a 20 KB |
| 🟧 | esboço — < 4 KB, praticamente vazio |
| ↳ | tratado dentro da nota do item-pai (agrupamento do vault) |
| 🟥 | **ausente — não há nota alguma** |

---
"""]
for s in ORD:
    itens=[r for r in rows if r['sigla']==s]
    if not itens: continue
    obj=any(i['objetiva']=='sim' for i in itens); dis=any(i['discursiva']=='sim' for i in itens)
    fase=" e ".join(x for x in (["Primeira Fase"] if obj else [])+(["Segunda Fase"] if dis else []))
    c=collections.Counter(cob[i['id']]['status'] for i in itens)
    resumo=" · ".join(f"{ICON[k]} {v}" for k,v in sorted(c.items()) if k in ICON)
    L.append(f"\n## {NOME[s]}  `{s}`\n")
    L.append(f"**{fase}** — {len(itens)} itens no programa\n")
    L.append(f"Cobertura: {resumo}\n")
    for r in itens:
        st=cob[r['id']]['status']; kb=cob[r['id']]['kb']
        ind="  "*(int(r['nivel'])-1)
        extra=f" *({kb} KB)*" if st in ("parcial","esboco") else (" **← sem nota**" if st=="ausente" else "")
        L.append(f"{ind}- {ICON.get(st,'·')} `{r['id']}` **{r['num']}** {r['titulo']}{extra}")
    L.append("")
L.append("""
---

## Notas relacionadas
- [[Mapa Mestre da Prova — CACD]] — como cada fase é pontuada
- [[Cobertura do Edital — Diagnóstico]] — prioridades de trabalho
- [[Mudanças do Edital 2025 → 2026]]
""")
open("Conteúdo Programático — íntegra oficial.md","w",encoding='utf-8').write("\n".join(L))
print("gerado:", sum(1 for r in rows), "itens")
