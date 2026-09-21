#!/usr/bin/env python3
"""Classifica cada item de prova num tópico do edital, usando lexico.py.
Score = soma dos pesos IDF das palavras do léxico encontradas no item,
restrito aos tópicos da disciplina do item."""
import csv, os, re, sys, math, unicodedata
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lexico import LEX

BASE=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
os.chdir(BASE)

STOP=set("de da do das dos e a o as os um uma no na nos nas em por para com que se ao aos à às pelo pela dos sua seu suas seus como entre sobre".split())
def norm(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9 ]',' ',s)
def toks(s):
    return [w for w in norm(s).split() if len(w)>2 and w not in STOP]

# bag por topico
bag={k:set(toks(v[1])) for k,v in LEX.items()}
# IDF sobre os topicos
df=Counter()
for s in bag.values():
    for w in s: df[w]+=1
N=len(bag)
idf={w: math.log(N/df[w]) + 1.0 for w in df}

por_disc=defaultdict(list)
for k in bag:
    por_disc[k.split('-')[0]].append(k)

rows=list(csv.DictReader(open("_dados/itens_tps.csv",encoding='utf-8')))
out=[]
for r in rows:
    d=r['disciplina']
    cands=por_disc.get(d,[])
    if not cands:
        out.append({**r,"edital_id":"","score":0,"margem":0,"conf":"n/a"}); continue
    txt=set(toks(r['texto']+" "+r['contexto']))
    sc={k: sum(idf[w] for w in bag[k] & txt) for k in cands}
    ordenado=sorted(sc.items(), key=lambda x:-x[1])
    top, s1 = ordenado[0]
    s2 = ordenado[1][1] if len(ordenado)>1 else 0.0
    margem = s1-s2
    if s1==0: conf="nenhum"
    elif s1>=6 and margem>=2: conf="alta"
    elif s1>=3: conf="media"
    else: conf="baixa"
    out.append({**r,"edital_id":top if s1>0 else "","score":round(s1,2),"margem":round(margem,2),"conf":conf})

campos=[c for c in out[0].keys() if c not in ("contexto",)]
with open("_dados/itens_classificados.csv","w",newline="",encoding="utf-8") as fh:
    w=csv.DictWriter(fh,fieldnames=campos,extrasaction='ignore'); w.writeheader(); w.writerows(out)

c=Counter(r['conf'] for r in out)
print("confianca da classificacao:", dict(c))
print(f"  classificados: {sum(1 for r in out if r['edital_id'])}/{len(out)}")
for d in ("PI","HB","HM","GEO","ECO","DIR","LP","ING"):
    sel=[r for r in out if r['disciplina']==d]
    if not sel: continue
    cc=Counter(r['conf'] for r in sel)
    print(f"  {d:4s} n={len(sel):4d}  alta={cc['alta']:4d} media={cc['media']:4d} baixa={cc['baixa']:4d} nenhum={cc['nenhum']:4d}")
