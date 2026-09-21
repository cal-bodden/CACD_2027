---
title: DIAGNOSTICO — Fase 0
tags: [cacd-2027, sistema, diagnostico]
gerado_em: 2026-09-21
status: aguardando-aprovacao
atualizado: 2026-09-21 (adendo — espelhos oficiais)
---

# DIAGNÓSTICO — Fase 0 (somente leitura)

Nenhuma escrita foi feita no VAULT, em MATERIAIS ou no Anki além deste arquivo.
Tudo abaixo foi medido por script (hash sha256, parse dos `.md`, AnkiConnect, `pdftotext` só em gabaritos e na 1ª página dos cadernos).

---

## 0. Resumo executivo — o que decide as próximas fases

| # | Achado | Consequência |
|---|---|---|
| **B1** | **RESOLVIDO (adendo).** A divergência vinha de **cadernos diferentes**: os `TPS_2026_*` do vault e o gabarito em MATERIAIS são do **caderno 01** (`178_IRBRCACDOBJ_001_01`); sua prova e seu gabarito são do **caderno 03** (`…_001_03`), com os itens embaralhados. Li suas folhas de resposta (GIF) por processamento de imagem e corrigi contra o gabarito do caderno 03: **162 acertos (148 + 14 anulados) / 63 erros / 15 brancos = 146,25** — igual ao espelho oficial, e 6 de 8 disciplinas batem item a item (as outras 2 diferem só por 2 rótulos trocados no vault, ver §7.1). Casando o texto de cada item, construí o mapa caderno 03 → caderno 01: **240/240 mapeados, bijeção perfeita, gabaritos consistentes em 240/240**. `Prova_2026.md` (digitado) tem 6 entradas erradas (itens 15, 96, 135, 199, 202, 206 do caderno 03). | Primeira carga de `erros.jsonl` **desbloqueada**: 63 erros + 15 brancos com id do vault (Apêndice A). `Prova_2026.md` vira candidato a arquivo (R15). |
| **B2** | Plugin **Tasks está instalado, mas não ativado** (`community-plugins.json` lista só realclaudian, charts, chartsview, task-progress-bar). | Ativar antes da Fase 4. |
| **B3** | **`TPS_2025_*` NÃO são cópias de 2024.** A versão de 28/03 era (o `RELATORIO.md` registra "65 sem gabarito"); a versão atual (13/06) contém a prova real de 2025 — a 1ª frase do caderno oficial está no arquivo e os 240 gabaritos batem 100% com o PDF oficial. O que sobrou da cópia antiga são os CSVs de `Cruzamentos/` (hash idêntico 2024=2025). | Nada a deduplicar entre 2024/2025 na Fase 2. Arquivar `Cruzamentos/`. |
| **B4** | Os TPS do vault **carregam gabarito para itens anulados** (2025: 16 itens; 2026: 14; 2024: há "X" no PDF oficial). | `itens.jsonl` precisa do campo `anulado`; estatísticas os excluem. |
| **B5** | O vault **já tem infraestrutura de itens**: `itens_tps.csv` (2.460 itens 2017–2026), `lexico.py` + `classificar.py` (1.785 classificados, 1.281 em confiança alta), `painel.py`. | Fase 2 reaproveita em vez de reescrever. |
| **B6** | Anki: deck `CACD 2027` tem **115 cartões, todos novos, zero revisões**. Coleção inteira: 78 revisões nos últimos 30 dias (BACEN e Russo). | O Anki não faz parte da rotina hoje. `CACD::Erros` nasce vazio; decidir o destino dos 115 (§9). |
| **B7** | Git: repositório sem nenhum commit, **695 arquivos em staging**, sem `.gitignore`, `.obsidian/workspace.json` em staging. | Primeiro ato da Fase 1: `.gitignore` + commit "pré-Fase 1". |
| **B8** | Dois "planos anteriores" reais existem e são recentes (ago–set/2026): a rotina em `_Relatórios de Desempenho.md` e o método em `Estratégia 2027 — Estudo Orientado à Prova.md`. | Confirmar na §5 qual deles vale como base do `PLANO.md`. |

---

## 1. Pré-requisitos verificados

| Item | Estado |
|---|---|
| AnkiConnect `localhost:8765` | ✅ responde (versão 6) |
| Plugin Tasks em `.obsidian/plugins/` | ⚠️ pasta `obsidian-tasks-plugin` existe; **não está em `community-plugins.json`** (desativado). Sem `data.json` → configuração padrão, sem filtro global. |
| Git no VAULT | ⚠️ existe (`master`), 0 commits, 695 arquivos staged, sem `.gitignore` |
| `~/.local/state/quickshell/user/todo.json` | não tocado (conteúdo: `[]`) |
| `pdftotext`/`pdfinfo` | disponíveis (`/usr/bin`) |
| Nomes de arquivo | todos em NFC (sem problema de normalização) |

---

## 2. Inventário do VAULT (`~/Documents/CACD_2027`)

**Total:** 645 `.md` · 31 `.json` · 23 `.csv` · 8 `.py` · 8 `.png` · 4 `.pdf` · ≈ 270 MB (dos quais 224 MB é um único PDF duplicado, ver R8).

| Pasta | Notas `.md` | Tamanho | Observação |
|---|---:|---:|---|
| 00 - GESTÃO & METADADOS | 70 | 20 MB | TPS, cruzamentos (13,8 MB), dados, relatórios |
| 01 - LÍNGUA PORTUGUESA | 11 | 460 KB | 2 notas < 300 B |
| 02 - LÍNGUA INGLESA | 7 | 60 KB | 4 de 7 notas < 300 B; pasta "Resumo" não corresponde a exercício da prova |
| 03 - HISTÓRIA DO BRASIL | 83 | 2,9 MB | |
| 04 - HISTÓRIA MUNDIAL | 89 | 2,6 MB | 2 notas vazias (História dos EUA 2 e 3) |
| 05 - POLÍTICA INTERNACIONAL | 145 | 4,6 MB | maior acervo |
| 06 - GEOGRAFIA | 31 | 1,3 MB | |
| 07 - ECONOMIA | 65 | 2,3 MB | 4 notas < 300 B (3.1.1 e 3.1.5 são stubs idênticos de 118 B) |
| 08 - DIREITO | 51 | 3,6 MB | 5 notas < 300 B |
| 09 - IDIOMA ADICIONAL | 5 | 16 KB | tudo vazio (~700 B no total) |
| 10 - SIMULADOS & EXERCÍCIOS | 8 | 336 KB | simulados sintéticos (IA); `_simulado.md` ≈ `S2.md` |
| 11 - FLASHCARDS & MAPAS MENTAIS | 2 | 8 KB | vazio |
| 12 - RECURSOS ADICIONAIS | 67 | 229 MB | 58 artigos (FA etc.), 3 compilados p/ Claude Project (5,5 MB), PDF de 214 MB |
| 13 - DOSSIÊS DE PROVA | 11 | 128 KB | 10 dossiês já feitos no método da "Estratégia 2027" |

