#!/usr/bin/env python3
"""Dump dos itens de um tópico do edital, com a resposta do candidato quando houver.
Uso: python3 ver_topico.py HB-6 [largura_texto]"""
import csv, re, sys, os
BASE=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
os.chdir(BASE)
alvo=sys.argv[1]; W=int(sys.argv[2]) if len(sys.argv)>2 else 210
rows=[r for r in csv.DictReader(open('_dados/itens_classificados.csv',encoding='utf-8')) if r['edital_id']==alvo]
resp={}
for line in open("../05 - Relatórios de Desempenho/Prova_2026.md",encoding='utf-8'):
    m=re.match(r'\s*(\d+)\s*-\s*(C|E|Branco)\s*$', line.strip())
    if m: resp[int(m.group(1))]=m.group(2)
print(f"### {alvo}: {len(rows)} itens\n")
for r in sorted(rows,key=lambda x:(x['ano'],int(x['item']))):
    mk=""
    if r['ano']=='2026':
        v=resp.get(int(r['item']))
        if v: mk="  <<VOCÊ:"+v+("✗" if (v!=r['gabarito'] and v!='Branco') else ("✓" if v==r['gabarito'] else "·"))+">>"
    print(f"[{r['ano']}·{r['item']:>3s}] {r['gabarito']:<7s}{mk}\n  {r['texto'][:W]}")
