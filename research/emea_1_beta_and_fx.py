#!/usr/bin/python3
# =============================================================================
# regions_1_beta_and_fx.py — BLAQUE BAUX regionals #1 (beta + FX drag).
#   Is a US-listed regional book a distinct exposure, or US beta wearing a flag —
#   and what does the embedded, unhedged FX cost you?
#
# FINDING: all three regions are high-beta US proxies that UNDERPERFORM SPY. EMEA's
# 11 country ETFs collapse to ~1.8 effective bets (corr-SPY 0.82); APAC 2.5/12;
# LATAM 2.2/5 with a brutal -55% drawdown. None beats SPY (+0.88). And the US-wrapper
# FX drag is real and uncompensated: over 2016-2026 hedged Japan (DXJ +367%) crushed
# unhedged Japan (EWJ +138%) — a -229% currency drag — while hedged Europe beat
# unhedged by -13%. The dollar (UUP +31%) was a persistent headwind; every region
# basket carries a ~-0.30 to -0.38 correlation to it. You are buying local equities
# AND making a losing, unintended short-dollar bet.
#
# RESULTS AS TESTED (2016-2026, EW region baskets, US-listed ETFs):
#   region  corr-SPY  beta  eff-bets   Sharpe  CAGR  maxDD
#   EMEA      0.82    0.90   1.8/11     +0.61  +10%  -40%
#   APAC      0.79    0.78   2.5/12     +0.52   +8%  -39%
#   LATAM     0.70    0.91   2.2/5      +0.68  +14%  -55%
#   SPY       1.00    1.00      -       +0.88  +15%  -34%
#   FX drag: Japan EWJ +138% vs DXJ +367% = -229% | Europe EZU +169% vs HEDJ +182% = -13%
#   dollar UUP +31%; basket corr to UUP: EMEA -0.38  APAC -0.30  LATAM -0.30
# Read-only.
# =============================================================================
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _emea_common import REGIONS, load

B = load(); ss, sc, sd = B.met(B.col("SPY"))
print("=" * 78, "\nREGIONALS #1 — is regional exposure just US beta + FX drag?\n" + "=" * 78)

print("\nA. REGIONAL BETA — a region basket vs holding SPY")
print(f"  {'region':6s} {'n':>3s} {'corr-SPY':>9s} {'beta':>6s} {'eff-bets':>9s}  {'Sharpe':>7s} {'CAGR':>6s} {'maxDD':>6s}")
for nm, g in REGIONS.items():
    b = B.basket(g); sh, cg, dd = B.met(b)
    print(f"  {nm:6s} {len(g):3d} {B.corr(b, B.col('SPY')):9.2f} {B.beta(b):6.2f} {B.eff_bets(g):6.1f}/{len(g):<3d} {sh:+7.2f} {cg*100:+5.0f}% {dd*100:+5.0f}%")
print(f"  {'SPY':6s} {'':3s} {1.00:9.2f} {1.00:6.2f} {'':9s}  {ss:+7.2f} {sc*100:+5.0f}% {sd*100:+5.0f}%")

print("\nB. FX DRAG — hedged vs unhedged wrapper isolates the USD cost (total return)")
for local, unh, hed in [("Japan", "EWJ", "DXJ"), ("Europe", "EZU", "HEDJ")]:
    cu = (B.M[-1, B.i[unh]] / B.M[0, B.i[unh]]) - 1; ch = (B.M[-1, B.i[hed]] / B.M[0, B.i[hed]]) - 1
    print(f"  {local:6s}: unhedged {unh} {cu*100:+5.0f}%   hedged {hed} {ch*100:+5.0f}%   FX drag {(cu-ch)*100:+5.0f}%")
duup = (B.M[-1, B.i['UUP']] / B.M[0, B.i['UUP']]) - 1
print(f"  dollar UUP {duup*100:+.0f}% over the sample; basket corr to UUP: " +
      "  ".join(f"{nm} {B.corr(B.basket(g), B.col('UUP')):+.2f}" for nm, g in REGIONS.items()))

print("\nVERDICT: regional exposure via US-listed ETFs is concentrated US beta wearing a flag")
print("(few effective bets, underperforms SPY, worse drawdowns) plus a large, uncompensated FX")
print("drag — most brutally in Japan. If a region is held at all, the currency must be HEDGED;")
print("unhedged, you are making a losing short-dollar bet you never chose.")