### 2.1 Corpus de provas (`00/04 - Provas Anteriores/`)

18 arquivos `TPS_AAAA_turno.md` — **2.460 itens autênticos**, todos com gabarito parseável (`## Questão … / ### Item … / #### Gabarito Oficial:`).

| Edição | Banca | Itens (M+T) | Formato no arquivo | Gabaritos ✔ vs oficial |
|---|---|---:|---|---|
| 2017 | IADES | 284 | 33+38 questões × 4 itens | (PDF oficial não está em MATERIAIS) |
| 2018 | IADES | 284 | idem | idem |
| 2019 | IADES | 284 | idem (Geografia com 48 itens e sem Direito — verificar rótulos) | idem |
| 2020 | IADES | 284 | idem | PDF em MATERIAIS, não conferido |
| 2022 | IADES | 292 | 34+39 × 4 | PDF em MATERIAIS, não conferido |
| 2023 | IADES | 292 | 35+38 × 4 | idem |
| 2024 | Cebraspe | 260 | 33+32 × 4 (formato oficial de 2024 era este) | PDF oficial tem "X" por item; vault não marca anulados |
| 2025 | Cebraspe | 240 | 120 + 120 itens corridos | **240/240 iguais**; 16 anulados sem marcação |
| 2026 | Cebraspe | 240 | idem | **240/240 iguais**; 14 anulados sem marcação |

Itens por disciplina (todas as edições): LP 348 · PI 404 · HB 360 · HM 351 · GEO 241 · ING 286 · ECO 269 · DIR 201.

Outros arquivos da pasta:
- `TPS 2022.md`, `TPS 2023.md`, `TPS 2024.md` (390 KB): **gabaritos comentados gerados por IA** (`**Resposta: CERTO** / **Fundamentação:**`), sem a estrutura de itens; só 25–30 % das frases coincidem com os `TPS_*`. Não são duplicatas — são outra coisa (justificativas sintéticas).
- `_Materias/*.md` (1 MB): os mesmos itens dos `TPS_*` fatiados por disciplina (>95 % das frases coincidem) → **derivável**.
- `Cruzamentos/` (13,8 MB, 36 arquivos): cruzamento item×nota que o próprio vault classificou como ruído (scores 0,08–0,23); os CSVs de 2025 são cópias byte a byte dos de 2024.
- `_dados/`: `itens_tps.csv`, `itens_classificados.csv`, `painel_preparacao.csv`, `lexico.py`, `classificar.py`, `painel.py`, `extrair_itens.py` — **infraestrutura útil**.

### 2.2 Pasta `00 - GESTÃO` restante
- `01 - Edital`: 364 itens do Anexo III parseados (`edital_itens.csv`), cobertura por item (`cobertura_edital.csv`), Mapa Mestre, Critérios 2ª fase, mudanças 2025→2026.
- `02 - Cronograma`: **vazio** (só frontmatter, tag `cacd-2025`).
- `03 - Estratégias & Métodos`: 8 arquivos — ver §5.
- `05 - Relatórios`: `Prova_2026.md` (240 respostas, ver B1) e `_Relatórios de Desempenho.md` (tabela 2025, espelho 2026, **plano 2027**).
- `06 - Backup de notas alteradas.`: 4 versões antigas de notas (GEO ×3, BACEN ×1), 380 KB.

### 2.3 Arquivos adicionados por você em 21/09 (em `00/05 - Relatórios de Desempenho/`)

| Arquivo | Tamanho | O que é | Proposta |
|---|--:|---|---|
| `Espelho_2026_Oficial.gif` | 2,4 MB | folha de respostas real — manhã (itens 1–120) | manter no vault (documento pessoal), **ignorar no git** (>1 MB) |
| `Espelho_oficial_2026_2.gif` | 2,2 MB | folha de respostas real — tarde (121–240) | idem |
| `PROVA_2026_oficial_1.pdf` / `_2.pdf` | 0,7 / 0,9 MB | cadernos **03** manhã/tarde (9 p. cada) | mover para `MATERIAIS/…/2026_CEBRASPE/caderno_03/` (documento oficial; MATERIAIS é o lugar dos PDFs) |
| `Gabarito_2026_oficial_1.pdf` / `_2.pdf` | 0,3 MB cada | gabaritos definitivos do caderno **03** | idem |

Hashes diferentes dos de MATERIAIS (são cadernos diferentes, não duplicatas).

---

## 3. Inventário de MATERIAIS (`~/Documents/CACD_Outros`)

**Total:** 896 MB · 212 arquivos: 184 PDF, 12 EPUB, 12 MD, 1 ZIP, 1 TXT, 1 `.crdownload`, 1 `.pdf` que é HTML. Sem git (correto). Hash de todos os arquivos em `scratchpad` (não gravado no vault).

| Pasta | Arquivos | Tamanho | Conteúdo |
|---|---:|---:|---|
| 00_Guias_Editais | 150 | 175 MB | 6 guias de aprovados (113 MB), editais 2022–2026, **provas**: 1ª fase 2016 (CESPE), 2020, 2022–2026; demais fases 2016, 2020, 2022–2026, com padrões de resposta. Cada ano tem `_fontes.md` com URLs oficiais. |
| 03_Historia_do_Brasil | 8 | 98 MB | Fausto (PDF+TXT), Schwarcz, Ricupero, Carvalho, Sampaio, Cidadania no Brasil |
| 04_Historia_Mundial | 4 | 11 MB | Hobsbawm ×3, manual Atualidades |
| 05_Geografia | 7 | 59 MB | Cresswell, Milton Santos ×2, Becker (0 B — download falhou), Kaplan, manual |
| 06_Politica_Internacional | 22 | 243 MB | 15 aulas PDF (Aula 1–17) **+ o mesmo conjunto zipado (102 MB)**, Kissinger ×2, Nogueira & Messari, Kennedy, UE |
| 07_Economia | 6 | 78 MB | Blanchard ×2, Varian, Giambiagi, Manual do Candidato, Brasil e a Economia Global |
| 08_Direito_Internacional_Publico | 7 | 15 MB | Mazzuoli, Manual do Candidato ×2, Macau DIP 2026 (2 PDFs), edital BCB (fora de lugar), `.pdf` de 160 B (erro 504) |
| 09_Direito_Constitucional | 5 | 216 MB | Esquematizado 2020 (214 MB), Macau Aula 01 ×3 (original, anotada, resumo), `.~lock` |
| 99_A_Classificar | 1 | 2,8 MB | `Unconfirmed 45207.crdownload` — PDF corrompido (xref inválido) |
| raiz | 2 | 1 MB | `Atualidades-Concursos-Manual-Espanhol.pdf` (deveria estar em 11_Espanhol), README |
| 01_Portugues, 02_Ingles, 10_Direito_Administrativo, 11_Espanhol, 12_Frances, 90_Fontes_Gerais, Guias | 0 | 0 | **vazias** |

