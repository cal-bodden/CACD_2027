---
title: PLANO — CACD 2027
tags: [cacd-2027, sistema, plano]
status: PROPOSTA (vira PLANO.md após aprovação)
fonte_de_dados: "[[_Relatórios de Desempenho]] § Plano CACD 2027 (P1)"
orcamento: ~24 h/semana · domingo livre · blocos curtos antes do trabalho
---

# PLANO — CACD 2027

> Princípio geral: **o item de prova é a unidade de estudo**. Teoria só entra puxada por erro ou onde falta arcabouço (§5).
> Nada de releitura ou grifo como atividade. Cada componente abaixo diz **por que** existe (princípio) e **como se verifica** (métrica do `relatorio`).

## 0. Hoje

```tasks
not done
due before tomorrow
path includes _sistema/PLANO
short mode
```

## 1. Rotina diária (seg–sex) — 3 blocos em ordem fixa · ~2h50

| Bloco | Quando | Duração | O que | Comando | Princípio | Métrica (`relatorio`) |
|---|---|---:|---|---|---|---|
| **1** | antes do trabalho | 35 min | Anki `CACD::Erros` (até 15 min) + micro-prática de idioma: 12 itens LP/ING | `sessao -d LP,ING -n 12` | espaçamento (FSRS) · recuperação | cartões vencidos = 0 ao fim do bloco; erro/marcados LP e ING (30 d) |
| **2** | noite | 90 min | bateria intercalada de 30 itens (ponderada por prioridade × erro × tempo sem contato) + classificação dos erros e cartões | `sessao -n 30` → `registrar` | intercalação · recuperação · feedback elaborativo · calibração | erro/marcados por disciplina; calibração por confiança; saldo real vs. sem chutes; 0 erros sem classificar |
| **3** | noite | 35 min | produção: 1 parágrafo discursivo (15–20 linhas) sobre o tópico do erro mais caro do dia, **ou** nota-base (§5) | escrever em `10 - SIMULADOS & EXERCÍCIOS/2ª Fase - Discursivas/AAAA-MM-DD.md` | efeito de geração | nº de parágrafos/semana (meta 4) — checklist abaixo |

- [ ] Bloco 1 — Anki + 12 itens LP/ING 🔁 every weekday 📅 2026-09-22
- [ ] Bloco 2 — `sessao -n 30` + `registrar` 🔁 every weekday 📅 2026-09-22
- [ ] Bloco 3 — parágrafo discursivo ou nota-base 🔁 every weekday 📅 2026-09-22
- [ ] Espanhol 30 min (resumo ou versão PT→ES com correção por padrão de resposta) 🔁 every tuesday, thursday 📅 2026-09-22
- [ ] Inglês 2ª fase 30 min (versão PT→EN ou redação; 2× semana além do bloco 1) 🔁 every monday, wednesday 📅 2026-09-23

## 2. Sábado — ~6h

| Hora | O que | Comando | Princípio | Métrica |
|---|---|---|---|---|
| 2h | bateria longa em ritmo de prova (60 itens, 2 min/item) + `registrar` | `sessao -n 60` | recuperação sob pressão de tempo · calibração | erro/marcados e brancos da bateria vs. média semanal |
| 1h30 | **até dez/2026:** 2 questões discursivas de provas anteriores (MATERIAIS `Demais_Fases`), corrigidas pelo padrão de resposta · **a partir de jan/2027:** 1 prova discursiva completa corrigida por terceiro | — | efeito de geração | discursivas corrigidas acumuladas (meta: 12 até mar/2027) |
| 1h | revisão dos erros da semana: reler as *proposições* que você escreveu (`erros.jsonl`), não as notas | `relatorio` §1 | feedback elaborativo | erros da semana reclassificados = 0 |
| 1h | nota-base (§5) ou Espanhol/Inglês 2ª fase | — | — | — |

- [ ] Sábado — bateria de 60 + registrar 🔁 every saturday 📅 2026-09-26
- [ ] Sábado — 2 discursivas de prova anterior com padrão de resposta 🔁 every saturday 📅 2026-09-26
- [ ] Sábado — 1 discursiva completa corrigida por terceiro 🔁 every saturday 📅 2027-01-09
- [ ] Sábado — releitura das proposições da semana (erros.jsonl) 🔁 every saturday 📅 2026-09-26

## 3. Domingo — livre (10 min de relatório)

- [ ] `relatorio --salvar` e ler: o que mudou, qual disciplina entra em foco na semana 🔁 every sunday 📅 2026-09-27

## 4. Mensal

- [ ] Simulado completo (uma edição inteira em 2 blocos de 120 itens, cronometrado: 2016 → 2020 → 2022 → 2023 → 2024) + `registrar` 🔁 every month on the first saturday 📅 2026-10-03
- [ ] Revisão do método: ler `relatorio`, ajustar `prioridades.json` e este plano com base em dados 🔁 every month on the last sunday 📅 2026-09-27

## 5. Notas-base (única teoria "antes das questões") — bloco 3 / sábado, até 31/10/2026

Só onde o diagnóstico mostrou falta de arcabouço; cada uma termina em **10 proposições C/E escritas por você** (viram cartões via `registrar` só se errar depois).

