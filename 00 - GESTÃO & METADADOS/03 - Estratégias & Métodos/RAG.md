      File "<string>", line 1, in <module>
    … +18 lines (ctrl + t to view transcript)
        import narwhals.stable.v2 as nw
    ModuleNotFoundError: No module named 'narwhals'

───────────────────────────────────────────────────────────────

• As bibliotecas de RAG não estão instaladas, e sklearn está
  quebrado por dependência ausente. Vou montar uma versão local
  sem dependências Python externas: usar pdftotext/pdfinfo do
  sistema para extrair PDFs e um índice BM25 simples em Python
  puro, com caminho preparado para trocar por embeddings
  depois.

• Ran command -v pdftotext
  └ /usr/bin/pdftotext

• Ran command -v pdfinfo
  └ /usr/bin/pdfinfo

• Explored
  └ Search *.pdf in CACD_Outros
    Search *.pdf in CACD_Outros

───────────────────────────────────────────────────────────────

• Vou criar o projeto em Documents/CACD_RAG com uma CLI única
  (cacd_rag.py). Ela vai fazer inventário, extração, chunks,
  busca BM25 com metadados, e comandos de estudo que devolvem
  um pacote de contexto pronto para usar com um LLM.

• Ran mkdir -p /home/hyprtest/Documents/CACD_RAG
  └ (no output)

───────────────────────────────────────────────────────────────

• Agora vou adicionar os arquivos do RAG. A implementação
  ficará sem dependências externas obrigatórias para funcionar
  imediatamente no ambiente atual.

