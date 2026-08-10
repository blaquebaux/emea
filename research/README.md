# Blaque Baux EMEA — research

First-pass Path-A research on **Europe / Middle East / Africa via US-listed country ETFs.** The
three regional sleeves (EMEA / APAC / LATAM) are one research object — regional exposure bought
through US wrappers — so they share this module and its two sketches; this repo frames the joint
result from EMEA. All sketches read Alpaca SIP daily bars (2016–2026), are read-only, print results.

EMEA universe (11): `EWG EWU EWQ EWI EWP EWL EWD EWN` (Europe) + `EIS` (Israel) + `EZA` (S. Africa) + `TUR` (Turkey).

```bash
export $(grep -v '^#' ~/.config/blaquebaux/alpaca.env | xargs)   # or source it
python research/emea_1_beta_and_fx.py   # is EMEA just US beta + FX drag?
python research/emea_2_rotation.py       # does country / region rotation beat buy-and-hold?
```

## Scorecard

| # | Question | Result | Verdict |
|---|----------|--------|---------|
| 1 | Is EMEA a distinct exposure or US beta? | 11 ETFs → **1.8 bets**, corr-SPY 0.82, beta 0.90; +0.61/+10%/−40% vs SPY +0.88/+15%/−34% | ❌ US beta wearing a flag |
| 1 | What does the unhedged FX cost? | Europe EZU +169% vs hedged HEDJ +182% (−13%); basket corr to dollar **−0.38** | ⚠️ real, uncompensated drag |
| 2 | Does country rotation add alpha? | long-RS +0.61 = EW-hold +0.61; long-short **−0.23** | ❌ no — no dispersion pulse |
| 2 | Does cross-region rotation beat SPY? | 3-region trend-rotate +0.60 < EW-3 +0.65 < SPY +0.88 | ❌ no |

## The synthesis

- **EMEA is US beta wearing a flag — the starkest case in the family.** Eleven country ETFs spanning
  Germany to South Africa to Turkey collapse to just **1.8 effective bets** (corr-SPY 0.82, beta 0.90).
  The basket returns +0.61 Sharpe / +10% CAGR / −40% drawdown — strictly worse than simply holding
  SPY (+0.88 / +15% / −34%). You take on extra idiosyncratic and political risk (Turkey, South Africa)
  for *less* return and *deeper* drawdowns.

- **The US-wrapper FX drag is real and uncompensated.** EMEA is the most dollar-sensitive region
  (basket correlation to UUP **−0.38**); over the sample hedged Europe (HEDJ) beat unhedged (EZU) by
  ~13 points — mild next to Japan's −229% (see APAC), but the same tax. Bought unhedged through a US
  ETF, you are making a short-dollar bet you never chose.

- **Rotation is not a strategy here.** Within-EMEA relative strength ties buy-and-hold (long-RS +0.61 =
  EW-hold +0.61) and the long-short is **negative** (−0.23) — Europe's countries move together, there
  is no dispersion to harvest. Cross-region trend rotation (+0.60) also fails to beat SPY (+0.88).

**Verdict:** a **null** as a standalone sleeve. EMEA is concentrated US beta plus a currency tax plus
political tail risk, with no rotation edge. Its only honest role is as a **currency-hedged input to a
global relative-strength book** — and on that measure APAC, not EMEA, is the better candidate. The
result points back to the spine: the US risk premium led the whole sample; geography within equities
is just more beta (the geographic cousin of Blurred's "diversify across asset classes, not names").

## Files
- `_emea_common.py` — shared helpers + all three regional universes + benchmarks/FX pairs.
- `emea_1_beta_and_fx.py` — regional beta (all 3 regions vs SPY) + the hedged-vs-unhedged FX drag.
- `emea_2_rotation.py` — within-region country momentum + pooled & cross-region rotation vs SPY.
