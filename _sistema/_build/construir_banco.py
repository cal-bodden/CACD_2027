#!/usr/bin/env python3
"""Constrói _sistema/itens.jsonl a partir dos TPS_*.md (itens autênticos) + gabaritos oficiais (anulados),
classifica por tópico do edital (lexico.py) e gera respostas_2026.tsv / carga inicial de erros.jsonl.
Reprodutível: rode de novo sempre que os TPS_*.md ou o lexico.py mudarem.
Uso: python3 construir_banco.py [--gab DIR_COM_TXT_DOS_GABARITOS] [--mapa2026 mapa_2026.json --folha2026 folha.json]
"""
import re, os, sys, json, glob, unicodedata, collections, math, csv, argparse
V = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
G = [d for d in os.listdir(V) if unicodedata.normalize("NFC", d).startswith("00 - GEST")][0]
PA = os.path.join(V, G, [x for x in os.listdir(os.path.join(V, G)) if x.startswith("04")][0])
SIS = os.path.join(V, "_sistema")
ap = argparse.ArgumentParser(); ap.add_argument("--gab", default=None); ap.add_argument("--mapa2026"); ap.add_argument("--folha2026"); ap.add_argument("--extra", action="append", default=[])
args = ap.parse_args()

def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]", " ", s)
ABREV = {"Língua Portuguesa": "LP", "Língua Inglesa": "ING", "História do Brasil": "HB", "História Mundial": "HM",
         "Política Internacional": "PI", "Geografia": "GEO", "Economia": "ECO", "Direito": "DIR"}

# ---------- 1. itens dos TPS_*.md ----------
itens = []
for path in sorted(glob.glob(os.path.join(PA, "TPS_*_*.md"))):
    m = re.match(r"TPS_(\d{4})_(manha|tarde)\.md$", os.path.basename(path)); ano, turno = int(m.group(1)), m.group(2)
    txt = open(path, encoding="utf-8").read()
    partes = re.split(r"^## Questão\s+(\d+)\s*—\s*(.*?)$", txt, flags=re.M)
    for i in range(1, len(partes), 3):
        qnum, cab, corpo = int(partes[i]), partes[i+1], partes[i+2]
        disc = cab.split("—")[-1].strip()
        cm = re.search(r"\*\*Contexto:\*\*\s*(.+?)(?=\n###|\Z)", corpo, re.S)
        ctx = re.sub(r"\s+", " ", cm.group(1)).strip() if cm else ""
        its = re.split(r"^###\s*Item\s+(\d+)\s*$", corpo, flags=re.M)
        for j in range(1, len(its), 2):
            inum, body = int(its[j]), its[j+1]
            gm = re.search(r"^####\s*Gabarito Oficial:\s*(.+?)\s*$", body, re.M)
            g = norm(gm.group(1)).strip() if gm else ""
            gab = "C" if g.startswith("certo") else "E" if g.startswith("errado") else None
            enun = re.sub(r"\s+", " ", re.sub(r"^-{3,}\s*$", "", re.sub(r"^####.*$", "", body, flags=re.M), flags=re.M)).strip()
            flat = ano >= 2025  # formato Cebraspe 2025+: 1 item por "questão", numeração corrida
            T = "M" if turno == "manha" else "T"
            iid = f"{ano}-{T}-{qnum:03d}" if flat else f"{ano}-{T}-Q{qnum:02d}-{inum}"
            itens.append(dict(id=iid, ano=ano, turno=turno, banca=("CEBRASPE" if ano >= 2024 or ano <= 2016 else "IADES"),
                              disciplina=disc, questao=qnum, item=(qnum if flat else inum), contexto=ctx, enunciado=enun,
                              gabarito=gab, anulado=None, gabarito_verificado=False, topico_edital=None, topico_incerto=True,
                              origem="autentico"))
print(f"itens lidos dos TPS_*.md: {len(itens)}")

# ---------- 2. gabaritos oficiais ----------
def parse_cebraspe_flat(path):           # 2025/2026: "Item 1 2 3.." / "Gabarito C E X.."
    g = {}; L = open(path, encoding="utf-8").read().splitlines()
    for i, l in enumerate(L):
        if re.match(r"\s*Item\s+\d", l):
            nums = [int(x) for x in re.findall(r"\d+", l)]; vals = re.findall(r"\b([CEX])\b", L[i+1])
            if len(nums) == len(vals): g.update(zip(nums, vals))
    return g                              # {n: C/E/X}
