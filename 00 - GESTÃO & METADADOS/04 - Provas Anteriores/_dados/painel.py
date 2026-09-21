#!/usr/bin/env python3
"""Painel de preparação: por tópico do edital cruza
   incidência (2017-2026) x seu desempenho x estado da nota."""
import csv, os, re, sys
from collections import defaultdict, Counter
BASE=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..")
os.chdir(BASE)   # 00 - GESTÃO & METADADOS
P="04 - Provas Anteriores/_dados"

itens=[r for r in csv.DictReader(open(f"{P}/itens_classificados.csv",encoding='utf-8')) if r['edital_id']]
cob={r['id']:r for r in csv.DictReader(open("01 - Edital e Documentos Oficiais/_dados/cobertura_edital.csv",encoding='utf-8'))}

# respostas do candidato (2026)
resp={}
for line in open("05 - Relatórios de Desempenho/Prova_2026.md",encoding='utf-8'):
    m=re.match(r'\s*(\d+)\s*-\s*(C|E|Branco)\s*$', line.strip())
    if m: resp[int(m.group(1))]=m.group(2)

ag=defaultdict(lambda: dict(n=0,anos=set(),ult=0,alta=0,resp=0,ok=0,err=0,br=0))
for r in itens:
    k=r['edital_id']; a=ag[k]
    a['n']+=1; a['anos'].add(r['ano']); a['ult']=max(a['ult'],int(r['ano']))
    if r['conf']=='alta': a['alta']+=1
    if r['ano']=='2026' and r['gabarito'] in ('C','E'):
        v=resp.get(int(r['item']))
        if v is None: continue
        a['resp']+=1
        if v=='Branco': a['br']+=1
        elif v==r['gabarito']: a['ok']+=1
        else: a['err']+=1

def titulo(k):
    return cob[k]['titulo'] if k in cob else k
def status(k):
    return cob[k]['status'] if k in cob else '?'

linhas=[]
for k,a in ag.items():
    aval=a['ok']+a['err']
    pct = (100*a['ok']/aval) if aval else None
    linhas.append(dict(
        edital_id=k, disciplina=k.split('-')[0], titulo=titulo(k),
        itens=a['n'], anos=len(a['anos']), ultimo=a['ult'],
        conf_alta=a['alta'],
        resp_2026=a['resp'], acertos_2026=a['ok'], erros_2026=a['err'], brancos_2026=a['br'],
        pct_2026=("" if pct is None else round(pct,1)),
        estado_nota=status(k),
    ))
linhas.sort(key=lambda x:(-x['itens'], x['edital_id']))
with open(f"{P}/painel_preparacao.csv","w",newline="",encoding="utf-8") as fh:
    w=csv.DictWriter(fh,fieldnames=list(linhas[0].keys())); w.writeheader(); w.writerows(linhas)

print(f"topicos com incidencia medida: {len(linhas)}\n")
print("TOP 25 — tópicos mais cobrados (2017-2026)")
print(f"{'id':10s} {'itens':>5s} {'anos':>4s} {'ult':>4s} {'2026':>10s}  {'nota':12s} título")
for r in linhas[:25]:
    d=f"{r['acertos_2026']}/{r['acertos_2026']+r['erros_2026']}" if (r['acertos_2026']+r['erros_2026']) else "—"
    print(f"{r['edital_id']:10s} {r['itens']:5d} {r['anos']:4d} {r['ultimo']:4d} {d:>10s}  {r['estado_nota']:12s} {r['titulo'][:52]}")