> Leitura: as disciplinas de **prioridade 1 (Português, Inglês)** têm **zero** material em MATERIAIS e 520 KB no vault. Direito Administrativo idem.

---

## 4. Redundâncias candidatas (com evidência)

Ação proposta segue a Regra 2: mover para `_arquivo/` da mesma raiz + registro em `_arquivo/LOG.md`. Nada é apagado.

### 4.1 VAULT

| ID | Arquivo(s) | Evidência | Ação proposta |
|---|---|---|---|
| **R1** | `00/04/Cruzamentos/` (36 arquivos, 13,8 MB) | ruído reconhecido no próprio `Cobertura do Edital — Diagnóstico`; CSVs 2025 = 2024 (sha256 idêntico) | arquivar pasta inteira |
| **R2** | `00/04/_Materias/*.md` (8 arquivos, 1 MB) | >95 % das frases existem nos `TPS_*`; derivável do `itens.jsonl` | arquivar |
| **R3** | `00/04/TPS 2022.md`, `TPS 2023.md`, `TPS 2024.md` | justificativas sintéticas de IA sem estrutura; nome confunde com o corpus autêntico | **sua decisão**: (a) arquivar; (b) manter renomeado `Comentarios_IA_AAAA.md` como fonte de justificativas para cartões (rotulado *sintético*) |
| **R4** | `10/_simulado.md` vs `10/1ª Fase/S2.md` | diff de 2 linhas em 67 KB | arquivar `_simulado.md` |
| **R5** | `00/06 - Backup de notas alteradas.` (4 arquivos) | backups manuais; git passa a cumprir esse papel | arquivar |
| **R6** | `00/03/_análise.md` (125 KB, efemérides 2025), `_Indice_Geral_Tags.md` (129 KB, índice gerado), `SETUP COMPLETO - CONFIGURAÇÃO ARTIFACTS CACD.md`, `SISTEMA DE ESTABILIZAÇÃO POLÍTICA INTERNACIONAL.md`, `RAG.md` (log de terminal colado) | todos `cacd-2025`, sem uso diário | arquivar os 5 |
| **R7** | `00/03/_Estratégias & Métodos.md` | é o **plano 2025** ("Operação 5 pontos", prova de 20/07/2025) | arquivar **depois** de você confirmar §5 |
| **R8** | `12/Bibliografia/Direito Constitucional Esquematizado 2020.pdf` (214 MB) | sha256 idêntico ao de MATERIAIS/09 | arquivar a cópia do vault (fica fora do git de qualquer forma) |
| **R9** | `12/Multimídia/_ZCopy/transmissao_politica_monetaria 1.png` | sha256 idêntico ao sem " 1" | arquivar |
| **R10** | `12/Artigos & Papers/`: `50 Essential Python Concepts…`, `A Evolução da IA…`, `Body Language`, `What Every Body is Saying`, `Untitled.md` (0 B) | fora do escopo CACD / vazio | arquivar |
| **R11** | Notas de 0 B: `04/05/5.8 - História dos EUA/2. …` e `3. …`, `09/01 - Espanhol/Aulas Espanhol/Aula 00.md` | vazias | **sugiro deixar** (placeholders na árvore do edital); alternativa: arquivar |
| **R12** | `07/03/3.1 - …/3.1.1_….md` e `3.1.5_….md` | stubs idênticos de 118 B | deixar (placeholders) |
| **R13** | `02/02 - Segunda Fase/2 - Resumo (conforme Tabela 6.2 do Edital)/` | pasta não corresponde a nenhum exercício da prova de inglês desde o edital 2026 (nota do próprio vault) | arquivar; renomear `3 - Tradução` → `2 - Versão PT→EN` |
| **R14** | 431 notas com tag `cacd-2025` (23 com `cacd-2027`) | metadado obsoleto | **não fazer** (não é usado diariamente; Regra 8). Listo por transparência. |
| **R15** | `00/05/Prova_2026.md` | transcrição manual com 6 erros (itens 15, 96, 135, 199, 202, 206 do cad. 03); substituída pelo Apêndice A / `_sistema/respostas_2026.tsv` | arquivar após a Fase 2 gerar o TSV |
| — | `12/_Compilados/*.md` (5,5 MB) | concatenação de notas + TPS para Claude Projects, gerado 10/09 | **manter** (em uso), mas registrar que é derivado e regenerável |
| — | `02/…/Ingles_TPS_2026.md` | texto dos itens de inglês de 2026 sem gabarito | manter (nota de estudo) |
| — | `12/Multimídia/_ZCopy/*.pdf` (2 PDFs, 3,7 MB) | não existem em MATERIAIS | manter; opcional: mover para MATERIAIS/05 e /06 |
| — | `12/Bibliografia/Midias/Ed_1_IRBr_CACD_25_abertura.pdf` (52 p.) vs MATERIAIS `2025 - Edital … retificacoes.pdf` (55 p.) | versões diferentes do mesmo edital | manter |

### 4.2 MATERIAIS

| ID | Arquivo | Evidência | Ação proposta |
|---|---|---|---|
| **M1** | `06_PI/02/Política Internacional-20260623T172514Z-3-001.zip` (102 MB) | `unzip -l` = os 15 PDFs já extraídos ao lado, mesmos tamanhos | arquivar |
| **M2** | `08_DIP/02/.pdf` (160 B) | é uma página HTML "504 Gateway Time-out" | arquivar |
| **M3** | `09_DConst/02/.~lock.Direito Constitucional….pdf#` | lock file do LibreOffice | arquivar |
| **M4** | `05_Geo/02/Fronteira amazônica … Anna's Archive-1.pdf` | **0 bytes** (download falhou) | arquivar; rebaixar de novo se quiser o livro |
| **M5** | `99_A_Classificar/Unconfirmed 45207.crdownload` (2,9 MB) | PDF sem xref/trailer — corrompido | arquivar |
| **M6** | `Atualidades-Concursos-Manual-Espanhol.pdf` (raiz) | fora do padrão do README | mover para `11_Espanhol/02_Livros_Manuais/` |
| **M7** | `08_DIP/02/ED_1_BCB_23_ABERTURA.pdf` | edital do BCB dentro de DIP | arquivar (não é CACD) |
| — | `09_DConst/06/…/Aula 01_Direito Interno.pdf` (3 p.) | já convertido em nota no vault (`Aula 01 - Direito Interno (Macau) - Esquema para completar - 2026.md`) | manter (é a fonte) |
| — | pastas vazias (01, 02, 10, 11, 12, 90, Guias) | | manter; `Guias/` é redundante com `00_Guias_Editais` — arquivar? |