def parse_cebraspe_q4(path):             # 2016/2024: "Questão N ..." / "C E X C ..."
    g = {}; L = open(path, encoding="utf-8").read().splitlines()
    for i, l in enumerate(L):
        qs = [int(x) for x in re.findall(r"Quest[ãa]o\s*(\d+)", l)]
        if qs:
            for k in range(i+1, min(i+4, len(L))):
                vals = re.findall(r"(?<![A-Za-z])[CEX](?![A-Za-z])", L[k])
                if len(vals) >= 4*len(qs): 
                    for qi, q in enumerate(qs): g[q] = vals[4*qi:4*qi+4]
                    break
    return g                              # {q: [v1..v4]}
def parse_iades(path):                    # 2020/2022/2023, só Prova Tipo "A" de MANHÃ e TARDE
    g = {}; L = open(path, encoding="utf-8").read().splitlines(); sec = None; tipo = None
    for i, l in enumerate(L):
        s = l.strip()
        if s in ("MANHÃ", "TARDE"): sec = s; tipo = None; continue
        mt = re.search(r"Prova Tipo\s*[“\"]?([A-D])", l)
        if mt: tipo = mt.group(1); continue
        qs = [int(x) for x in re.findall(r"QUEST[ÃA]O\s*(\d+)", l)]
        if qs and tipo == "A" and sec:
            for k in range(i+1, min(i+4, len(L))):
                vals = re.findall(r"(?<![A-Za-z#])[CE#](?![A-Za-z#])", L[k])
                if len(vals) >= 4*len(qs):
                    for qi, q in enumerate(qs): g[q] = ["X" if v == "#" else v for v in vals[4*qi:4*qi+4]]
                    break
    return g
oficial = {}   # (ano, questao, item) -> C/E/X
if args.gab:
    for t, tag in (("manha", "M"), ("tarde", "T")):
        for ano in (2025, 2026):
            p = os.path.join(args.gab, f"gab_{ano}_{t}.txt")
            if os.path.exists(p):
                for n, v in parse_cebraspe_flat(p).items(): oficial[(ano, n, n)] = v
        p = os.path.join(args.gab, f"gab_2024_{t}.txt")
        if os.path.exists(p):
            for q, vs in parse_cebraspe_q4(p).items():
                for k, v in enumerate(vs, 1): oficial[(2024, q, k)] = v
    for n, ano in ((1, 2016), (2, 2016)):
        p = os.path.join(args.gab, f"gab_2016_{n}.txt")
        if os.path.exists(p):
            for q, vs in parse_cebraspe_q4(p).items():
                for k, v in enumerate(vs, 1): oficial[(2016, q, k)] = v
    for ano in (2020, 2022, 2023):
        p = os.path.join(args.gab, f"gab_{ano}.txt")
        if os.path.exists(p):
            for q, vs in parse_iades(p).items():
                for k, v in enumerate(vs, 1): oficial[(ano, q, k)] = v
print("gabaritos oficiais carregados:", collections.Counter(k[0] for k in oficial))

