# Blaque Baux EMEA

**Europe, the Middle East, and Africa.**

EMEA is a member of the Blaque Baux family. The [core repo](https://github.com/Carter-Warrens/blaquebaux)
is the **engine and blueprint** — a governed, systematic platform (Julia) with a venue-agnostic
execution controller and a Layer-3 live-money safety gate. EMEA points that engine in its own
direction and inherits the governance wholesale.

> **Not investment advice.** Educational/research software. Nothing here is validated. See [LICENSE](LICENSE).

```bash
git clone --recursive https://github.com/Carter-Warrens/blaquebaux-emea.git
julia --project=engine -e 'using Pkg; Pkg.instantiate()'   # one-time engine setup
```

## The thesis

Regional exposure via US-listed ETFs and ADRs (VGK, EZU, EWG, EWU, EIS, EZA and peers) — a macro / regional-rotation sleeve. Caveat: traded through US-listed wrappers, so it inherits US-hours pricing and embedded FX.

## Research — first pass done

Full detail in [`research/README.md`](research/README.md). The scorecard:

| # | Question | Verdict |
|---|----------|---------|
| 1 | Distinct exposure or US beta? | ❌ US beta wearing a flag — 11 ETFs → **1.8 bets**, corr-SPY 0.82; +0.61/+10%/−40% vs SPY +0.88/+15%/−34% |
| 1 | What does the unhedged FX cost? | ⚠️ real drag — Europe hedged HEDJ beat unhedged EZU by −13%; basket corr to dollar **−0.38** |
| 2 | Does country / region rotation add alpha? | ❌ no — long-RS +0.61 = EW-hold; long-short **−0.23**; cross-region rotate +0.60 < SPY +0.88 |

**The synthesis:** EMEA is the starkest "US beta wearing a flag" in the family — 11 country ETFs from
Germany to Turkey collapse to **1.8 effective bets** (corr-SPY 0.82, beta 0.90) and underperform SPY on
every axis (+0.61/+10%/−40% vs +0.88/+15%/−34%), while adding political tail risk. It is the most
dollar-sensitive region (corr to UUP −0.38), carrying an uncompensated FX drag (hedged Europe beats
unhedged), and rotation adds nothing (long-short country momentum is **negative**, −0.23 — Europe's
countries move together). A null as a standalone sleeve; at best a currency-hedged input to a global
relative-strength book — where APAC, not EMEA, is the better candidate.

## Status
**Research: first pass complete — a null (US beta + FX drag, no rotation edge)** (`research/`). No live
driver. Geography within equities is just more beta; the honest conclusion points back to the spine.

## The Blaque Baux family
This repo is one sleeve of the **Blaque Baux** family — a single governed engine steered in
many directions. The [core repo](https://github.com/Carter-Warrens/blaquebaux) is the
base/blueprint and holds the [full family roster](https://github.com/Carter-Warrens/blaquebaux#the-blaque-baux-family).

## Layout
```
engine/     the Blaque Baux platform (git submodule -> Carter-Warrens/blaquebaux)
research/   two Path-A sketches (regional beta + FX drag, country/region rotation) + scorecard
live/       governed live drivers (once a sleeve graduates to paper A/B)
```

## License
[MIT](LICENSE). (c) 2026 Carter Warrens.
