#!/usr/bin/env python3
"""Cruza itens do edital x notas do vault. Herda cobertura do item-pai quando o
vault agrupa sub-itens numa unica pasta (caso comum em Economia e PI)."""
import csv, os, re, sys
from collections import defaultdict, Counter

VAULT = "/home/hyprtest/Documents/CACD_2027"

DISC_DIR = {
 "01 - LÍNGUA PORTUGUESA": "LP", "02 - LÍNGUA INGLESA": "ING",
 "03 - HISTÓRIA DO BRASIL": "HB", "04 - HISTÓRIA MUNDIAL": "HM",
 "05 - POLÍTICA INTERNACIONAL": "PI", "06 - GEOGRAFIA": "GEO",
 "07 - ECONOMIA": "ECO", "08 - DIREITO": "DIR",
 "09 - IDIOMA ADICIONAL (2ª Fase)": "IDA",
}
pref = re.compile(r"^(\d{1,2}(?:\.\d{1,2}){0,2})\s*[-–.]?\s")
def numero(seg):
    m = pref.match(seg.strip())
    return ".".join(str(int(p)) for p in m.group(1).split(".")) if m else None

notas = []
for disc_dir, sigla in DISC_DIR.items():
    root = os.path.join(VAULT, disc_dir)
    if not os.path.isdir(root): continue
    for dirpath, _d, files in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        segs = [] if rel == "." else rel.split(os.sep)
        for f in files:
            if not f.endswith(".md"): continue
            p = os.path.join(dirpath, f)
            notas.append({"sigla": sigla, "path": os.path.relpath(p, VAULT),
                          "segs": segs, "nome": f[:-3], "bytes": os.path.getsize(p)})

# pastas de idiomas nao seguem a numeracao do edital: mapa explicito
IDIOMA = {
 ("ING","01 - Primeira Fase","1 - Compreensão de textos escritos"): "ING-1F-1",
 ("ING","01 - Primeira Fase","2 - Itens gramaticais relevantes"): "ING-1F-2",
 ("ING","02 - Segunda Fase","1 - Redação em língua inglesa"): "ING-2F-1",
 ("ING","02 - Segunda Fase","2 - Resumo (conforme Tabela 6.2 do Edital)"): "ING-2F-1",
 ("ING","02 - Segunda Fase","3 - Tradução (conforme Anexo III do Edital)"): "ING-2F-2",
 ("IDA","01 - Espanhol","1 - Elaboração de resumo"): "ESP-1",
 ("IDA","01 - Espanhol","2 - Versão do português para o espanhol"): "ESP-2",
 ("IDA","01 - Espanhol","Aulas Espanhol"): "ESP-1",
 ("IDA","02 - Francês","1 - Elaboração de resumo"): "FRA-1",
 ("IDA","02 - Francês","2 - Versão do português para o francês"): "FRA-2",
}

def id_do_caminho(sigla, segs):
    if sigla in ("ING","IDA"):
        return IDIOMA.get((sigla, *segs[:2]))
    nums = [numero(s) for s in segs]
    if sigla == "DIR":
        return f"DIR-{nums[1].split('.')[0]}" if len(nums) >= 2 and nums[1] else None
    if not nums or not nums[0]: return None
    cand = nums[0]
    for nxt in nums[1:]:
        if nxt and nxt.startswith(cand + "."): cand = nxt
        else: break
    return f"{sigla}-{cand}"

for n in notas: n["edital_id"] = id_do_caminho(n["sigla"], n["segs"])
por_id = defaultdict(list)
for n in notas:
    if n["edital_id"]: por_id[n["edital_id"]].append(n)

def util(ns):
    """bytes de notas de conteudo (exclui hub '_Nome.md' pequeno)"""
    return sum(n["bytes"] for n in ns if not (n["nome"].startswith("_") and n["bytes"] < 4000))

itens = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
por_item = {it["id"]: it for it in itens}
filhos = defaultdict(list)
for it in itens:
    if int(it["nivel"]) > 1:
        filhos[f"{it['sigla']}-{it['num'].rsplit('.',1)[0]}"].append(it["id"])

def desc(iid):
    out = []
    for c in filhos.get(iid, []):
        out.append(c); out.extend(desc(c))
    return out

def classifica(kb, tem_nota):
    if not tem_nota: return "ausente"
    if kb < 4:  return "esboco"
    if kb < 20: return "parcial"
    return "consolidado"

out = []
for it in itens:
    iid = it["id"]
    diretas = por_id.get(iid, [])
    kb_dir = util(diretas)/1024
    kb_desc = sum(util(por_id.get(d, []))/1024 for d in desc(iid))
    kb_tot = kb_dir + kb_desc
    if diretas or kb_desc:
        status = classifica(kb_tot, True)
        origem = "propria" if diretas else "descendentes"
    else:
        # procura no ancestral: vault agrupa sub-itens na pasta do pai
        anc, achou = iid, None
        while "." in anc.split("-",1)[1]:
            anc = f"{it['sigla']}-{anc.split('-',1)[1].rsplit('.',1)[0]}"
            if por_id.get(anc) and util(por_id[anc]) > 0:
                achou = anc; break
        if achou:
            status, origem, kb_tot = "coberto-no-pai", achou, round(util(por_id[achou])/1024,1)
        else:
            status, origem = "ausente", ""
    out.append({**it, "status": status, "kb": round(kb_tot,1),
                "notas_diretas": len(diretas), "origem": origem,
                "pasta": os.path.dirname(diretas[0]["path"]) if diretas else ""})

with open(sys.argv[2],"w",newline="",encoding="utf-8") as fh:
    w=csv.DictWriter(fh,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)

print(f"notas indexadas: {len(notas)}\n")
print(f"{'':5s} {'itens':>5s} {'consol':>7s} {'parcial':>7s} {'esboco':>7s} {'no-pai':>7s} {'ausente':>7s}   KB")
for s in ["LP","ING","HB","HM","PI","GEO","ECO","DIR","ESP","FRA"]:
    sel=[r for r in out if r["sigla"]==s]
    if not sel: continue
    c=Counter(r["status"] for r in sel)
    kb=sum(util(v) for k,v in por_id.items() if k.startswith(s+"-"))/1024
    print(f"{s:5s} {len(sel):5d} {c['consolidado']:7d} {c['parcial']:7d} {c['esboco']:7d} {c['coberto-no-pai']:7d} {c['ausente']:7d}  {kb:7.0f}")
print("\n=== LACUNAS REAIS (ausente/esboco) ===")
for r in out:
    if r["status"] in ("ausente","esboco"):
        print(f"  [{r['status']:9s}] {r['id']:12s} {r['titulo'][:80]}")
