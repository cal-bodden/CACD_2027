---
title: "Probabilidade e Variáveis Aleatórias"
area: "BACEN — Economia e Finanças"
disciplina: "Estatística e Econometria"
topico: "1 e 2 — Distribuições, esperança, momentos, esperança condicional e Lei dos Grandes Números"
banca: Cebraspe
tags: [bacen, p2, estatistica, probabilidade, distribuicoes, momentos, lgn]
aliases: ["Probabilidade", "Variáveis aleatórias", "Distribuição normal", "Distribuição binomial", "Momentos", "Lei dos grandes números"]
fonte: "Gran Concursos — Estatística (Probabilidades; Momentos de V.A.; Distribuição Normal e Binomial; Intervalos de Confiança), prof. Thiago Cardoso"
status: 🟡
---

# Probabilidade e Variáveis Aleatórias (Edital — Estatística, 1 e 2)

> [!info] De onde vem esta nota
> Baseada **exclusivamente** no material do **Gran** (Estatística, prof. Thiago Cardoso). Cobre os tópicos **1** (distribuições, esperança, momentos, esperança condicional) e **2** (Lei dos Grandes Números) do edital.

---

## Probabilidade — conceitos

**Conceito clássico** (eventos equiprováveis): $P = \dfrac{\text{casos favoráveis}}{\text{casos possíveis}}$.

**Axiomas de Kolmogorov:**
1. $P(A) \ge 0$ — probabilidade é número real não negativo;
2. $P(\Omega) = 1$ — probabilidade do espaço amostral é 1;
3. $P(A \cup B) = P(A) + P(B)$ **quando** $A \cap B = \varnothing$ (eventos mutuamente exclusivos).

- **União geral**: $P(A\cup B) = P(A) + P(B) - P(A\cap B)$ (operador **OU**).
- **Eventos mutuamente exclusivos**: interseção nula → não ocorrem juntos.

### Probabilidade condicional e independência
$$P(A\mid B) = \frac{P(A\cap B)}{P(B)}$$
- **Independência**: $P(A\cap B) = P(A)\cdot P(B)$ (o operador **E** corresponde à interseção).

---

## Variáveis aleatórias: esperança, variância, momentos

- **Esperança** $E(X)$ — valor médio (operador **linear**: $E(aX+b)=aE(X)+b$).
- **Variância** $Var(X)=E[(X-E(X))^2]$; **desvio padrão** $=\sqrt{Var(X)}$.
- **Momentos** — generalizam média/variância; a **Função Geradora de Momentos (FGM)** permite obtê-los por derivação.
- **Esperança condicional** $E(X\mid Y)$ — valor esperado de X dado Y.

## Principais distribuições

| Distribuição | Quando | Parâmetros | E(X) / Var(X) |
|---|---|---|---|
| **Bernoulli** | 1 ensaio com 2 resultados (sucesso/fracasso) | $p$ | $p$ / $p(1-p)$ |
| **Binomial** | $n$ ensaios de Bernoulli independentes | $n, p$ | $np$ / $np(1-p)$ |
| **Normal** | contínua, simétrica em torno da média | $\mu, \sigma^2$ | $\mu$ / $\sigma^2$ |

> [!tip] Normal padrão (Z)
> $Z=\frac{X-\mu}{\sigma}$. Regra prática: $P(Z<1)\approx 0{,}84$; a curva é simétrica e a área total = 1.

---

## Lei dos Grandes Números (LGN)

À medida que o número de repetições cresce, a **frequência relativa / média amostral converge para a probabilidade / média populacional**.
- **Lei fraca** — convergência **em probabilidade**.
- **Lei forte** — convergência **quase certa** (mais forte).

É a base que justifica usar a média amostral como estimador da média populacional (ver [[_02 Inferência Estatística#Teorema do Limite Central|TLC]]).

---

## Como a banca cobra (Cespe/Cebraspe)

> [!question] Probabilidade clássica — *CESPE/Ministério da Economia 2020*
> "Foram analisados 30 processos no dia; a probabilidade de um processo específico ter sido **o primeiro** a ser analisado é **superior a 1/10**."
> **Gabarito: ERRADO.** *(1/30 < 1/10 — quanto maior o denominador, menor a fração.)*

> [!question] Estimador de máxima verossimilhança — *CESPE/TCE-PA 2016*
> "Para a amostra A = {2, 3, 0, 1}, a estimativa de **máxima verossimilhança** para a variância populacional será igual a 5/3."
> **Gabarito: ERRADO.** *(A EMV da variância usa divisor n — não faz a correção de ajuste (n−1).)*

## Conexões
- [[_02 Inferência Estatística]] · [[_03 Regressão]]
- [[13 - BACEN, TCU/TCU/_INDEX|Estatística e Econometria — índice]]