### 4.3 Fora do escopo, mas relevante
- `~/Documents/CACD_Vault_2025` (3,6 GB, git próprio, último commit 24/03/2026): é o **vault anterior**; a pasta `00 - GESTÃO` do vault 2027 é uma cópia dele com acréscimos. Não proponho ação (não é VAULT nem MATERIAIS).
- `~/Documents/CACD_RAG` (51 MB): índice BM25 sobre o vault, correspondente ao `RAG.md`.

---

## 5. Plano de estudos anterior — candidatos para confirmação

| ID | Arquivo | O que é | Data | Recomendação |
|---|---|---|---|---|
| **P1** | `00/05/_Relatórios de Desempenho.md` § "Tabelas de referência — Plano CACD 2027" | diagnóstico por disciplina (erro/marcados 2025→2026, meta 2027), aritmética até a aprovação, **rotina semanal de 24 h** (6 blocos), calendário ago/2026–ago/2027 com checkpoints, 4 compromissos não negociáveis, classificação de erros A–G, lista "o que NÃO fazer" | set/2026 | **É o plano anterior.** Compatível com a missão em quase tudo; conflitos: (i) rotina de 24 h/sem vs. "blocos curtos"; (ii) taxonomia de erro A–G vs. a nova `tipo_erro`/`armadilha`; (iii) Espanhol diário como compromisso nº 1 — a missão não menciona idioma adicional. |
| **P2** | `00/03/Estratégia 2027 — Estudo Orientado à Prova.md` | método "dossiê de tópico" (6 seções), ciclo erro→ponto de corte, fórmula de prioridade, sequência de 4 fases; 10 dossiês já produzidos em `13 - DOSSIÊS DE PROVA` | ago/2026 | **Método anterior**, parcialmente executado. A missão o substitui pelo banco de itens + Anki; os dossiês existentes viram fonte para "nota puxada por erro" (bloco 3). |
| **P3** | `00/03/_Estratégias & Métodos.md` | "Plano de Estudos CACD 2025 — Operação 5 pontos" | mai/2025 | obsoleto → arquivar (R7) |
| **P4** | `00/02/_Cronograma de Estudos.md` | vazio | — | será substituído pelo `PLANO.md` |
| — | `~/Documents/Estudos_Concursos/02_CRONOGRAMA.md`, `03_ESTRATEGIA.md` | plano BACEN/TCU | — | não é CACD |

---

## 6. Lacunas do corpus

| Edição | No vault | Em MATERIAIS | Nota |
|---|---|---|---|
| 2011–2015 (CESPE) | ✗ | ✗ | **maior lacuna de valor**: mesma banca de 2024–2027, formato C/E. Não há nada local. |
| 2016 (CESPE) | ✗ | ✅ caderno M/T + gabaritos definitivos (PDF) | extraível para o banco (Fase 2, opcional) |
| 2017–2019 (IADES) | ✅ | ✗ | |
| 2020 (IADES) | ✅ | ✅ | |
| **2021 (IADES)** | ✗ | ✗ | você fez essa prova (42,50); não há caderno nem gabarito em lugar nenhum |
| 2022–2023 (IADES) | ✅ | ✅ (tipos A–D, gabaritos, justificativas) | |
| 2024 (Cebraspe) | ✅ | ✅ | vault sem marcação de anulados |
| 2025 (Cebraspe) | ✅ (prova real, confirmada) | ✅ | 16 anulados sem marcação; **não há suas respostas item a item** de 2025, só a tabela por disciplina |
| 2026 (Cebraspe) | ✅ (240/240 gabaritos = oficial) | ✅ caderno M/T + gabaritos definitivos | **suas respostas: ver B1** |

Discursivas: MATERIAIS tem provas + padrões de resposta 2016, 2020, 2022–2026; o vault tem 46 B em `10/2ª Fase - Discursivas`. Não é objeto desta missão, mas o bloco 3 (produção) vai precisar disso a partir de jan/2027.

---

## 7. Relatórios de desempenho — tendências

% de acerto sobre o total de itens da disciplina (2017–2024 de `_Provas Anteriores.md`; 2025 de `_Relatórios`, sem espelho oficial; 2026 do espelho oficial):

| Disciplina | 2017 | 2018 | 2023 | 2024 | 2025 | **2026** | Erros 2026 | Erro/marcados 2026 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| Português | 35,0 | 50,0 | 55,7 | 58,8 | 77,5 | **72,5** | 9 | 23,7 % |
| Inglês | 69,4 | 71,9 | 66,7 | 51,8 | 64,3 | **70,0** | 9 | 30,0 % |
| Direito | 50,0 | 45,0 | 83,9 | 57,1 | 76,9 | **56,0** | 10 | **41,7 %** |
| Economia | 59,4 | 71,0 | 73,2 | 73,2 | 80,8 | **56,0** | 8 | 36,4 % |
| Geografia | 91,6 | 75,0 | 79,2 | 66,7 | 66,7 | **64,0** | 6 | 27,3 % |
| Pol. Internacional | 62,5 | 35,4 | 52,3 | 58,8 | 82,5 | **67,5** | 11 | 28,9 % |
| Hist. Mundial | 47,7 | 56,8 | 48,9 | 66,7 | 76,9 | **68,0** | 7 | 29,2 % |
| Hist. Brasil | 47,7 | 68,0 | 69,3 | 73,6 | 66,7 | **80,0** | 3 | 11,1 % |
| **Nota** | 41,00 | 40,00 | 46,63 | 41,13 | (não registrada; 179 acertos pela tabela) | **146,25** (3216º) | 63 | 28,0 % |

### 7.1 Prova 2026 reconstruída item a item (adendo)

Fonte: folhas de resposta oficiais lidas por imagem + gabarito do caderno 03 + mapa para a numeração do vault (caderno 01). Total confere com o espelho: 162 / 63 / 15.

| Disciplina | Itens | Acertos (c/ anulados) | Erros | Brancos | Erros — nº do item **no vault** (caderno 01) |
|---|--:|--:|--:|--:|---|
| Língua Portuguesa | 40 | 29 | 9 | 2 | 3, 8, 13, 17, 20, 25, 28, 30, 31 |
| História do Brasil | 30 | 24 | 3 | 3 | 56, 66, 70 |
| História Mundial | 25 | 17 | 7 | 1 | 75, 77, 79, 80, 82, 89, 93 |
| Geografia | 25 | 16 | 6 | 3 | 99, 100, 102, 103, 106, 112 |
| Língua Inglesa | 30 | 21 | 9 | 0 | 122, 124, 125, 126, 127, 131, 141, 147, 149 |
| Política Internacional | 40 | 27 | 11 | 2 | 155, 156, 159, 165, 169, 172, 177, 179, 180, 184, 186 |
| Economia | 25 | 14 | 8 | 3 | 191, 192, 193, 194, 199, 203, 211, 213 |
| Direito | 25 | 14 | 10 | 1 | 216, 222, 224, 225, 230, 231, 235, 237, 238, 240 |

