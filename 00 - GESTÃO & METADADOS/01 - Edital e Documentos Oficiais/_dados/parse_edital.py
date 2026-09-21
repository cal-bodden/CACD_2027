#!/usr/bin/env python3
"""Converte o Anexo III (Dos Objetos de Avaliacao) do edital CACD em CSV estruturado."""
import re, csv, sys, json, unicodedata

SRC = sys.argv[1]
OUT = sys.argv[2]

DISC = {
    "LÍNGUA PORTUGUESA": ("LP", "Língua Portuguesa"),
    "LÍNGUA INGLESA": ("ING", "Língua Inglesa"),
    "HISTÓRIA DO BRASIL": ("HB", "História do Brasil"),
    "HISTÓRIA MUNDIAL": ("HM", "História Mundial"),
    "POLÍTICA INTERNACIONAL": ("PI", "Política Internacional"),
    "GEOGRAFIA": ("GEO", "Geografia"),
    "ECONOMIA": ("ECO", "Economia"),
    "DIREITO": ("DIR", "Direito"),
    "LÍNGUA ESPANHOLA": ("ESP", "Língua Espanhola"),
    "LÍNGUA FRANCESA": ("FRA", "Língua Francesa"),
}

raw = open(SRC, encoding="utf-8").read()

# quebra por disciplina
head_re = re.compile(r"^(" + "|".join(map(re.escape, DISC)) + r") \((.*?)\):", re.M)
marks = list(head_re.finditer(raw))
blocks = []
for i, m in enumerate(marks):
    end = marks[i+1].start() if i+1 < len(marks) else len(raw)
    body = raw[m.end():end]
    blocks.append((m.group(1), m.group(2), body))

# junta linhas quebradas do pdftotext
def flatten(t):
    t = re.sub(r"-\n", "", t)           # hifenizacao de quebra
    t = re.sub(r"\s*\n\s*", " ", t)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip()

# numeracao: "12 " ou "3.4 " ou "1.1.1 " seguido de maiuscula/abertura
num_re = re.compile(r"(?<![\w.,/º§-])(\d{1,2}(?:\.\d{1,2}){0,2})\.?\s+(?=[A-ZÀ-ÜÍÉÓÚÂÊÔÃÕÇ“\"O])")

rows = []
for disc_nome, fases_txt, body in blocks:
    sigla, nome = DISC[disc_nome]
    txt = flatten(body)
    obj = "Primeira" in fases_txt
    dis = "Segunda" in fases_txt
    # "Primeira Fase: ... Segunda Fase: ..." (caso Ingles) -> marca sub-blocos
    hits = list(num_re.finditer(txt))
    for j, h in enumerate(hits):
        num = h.group(1).rstrip(".")
        end = hits[j+1].start() if j+1 < len(hits) else len(txt)
        titulo = txt[h.end():end].strip()
        titulo = re.sub(r"\s+", " ", titulo).strip(" .;")
        if not titulo:
            continue
        # descarta falsos positivos muito curtos e sem letra
        if len(titulo) < 3:
            continue
        nivel = num.count(".") + 1
        rows.append({
            "id": f"{sigla}-{num}",
            "disciplina": nome,
            "sigla": sigla,
            "num": num,
            "nivel": nivel,
            "titulo": titulo,
            "objetiva": "sim" if obj else "nao",
            "discursiva": "sim" if dis else "nao",
        })

# valida sequencia de numeracao de topo por disciplina
prob = []
for sigla, nome in DISC.values():
    tops = [int(r["num"]) for r in rows if r["sigla"] == sigla and r["nivel"] == 1]
    esperado = list(range(1, len(tops)+1))
    if tops != esperado:
        prob.append((sigla, tops))

with open(OUT, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

print(f"itens: {len(rows)}")
from collections import Counter
c = Counter(r["sigla"] for r in rows)
for s, n in c.items():
    tops = sum(1 for r in rows if r["sigla"]==s and r["nivel"]==1)
    print(f"  {s}: {n} itens ({tops} de nivel 1)")
if prob:
    print("ALERTA numeracao de topo fora de sequencia:")
    for s, t in prob:
        print("  ", s, t)
