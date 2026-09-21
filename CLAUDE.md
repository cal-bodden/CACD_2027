# CACD 2027 — convenções do sistema de estudo

Vault Obsidian de preparação para o CACD 2027 (1ª fase Cebraspe, certo/errado, +1/−0,25). Trabalhe em **português do Brasil**.
O método é **estudo por questões**: o item de prova é a unidade; teoria só puxada por erro. Este arquivo vale para qualquer sessão (CLI ou Claudian).

## Mapa
| Caminho | O que é |
|---|---|
| `_sistema/itens.jsonl` | banco de itens **autênticos** (2016, 2017–2020, 2022–2026; 2.752 itens). Gerado por `_sistema/_build/construir_banco.py` — não editar à mão |
| `_sistema/erros.jsonl` | registro de erros/brancos/acertos inseguros com classificação (`tipo_erro`, `armadilha`, `proposicao`, `distorcao`, `anki_note_id`) |
| `_sistema/respostas.jsonl` | todas as respostas dadas em `sessao` (id_item, resposta, confiança, gabarito) |
| `_sistema/respostas_2026.tsv` | prova real de 2026 item a item (caderno 03 do candidato ↔ caderno 01 do vault) |
| `_sistema/PLANO.md` | plano operacional com tarefas (plugin Tasks). Estrutura só muda na revisão mensal |
| `_sistema/DIAGNOSTICO.md` | diagnóstico da Fase 0 (inventário, redundâncias, decisões) |
| `_sistema/scripts/` | `sessao`, `registrar`, `relatorio` (Python 3, sem dependências) |
| `_sistema/prioridades.json` | (opcional) pesos por disciplina usados por `sessao`; padrão no próprio script |
| `00 - GESTÃO & METADADOS/04 - Provas Anteriores/TPS_AAAA_turno.md` | corpus-fonte dos itens (frontmatter `origem: autentico`) |
| `…/Comentarios_IA_AAAA.md` | justificativas geradas por IA (`origem: comentario`) — só explicação, **nunca** gabarito nem estatística |
| `00 - GESTÃO & METADADOS/05 - Relatórios de Desempenho/_Relatórios de Desempenho.md` | fonte de dados e restrições do plano (P1): metas, checkpoints, compromissos, "o que não fazer" |
| `01`–`09 - …/` | notas de conteúdo por disciplina, na árvore do edital. **Conteúdo intocável** salvo pedido explícito |
| `13 - DOSSIÊS DE PROVA/` | dossiês por tópico (método anterior); fonte para o bloco de produção |
| `_arquivo/` + `LOG.md` | tudo que foi retirado de circulação (Regra 2). Idem em `~/Documents/CACD_Outros/_arquivo/` |
| `~/Documents/CACD_Outros/` | MATERIAIS: PDFs, provas oficiais (`00_Guias_Editais/Provas_CACD/`), livros. Fora do git |

## Regras invioláveis
1. **Nada é apagado.** Redundância vai para `_arquivo/` da mesma raiz, com linha em `_arquivo/LOG.md` (data, origem, destino, motivo). No Anki: suspender ou tag `revisar-remocao`, nunca deletar.
2. **Notas de conteúdo não se editam, movem nem fundem** sem pedido explícito. Pode-se renomear arquivos e alterar frontmatter (metadados).
3. **Autêntico ≠ sintético.** Todo item/cartão carrega `origem` (`autentico` | `sintetico` | `comentario`). Estatísticas usam **só** `autentico`. Gabarito válido é **só o oficial** (PDF do Cebraspe/IADES em MATERIAIS).
4. Não implementar repetição espaçada própria: o Anki/FSRS cuida.
5. Cartões nascem **só** de erros e de acertos com dúvida/chute, via `registrar`; contêm a proposição correta e a distorção, não o enunciado literal. Deck `CACD::Erros`, tipo `CACD-Proposicao` (Proposicao, Armadilha, Fonte, Origem, Disciplina, Topico), tags `disciplina::X topico::Y armadilha::Z tipo::T`. Checar duplicata com `canAddNotes` antes de inserir.
6. Não ler PDFs inteiros: inventário por nome/tamanho/sha256; extrair só páginas iniciais para classificar. Exceção já feita: cadernos de prova (extração de itens).
7. Não tocar em `~/.local/state/quickshell/user/todo.json`.
8. Elegância não é objetivo. Se não for usado diariamente, não construir. Mudança estrutural só na revisão mensal, com dados.
9. Git: `.gitignore` exclui PDF/EPUB/ZIP/GIF, imagens grandes, `.obsidian/workspace*`, plugins. Commits ocasionais; MATERIAIS fora do git.

## Convenções de dados
- `id` do item: `AAAA-M|T-NNN` (Cebraspe 2025+, numeração corrida) ou `AAAA-M|T-Qnn-k` (formato questão × 4 itens). Campo `anulado` (bool) e `gabarito_verificado`; 2026 tem `item_caderno_03`.
- `topico_edital` = id do Anexo III (`edital_itens.csv`); `topico_incerto: true` quando o classificador (`lexico.py`) não teve confiança alta — não adivinhar.
- Correções conhecidas: itens 216 e 217 de 2026 são Direito (`disciplina_original: Economia`). Questão 1 (manhã) e 35 (tarde) de 2017–2020 não estão no corpus.
- `tipo_erro`: lacuna_conteudo | armadilha_logica | leitura | gestao_risco. `armadilha`: negacao_sutil | atribuicao_errada | anacronismo | falsa_exclusividade | inversao_causal | quantificador_universal | extrapolacao | outra. `confianca`: certeza | duvida | chute.
- Tarefas (plugin Tasks): `- [ ] descrição 🔁 every weekday 📅 AAAA-MM-DD`, em `_sistema/PLANO.md`.

## Operação diária
```
_sistema/scripts/sessao -d LP,ING -n 12     # bloco 1 (com Anki antes)
_sistema/scripts/sessao -n 30               # bloco 2: bateria intercalada, sem gabarito até o fim
_sistema/scripts/registrar                  # classifica erros/inseguros → cartão no Anki
_sistema/scripts/relatorio [--salvar]       # domingo e revisão mensal
```
Reconstruir o banco (após editar TPS_*.md ou lexico.py): `python3 _sistema/_build/construir_banco.py --gab <txt dos gabaritos> --mapa2026 … --folha2026 … --extra _sistema/_build/itens_2016.jsonl`.

## Ao assumir uma sessão nova
1. Ler `_sistema/PLANO.md` (§0 Hoje) e, se pedido, rodar `relatorio`.
2. Nunca gerar cartões em massa, nem "resumos" de notas, nem novas notas de conteúdo sem pedido.
3. Se o AnkiConnect (`localhost:8765`) não responder ou o plugin Tasks estiver desativado, avisar antes de continuar.
4. Ao propor mudança de método, mostrar a métrica do `relatorio` que a justifica.
