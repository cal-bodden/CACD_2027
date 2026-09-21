#!/usr/bin/env python3
"""Extrai um registro por item de prova dos arquivos TPS_*.md -> itens_tps.csv"""
import re, os, csv, glob, unicodedata

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
os.chdir(BASE)

DISC = {
 "lingua portuguesa":"LP","lingua inglesa":"ING","historia do brasil":"HB",
 "historia mundial":"HM","politica internacional":"PI","geografia":"GEO",
 "economia":"ECO","direito":"DIR",
}
def slug(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return re.sub(r'\s+',' ',re.sub(r'[^a-z ]',' ',s)).strip()

GAB = re.compile(r'^####\s*Gabarito Oficial:\s*(.+?)\s*$', re.M)

def norm_gab(g):
    g=slug(g)
    if g.startswith('certo'): return 'C'
    if g.startswith('errado'): return 'E'
    if 'anulado' in g: return 'ANULADO'
    return g.upper()[:12] or '?'

rows=[]
for path in sorted(glob.glob("TPS_20*_*.md")):
    m=re.match(r'TPS_(\d{4})_(manha|tarde)\.md$', os.path.basename(path))
    if not m: continue
    ano, turno = m.group(1), m.group(2)
    txt=open(path,encoding='utf-8').read()
    # blocos por questao
    partes=re.split(r'^## Questão\s+(\d+)\s*—\s*(.*?)$', txt, flags=re.M)
    # partes: [pre, num, cabecalho, corpo, num, cabecalho, corpo, ...]
    for i in range(1, len(partes), 3):
        qnum, cab, corpo = partes[i], partes[i+1], partes[i+2]
        d=None
        cs=slug(cab)
        for k,v in DISC.items():
            if k in cs: d=v; break
        ctx=''
        cm=re.search(r'\*\*Contexto:\*\*\s*(.+?)(?=\n###|\Z)', corpo, re.S)
        if cm: ctx=re.sub(r'\s+',' ',cm.group(1)).strip()
        # itens
        its=re.split(r'^###\s*Item\s+(\d+)\s*$', corpo, flags=re.M)
        for j in range(1, len(its), 2):
            inum, ibody = its[j], its[j+1]
            g=GAB.search(ibody)
            texto=GAB.sub('', ibody)
            texto=re.sub(r'^-{3,}\s*$','',texto,flags=re.M)
            texto=re.sub(r'\s+',' ',texto).strip()
            rows.append({
              "ano":ano,"turno":turno,"questao":qnum,"item":inum,
              "disciplina":d or "?", "gabarito":norm_gab(g.group(1)) if g else "?",
              "tem_contexto":"sim" if ctx else "nao",
              "n_chars":len(texto),
              "texto":texto,
              "contexto":ctx[:4000],
            })

with open("_dados/itens_tps.csv","w",newline="",encoding="utf-8") as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

from collections import Counter
print(f"itens extraidos: {len(rows)}")
print("\npor disciplina:")
for d,n in Counter(r['disciplina'] for r in rows).most_common():
    print(f"  {d:5s} {n:5d}")
print("\npor ano:")
for a,n in sorted(Counter(r['ano'] for r in rows).items()):
    print(f"  {a} {n:5d}")
print("\ngabarito:", dict(Counter(r['gabarito'] for r in rows)))
