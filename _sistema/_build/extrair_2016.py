#!/usr/bin/env python3
"""Extrai os itens da prova CESPE 2016 (2 cadernos) a partir do texto `pdftotext -layout` (duas colunas).
Saída: itens_2016.jsonl no formato de construir_banco.py (gabarito preenchido depois pelo oficial).
Uso: extrair_2016.py DIR_COM_p2016_{1,2}_lay.txt SAIDA.jsonl"""
import re, sys, json, collections
S = sys.argv[1]; OUT = sys.argv[2]
HEAD = {"LÍNGUA PORTUGUESA": "Língua Portuguesa", "POLÍTICA INTERNACIONAL": "Política Internacional", "GEOGRAFIA": "Geografia",
        "LÍNGUA INGLESA": "Língua Inglesa", "HISTÓRIA DO BRASIL": "História do Brasil", "HISTÓRIA MUNDIAL": "História Mundial",
        "NOÇÕES DE DIREITO": "Direito", "NOÇÕES DE ECONOMIA": "Economia"}
PUNCT = (".", "!", "?", ")", "”", '"', "…")
def stream(path):
    """Lineariza cada página: coluna esquerda, depois direita. Limite de coluna estimado por página."""
    out = []
    for page in open(path, encoding="utf-8").read().split("\f"):
        L = page.splitlines(); starts = collections.Counter()
        for l in L:
            for m in re.finditer(r"\S {4,}(?=\S)", l):
                if m.end() >= 55 and len(l[:m.start()].strip()) >= 25: starts[m.end()] += 1   # só linhas com texto real à esquerda
        tot = sum(starts.values()); cands = [pos for pos, c in starts.items() if c >= max(2, 0.12 * tot)]
        col = min(cands) if cands else 10**6       # menor posição frequente = início da coluna; sem candidatos = página de coluna única
        left, right = [], []
        for l in L:
            s = l.strip(); hit = [h for h in HEAD if h in s]
            if hit:                                  # cabeçalho de disciplina: marcador na coluna em que aparece; resto da linha segue normal
                pos = l.find(hit[0]); side = left if pos < col - 10 else right
                side.append("##HEAD:" + hit[0]); (right if side is left else left).append("")
                l = l[:pos] + " " * len(hit[0]) + l[pos + len(hit[0]):]
                if not l.strip(): continue
            cut = col
            if len(l) > col and l[col-1] != " ":          # corte cairia no meio de uma palavra: recua ao último gap
                g = [m.end() for m in re.finditer(r" {2,}", l[:col])]; cut = g[-1] if g else col
            left.append(l[:cut].rstrip()); right.append(l[cut:].rstrip() if len(l) > cut else "")
        out += left + [""] + right + [""]
    return out
def clean(lines):
    return re.sub(r"\s+", " ", " ".join(re.sub(r"^\s*\d{1,3}\s{2,}", "", l).strip() for l in lines if l.strip())).strip()
itens = []
class St: pass
st = St()
def reset(): st.q = None; st.items = {}; st.comando = []; st.cur = None; st.expect = 1
def flush(buf_ctx):
    if st.q is None: return
    ctx = clean(buf_ctx); cmd = clean(st.comando)
    for k in (1, 2, 3, 4):
        txt = clean(st.items.get(k, []))
        itens.append(dict(id=f"2016-{'M' if st.turno=='manha' else 'T'}-Q{st.q:02d}-{k}", ano=2016, turno=st.turno, banca="CEBRASPE",
                          disciplina=st.disc, questao=st.q, item=k, contexto=(ctx + " " + cmd).strip()[:4000], enunciado=txt,
                          gabarito=None, anulado=None, gabarito_verificado=False, topico_edital=None, topico_incerto=True,
                          origem="autentico", extracao_incerta=(not txt or not txt.endswith(PUNCT))))
    reset()
for n, turno in ((1, "manha"), (2, "tarde")):
    st.turno = turno; st.disc = None; reset(); buf_ctx = []
    for l in stream(f"{S}/p2016_{n}_lay.txt"):
        s = l.strip()
        done4 = st.cur == 4 and st.items.get(4) and clean(st.items[4]).endswith(PUNCT)
        if not s:
            if done4: flush(buf_ctx); buf_ctx = []
            continue
        if s.startswith("||263_") or s.startswith("CESPE | CEBRASPE") or re.match(r"^– \d+ –$", s) or s == "DIREITO INTERNACIONAL": continue
        if s.startswith("##HEAD:"): st.disc = HEAD[s[7:]]; continue
        mq = re.match(r"^QUESTÃO\s+(\d+)$", s)
        if mq: flush(buf_ctx); buf_ctx = []; st.q = int(mq.group(1)); continue
        if st.q is None: buf_ctx.append(l); continue
        mi = re.match(r"^\s*([1-4])\s{2,}(\S.*)$", l) or re.match(r"^\s*([1-4])()\s*$", l)
        if mi and int(mi.group(1)) == st.expect:
            st.cur = st.expect; st.expect += 1; st.items[st.cur] = [mi.group(2)]; continue
        if done4 and (re.match(r"^\s*\d{1,3}\s{2,}\S", l) or re.match(r"^\s*Texto [IVX]+", s)):
            flush(buf_ctx); buf_ctx = [l]; continue
        if st.cur is None: st.comando.append(l)
        else: st.items[st.cur].append(l)
    flush(buf_ctx)
with open(OUT, "w", encoding="utf-8") as f:
    for it in itens: f.write(json.dumps(it, ensure_ascii=False) + "\n")
print("itens:", len(itens), "| questões:", len({(i['turno'], i['questao']) for i in itens}))
print("questões por disciplina:", dict(collections.Counter(i["disciplina"] for i in itens if i["item"] == 1)))
print("vazios:", [i["id"] for i in itens if not i["enunciado"]])
print("incertos:", sum(1 for i in itens if i["extracao_incerta"]), [i["id"] + " | …" + i["enunciado"][-45:] for i in itens if i["extracao_incerta"]][:14])
print(">600 chars:", [i["id"] for i in itens if len(i["enunciado"]) > 600])
