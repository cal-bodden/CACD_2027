---
title: Cobertura do Edital — Diagnóstico
area: Edital e Documentos Oficiais
subarea: GESTÃO & METADADOS
tags:
  - cacd-2027
  - edital
  - diagnostico
  - cobertura
atualizado: 2026-08-22
---

# Cobertura do Edital — Diagnóstico

Cruzamento automático entre os **364 itens** do Anexo III do edital e as **482 notas** das oito pastas de disciplina do vault. Fonte de dados: [[_dados/cobertura_edital.csv]].

---

## 1. O quadro geral

O vault **não tem problema de volume**: são ~15 MB de notas e apenas **1 item do edital sem nota alguma**. O problema é de **alocação**. Compare o esforço já investido com o peso de cada disciplina na nota final (que, lembrando, é só a 2ª fase — ver [[Mapa Mestre da Prova — CACD]]):

| Disciplina | Notas | Volume | Pontos na 2ª fase | KB por ponto |
|---|---:|---:|---:|---:|
| Política Internacional | 145 | 4.334 KB | 100 | 43 |
| História do Brasil | 83 | 2.715 KB | 100 | 27 |
| **História Mundial** | 89 | **2.475 KB** | **0** | **∞** |
| Economia | 65 | 2.096 KB | 100 | 21 |
| Direito | 47 | 1.985 KB | 100 | 20 |
| Geografia | 31 | 1.154 KB | 100 | 12 |
| Língua Portuguesa | 11 | 436 KB | 100 | 4 |
| **Língua Inglesa** | 6 | **19 KB** | 100 | **0,2** |
| **Espanhol / Francês** | 5 | **~0 KB** | 100 | **0** |

> [!warning] A distorção central
> **25% da nota final** (Inglês 2ª fase + idioma adicional = 200 de 800 pontos) está apoiada em **menos de 20 KB** de material — cerca de **0,1%** do vault.
> Ao mesmo tempo, **História Mundial**, que vale **zero** na classificação, concentra 2,5 MB — o segundo maior acervo do vault.
>
> Isso não significa abandonar História Mundial: ela ainda é a porta da 1ª fase. Significa que ela já está **pronta** e não deve receber mais horas de produção de nota.

---

## 2. Cobertura por disciplina

Contagem sobre todos os níveis do edital (🟩 consolidado ≥20 KB · 🟨 parcial 4–20 KB · 🟧 esboço <4 KB · ↳ coberto na nota do item-pai · 🟥 ausente):

| Disciplina | Itens | 🟩 | 🟨 | 🟧 | ↳ | 🟥 |
|---|---:|---:|---:|---:|---:|---:|
| Língua Portuguesa | 11 | 8 | 2 | 1 | 0 | 0 |
| Língua Inglesa | 4 | 0 | 2 | 2 | 0 | 0 |
| História do Brasil | 62 | 54 | 7 | 1 | 0 | 0 |
| História Mundial | 67 | 58 | 8 | 0 | 0 | 1 |
| Política Internacional | 42 | 32 | 2 | 0 | 8 | 0 |
| Geografia | 30 | 28 | 2 | 0 | 0 | 0 |
| Economia | 109 | 26 | 1 | 1 | 80 | 1 |
| Direito | 35 | 20 | 12 | 3 | 0 | 0 |
| Espanhol | 2 | 0 | 0 | 2 | 0 | 0 |
| Francês | 2 | 0 | 0 | 2 | 0 | 0 |

> [!note] Sobre os 80 itens "↳" de Economia e os 8 de PI
> Não são lacunas. O vault agrupa vários sub-itens do edital numa única pasta — por exemplo, `ECO-1.1.1` a `ECO-1.1.4` moram todos em `1.1 - Demanda do Consumidor (Preferências, Equilíbrio, Curva, Elasticidade)`, e `PI-3.1` a `PI-3.4` em `03 - Brasil e América do Sul`. O conteúdo existe; só não há pasta por sub-item.

---

## 3. As 14 lacunas reais

Itens do edital com nota ausente ou praticamente vazia, **ordenados por retorno**:

### 🔴 Prioridade 1 — vale 200 pontos e está zerado

| Item | Título | Estado |
|---|---|---|
| `ESP-1` / `ESP-2` | Resumo em espanhol (50 pts) · Versão PT→ES (50 pts) | 🟧 ~700 bytes no total |
| `FRA-1` / `FRA-2` | Resumo em francês (50 pts) · Versão PT→FR (50 pts) | 🟧 ~360 bytes no total |
| `ING-2F-1` | Redação em inglês, 65–70 linhas (70 pts) | 🟧 182 bytes |
| `ING-2F-2` | **Versão PT→EN**, 20–40 linhas (30 pts) | 🟧 191 bytes |

**Decisão pendente:** o edital exige escolher **espanhol *ou* francês**. Hoje o vault mantém as duas pastas vazias em paralelo. Escolher uma e concentrar nela é a maior alavanca isolada disponível.