# ---------- 3. itens extra (ex.: 2016 extraído dos PDFs) ----------
for p in args.extra:
    ex = [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
    itens += ex; print(f"itens extra de {os.path.basename(p)}: {len(ex)}")

# ---------- 4. aplicar gabarito oficial / anulados ----------
diverg = []; anul = collections.Counter(); verif = collections.Counter()
for it in itens:
    key = (it["ano"], it["questao"], it["item"])
    if key in oficial:
        v = oficial[key]; it["gabarito_verificado"] = True; verif[it["ano"]] += 1
        if v == "X":
            it["anulado"] = True; anul[it["ano"]] += 1
        else:
            it["anulado"] = False
            if it["gabarito"] is None: it["gabarito"] = v
            elif it["gabarito"] != v:
                diverg.append((it["id"], it["gabarito"], v)); it["gabarito_vault"] = it["gabarito"]; it["gabarito"] = v
print("verificados por ano:", dict(verif)); print("anulados por ano:", dict(anul)); print("divergências vault≠oficial (corrigidas p/ oficial):", len(diverg), diverg[:15])

# ---------- 5. correção de rótulo 2026 (itens 216/217 são Direito) ----------
for it in itens:
    if it["ano"] == 2026 and it["questao"] in (216, 217) and it["disciplina"] == "Economia":
        it["disciplina_original"] = "Economia"; it["disciplina"] = "Direito"

# ---------- 6. classificação por tópico (lexico.py do vault) ----------
sys.path.insert(0, os.path.join(PA, "_dados"))
from lexico import LEX
STOP = set("de da do das dos e a o as os um uma no na nos nas em por para com que se ao aos à às pelo pela dos sua seu suas seus como entre sobre".split())
def toks(s): return [w for w in norm(s).split() if len(w) > 2 and w not in STOP]
bag = {k: set(toks(v[1])) for k, v in LEX.items()}
df = collections.Counter(w for s in bag.values() for w in s); N = len(bag)
idf = {w: math.log(N/df[w]) + 1.0 for w in df}
por_disc = collections.defaultdict(list)
for k in bag: por_disc[k.split("-")[0]].append(k)
conf_c = collections.Counter()
for it in itens:
    cands = por_disc.get(ABREV.get(it["disciplina"], ""), [])
    if not cands: it["topico_edital"] = None; it["topico_incerto"] = True; conf_c["n/a"] += 1; continue
    tset = set(toks(it["enunciado"] + " " + it["contexto"]))
    sc = sorted(((sum(idf[w] for w in bag[k] & tset), k) for k in cands), reverse=True)
    s1, top = sc[0]; s2 = sc[1][0] if len(sc) > 1 else 0
    if s1 >= 6 and s1 - s2 >= 2: it["topico_edital"] = top; it["topico_incerto"] = False; conf_c["alta"] += 1
    elif s1 > 0: it["topico_edital"] = top; it["topico_incerto"] = True; conf_c["incerto"] += 1
    else: it["topico_edital"] = None; it["topico_incerto"] = True; conf_c["nenhum"] += 1
print("classificação:", dict(conf_c))

# ---------- 7. 2026: nº do caderno 03 ----------
if args.mapa2026:
    mp = json.load(open(args.mapa2026)); m01 = {int(k): v for k, v in mp["mapa_c01_para_c03"].items()}
    for it in itens:
        if it["ano"] == 2026: it["item_caderno_03"] = m01[it["questao"]]

# ---------- 8. gravar itens.jsonl ----------
ids = [it["id"] for it in itens]; assert len(ids) == len(set(ids)), "ids duplicados"
dup = collections.Counter(norm(it["enunciado"])[:200] for it in itens); print("enunciados duplicados (200 chars):", sum(1 for v in dup.values() if v > 1))
itens.sort(key=lambda x: (x["ano"], x["turno"] != "manha", x["questao"], x["item"]))
os.makedirs(SIS, exist_ok=True)
with open(os.path.join(SIS, "itens.jsonl"), "w", encoding="utf-8") as f:
    for it in itens: f.write(json.dumps(it, ensure_ascii=False) + "\n")
print(f"gravado _sistema/itens.jsonl: {len(itens)} itens;", collections.Counter(it["ano"] for it in itens))

# ---------- 9. prova 2026: respostas e carga inicial de erros ----------
if args.mapa2026 and args.folha2026:
    folha = {int(k): v for k, v in json.load(open(args.folha2026)).items()}
    g03 = {int(k): v for k, v in mp["gab_c03"].items()}
    by_q = {it["questao"]: it for it in itens if it["ano"] == 2026}
    rows = []; erros = []
    for n01, n03 in sorted(m01.items()):
        it = by_q[n01]; o = g03[n03]; a = folha[n03]
        res = "anulado" if o == "X" else "branco" if a == "B" else "acerto" if a == o else "erro"
        rows.append([it["id"], n01, n03, ABREV[it["disciplina"]], a, o, res])
        if res in ("erro", "branco"):
            erros.append(dict(id_item=it["id"], data="2026-03-29", minha_resposta=("branco" if a == "B" else a), gabarito=o,
                              confianca=None, tipo_erro=None, armadilha=None, nota_vinculada=None,
                              contexto_registro="prova_2026", resultado=res))
    with open(os.path.join(SIS, "respostas_2026.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t"); w.writerow(["id_item", "item_caderno01_vault", "item_caderno03_meu", "disc", "minha", "gabarito", "resultado"]); w.writerows(rows)
    pe = os.path.join(SIS, "erros.jsonl")
    if not os.path.exists(pe) or os.path.getsize(pe) == 0:
        with open(pe, "w", encoding="utf-8") as f:
            for e in erros: f.write(json.dumps(e, ensure_ascii=False) + "\n")
        print(f"gravado erros.jsonl (carga inicial): {len(erros)} registros", collections.Counter(e["resultado"] for e in erros))
    else:
        print("erros.jsonl já existe — carga inicial NÃO regravada")
    print("respostas_2026.tsv:", collections.Counter(r[6] for r in rows))