> **Rótulo errado no vault:** `TPS_2026_tarde.md` marca os itens **216 e 217** como Economia, mas são Direito (direitos e garantias fundamentais, art. 5º da CF). Com essa correção, o vault fica com ECO 25 / DIR 25 e todas as 8 disciplinas batem com o espelho oficial. Corrigir na Fase 2 (A2.1).

Leitura dos erros: Inglês errou 9 **sem deixar nenhum branco** (30 % dos marcados); Economia concentrou 3 brancos + 8 erros em 25 itens; Direito tem 10 erros em 24 válidos. Os 63 erros são a primeira carga de `erros.jsonl`; a lista item a item está no Apêndice A.

Confronto com as prioridades da missão:

1. **Português e Inglês** — *ganho potencial confirmado, "estagnados" não*. Português subiu de 35 % para 72–77 %; Inglês oscila (52–72 %). Juntos somam 18 dos 63 erros, com 0 brancos em Inglês (30 % dos marcados errados → gestão de risco).
2. **Direito pior desempenho** — confirmado (41,7 % erro/marcados; volatilidade 45→84→57→77→56 indica dependência de contato recente).
3. **Geografia sem base** — confirmado por queda monotônica 92→64 %; o caso GEO-7.3 (1/7 em 2026 com 45 KB de nota) mostra que o problema é de forma, não de volume.
4. **Decaimento sem contato** — a evidência mais forte do conjunto: de 2025 para 2026, Economia 81→56, Direito 77→56, PI 82→67. Se a tabela de 2025 estiver correta, você teve **mais acertos em 2025 (179) do que em 2026 (162)**.
5. **HB manutenção** — confirmado (80 %, 3 erros).
6. Fora das prioridades: **História Mundial** com 29 % de erro entre marcados (7 erros em 25) merece ao menos manutenção espaçada.

---

## 8. Cobertura do vault × edital × frequência nos TPS

Base: `cobertura_edital.csv` (364 itens: 226 consolidado, 36 parcial, 12 esboço, 2 ausente, 88 cobertos na nota-pai) × `itens_classificados.csv` (1.785 itens classificados; LP e ING não são classificados pelo léxico — 634 "n/a").

Tópicos **não consolidados** com maior incidência nos TPS (itens classificados / em confiança alta):

| Itens | Alta | Estado | Tópico |
|--:|--:|---|---|
| 23 | 18 | parcial (13 KB) | PI-13.14 Reforma das Nações Unidas |
| 11 | 8 | **ausente** | HM-8 RI no século XXI (paradigmas digitais) |
| 9 | 8 | parcial | DIR-13 Regime jurídico do Serviço Exterior (Lei 11.440) |
| 8 | 7 | parcial | DIR-12 Servidor público, improbidade |
| 7 | 3 | **ausente** | ECO-5 Bancos digitais / dinheiro digital |
| 7 | 1 | parcial | DIR-15 DIP e direito interno |
| 6 | 4 | parcial | PI-13.11 Crimes de guerra, genocídio |
| 6 | 4 | parcial | DIR-3 Constituição, controle de constitucionalidade |
| 4 | 1 | parcial | DIR-1 Normas jurídicas |
| 3 | 2 | parcial | DIR-9 Administração Pública |
| 3 | 1 | esboço | DIR-19 Formação do território |
| 2 | 1 | esboço | DIR-26 MERCOSUL / Direito da Integração |

Padrão: **Direito concentra 10 das 12 lacunas com incidência** — coerente com o pior desempenho. Os tópicos mais cobrados no total (ECO-2 108 itens, HM-3 82, HB-6 65, ECO-1 64, HM-1 59, HM-4 52, GEO-7 35) estão todos "consolidados" — o problema neles é desempenho, não cobertura (ex.: HM-1 3/7, HB-6 4/8, GEO-7 1/7 em 2026).

Notas-base que a missão prevê "antes das questões": GEO-1 (pensamento geográfico) existe com 148 KB em 4 notas; geopolítica clássica (GEO-6) consolidada; microeconomia da firma (ECO-1.2) e estágios de integração (ECO-3.x/PI-15) consolidados. Ou seja, **o material-base existe**; falta convertê-lo em capacidade de julgar itens.

---

## 9. Estado do Anki (via AnkiConnect)

| Métrica | Valor |
|---|---|
| Notas / cartões (coleção) | 5.983 / 21.129 (20.842 novos; 20.004 são "The Ultimate Guide to Russian") |
| Decks de topo | BACEN (275), BCB 2024 (75), **CACD 2027 (115)**, Russo (368), Russo A1 (292), Ultimate Russian (20.004), Default (0), Filtered Deck (10) |
| Deck CACD 2027 | só `07 - Economia::02 - Macroeconomia::2.1…2.8`; **115 cartões novos, 0 revisões, 0 due** |
| Tipos de nota CACD | `CACD — Conceito` (70 notas; campos Frente, Resposta, Desenvolvimento, Armadilha, Fonte) e `CACD — Item C/E` (45; Item, Gabarito, Justificativa, Padrao, Fonte) — alguns derivados de itens de 2026 ("Item 201 de 2026") |
| Tags nas notas CACD | `cacd-2027`, `economia`, `macroeconomia`, `eco-2.x`, `conceito`/`item-ce`, `prioridade-1` — **100 % têm disciplina**; convenção `disciplina::X` ainda não existe |
| Leeches | 0 (tag `leech`) |
| Suspensos | 0 |
| Duplicatas (1º campo, deck CACD) | 0 |
| Revisões últimos 30 dias (coleção) | 78 (BACEN 78 / Russo 88 nos últimos 60 d) |
| FSRS | preset "Default" tem `fsrsParams6` preenchido e `desiredRetention` 0,90 — consistente com FSRS ativo, mas o toggle é da coleção e não é legível pela API. **Confirme visualmente.** |
| Precedente de tag de armadilha | deck BACEN usa `armadilha::absoluto`, `armadilha::cauda-envenenada`, `armadilha::inversao-de-sinal`, `armadilha::nivel-vs-taxa`, `armadilha::troca-de-escolas` |

Não há deck `CACD::Erros` nem tipo `CACD-Proposicao`. Os 115 cartões existentes **violam a regra "cartões só de erros"** (foram gerados de conteúdo, não de erros seus) — decisão em A-F3.3.

---

## 10. Proposta de ações — aprovar item a item