• Edited 3 files (+814 -0)
  └ Documents/CACD_RAG/.gitignore (+8 -0)
    1 +raw_index/
    2 +text/
    3 +chunks/
    4 +vector_store/
    5 +metadata/
    6 +outputs/
    7 +*.pyc
    8 +__pycache__/

  └ Documents/CACD_RAG/README.md (+73 -0)
     1 +# CACD RAG Local
     2 +
     3 +RAG local para estudar com o acervo em `Documents/CACD_
        Outros`.
     4 +
     5 +Esta primeira versao roda sem dependencias Python exter
        nas. Ela usa:
     6 +
     7 +- `pdftotext` para extrair texto dos PDFs.
     8 +- `pdfinfo` para validar paginas.
     9 +- BM25 em Python puro para busca lexical com metadados.
    10 +
    11 +## Estrutura
    12 +
    13 +- `raw_index/`: inventario dos arquivos originais.
    14 +- `text/`: texto extraido por documento.
    15 +- `chunks/`: trechos prontos para recuperacao.
    16 +- `vector_store/`: indice BM25 local.
    17 +- `metadata/`: catalogos em JSONL/CSV.
    18 +- `outputs/`: pacotes de contexto para usar com LLM.
    19 +
    20 +## Comandos principais
    21 +
    22 +Construir o indice:
    23 +
    24 +```bash
    25 +python3 /home/hyprtest/Documents/CACD_RAG/cacd_rag.py b
        uild
    26 +```
    27 +
    28 +Buscar contexto:
    29 +
    30 +```bash
    31 +python3 /home/hyprtest/Documents/CACD_RAG/cacd_rag.py s
        earch "politica externa independente" --materia Histori
        a_do_Brasil
    32 +```
    33 +
    34 +Gerar pacote de contexto para uma pergunta:
    35 +
    36 +```bash
    37 +python3 /home/hyprtest/Documents/CACD_RAG/cacd_rag.py a
        sk "Como o CACD cobra balanco de pagamentos?" --materia
         Economia
    38 +```
    39 +
    40 +Estudo ativo por materia:
    41 +
    42 +```bash
    43 +python3 /home/hyprtest/Documents/CACD_RAG/cacd_rag.py e
        studar_materia Geografia
    44 +```
    45 +
    46 +Analisar provas:
    47 +
    48 +```bash
    49 +python3 /home/hyprtest/Documents/CACD_RAG/cacd_rag.py p
        rovas --ano 2025 --banca CEBRASPE --fase segunda_fase -
        -disciplina-prova Economia
    50 +```
    51 +
    52 +Correção discursiva assistida:
    53 +
    54 +```bash
    55 +python3 /home/hyprtest/Documents/CACD_RAG/cacd_rag.py d
        iscursiva /caminho/para/sua_resposta.txt --disciplina-p
        rova Economia --fase segunda_fase
    56 +```
    57 +
    58 +## Como usar com um LLM
    59 +
    60 +Os comandos `ask`, `estudar_materia`, `provas` e `discu
        rsiva` gravam um arquivo em `outputs/`.
    61 +Esse arquivo contem:
    62 +
    63 +- pergunta ou tarefa;
    64 +- instrucao para o LLM;
    65 +- contexto recuperado;
    66 +- fonte e pagina de cada trecho.
    67 +
    68 +Cole esse pacote em um LLM ou use-o como entrada de uma
         futura integracao local/API.
    69 +
    70 +## Proximo upgrade recomendado
    71 +
    72 +Depois de validar a busca lexical, adicionar embeddings
         locais com `sentence-transformers`
    73 +e um vector store como FAISS ou Chroma. A estrutura de
        metadados ja foi pensada para isso.

  └ Documents/CACD_RAG/cacd_rag.py (+733 -0)
      1 +#!/usr/bin/env python3
      2 +"""RAG local para estudos do CACD.
      3 +
      4 +Implementa inventario, extracao de texto, chunking, bu
         sca BM25 simples e
      5 +comandos de estudo sem depender de bibliotecas Python
         externas.
      6 +"""
      7 +
      8 +from __future__ import annotations
      9 +
     10 +import argparse
     11 +import csv
     12 +import hashlib
     13 +import json
     14 +import math
     15 +import os
     16 +import re
     17 +import subprocess
     18 +import sys
     19 +from collections import Counter, defaultdict
     20 +from dataclasses import dataclass
     21 +from pathlib import Path
     22 +from typing import Iterable
     23 +
     24 +
     25 +DEFAULT_SOURCE_DIR = Path("/home/hyprtest/Documents/CA
         CD_Outros")
     26 +DEFAULT_RAG_DIR = Path("/home/hyprtest/Documents/CACD_
         RAG")
     27 +
     28 +TOKEN_RE = re.compile(r"[a-zA-ZÀ-ÿ0-9_]{2,}", re.UNICO
         DE)
     29 +SUBJECTS = {
     30 +    "01_Portugues": "Portugues",
     31 +    "02_Ingles": "Ingles",
     32 +    "03_Historia_do_Brasil": "Historia_do_Brasil",
     33 +    "04_Historia_Mundial": "Historia_Mundial",
     34 +    "05_Geografia": "Geografia",
     35 +    "06_Politica_Internacional": "Politica_Internacion
         al",
     36 +    "07_Economia": "Economia",
     37 +    "08_Direito_Internacional_Publico": "Direito_Inter
         nacional_Publico",
     38 +    "09_Direito_Constitucional": "Direito_Constitucion
         al",
     39 +    "10_Direito_Administrativo": "Direito_Administrati
         vo",
     40 +    "11_Espanhol": "Espanhol",
     41 +    "12_Frances": "Frances",
     42 +}
     43 +
     44 +
     45 +@dataclass(frozen=True)
     46 +class Paths:
     47 +    source: Path
     48 +    rag: Path
     49 +
     50 +    @property
     51 +    def raw_index(self) -> Path:
     52 +        return self.rag / "raw_index"
     53 +
     54 +    @property
     55 +    def text(self) -> Path:
     56 +        return self.rag / "text"
     57 +
     58 +    @property
     59 +    def chunks(self) -> Path:
     60 +        return self.rag / "chunks"
     61 +
     62 +    @property
     63 +    def vector_store(self) -> Path:
     64 +        return self.rag / "vector_store"
     65 +
     66 +    @property
     67 +    def metadata(self) -> Path:
     68 +        return self.rag / "metadata"
     69 +
     70 +    @property
     71 +    def outputs(self) -> Path:
     72 +        return self.rag / "outputs"
     73 +
     74 +
     75 +def ensure_dirs(paths: Paths) -> None:
     76 +    for directory in (
     77 +        paths.raw_index,
     78 +        paths.text,
     79 +        paths.chunks,
     80 +        paths.vector_store,
     81 +        paths.metadata,
     82 +        paths.outputs,
     83 +    ):
     84 +        directory.mkdir(parents=True, exist_ok=True)
     85 +
     86 +
     87 +def rel(path: Path, base: Path) -> str:
     88 +    return str(path.relative_to(base))
     89 +
     90 +
     91 +def stable_id(text: str) -> str:
     92 +    return hashlib.sha1(text.encode("utf-8", errors="i
         gnore")).hexdigest()[:16]
     93 +
     94 +
     95 +def sha256_file(path: Path) -> str:
     96 +    digest = hashlib.sha256()
     97 +    with path.open("rb") as handle:
     98 +        for block in iter(lambda: handle.read(1024 * 1
         024), b""):
     99 +            digest.update(block)
    100 +    return digest.hexdigest()
    101 +
    102 +
    103 +def tokenize(text: str) -> list[str]:
    104 +    return [t.lower() for t in TOKEN_RE.findall(text)]
    105 +
    106 +
    107 +def normalize_space(text: str) -> str:
    108 +    text = text.replace("\x00", " ")
    109 +    text = re.sub(r"[ \t]+", " ", text)
    110 +    text = re.sub(r"\n{3,}", "\n\n", text)
    111 +    return text.strip()
    112 +
    113 +
    114 +def infer_metadata(path: Path, source_root: Path) -> d
         ict[str, str | int | None]:
    115 +    relative = Path(rel(path, source_root))
    116 +    parts = relative.parts
    117 +    filename = path.name
    118 +    lower = str(relative).lower()
    119 +
    120 +    materia = ""
    121 +    for directory, subject in SUBJECTS.items():
    122 +        if parts and parts[0] == directory:
    123 +            materia = subject
    124 +            break
    125 +
    126 +    tipo_documento = "documento"
    127 +    if "provas_cacd" in lower:
    128 +        tipo_documento = "prova"
    129 +    if "gabarito" in lower:
    130 +        tipo_documento = "gabarito"
    131 +    if "padrao" in lower or "padr" in lower and "respo
         sta" in lower:
    132 +        tipo_documento = "padrao_resposta"
    133 +    if "edital" in lower or "editais_cacd" in lower:
    134 +        tipo_documento = "edital"
    135 +    if "guia" in lower or any(word in lower for word i
         n ["capivara", "jacare", "sarue", "carcara"]):
    136 +        tipo_documento = "guia"
    137 +    if filename.lower().endswith(".md"):
    138 +        tipo_documento = "nota"
    139 +
    140 +    fase = ""
    141 +    if "primeira_fase" in lower or "1fase" in lower:
    142 +        fase = "primeira_fase"
    143 +    elif "demais_fases" in lower:
    144 +        if "2fase" in lower:
    145 +            fase = "segunda_fase"
    146 +        elif "3fase" in lower:
    147 +            fase = "terceira_fase"
    148 +        else:
    149 +            fase = "demais_fases"
    150 +
    151 +    banca = ""
    152 +    for candidate in ("IADES", "CEBRASPE"):
    153 +        if candidate.lower() in lower:
    154 +            banca = candidate
    155 +            break
    156 +
    157 +    year_match = re.search(r"(20[0-9]{2})", lower)
    158 +    ano = int(year_match.group(1)) if year_match else
         None
    159 +
    160 +    disciplina = ""
    161 +    discipline_aliases = {
    162 +        "lingua_portuguesa": "Portugues",
    163 +        "portuguesa": "Portugues",
    164 +        "portugues": "Portugues",
    165 +        "lingua_inglesa": "Ingles",
    166 +        "inglesa": "Ingles",
    167 +        "ingles": "Ingles",
    168 +        "historia_do_brasil": "Historia_do_Brasil",
    169 +        "geografia": "Geografia",
    170 +        "politica_internacional": "Politica_Internacio
         nal",
    171 +        "economia": "Economia",
    172 +        "direito": "Direito",
    173 +        "espanhol_frances": "Espanhol_Frances",
    174 +        "espanhol": "Espanhol",
    175 +        "frances": "Frances",
    176 +    }
    177 +    for marker, value in discipline_aliases.items():
    178 +        if marker in lower:
    179 +            disciplina = value
    180 +            break
    181 +
    182 +    prioridade = "media"
    183 +    if tipo_documento in {"edital", "prova", "gabarito
         ", "padrao_resposta"}:
    184 +        prioridade = "alta"
    185 +    elif tipo_documento == "nota":
    186 +        prioridade = "baixa"
    187 +
    188 +    return {
    189 +        "path": str(path),
    190 +        "relative_path": str(relative),
    191 +        "filename": filename,
    192 +        "materia": materia,
    193 +        "tipo_documento": tipo_documento,
    194 +        "fase": fase,
    195 +        "ano": ano,
    196 +        "banca": banca,
    197 +        "disciplina_prova": disciplina,
    198 +        "prioridade": prioridade,
    199 +    }
    200 +
    201 +
    202 +def iter_source_files(source_root: Path) -> Iterable[P
         ath]:
    203 +    extensions = {".pdf", ".md", ".txt"}
    204 +    for path in sorted(source_root.rglob("*")):
    205 +        if path.is_file() and path.suffix.lower() in e
         xtensions:
    206 +            yield path
    207 +
    208 +
    209 +def run_pdfinfo(path: Path) -> int | None:
    210 +    try:
    211 +        result = subprocess.run(
    212 +            ["pdfinfo", str(path)],
    213 +            check=False,
    214 +            stdout=subprocess.PIPE,
    215 +            stderr=subprocess.PIPE,
    216 +            text=True,
    217 +        )
    218 +    except FileNotFoundError:
    219 +        return None
    220 +    if result.returncode != 0:
    221 +        return None
    222 +    match = re.search(r"^Pages:\s+(\d+)", result.stdou
         t, re.MULTILINE)
    223 +    return int(match.group(1)) if match else None
    224 +
    225 +
    226 +def extract_pdf(path: Path) -> list[dict[str, str | in
         t]]:
    227 +    pages = run_pdfinfo(path) or 0
    228 +    extracted: list[dict[str, str | int]] = []
    229 +    if pages == 0:
    230 +        return extracted
    231 +
    232 +    for page in range(1, pages + 1):
    233 +        try:
    234 +            result = subprocess.run(
    235 +                ["pdftotext", "-f", str(page), "-l", s
         tr(page), "-layout", str(path), "-"],
    236 +                check=False,
    237 +                stdout=subprocess.PIPE,
    238 +                stderr=subprocess.PIPE,
    239 +            )
    240 +        except FileNotFoundError as exc:
    241 +            raise RuntimeError("pdftotext nao encontra
         do no sistema") from exc
    242 +        text = result.stdout.decode("utf-8", errors="r
         eplace")
    243 +        text = normalize_space(text)
    244 +        if text:
    245 +            extracted.append({"page": page, "text": te
         xt})
    246 +    return extracted
    247 +
    248 +
    249 +def extract_text_file(path: Path) -> list[dict[str, st
         r | int]]:
    250 +    text = path.read_text(encoding="utf-8", errors="re
         place")
    251 +    return [{"page": 1, "text": normalize_space(text)}
         ] if text.strip() else []
    252 +
    253 +
    254 +def chunk_page(
    255 +    page_text: str,
    256 +    *,
    257 +    chunk_tokens: int,
    258 +    overlap_tokens: int,
    259 +) -> list[str]:
    260 +    tokens = page_text.split()
    261 +    if not tokens:
    262 +        return []
    263 +    if len(tokens) <= chunk_tokens:
    264 +        return [" ".join(tokens)]
    265 +
    266 +    chunks: list[str] = []
    267 +    step = max(1, chunk_tokens - overlap_tokens)
    268 +    for start in range(0, len(tokens), step):
    269 +        end = min(len(tokens), start + chunk_tokens)
    270 +        chunk = " ".join(tokens[start:end]).strip()
    271 +        if chunk:
    272 +            chunks.append(chunk)
    273 +        if end >= len(tokens):
    274 +            break
    275 +    return chunks
    276 +
    277 +
    278 +def write_jsonl(path: Path, rows: Iterable[dict]) -> N
         one:
    279 +    with path.open("w", encoding="utf-8") as handle:
    280 +        for row in rows:
    281 +            handle.write(json.dumps(row, ensure_ascii=
         False, sort_keys=True) + "\n")
    282 +
    283 +
    284 +def read_jsonl(path: Path) -> list[dict]:
    285 +    if not path.exists():
    286 +        return []
    287 +    with path.open("r", encoding="utf-8") as handle:
    288 +        return [json.loads(line) for line in handle if
          line.strip()]
    289 +
    290 +
    291 +def command_inventory(args: argparse.Namespace) -> Non
         e:
    292 +    paths = Paths(args.source, args.rag)
    293 +    ensure_dirs(paths)
    294 +    rows = []
    295 +    for path in iter_source_files(paths.source):
    296 +        meta = infer_metadata(path, paths.source)
    297 +        stat = path.stat()
    298 +        meta.update(
    299 +            {
    300 +                "extension": path.suffix.lower(),
    301 +                "size_bytes": stat.st_size,
    302 +                "sha256": sha256_file(path),
    303 +                "pages": run_pdfinfo(path) if path.suf
         fix.lower() == ".pdf" else 1,
    304 +            }
    305 +        )
    306 +        rows.append(meta)
    307 +
    308 +    write_jsonl(paths.raw_index / "files.jsonl", rows)
    309 +    with (paths.metadata / "files.csv").open("w", enco
         ding="utf-8", newline="") as handle:
    310 +        if rows:
    311 +            writer = csv.DictWriter(handle, fieldnames
         =list(rows[0].keys()))
    312 +            writer.writeheader()
    313 +            writer.writerows(rows)
    314 +    print(f"Inventario criado: {len(rows)} arquivos")
    315 +
    316 +
    317 +def command_extract(args: argparse.Namespace) -> None:
    318 +    paths = Paths(args.source, args.rag)
    319 +    ensure_dirs(paths)
    320 +    files = read_jsonl(paths.raw_index / "files.jsonl"
         )
    321 +    if not files:
    322 +        command_inventory(args)
    323 +        files = read_jsonl(paths.raw_index / "files.js
         onl")
    324 +
    325 +    extracted_rows = []
    326 +    for item in files:
    327 +        src = Path(item["path"])
    328 +        doc_id = stable_id(item["relative_path"])
    329 +        out_path = paths.text / f"{doc_id}.jsonl"
    330 +        if out_path.exists() and not args.force:
    331 +            extracted_rows.append({"doc_id": doc_id, *
         *item, "text_file": str(out_path)})
    332 +            continue
    333 +
    334 +        if src.suffix.lower() == ".pdf":
    335 +            pages = extract_pdf(src)
    336 +        else:
    337 +            pages = extract_text_file(src)
    338 +
    339 +        page_rows = []
    340 +        for page in pages:
    341 +            page_rows.append(
    342 +                {
    343 +                    "doc_id": doc_id,
    344 +                    "page": page["page"],
    345 +                    "text": page["text"],
    346 +                    "relative_path": item["relative_pa
         th"],
    347 +                }
    348 +            )
    349 +        write_jsonl(out_path, page_rows)
    350 +        extracted_rows.append({"doc_id": doc_id, **ite
         m, "text_file": str(out_path)})
    351 +
    352 +    write_jsonl(paths.metadata / "documents.jsonl", ex
         tracted_rows)
    353 +    print(f"Extracao concluida: {len(extracted_rows)}
         documentos")
    354 +
    355 +
    356 +def command_chunk(args: argparse.Namespace) -> None:
    357 +    paths = Paths(args.source, args.rag)
    358 +    ensure_dirs(paths)
    359 +    docs = read_jsonl(paths.metadata / "documents.json
         l")
    360 +    if not docs:
    361 +        command_extract(args)
    362 +        docs = read_jsonl(paths.metadata / "documents.
         jsonl")
    363 +
    364 +    rows = []
    365 +    for doc in docs:
    366 +        pages = read_jsonl(Path(doc["text_file"]))
    367 +        for page in pages:
    368 +            for index, text in enumerate(
    369 +                chunk_page(
    370 +                    page["text"],
    371 +                    chunk_tokens=args.chunk_tokens,
    372 +                    overlap_tokens=args.overlap_tokens
         ,
    373 +                )
    374 +            ):
    375 +                chunk_id = stable_id(f"{doc['doc_id']}
         :{page['page']}:{index}:{text[:80]}")
    376 +                rows.append(
    377 +                    {
    378 +                        "chunk_id": chunk_id,
    379 +                        "doc_id": doc["doc_id"],
    380 +                        "page_start": page["page"],
    381 +                        "page_end": page["page"],
    382 +                        "text": text,
    383 +                        "token_count": len(text.split(
         )),
    384 +                        "relative_path": doc["relative
         _path"],
    385 +                        "filename": doc["filename"],
    386 +                        "materia": doc["materia"],
    387 +                        "tipo_documento": doc["tipo_do
         cumento"],
    388 +                        "fase": doc["fase"],
    389 +                        "ano": doc["ano"],
    390 +                        "banca": doc["banca"],
    391 +                        "disciplina_prova": doc["disci
         plina_prova"],
    392 +                        "prioridade": doc["prioridade"
         ],
    393 +                    }
    394 +                )
    395 +
    396 +    write_jsonl(paths.chunks / "chunks.jsonl", rows)
    397 +    print(f"Chunks criados: {len(rows)}")
    398 +
    399 +
    400 +def build_bm25(chunks: list[dict]) -> dict:
    401 +    doc_freq: Counter[str] = Counter()
    402 +    tokenized = []
    403 +    total_len = 0
    404 +    for chunk in chunks:
    405 +        tokens = tokenize(chunk["text"])
    406 +        counts = Counter(tokens)
    407 +        tokenized.append({"chunk_id": chunk["chunk_id"
         ], "counts": counts, "length": len(tokens)})
    408 +        total_len += len(tokens)
    409 +        for token in counts:
    410 +            doc_freq[token] += 1
    411 +
    412 +    return {
    413 +        "n": len(chunks),
    414 +        "avgdl": total_len / max(1, len(chunks)),
    415 +        "doc_freq": dict(doc_freq),
    416 +        "documents": [
    417 +            {
    418 +                "chunk_id": row["chunk_id"],
    419 +                "length": row["length"],
    420 +                "counts": dict(row["counts"]),
    421 +            }
    422 +            for row in tokenized
    423 +        ],
    424 +    }
    425 +
    426 +
    427 +def command_index(args: argparse.Namespace) -> None:
    428 +    paths = Paths(args.source, args.rag)
    429 +    ensure_dirs(paths)
    430 +    chunks = read_jsonl(paths.chunks / "chunks.jsonl")
    431 +    if not chunks:
    432 +        command_chunk(args)
    433 +        chunks = read_jsonl(paths.chunks / "chunks.jso
         nl")
    434 +
    435 +    index = build_bm25(chunks)
    436 +    (paths.vector_store / "bm25_index.json").write_tex
         t(
    437 +        json.dumps(index, ensure_ascii=False),
    438 +        encoding="utf-8",
    439 +    )
    440 +    print(f"Indice BM25 criado: {index['n']} chunks")
    441 +
    442 +
    443 +def passes_filters(chunk: dict, args: argparse.Namespa
         ce) -> bool:
    444 +    for attr in ("materia", "tipo_documento", "fase",
         "banca", "disciplina_prova"):
    445 +        value = getattr(args, attr, None)
    446 +        if value and str(chunk.get(attr, "")).lower()
         != str(value).lower():
    447 +            return False
    448 +    if getattr(args, "ano", None) and str(chunk.get("a
         no", "")) != str(args.ano):
    449 +        return False
    450 +    return True
    451 +
    452 +
    453 +def load_search_data(paths: Paths) -> tuple[list[dict]
         , dict]:
    454 +    chunks = read_jsonl(paths.chunks / "chunks.jsonl")
    455 +    index_path = paths.vector_store / "bm25_index.json
         "
    456 +    if not chunks or not index_path.exists():
    457 +        raise SystemExit("Indice ausente. Rode: python
         3 cacd_rag.py build")
    458 +    index = json.loads(index_path.read_text(encoding="
         utf-8"))
    459 +    return chunks, index
    460 +
    461 +
    462 +def search_chunks(paths: Paths, query: str, args: argp
         arse.Namespace, limit: int) -> list[dict]:
    463 +    chunks, index = load_search_data(paths)
    464 +    by_id = {chunk["chunk_id"]: chunk for chunk in chu
         nks}
    465 +    candidates = {chunk["chunk_id"] for chunk in chunk
         s if passes_filters(chunk, args)}
    466 +    query_terms = tokenize(query)
    467 +    if not query_terms:
    468 +        return []
    469 +
    470 +    n = index["n"]
    471 +    avgdl = index["avgdl"] or 1
    472 +    doc_freq = index["doc_freq"]
    473 +    k1 = 1.5
    474 +    b = 0.75
    475 +    scores: defaultdict[str, float] = defaultdict(floa
         t)
    476 +
    477 +    for doc in index["documents"]:
    478 +        chunk_id = doc["chunk_id"]
    479 +        if chunk_id not in candidates:
    480 +            continue
    481 +        length = doc["length"] or 1
    482 +        counts = doc["counts"]
    483 +        for term in query_terms:
    484 +            freq = counts.get(term, 0)
    485 +            if not freq:
    486 +                continue
    487 +            df = doc_freq.get(term, 0)
    488 +            idf = math.log(1 + (n - df + 0.5) / (df +
         0.5))
    489 +            denom = freq + k1 * (1 - b + b * length /
         avgdl)
    490 +            scores[chunk_id] += idf * freq * (k1 + 1)
         / denom
    491 +
    492 +    ranked = sorted(scores.items(), key=lambda item: i
         tem[1], reverse=True)[:limit]
    493 +    results = []
    494 +    for chunk_id, score in ranked:
    495 +        chunk = dict(by_id[chunk_id])
    496 +        chunk["score"] = round(score, 4)
    497 +        results.append(chunk)
    498 +    return results
    499 +
    500 +
    501 +def format_context(results: list[dict], max_chars: int
          = 1200) -> str:
    502 +    blocks = []
    503 +    for idx, item in enumerate(results, 1):
    504 +        text = item["text"]
    505 +        if len(text) > max_chars:
    506 +            text = text[:max_chars].rstrip() + "..."
    507 +        source = f"{item['relative_path']} p.{item['pa
         ge_start']}"
    508 +        meta = ", ".join(
    509 +            str(v)
    510 +            for v in [
    511 +                item.get("materia"),
    512 +                item.get("tipo_documento"),
    513 +                item.get("fase"),
    514 +                item.get("ano"),
    515 +                item.get("banca"),
    516 +                item.get("disciplina_prova"),
    517 +            ]
    518 +            if v
    519 +        )
    520 +        blocks.append(f"[{idx}] {source} | score={item
         ['score']} | {meta}\n{text}")
    521 +    return "\n\n---\n\n".join(blocks)
    522 +
    523 +
    524 +def save_output(paths: Paths, prefix: str, content: st
         r) -> Path:
    525 +    paths.outputs.mkdir(parents=True, exist_ok=True)
    526 +    name = f"{prefix}_{stable_id(content)}.md"
    527 +    out = paths.outputs / name
    528 +    out.write_text(content, encoding="utf-8")
    529 +    return out
    530 +
    531 +
    532 +def command_search(args: argparse.Namespace) -> None:
    533 +    paths = Paths(args.source, args.rag)
    534 +    results = search_chunks(paths, args.query, args, a
         rgs.limit)
    535 +    print(format_context(results, max_chars=args.max_c
         hars))
    536 +
    537 +
    538 +def command_ask(args: argparse.Namespace) -> None:
    539 +    paths = Paths(args.source, args.rag)
    540 +    results = search_chunks(paths, args.query, args, a
         rgs.limit)
    541 +    context = format_context(results, max_chars=args.m
         ax_chars)
    542 +    content = f"""# Pacote de contexto para pergunta
    543 +
    544 +## Pergunta
    545 +{args.query}
    546 +
    547 +## Instrucao para o LLM
    548 +Responda apenas com base no contexto abaixo. Separe fa
         tos documentados de inferencias. Cite arquivo e pagina
          em cada ponto relevante. Se o contexto for insuficien
         te, diga exatamente o que faltou.
    549 +
    550 +## Contexto recuperado
    551 +{context}
    552 +"""
    553 +    out = save_output(paths, "pergunta", content)
    554 +    print(content)
    555 +    print(f"\nSalvo em: {out}")
    556 +
    557 +
    558 +def command_estudar_materia(args: argparse.Namespace)
         -> None:
    559 +    query = args.query or f"topicos recorrentes pontos
          centrais provas padroes {args.materia}"
    560 +    args.materia = args.materia
    561 +    paths = Paths(args.source, args.rag)
    562 +    results = search_chunks(paths, query, args, args.l
         imit)
    563 +    context = format_context(results, max_chars=args.m
         ax_chars)
    564 +    content = f"""# Estudo ativo - {args.materia}
    565 +
    566 +## Objetivo
    567 +Gerar roteiro de estudo ativo, perguntas, flashcards e
          revisao para {args.materia}.
    568 +
    569 +## Instrucao para o LLM
    570 +Use o contexto recuperado para produzir:
    571 +
    572 +1. Tópicos prioritários.
    573 +2. Perguntas ativas de revisão.
    574 +3. Flashcards no formato Pergunta | Resposta | Fonte.
    575 +4. Pontos que merecem revisão por prova/padrão.
    576 +5. Lacunas do contexto, se houver.
    577 +
    578 +Sempre cite arquivo e página.
    579 +
    580 +## Contexto recuperado
    581 +{context}
    582 +"""
    583 +    out = save_output(paths, "estudo", content)
    584 +    print(content)
    585 +    print(f"\nSalvo em: {out}")
    586 +
    587 +
    588 +def command_provas(args: argparse.Namespace) -> None:
    589 +    query_parts = ["prova questao gabarito padrao resp
         osta"]
    590 +    for value in (args.ano, args.banca, args.fase, arg
         s.disciplina_prova):
    591 +        if value:
    592 +            query_parts.append(str(value))
    593 +    args.tipo_documento = args.tipo_documento or ""
    594 +    paths = Paths(args.source, args.rag)
    595 +    results = search_chunks(paths, " ".join(query_part
         s), args, args.limit)
    596 +    context = format_context(results, max_chars=args.m
         ax_chars)
    597 +    content = f"""# Analise de provas CACD
    598 +
    599 +## Filtros
    600 +- ano: {args.ano or 'todos'}
    601 +- banca: {args.banca or 'todas'}
    602 +- fase: {args.fase or 'todas'}
    603 +- disciplina: {args.disciplina_prova or 'todas'}
    604 +
    605 +## Instrucao para o LLM
    606 +Com base no contexto, identifique padrões de cobrança,
          tópicos recorrentes, comandos de questão e relação en
         tre prova e padrão/gabarito. Cite arquivo e página.
    607 +
    608 +## Contexto recuperado
    609 +{context}
    610 +"""
    611 +    out = save_output(paths, "provas", content)
    612 +    print(content)
    613 +    print(f"\nSalvo em: {out}")
    614 +
    615 +
    616 +def command_discursiva(args: argparse.Namespace) -> No
         ne:
    617 +    answer_text = Path(args.answer_file).read_text(enc
         oding="utf-8", errors="replace")
    618 +    query = f"{args.query or ''} {answer_text[:3000]}"
    619 +    args.tipo_documento = "padrao_resposta"
    620 +    paths = Paths(args.source, args.rag)
    621 +    results = search_chunks(paths, query, args, args.l
         imit)
    622 +    context = format_context(results, max_chars=args.m
         ax_chars)
    623 +    content = f"""# Correcao discursiva assistida
    624 +
    625 +## Resposta do aluno
    626 +{answer_text}
    627 +
    628 +## Instrucao para o LLM
    629 +Compare a resposta do aluno com os padroes de resposta
          recuperados. Entregue:
    630 +
    631 +1. Diagnostico por criterio substantivo.
    632 +2. Pontos presentes na resposta.
    633 +3. Pontos ausentes ou fracos.
    634 +4. Sugestoes de melhoria.
    635 +5. Trechos de fonte usados, com arquivo e pagina.
    636 +
    637 +Nao invente criterio que nao esteja apoiado pelo conte
         xto.
    638 +
    639 +## Contexto recuperado
    640 +{context}
    641 +"""
    642 +    out = save_output(paths, "discursiva", content)
    643 +    print(content)
    644 +    print(f"\nSalvo em: {out}")
    645 +
    646 +
    647 +def command_build(args: argparse.Namespace) -> None:
    648 +    command_inventory(args)
    649 +    command_extract(args)
    650 +    command_chunk(args)
    651 +    command_index(args)
    652 +
    653 +
    654 +def add_common_filters(parser: argparse.ArgumentParser
         ) -> None:
    655 +    parser.add_argument("--materia", default="")
    656 +    parser.add_argument("--tipo-documento", default=""
         )
    657 +    parser.add_argument("--fase", default="")
    658 +    parser.add_argument("--ano", default="")
    659 +    parser.add_argument("--banca", default="")
    660 +    parser.add_argument("--disciplina-prova", default=
         "")
    661 +    parser.add_argument("--limit", type=int, default=8
         )
    662 +    parser.add_argument("--max-chars", type=int, defau
         lt=1200)
    663 +
    664 +
    665 +def build_parser() -> argparse.ArgumentParser:
    666 +    parser = argparse.ArgumentParser(description="RAG
         local para CACD")
    667 +    parser.add_argument("--source", type=Path, default
         =DEFAULT_SOURCE_DIR)
    668 +    parser.add_argument("--rag", type=Path, default=DE
         FAULT_RAG_DIR)
    669 +    sub = parser.add_subparsers(dest="command", requir
         ed=True)
    670 +
    671 +    inventory = sub.add_parser("inventory")
    672 +    inventory.set_defaults(func=command_inventory)
    673 +
    674 +    extract = sub.add_parser("extract")
    675 +    extract.add_argument("--force", action="store_true
         ")
    676 +    extract.set_defaults(func=command_extract)
    677 +
    678 +    chunk = sub.add_parser("chunk")
    679 +    chunk.add_argument("--chunk-tokens", type=int, def
         ault=700)
    680 +    chunk.add_argument("--overlap-tokens", type=int, d
         efault=100)
    681 +    chunk.add_argument("--force", action="store_true")
    682 +    chunk.set_defaults(func=command_chunk)
    683 +
    684 +    index = sub.add_parser("index")
    685 +    index.add_argument("--chunk-tokens", type=int, def
         ault=700)
    686 +    index.add_argument("--overlap-tokens", type=int, d
         efault=100)
    687 +    index.add_argument("--force", action="store_true")
    688 +    index.set_defaults(func=command_index)
    689 +
    690 +    build = sub.add_parser("build")
    691 +    build.add_argument("--chunk-tokens", type=int, def
         ault=700)
    692 +    build.add_argument("--overlap-tokens", type=int, d
         efault=100)
    693 +    build.add_argument("--force", action="store_true")
    694 +    build.set_defaults(func=command_build)
    695 +
    696 +    search = sub.add_parser("search")
    697 +    search.add_argument("query")
    698 +    add_common_filters(search)
    699 +    search.set_defaults(func=command_search)
    700 +
    701 +    ask = sub.add_parser("ask")
    702 +    ask.add_argument("query")
    703 +    add_common_filters(ask)
    704 +    ask.set_defaults(func=command_ask)
    705 +
    706 +    estudar = sub.add_parser("estudar_materia")
    707 +    estudar.add_argument("materia")
    708 +    estudar.add_argument("--query", default="")
    709 +    add_common_filters(estudar)
    710 +    estudar.set_defaults(func=command_estudar_materia)
    711 +
    712 +    provas = sub.add_parser("provas")
    713 +    add_common_filters(provas)
    714 +    provas.set_defaults(func=command_provas)
    715 +
    716 +    discursiva = sub.add_parser("discursiva")
    717 +    discursiva.add_argument("answer_file")
    718 +    discursiva.add_argument("--query", default="")
    719 +    add_common_filters(discursiva)
    720 +    discursiva.set_defaults(func=command_discursiva)
    721 +
    722 +    return parser
    723 +
    724 +
    725 +def main(argv: list[str] | None = None) -> int:
    726 +    parser = build_parser()
    727 +    args = parser.parse_args(argv)
    728 +    args.func(args)
    729 +    return 0
    730 +
    731 +
    732 +if __name__ == "__main__":
    733 +    raise SystemExit(main())

───────────────────────────────────────────────────────────────

• Vou fazer uma checagem rápida da CLI antes de indexar tudo.
  Já vi um ponto a ajustar: no comando estudar_materia, o
  filtro --materia não deve conflitar com a matéria posicional.

• Edited Documents/CACD_RAG/cacd_rag.py (+4 -3)
    653
    654 -def add_common_filters(parser: argparse.ArgumentParser
         ) -> None:
    655 -    parser.add_argument("--materia", default="")
    654 +def add_common_filters(parser: argparse.ArgumentParser
         , *, include_materia: bool = True) -> None:
    655 +    if include_materia:
    656 +        parser.add_argument("--materia", default="")
    657      parser.add_argument("--tipo-documento", default=""
         )
        ⋮
    709      estudar.add_argument("--query", default="")
    709 -    add_common_filters(estudar)
    710 +    add_common_filters(estudar, include_materia=False)
    711      estudar.set_defaults(func=command_estudar_materia)

───────────────────────────────────────────────────────────────

• Ajuste feito. Vou validar --help e iniciar a construção do
  índice; a extração dos PDFs pode levar um pouco.

• Ran python3 /home/hyprtest/Documents/CACD_RAG/cacd_rag.py
  │ --help
  └ usage: cacd_rag.py [-h] [--source SOURCE] [--rag RAG]

    … +10 lines (ctrl + t to view transcript)
      --source SOURCE
      --rag RAG

• Ran python3 /home/hyprtest/Documents/CACD_RAG/cacd_rag.py
  │ estudar_materia --help
  └ usage: cacd_rag.py estudar_materia [-h] [--query QUERY]
                                       [--tipo-documento
    … +20 lines (ctrl + t to view transcript)
      --limit LIMIT
      --max-chars MAX_CHARS

───────────────────────────────────────────────────────────────

• A CLI está válida. Vou construir o índice completo agora:
  inventário, extração por página, chunks e índice BM25 local.

───────────────────────────────────────────────────────────────

• A construção ainda está rodando, provavelmente na etapa de
  extração dos PDFs maiores. Vou acompanhar até terminar e só
  depois testar buscas reais.

• Waited for background terminal · python3 /home/hyprtest/
Documents/CACD_RAG/cacd_rag.py build

───────────────────────────────────────────────────────────────

• Ainda está processando. Como são mais de cem PDFs e a
  extração é página a página para preservar citação, isso pode
  levar alguns minutos.

• Waited for background terminal · python3 /home/hyprtest/
Documents/CACD_RAG/cacd_rag.py build

───────────────────────────────────────────────────────────────

• A tarefa continua em execução sem erros visíveis. Vou deixar
  finalizar; se ficar lento demais, ajusto para mostrar
  progresso por documento em uma próxima melhoria.

• Waited for background terminal · python3 /home/hyprtest/
Documents/CACD_RAG/cacd_rag.py build

───────────────────────────────────────────────────────────────

• Ainda está rodando. O desenho preserva páginas para citação,
  mas a primeira indexação é a etapa mais pesada; depois as
  consultas usam os arquivos já extraídos.

• Ran python3 /home/hyprtest/Documents/CACD_RAG/cacd_rag.py
  │ build
  └ Inventario criado: 137 arquivos
    Extracao concluida: 137 documentos
    Chunks criados: 5905
    Indice BM25 criado: 5905 chunks

───────────────────────────────────────────────────────────────

• O índice foi criado: 137 documentos e 5.905 chunks. Vou
  testar agora consultas representativas para verificar filtros
  por matéria, prova e padrão de resposta.

• Ran python3 /home/hyprtest/Documents/CACD_RAG/cacd_rag.py
  │ search "balanco de pagamentos" --materia Economia --limit
  │ 3 --max-chars 500
  └ [1] 07_Economia/02_Livros_Manuais/O Brasil E A Economia
    Global.pdf p.122 | score=6.792 | Economia, documento,
    … +29 lines (ctrl + t to view transcript)
    Pagamentos segue critérios formula- Balanço de Pagamentos,
    a renda, a poupança, o PIB e seus dos pelo...

• Ran python3 /home/hyprtest/Documents/CACD_RAG/cacd_rag.py
  │ estudar_materia Geografia --limit 3 --max-chars 500
  └ # Estudo ativo - Geografia

    … +41 lines (ctrl + t to view transcript)
    Salvo em: /home/hyprtest/Documents/CACD_RAG/outputs/
    estudo_cc2328ebd68da2f7.md

• Ran python3 /home/hyprtest/Documents/CACD_RAG/cacd_rag.py
  │ provas --ano 2025 --banca CEBRASPE --fase segunda_fase
  │ --disciplina-prova Economia --limit 4 --max-chars 500
  └ # Analise de provas CACD

    … +33 lines (ctrl + t to view transcript)
    Salvo em: /home/hyprtest/Documents/CACD_RAG/outputs/
    provas_f3a1bbfbf98b0ca0.md

───────────────────────────────────────────────────────────────

• Os testes funcionaram, mas apareceu um erro de classificação:
  arquivos em 00_Guias_Editais/Provas_CACD foram marcados como
  guia por causa do nome da pasta. Vou corrigir a regra de
  metadados e reconstruir só as partes leves do índice; a
  extração já fica reaproveitada.

• Edited Documents/CACD_RAG/cacd_rag.py (+4 -2)
    132          tipo_documento = "padrao_resposta"
    133 -    if "edital" in lower or "editais_cacd" in lower:
    133 +    if tipo_documento == "documento" and ("edital" in
         lower or "editais_cacd" in lower):
    134          tipo_documento = "edital"
    135 -    if "guia" in lower or any(word in lower for word i
         n ["capivara", "jacare", "sarue", "carcara"]):
    135 +    if tipo_documento == "documento" and (
    136 +        "guia" in lower or any(word in lower for word
         in ["capivara", "jacare", "sarue", "carcara"])
    137 +    ):
    138          tipo_documento = "guia"

───────────────────────────────────────────────────────────────

• A regra foi ajustada para que provas, gabaritos e padrões
  tenham precedência sobre “Guias_Editais”. Vou reconstruir
  inventário, chunks e índice usando os textos já extraídos.

• Ran python3 /home/hyprtest/Documents/CACD_RAG/cacd_rag.py
  │ inventory && python3 /home/hyprtest/Documents/CACD_RAG/
  │ cacd_rag.py extract && python3 /home/hyprtest/Documents/
  │ … +2 lines
  └ Inventario criado: 137 arquivos
    Extracao concluida: 137 documentos
    Chunks criados: 5905
    Indice BM25 criado: 5905 chunks

───────────────────────────────────────────────────────────────

• A reconstrução reaproveitou a extração e terminou rápido. Vou
  repetir o teste de provas para confirmar que os metadados
  agora saem corretos.

• Explored
  └ List CACD_RAG

• Ran python3 /home/hyprtest/Documents/CACD_RAG/cacd_rag.py
  │ provas --ano 2025 --banca CEBRASPE --fase segunda_fase
  │ --disciplina-prova Economia --limit 3 --max-chars 400
  └ # Analise de provas CACD

    … +34 lines (ctrl + t to view transcript)
    Salvo em: /home/hyprtest/Documents/CACD_RAG/outputs/
    provas_4c9c7832931d7c1e.md

• Ran python3 /home/hyprtest/Documents/CACD_RAG/cacd_rag.py
  │ search "gabarito definitivo primeira fase"
  │ --tipo-documento gabarito --ano 2026 --banca CEBRASPE
  │ … +1 lines
  └ [1] 00_Guias_Editais/Provas_CACD/
    Primeira_Fase/2026_CEBRASPE/2026_CACD_1fase_gabarito_defini
    … +19 lines (ctrl + t to view transcript)
    Obs.: ( X ) item anulado. Item 121 122 123 124 125 126 127
    128 129 130 131 13...

───────────────────────────────────────────────────────────────

• Os testes agora retornam metadados corretos (prova,
  padrao_resposta, gabarito) e filtros por ano/banca/fase. Vou
  fazer uma última validação de sintaxe e um resumo
  quantitativo do índice.

• Ran python3 -m py_compile /home/hyprtest/Documents/CACD_RAG/
  │ cacd_rag.py
  └ (no output)

• Ran python3 - <<'PY'
  │ import json
  │ from pathlib import Path
  │ … +17 lines
  └ files 137
    documents 137
    … +5 lines (ctrl + t to view transcript)
    529, 'segunda_fase': 464, 'terceira_fase': 295}
    banca {'(vazio)': 4612, 'CEBRASPE': 507, 'IADES': 786}

───────────────────────────────────────────────────────────────

• Implementei o RAG local em Documents/CACD_RAG.

  Ele já está indexado e funcionando sobre Documents/
  CACD_Outros:

  - 137 arquivos inventariados
  - 137 documentos extraídos
  - 5.905 chunks
  - índice BM25 local em Python puro
  - metadados por matéria, fase, ano, banca, tipo de documento
    e disciplina

  - comandos para busca, perguntas, estudo por matéria, análise
    de provas e correção discursiva assistida

  Arquivos principais:

  - Documents/CACD_RAG/cacd_rag.py
  - Documents/CACD_RAG/README.md

  Exemplo de uso:

  python3 /home/hyprtest/Documents/CACD_RAG/cacd_rag.py ask
  "Como o CACD cobra balanco de pagamentos?" --materia Economia

  Também validei:

  - sintaxe Python ok
  - busca por prova/padrão/gabarito ok
  - filtros por ano, banca, fase e disciplina_prova ok

  Observação prática: como não havia sentence-transformers,
  Chroma, FAISS ou PyMuPDF instalados, implementei uma versão
  local sem dependências externas. Ela já serve para estudo
  ativo e pode ser evoluída depois para embeddings sem mudar a
  estrutura do acervo.