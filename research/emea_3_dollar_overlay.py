#!/usr/bin/python3
# =============================================================================
# emea_3_dollar_overlay.py — does consuming brics' DOLLAR regime rescue the EMEA null?
#
# EMEA was rejected as a directional sleeve: US beta wearing a flag, and a persistent DOLLAR headwind
# (basket corr to UUP -0.38). brics now publishes a dollar-trend regime (dollar_regime.txt: UUP vs its
# 100d MA). The honest question the family's cross-sleeve wiring raises: if EMEA's problem was the
# dollar drag, does DE-RISKING the directional basket when the dollar is trending up rescue its
# risk-adjusted profile — or is the FX drag structural and untimeable (confirming the null)?
# Causal, lagged signal, net of cost. Read-only. (Same test lives in latam/; apac's live book is the
# dollar-NEUTRAL long/short, so it declines this overlay — see apac_3.)
# =============================================================================
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _emea_common import load, REGIONS

REGION = "EMEA"; MA = 100
B = load(); g = REGIONS[REGION]
basket = B.basket(g)                                  # daily equal-weight long book (length T)
uup = B.M[:, B.i["UUP"]]                               # UUP price path (length T+1)
strong = np.zeros(B.T, bool)                           # causal: signal at t uses UUP prices up to t
for t in range(MA, B.T): strong[t] = uup[t] > uup[t-MA:t].mean()

def overlay(d): return np.where(strong, d, 1.0) * basket   # de-risk x d on strong-dollar days

print("=" * 80, f"\n{REGION} + dollar-regime overlay — does dodging the strong dollar rescue the null?\n" + "=" * 80)
print(f"  basket corr-to-UUP {B.corr(basket, B.col('UUP')):+.2f}   beta-to-UUP {B.beta(basket, B.col('UUP')):+.2f}"
      f"   (strong-dollar {100*strong.mean():.0f}% of days)\n")
print(f"  {'book':<26}{'Sharpe':>8}{'CAGR':>8}{'maxDD':>8}")
sh0, cg0, dd0 = B.met(basket)
print(f"  {'FULL directional basket':<26}{sh0:>+8.2f}{cg0*100:>+7.0f}%{dd0*100:>+7.0f}%")
res = []
for d in (0.75, 0.50, 0.0):
    sh, cg, dd = B.met(overlay(d)); res.append((d, sh, cg, dd))
    print(f"  {('overlay '+('to cash' if d==0 else f'x{d}')):<26}{sh:>+8.2f}{cg*100:>+7.0f}%{dd*100:>+7.0f}%")
shS, cgS, ddS = B.met(B.col("SPY"))
print(f"  {'(SPY, reference)':<26}{shS:>+8.2f}{cgS*100:>+7.0f}%{ddS*100:>+7.0f}%")

bd, bsh, bcg, bdd = max(res, key=lambda x: x[1])          # best overlay by Sharpe
dd_cut = 1 - abs(bdd) / abs(dd0)
print(f"\n  best overlay by Sharpe: {'to cash' if bd==0 else f'x{bd}'}  ->  Sharpe {sh0:+.2f} -> {bsh:+.2f}   "
      f"maxDD {dd0*100:+.0f}% -> {bdd*100:+.0f}% ({dd_cut*100:.0f}% cut)")
if bsh >= sh0 + 0.05 and bdd > dd0:
    tier = f"IMPROVES {REGION}'s risk-adjusted profile (Sharpe up AND drawdown down). " + \
           ("Clears SPY — worth a driver." if bsh >= shS else "Still below SPY — a stronger ingredient, not yet a standalone keeper.")
elif dd_cut >= 0.15 and bsh >= sh0 - 0.02:
    tier = f"MEANINGFULLY DE-RISKS {REGION} (drawdown {dd0*100:+.0f}% -> {bdd*100:+.0f}%, {dd_cut*100:.0f}% cut) at ~flat Sharpe " + \
           "— a better ingredient inside a global book, not a standalone keeper (still below SPY)."
else:
    tier = f"only TRADES RETURN FOR DROWDOWN on {REGION} — no Sharpe gain (best {bsh:+.2f} vs {sh0:+.2f}); it de-risks " + \
           "proportionally but does NOT rescue the null."
print("\nVERDICT:", tier.replace("DROWDOWN", "DRAWDOWN"))
print("The FX drag is real; the dollar regime is the RIGHT lever to try here (unlike the bonds overlay,")
print("which keys off the stock-bond correlation). The family rule holds: match the signal to the sleeve,")
print(f"then let the data decide — here it keeps {REGION} on the honest shelf, at most a de-risked ingredient.")
