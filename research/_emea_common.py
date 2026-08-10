#!/usr/bin/python3
# =============================================================================
# _regions_common.py — shared helpers for the BLAQUE BAUX regional sleeves
#                       (EMEA / APAC / LATAM). Identical across the three repos.
#
# All three sleeves are the SAME research object: regional exposure bought through
# US-listed country ETFs, plus the question of whether rotating across countries or
# regions is a strategy. So the three repos share this module and its sketches; each
# repo just frames the story from its own region.
#
# Universes are US-listed single-country ETFs (US-hours pricing, embedded unhedged
# FX — the standing caveat). Benchmarks: SPY (US), UUP (dollar). Hedged wrappers
# (HEDJ Europe, DXJ Japan) let us isolate the FX cost against their unhedged twins.
# Keys come from env only (ALPACA_KEY_ID / ALPACA_SECRET_KEY) — never hardcoded.
# =============================================================================
import os, json, urllib.request, math
import numpy as np

_H = {"APCA-API-KEY-ID": os.environ["ALPACA_KEY_ID"],
      "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"]}

# single-country ETFs by region
EMEA  = ["EWG","EWU","EWQ","EWI","EWP","EWL","EWD","EWN","EIS","EZA","TUR"]   # Europe + Israel + S.Africa + Turkey
APAC  = ["EWJ","EWY","EWT","MCHI","EWA","EWH","EWS","INDA","EIDO","THD","EWM","EPHE"]
LATAM = ["EWZ","EWW","ECH","EPU","ARGT"]
REGIONS = {"EMEA": EMEA, "APAC": APAC, "LATAM": LATAM}
# benchmarks + hedged/unhedged FX pairs
EXTRA = ["SPY","UUP","EZU","HEDJ","DXJ"]


def _closes(sym, start="2016-01-01", end="2026-08-01"):
    u = (f"https://data.alpaca.markets/v2/stocks/bars?symbols={sym}&timeframe=1Day"
         f"&start={start}&end={end}&adjustment=all&feed=sip&limit=10000")
    b = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=_H), timeout=40)
                  ).get("bars", {}).get(sym, [])
    return {x["t"][:10]: x["c"] for x in b}


def load():
    """Fetch every region + benchmark once; return an aligned bundle."""
    syms = EMEA + APAC + LATAM + EXTRA
    D = {s: _closes(s) for s in syms}
    ds = sorted(set.intersection(*[set(v) for v in D.values()]))
    M = np.array([[D[s][d] for s in syms] for d in ds], float)
    return _Bundle(syms, ds, M)


class _Bundle:
    def __init__(self, syms, ds, M):
        self.syms, self.ds, self.M = syms, ds, M
        self.i = {s: syms.index(s) for s in syms}
        self.R = M[1:] / M[:-1] - 1
        self.T = len(self.R)

    def col(self, s):     return self.R[:, self.i[s]]
    def basket(self, g):  return self.R[:, [self.i[s] for s in g]].mean(1)

    def met(self, r):
        r = r[np.isfinite(r)]; s = r.std()
        sh = r.mean() / s * math.sqrt(252) if s > 0 else float("nan")
        lvl = np.cumprod(1 + r); dd = (lvl / np.maximum.accumulate(lvl) - 1).min()
        return sh, lvl[-1] ** (252 / len(r)) - 1, dd

    def eff_bets(self, g):
        C = np.corrcoef(self.R[:, [self.i[s] for s in g]].T)
        lam = np.linalg.eigvalsh(C); return (lam.sum() ** 2) / (lam ** 2).sum()

    def corr(self, a, b):  return float(np.corrcoef(a, b)[0, 1])
    def beta(self, r, mkt=None):
        mkt = self.col("SPY") if mkt is None else mkt
        return float(np.cov(r, mkt)[0, 1] / mkt.var())

    def momentum(self, names, mode="long", look=126, reb=21, cost=5.0):
        """Rank `names` by trailing return; rotate. mode: 'long' top-third, 'ls' top-minus-bottom."""
        idx = [self.i[s] for s in names]; n = len(idx); k = max(1, n // 3)
        Rl = self.R[:, idx]; wp = np.zeros(n); pnl = []; c = cost / 1e4
        for t in range(look, self.T - 1):
            if (t - look) % reb == 0:
                tr = self.M[t, idx] / self.M[t - look, idx] - 1
                o = np.argsort(tr); w = np.zeros(n)
                w[o[-k:]] = 1.0 / k
                if mode == "ls": w[o[:k]] = -1.0 / k
            else:
                w = wp
            pnl.append(float(np.nansum(w * Rl[t + 1])) - np.abs(w - wp).sum() * c); wp = w
        return self.met(np.array(pnl))