### Fase 1 — Limpeza
- **A1.1** Criar `.gitignore` (`*.pdf`, `*.epub`, `*.zip`, `*.png`/`*.jpg` > 1 MB via lista explícita, `.obsidian/workspace*`, `.obsidian/plugins/`, `.obsidian/cache`, `__pycache__/`, `*.pyc`, `.claudian/sessions/`, arquivos > 5 MB listados por nome) e fazer o commit "pré-Fase 1" com o estado atual.
- **A1.2** Arquivar R1 (Cruzamentos), R2 (_Materias), R4 (_simulado.md), R5 (Backups), R6 (5 arquivos 2025), R8 (PDF 214 MB), R9 (png dup), R10 (artigos fora de escopo + Untitled) → `VAULT/_arquivo/` + `LOG.md`.
- **A1.3** R3 (`TPS 2022/2023/2024.md`): escolha (a) arquivar ou (b) renomear como sintético.
- **A1.4** R7 (plano 2025): arquivar após confirmação de §5.
- **A1.5** R13: arquivar pasta "Resumo" de Inglês 2ª fase e renomear "Tradução" → "Versão PT→EN".
- **A1.6b** Mover `PROVA_2026_oficial_*.pdf` e `Gabarito_2026_oficial_*.pdf` para `MATERIAIS/00_Guias_Editais/Provas_CACD/Primeira_Fase/2026_CEBRASPE/caderno_03/` (com `_fontes.md` indicando origem); manter os 2 GIFs no vault, fora do git.
- **A1.6** MATERIAIS: M1–M5 e M7 → `MATERIAIS/_arquivo/` + `LOG.md`; M6 mover para `11_Espanhol/02_Livros_Manuais/`.
- **A1.7** Ativar o plugin Tasks (você, no Obsidian).
- **A1.8** Commit "pós-Fase 1".

### Fase 2 — Banco de itens
- **A2.1** Gerar `_sistema/itens.jsonl` a partir dos 18 `TPS_*.md` (2.460 itens) com os campos pedidos **+ `anulado`** (true para os 16 de 2025 e 14 de 2026 lidos do PDF oficial; 2024 lido do PDF oficial por questão/item). `id` = `AAAA-T-NNN` (ex.: `2026-M-011`), numeração do **caderno 01** (a do vault). Para 2026, campo extra `item_caderno_03` com o mapa validado. **Corrigir a disciplina dos itens 216 e 217 de 2026 (Economia → Direito).**
- **A2.2** Sem deduplicação 2024/2025 (não são cópias — B3). Em vez disso, dedupe genérico por hash do enunciado (esperado: 0).
- **A2.3** `topico_edital`: reaproveitar `lexico.py`/`classificar.py`; `conf == alta` → tópico; caso contrário `topico_incerto: true` com o candidato. LP/ING recebem só a disciplina (o léxico não os cobre).
- **A2.4** Opcional: extrair 2016 (CESPE) dos PDFs em MATERIAIS para o banco (rotulado `autentico`, `banca: CESPE`). Requer parse de PDF de 2 cadernos — não conto como "ler PDF inteiro", mas peço aprovação explícita.
- **A2.5** Criar `_sistema/erros.jsonl` (vazio) com o esquema pedido.
- **A2.6** Primeira carga: gravar `_sistema/respostas_2026.tsv` (240 linhas: item cad. 03, item vault, disciplina, minha resposta, gabarito, resultado — Apêndice A) e, a partir dele, 63 registros em `erros.jsonl` (`minha_resposta` = C/E, `data` = 2026-03-29) + 15 registros de branco (`minha_resposta` = branco, `tipo_erro` = gestao_risco). `confianca`, `tipo_erro` e `armadilha` ficam **vazios** para você preencher na revisão (bloco 2 do plano) — não vou adivinhar.

### Fase 3 — Anki
- **A3.1** Criar tipo de nota `CACD-Proposicao` (Proposicao, Armadilha, Fonte, Origem, Disciplina, Topico) e deck `CACD::Erros`.
- **A3.2** Tags `disciplina::X`, `topico::Y`, `armadilha::Z`; checagem `canAddNotes` antes de inserir.
- **A3.3** Destino dos 115 cartões de `CACD 2027` — escolha: (a) deixar intocados, fora da rotina; (b) suspender + tag `revisar-remocao`; (c) migrar para `CACD::Erros` **somente** os `Item C/E` cujo item de 2026 você errou (após resolver B1).
- **A3.4** Você confirma FSRS ativo na coleção.

### Fase 4 — Plano
- **A4.1** Base: **P1** (rotina/compromissos/calendário) adaptada aos 3 blocos fixos da missão; **P2** rebaixado a "método de dossiê" usado no bloco 3; P3 arquivado.
- **A4.2** Diff (novas/mantidas/arquivadas) apresentado antes de escrever `PLANO.md`.
- **A4.3** Decisão pendente sobre Espanhol diário (compromisso nº 1 do P1): mantém, reduz ou sai do plano?

---

## 11. Perguntas que precisam de resposta antes de prosseguir

1. ~~Prova_2026.md é real?~~ **Resolvido** (B1). Nova pergunta: na primeira carga, quer marcar `confianca` (certeza/dúvida/chute) de memória para os 78 itens errados/brancos, ou deixa vazio e preenche ao refazer cada item no bloco 2?
2. **Tem as folhas de resposta de 2025** (como as de 2026)? Se sim, faço o mesmo processo; atenção ao nº do caderno. Só há a tabela por disciplina.
3. **R3**: arquivar ou manter os comentários sintéticos `TPS 20xx.md`?
4. **A2.4**: extrair 2016 (CESPE) para o banco?
5. **A3.3**: o que fazer com os 115 cartões existentes?
6. **A4.3**: Espanhol (ou Francês) diário entra no plano?
7. Confirma que P1 (`_Relatórios de Desempenho.md`) é o plano anterior a preservar?

---

## Apêndice A — Prova 2026, item a item (validado contra o espelho oficial)

Colunas: nº no **seu caderno (03)**; nº no **vault** (`TPS_2026_*`, caderno 01); disciplina (216/217 já corrigidos para DIR); sua marcação (B = branco); gabarito do caderno 03 (X = anulado); resultado (✓ acerto, ✗ erro, B branco, X anulado).

