#!/usr/bin/python3
# =============================================================================
# regions_2_rotation.py — BLAQUE BAUX regionals #2 (country & region rotation).
#   The real testable alpha: does relative strength across countries / regions
#   rotate into a signal that beats buy-and-hold — and SPY?
#
# FINDING: mostly no. Within a region, long top-third relative strength ~ ties EW
# buy-and-hold (EMEA +0.61 vs +0.61, LATAM +0.39 vs +0.68 — worse). Long-short
# country momentum is negative in EMEA (-0.23) and flat in LATAM (-0.04); only APAC
# has a real dispersion pulse (+0.30 long-short) — Japan/Taiwan/Korea/India genuinely
# diverge. Pooled across all 28 countries the long book (+0.59) still ties EW (+0.62)
# and the long-short is negative (-0.18). Cross-REGION trend rotation (+0.60) ties
# equal-weighting the three regions (+0.65). Nothing here beats simply holding SPY
# (+0.88) — the regions are one correlated risk-on basket, and US led the whole sample.
#
# RESULTS AS TESTED (2016-2026, 126d look / 21d rebal / 5bp; Sharpe):
#   within-region:  EMEA hold +0.61 long-RS +0.61 long-short -0.23
#                   APAC hold +0.52 long-RS +0.58 long-short +0.30   <- only real dispersion
#                   LATAM hold +0.68 long-RS +0.39 long-short -0.04
#   pooled 28: EW +0.62 | long top-third +0.59 | long-short -0.18
#   cross-region: EW-3 +0.65 | trend-rotate +0.60      (SPY +0.88 throughout)
# Read-only.
# =============================================================================
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _emea_common import REGIONS, EMEA, APAC, LATAM, load

B = load(); ss, sc, sd = B.met(B.col("SPY"))
print("=" * 78, "\nREGIONALS #2 — does country / region rotation beat buy-and-hold (and SPY)?\n" + "=" * 78)

print("\nC. WITHIN-REGION country momentum (long top-third RS / long-short top-minus-bottom)")
for nm, g in REGIONS.items():
    h = B.met(B.basket(g))[0]; lo = B.momentum(g, "long")[0]; ls = B.momentum(g, "ls")[0]
    star = "   <- real dispersion" if ls > 0.15 else ""
    print(f"  {nm:6s} EW-hold {h:+.2f} | long-RS {lo:+.2f} | long-short {ls:+.2f}{star}")

print("\nD. POOLED & CROSS-REGION rotation")
allc = EMEA + APAC + LATAM
ew = B.met(np.column_stack([B.col(s) for s in allc]).mean(1))
print(f"  pooled {len(allc)} countries: EW-hold {ew[0]:+.2f} | long top-third {B.momentum(allc,'long')[0]:+.2f} | long-short {B.momentum(allc,'ls')[0]:+.2f}")
# cross-region: rotate the 3 region baskets by trend (hold those with positive 126d trend)
Rb = np.column_stack([B.basket(EMEA), B.basket(APAC), B.basket(LATAM)]); lvl = np.cumprod(1 + Rb, 0)
wp = np.zeros(3); pnl = []
for t in range(126, B.T - 1):
    if (t - 126) % 21 == 0:
        pos = (lvl[t] / lvl[t - 126] - 1) > 0
        w = (pos / pos.sum()) if pos.any() else np.ones(3) / 3
    else:
        w = wp
    pnl.append(float(np.nansum(w * Rb[t + 1])) - np.abs(w - wp).sum() * 5e-4); wp = w
print(f"  3 regions:            EW-hold {B.met(Rb.mean(1))[0]:+.2f} | trend-rotate {B.met(np.array(pnl))[0]:+.2f}")
print(f"  SPY (same window):    {ss:+.2f}")

print("\nVERDICT: rotation is not a strategy here. Within-region relative strength ties buy-and-hold")
print("(only APAC has a real long-short pulse, +0.30, from genuine country dispersion), and neither")
print("pooled country momentum nor cross-region trend rotation beats holding SPY. The regions are one")
print("correlated risk-on basket; US led the whole sample. Honest role: rotation INPUTS to a global")
print("relative-strength book (APAC the best candidate) — currency-hedged — never a standalone sleeve.")