- [ ] GEO-1 pensamento geográfico (Cresswell + notas `06 - GEOGRAFIA/01`) → 10 proposições 📅 2026-10-03
- [ ] GEO-6 geopolítica clássica (Mahan, Mackinder, Spykman, Haushofer, Ratzel) → 10 proposições 📅 2026-10-10
- [ ] ECO-1.2 microeconomia da firma (custos, maximização, estruturas de mercado — Varian) → 10 proposições 📅 2026-10-17
- [ ] ECO-3 / PI-15 estágios da integração econômica (Balassa; MERCOSUL como caso) → 10 proposições 📅 2026-10-24

## 6. Calendário e checkpoints (preservados de P1)

| Período | Foco | Entregável verificável |
|---|---|---|
| set–out 2026 | rotina estabilizada + notas-base | 4 semanas seguidas com blocos 1–2 ≥ 90 % dos dias úteis (`relatorio` §4) |
| nov 2026 | Direito por itens (DIR = 3 na prioridade) + Economia manutenção | erro/marcados DIR < 30 % nas sessões |
| **dez 2026 — CHECKPOINT 1** | simulado completo | **LP e ING ≤ 15 % erro/marcados** |
| jan–fev 2027 | discursivas semanais corrigidas | 8 discursivas |
| **mar 2027 — CHECKPOINT 2** | | **12+ discursivas corrigidas acumuladas** |
| abr–mai 2027 | Economia formalizada + simulados | simulado mensal com classificação |
| jun–jul 2027 | intensificação das discursivas | 3–4/semana |
| ago 2027 | só erros próprios | zero conteúdo novo nas 3 últimas semanas |

- [ ] CHECKPOINT 1 — simulado completo: LP e ING ≤ 15 % erro/marcados 📅 2026-12-12
- [ ] CHECKPOINT 2 — 12 discursivas corrigidas acumuladas 📅 2027-03-27

## 7. Metas 2027 e aritmética (preservadas de P1)

| Disciplina | Erro/marcados 2025 | 2026 | **Meta 2027** | Prioridade no `sessao` |
|---|--:|--:|--:|--:|
| Português | 22,5 % | 23,7 % | 12 % | 3 |
| Inglês | 28,0 % | 30,0 % | 15 % | 3 |
| Direito | 20,0 % | 41,7 % | 12 % | 3 |
| Geografia | 23,8 % | 27,3 % | 14 % | 2,5 |
| Economia | 16,0 % | 36,4 % | 14 % | 2 |
| Política Internacional | 13,2 % | 28,9 % | 8 % | 2 |
| História Mundial | 20,0 % | 29,2 % | 12 % | 1,5 |
| História do Brasil | 25,9 % | 11,1 % | manter 11 % | 1 |

Aritmética até a aprovação (P1 §2): 22 erros evitados = **+30,5 pontos** → projeção ~186. Contribuições: Port +6,25 · Ing +5,00 · HB manter +5,00 · Eco +4,25 (1 erro + 3 brancos) · Dir/Geo/HM/PI +2,50 cada.

## 8. Compromissos não negociáveis

| # | Compromisso | Início | Verificação |
|---|---|---|---|
| 1 | Espanhol **≥ 2×/semana**, 30 min (alterado de "diário", decisão de 21/09/2026) | imediato | checklist §1 |
| 2 | Português e Inglês como estudo técnico (itens diários, bloco 1) | imediato | ≤ 15 % erro/marcados no simulado de dez/2026 |
| 3 | 1 discursiva/semana corrigida por terceiro | jan/2027 | 12 corrigidas até mar/2027 |
| 4 | Simulado completo mensal com classificação de erros | out/2026 | 1/mês, `registrar` zerado |

## 9. O que NÃO fazer (preservado de P1)

| Item | Motivo |
|---|---|
| Cobrir o edital inteiro | cobertura total não converte em pontos (5 anos de evidência) |
| Criar notas novas por sistematização | o vault já tem conteúdo; falta ativação |
| Estudar História do Brasil além de manutenção | já em 11 % de erro |
| Pedir licença antes de dez/2026 | sem evidência de que o método funciona |
| Abrir frente nova de concurso durante o ciclo | foi o que produziu 2026 |
| Reler/grifar notas como "estudo" | não é recuperação; só puxado por erro |

## 10. Orçamento

| | h/semana |
|---|--:|
| Blocos 1–3, seg–sex (2h50 × 5) | 14,2 |
| Espanhol 2 × 30 min + Inglês 2ª fase 2 × 30 min | 2,0 |
| Sábado | 6,0 |
| Domingo (relatório) | 0,2 |
| **Total** | **22,4** (folga de ~1,5 h no teto de 24 h) |

## 11. Como o método se corrige a si mesmo

`sessao` pesa cada disciplina por **prioridade × taxa de erro (60 d) × dias sem contato**; portanto, uma disciplina que melhora sai de foco sozinha e uma que decai volta. Os pesos aparecem no cabeçalho de cada sessão. Mudanças estruturais (blocos, metas, prioridades) só na revisão mensal (§4), com o `relatorio` na mão.