| item (cad. 03) | item (cad. 01 = vault) | disc. | minha | gabarito | resultado |
|--:|--:|---|---|---|---|
| 1 | 1 | LP | C | C | ✓ |
| 2 | 2 | LP | E | E | ✓ |
| 3 | 3 | LP | E | C | ✗ |
| 4 | 6 | LP | E | E | ✓ |
| 5 | 9 | LP | C | C | ✓ |
| 6 | 7 | LP | E | E | ✓ |
| 7 | 4 | LP | E | E | ✓ |
| 8 | 5 | LP | C | C | ✓ |
| 9 | 8 | LP | E | C | ✗ |
| 10 | 12 | LP | E | E | ✓ |
| 11 | 13 | LP | E | C | ✗ |
| 12 | 11 | LP | E | X | X |
| 13 | 10 | LP | C | C | ✓ |
| 14 | 14 | LP | E | E | ✓ |
| 15 | 15 | LP | B | E | B |
| 16 | 16 | LP | E | E | ✓ |
| 17 | 19 | LP | C | C | ✓ |
| 18 | 17 | LP | C | E | ✗ |
| 19 | 18 | LP | C | C | ✓ |
| 20 | 20 | LP | E | C | ✗ |
| 21 | 21 | LP | E | E | ✓ |
| 22 | 22 | LP | B | C | B |
| 23 | 23 | LP | E | E | ✓ |
| 24 | 29 | LP | C | C | ✓ |
| 25 | 30 | LP | E | C | ✗ |
| 26 | 24 | LP | C | C | ✓ |
| 27 | 25 | LP | E | C | ✗ |
| 28 | 27 | LP | E | E | ✓ |
| 29 | 26 | LP | E | E | ✓ |
| 30 | 28 | LP | C | E | ✗ |
| 31 | 31 | LP | E | C | ✗ |
| 32 | 32 | LP | E | E | ✓ |
| 33 | 35 | LP | E | E | ✓ |
| 34 | 34 | LP | C | C | ✓ |
| 35 | 33 | LP | E | E | ✓ |
| 36 | 36 | LP | C | C | ✓ |
| 37 | 37 | LP | C | X | X |
| 38 | 40 | LP | C | C | ✓ |
| 39 | 39 | LP | E | E | ✓ |
| 40 | 38 | LP | E | E | ✓ |
| 41 | 42 | HB | E | E | ✓ |
| 42 | 44 | HB | E | X | X |
| 43 | 45 | HB | C | C | ✓ |
| 44 | 41 | HB | E | E | ✓ |
| 45 | 43 | HB | C | C | ✓ |
| 46 | 48 | HB | C | X | X |
| 47 | 50 | HB | E | E | ✓ |
| 48 | 51 | HB | E | E | ✓ |
| 49 | 49 | HB | E | E | ✓ |
| 50 | 46 | HB | C | C | ✓ |
| 51 | 47 | HB | C | C | ✓ |
| 52 | 54 | HB | B | C | B |
| 53 | 53 | HB | E | E | ✓ |
| 54 | 52 | HB | E | E | ✓ |
| 55 | 55 | HB | C | C | ✓ |
| 56 | 58 | HB | C | X | X |
| 57 | 59 | HB | B | C | B |
| 58 | 57 | HB | E | E | ✓ |
| 59 | 60 | HB | C | C | ✓ |
| 60 | 56 | HB | C | E | ✗ |
| 61 | 62 | HB | B | E | B |
| 62 | 63 | HB | E | E | ✓ |
| 63 | 64 | HB | C | C | ✓ |
| 64 | 61 | HB | E | E | ✓ |
| 65 | 65 | HB | E | E | ✓ |
| 66 | 68 | HB | C | C | ✓ |
| 67 | 69 | HB | C | X | X |
| 68 | 70 | HB | E | C | ✗ |
| 69 | 67 | HB | E | E | ✓ |
| 70 | 66 | HB | C | E | ✗ |
| 71 | 73 | HM | E | E | ✓ |
| 72 | 72 | HM | C | C | ✓ |
| 73 | 76 | HM | E | E | ✓ |
| 74 | 71 | HM | E | E | ✓ |
| 75 | 75 | HM | E | C | ✗ |
| 76 | 74 | HM | E | E | ✓ |
| 77 | 82 | HM | E | C | ✗ |
| 78 | 83 | HM | C | C | ✓ |
| 79 | 77 | HM | E | C | ✗ |
| 80 | 80 | HM | E | C | ✗ |
| 81 | 81 | HM | E | E | ✓ |
| 82 | 78 | HM | C | X | X |
| 83 | 79 | HM | E | C | ✗ |
| 84 | 84 | HM | E | E | ✓ |
| 85 | 85 | HM | C | C | ✓ |
| 86 | 86 | HM | C | C | ✓ |
| 87 | 87 | HM | C | X | X |
| 88 | 88 | HM | C | C | ✓ |
| 89 | 89 | HM | C | E | ✗ |
| 90 | 91 | HM | E | E | ✓ |
| 91 | 90 | HM | C | C | ✓ |
| 92 | 92 | HM | E | E | ✓ |
| 93 | 93 | HM | C | E | ✗ |
| 94 | 94 | HM | B | C | B |
| 95 | 95 | HM | E | X | X |
| 96 | 98 | GEO | B | E | B |
| 97 | 97 | GEO | E | E | ✓ |
| 98 | 96 | GEO | C | C | ✓ |
| 99 | 100 | GEO | E | C | ✗ |
| 100 | 101 | GEO | C | C | ✓ |
| 101 | 99 | GEO | C | E | ✗ |
| 102 | 102 | GEO | C | E | ✗ |
| 103 | 103 | GEO | C | E | ✗ |
| 104 | 104 | GEO | C | C | ✓ |
| 105 | 105 | GEO | B | E | B |
| 106 | 108 | GEO | C | C | ✓ |
| 107 | 107 | GEO | C | C | ✓ |
| 108 | 106 | GEO | E | C | ✗ |
| 109 | 110 | GEO | C | X | X |
| 110 | 111 | GEO | C | C | ✓ |
| 111 | 109 | GEO | E | E | ✓ |
| 112 | 112 | GEO | C | E | ✗ |
| 113 | 115 | GEO | C | C | ✓ |
| 114 | 114 | GEO | E | E | ✓ |
| 115 | 113 | GEO | E | E | ✓ |
| 116 | 116 | GEO | C | C | ✓ |
| 117 | 117 | GEO | E | E | ✓ |
| 118 | 118 | GEO | B | E | B |
| 119 | 120 | GEO | C | C | ✓ |
| 120 | 119 | GEO | C | C | ✓ |
| 121 | 123 | ING | C | C | ✓ |
| 122 | 121 | ING | C | C | ✓ |
| 123 | 122 | ING | C | E | ✗ |
| 124 | 124 | ING | C | E | ✗ |
| 125 | 125 | ING | C | E | ✗ |
| 126 | 126 | ING | E | C | ✗ |
| 127 | 127 | ING | C | E | ✗ |
| 128 | 128 | ING | C | C | ✓ |
| 129 | 129 | ING | C | C | ✓ |
| 130 | 130 | ING | E | E | ✓ |
| 131 | 133 | ING | E | E | ✓ |
| 132 | 132 | ING | C | C | ✓ |
| 133 | 134 | ING | E | E | ✓ |
| 134 | 135 | ING | C | C | ✓ |
| 135 | 131 | ING | C | E | ✗ |
| 136 | 136 | ING | E | E | ✓ |
| 137 | 139 | ING | E | E | ✓ |
| 138 | 138 | ING | C | C | ✓ |
| 139 | 140 | ING | E | E | ✓ |
| 140 | 137 | ING | C | C | ✓ |
| 141 | 142 | ING | C | C | ✓ |
| 142 | 144 | ING | E | E | ✓ |
| 143 | 143 | ING | E | E | ✓ |
| 144 | 141 | ING | E | C | ✗ |
| 145 | 145 | ING | C | C | ✓ |
| 146 | 149 | ING | C | E | ✗ |
| 147 | 150 | ING | C | C | ✓ |
| 148 | 146 | ING | C | C | ✓ |
| 149 | 148 | ING | C | C | ✓ |
| 150 | 147 | ING | C | E | ✗ |
| 151 | 151 | PI | C | C | ✓ |
| 152 | 153 | PI | C | C | ✓ |
| 153 | 154 | PI | B | C | B |
| 154 | 152 | PI | C | C | ✓ |
| 155 | 157 | PI | B | C | B |
| 156 | 155 | PI | E | C | ✗ |
| 157 | 156 | PI | C | E | ✗ |
| 158 | 159 | PI | C | E | ✗ |
| 159 | 158 | PI | E | E | ✓ |
| 160 | 160 | PI | C | X | X |
| 161 | 161 | PI | E | E | ✓ |
| 162 | 164 | PI | E | E | ✓ |
| 163 | 163 | PI | E | E | ✓ |
| 164 | 162 | PI | C | X | X |
| 165 | 167 | PI | C | C | ✓ |
| 166 | 170 | PI | C | C | ✓ |
| 167 | 165 | PI | C | E | ✗ |
| 168 | 169 | PI | C | E | ✗ |
| 169 | 166 | PI | E | E | ✓ |
| 170 | 168 | PI | C | C | ✓ |
| 171 | 171 | PI | E | E | ✓ |
| 172 | 172 | PI | C | E | ✗ |
| 173 | 173 | PI | E | E | ✓ |
| 174 | 174 | PI | C | C | ✓ |
| 175 | 175 | PI | C | C | ✓ |
| 176 | 178 | PI | C | C | ✓ |
| 177 | 177 | PI | C | E | ✗ |
| 178 | 176 | PI | E | E | ✓ |
| 179 | 179 | PI | C | E | ✗ |
| 180 | 180 | PI | C | E | ✗ |
| 181 | 181 | PI | C | C | ✓ |
| 182 | 182 | PI | C | C | ✓ |
| 183 | 183 | PI | E | E | ✓ |
| 184 | 186 | PI | C | E | ✗ |
| 185 | 185 | PI | C | C | ✓ |
| 186 | 184 | PI | E | C | ✗ |
| 187 | 187 | PI | E | E | ✓ |
| 188 | 190 | PI | E | E | ✓ |
| 189 | 189 | PI | C | C | ✓ |
| 190 | 188 | PI | E | E | ✓ |
| 191 | 194 | ECO | E | C | ✗ |
| 192 | 195 | ECO | E | E | ✓ |
| 193 | 193 | ECO | E | C | ✗ |
| 194 | 192 | ECO | C | E | ✗ |
| 195 | 191 | ECO | E | C | ✗ |
| 196 | 196 | ECO | C | C | ✓ |
| 197 | 197 | ECO | E | E | ✓ |
| 198 | 198 | ECO | C | C | ✓ |
| 199 | 199 | ECO | E | C | ✗ |
| 200 | 200 | ECO | B | E | B |
| 201 | 201 | ECO | E | E | ✓ |
| 202 | 202 | ECO | E | E | ✓ |
| 203 | 204 | ECO | C | X | X |
| 204 | 207 | ECO | E | E | ✓ |
| 205 | 205 | ECO | C | C | ✓ |
| 206 | 203 | ECO | C | E | ✗ |
| 207 | 206 | ECO | B | C | B |
| 208 | 209 | ECO | C | C | ✓ |
| 209 | 211 | ECO | C | E | ✗ |
| 210 | 208 | ECO | B | E | B |
| 211 | 210 | ECO | C | C | ✓ |
| 212 | 213 | ECO | E | C | ✗ |
| 213 | 214 | ECO | E | E | ✓ |
| 214 | 212 | ECO | C | C | ✓ |
| 215 | 215 | ECO | E | E | ✓ |
| 216 | 216 | DIR | C | E | ✗ |
| 217 | 217 | DIR | C | C | ✓ |
| 218 | 218 | DIR | C | C | ✓ |
| 219 | 221 | DIR | C | C | ✓ |
| 220 | 222 | DIR | C | E | ✗ |
| 221 | 220 | DIR | C | C | ✓ |
| 222 | 219 | DIR | C | C | ✓ |
| 223 | 225 | DIR | E | C | ✗ |
| 224 | 224 | DIR | C | E | ✗ |
| 225 | 223 | DIR | E | E | ✓ |
| 226 | 227 | DIR | C | X | X |
| 227 | 228 | DIR | E | E | ✓ |
| 228 | 226 | DIR | E | E | ✓ |
| 229 | 230 | DIR | E | C | ✗ |
| 230 | 229 | DIR | E | E | ✓ |
| 231 | 232 | DIR | B | E | B |
| 232 | 231 | DIR | E | C | ✗ |
| 233 | 235 | DIR | C | E | ✗ |
| 234 | 234 | DIR | E | E | ✓ |
| 235 | 233 | DIR | C | C | ✓ |
| 236 | 236 | DIR | C | C | ✓ |
| 237 | 237 | DIR | C | E | ✗ |
| 238 | 238 | DIR | E | C | ✗ |
| 239 | 239 | DIR | E | E | ✓ |
| 240 | 240 | DIR | C | E | ✗ |


### Respostas recebidas em 21/09
- (1) `confianca`/`tipo_erro`/`armadilha`: **preenche ao refazer** → primeira carga só com id, resposta, gabarito e data.
- (2) 2025: **sem folhas de resposta** (só os cadernos) → sem carga item a item de 2025.
- (5) Cartões Anki existentes: **permanecem no deck `CACD 2027`**, intocados. Não haverá espelho dos cartões no vault (Regra 8); se um dia houver, usar `11 - FLASHCARDS & MAPAS MENTAIS/Decks Anki/`.
- (6) Espanhol **≥ 2×/semana**; Inglês **≥ 2×/semana** como sessão dedicada (a micro-prática diária de idioma do bloco 1 continua, conforme a missão).
- Pendentes: (3) R3, (4) A2.4, (7) P1, e a aprovação de A1.1–A4.3.

*Dados intermediários (hashes, listas, scripts de verificação) ficaram no scratchpad da sessão e não foram gravados no vault.*