> [!danger] `ING-2F-2` está com a nomenclatura errada
> A pasta chama-se `3 - Tradução (conforme Anexo III do Edital)`, mas desde o edital 2026 o exercício é **versão PT→EN**, não tradução EN→PT. Há ainda uma pasta `2 - Resumo (conforme Tabela 6.2 do Edital)` que **não corresponde a nenhum exercício** da prova de inglês. Ver [[Mudanças do Edital 2025 → 2026]].

### 🟠 Prioridade 2 — Direito, disciplina discursiva mais rasa

Direito vale 100 pontos na 2ª fase e tem **35 itens de edital** — a maior granularidade de todas. É a disciplina com mais itens em 🟨/🟧 (15 de 35):

| Item | Título | KB |
|---|---|---:|
| `DIR-5` | Estado democrático de direito. Conceito e objetivos. Divisão de poderes | 0,2 |
| `DIR-19` | Território. Formação do território brasileiro | 0,3 |
| `DIR-26` | Direito da Integração Regional. MERCOSUL. Órgão de Solução de Controvérsias | 0,3 |
| `DIR-4` | Estado: elementos, soberania, formas, competências, sistemas de governo | 5,2 |
| `DIR-2` | Personalidade jurídica | 6,4 |
| `DIR-8` | Direitos e garantias fundamentais no ordenamento jurídico brasileiro | 6,2 |
| `DIR-3` | Constituição: conceito, classificações, primado, controle de constitucionalidade | 9,7 |
| `DIR-1` | Normas jurídicas | 10,2 |
| `DIR-9` | Administração Pública no Brasil | 11,0 |
| `DIR-10` | Licitações e contratos administrativos | 11,0 |
| `DIR-13` | Regime Jurídico dos Servidores do Serviço Exterior (Lei 11.440/2006) | 12,2 |
| `DIR-14` | Finanças públicas. Normas orçamentárias | 12,4 |
| `DIR-15` | Direito Internacional. DIP e Direito Interno | 13,3 |
| `DIR-12` | Direitos, deveres e responsabilidades do servidor público. Improbidade | 13,4 |
| `DIR-17` | DIP e direito internacional privado (LINDB) | 17,7 |

`DIR-26` (MERCOSUL) é especialmente crítico: é ponto de cruzamento com `PI-3.2` e cai nas duas fases.

### 🟡 Prioridade 3 — pontuais

| Item | Título | Estado |
|---|---|---|
| `ECO-5` | Bancos digitais, meios de pagamento, "dinheiro de plástico" → "dinheiro digital" | 🟥 **sem nota** |
| `HM-8` | Relações internacionais no séc. XXI: paradigmas digitais, redes sociais | 🟥 **sem nota** (pasta existe, vazia) |
| `LP-2.1` | Compreensão, interpretação e análise crítica de textos | 🟧 281 bytes |
| `HB-10.6` | Manifestações culturais | 🟧 236 bytes |
| `ECO-4.3.1` | Modelo de Industrialização por Substituição de Importações (ISI) | 🟧 |

> [!tip] `ECO-5`, `HM-8` e `HB-11` formam o eixo "agenda digital" do programa
> São os três itens que o edital dedica às transformações digitais: `ECO-5` (dinheiro digital), `HM-8` (RI no século XXI) e `HB-11` (impactos tecnológicos no Brasil). Apenas `HB-11` está pronto (37,9 KB) — os outros dois estão em **zero**, e são os únicos itens de **nível 1** de todo o programa sem uma única nota. `ECO-5` é um dos cinco grandes blocos de Economia.

---

## 4. Lacunas fora do conteúdo programático

Coisas que o edital não numera, mas que a prova exige:

- **Provas discursivas anteriores: não existem no vault.** A pasta `10 - SIMULADOS & EXERCÍCIOS/2ª Fase - Discursivas/` tem 46 bytes. Estão catalogadas 16 provas objetivas (568 itens, ver [[RELATORIO]]) e **nenhuma** prova escrita. Como a 2ª fase é 100% da nota final, é a assimetria mais séria do acervo.
- **Metadados desatualizados:** 436 notas ainda carregam a tag `cacd-2025`.
- **Cruzamentos de baixa qualidade:** os arquivos em `04 - Provas Anteriores/Cruzamentos/` casam itens de prova majoritariamente com **outras provas**, não com notas de estudo (scores de 0,08 a 0,23 — ruído). O sinal é fraco demais para orientar estudo.

---

## 5. Notas relacionadas
- [[Mapa Mestre da Prova — CACD]] — arquitetura e pontuação das duas fases
- [[Conteúdo Programático — íntegra oficial]] — os 364 itens, item a item
- [[Mudanças do Edital 2025 → 2026]]
- [[_Relatórios de Desempenho]] — desempenho por disciplina
