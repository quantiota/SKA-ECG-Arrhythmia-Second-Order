#!/usr/bin/env python3
"""Cycle vectors of a first-order SKA run, the input of the second-order learning.

From the first-order steps (one step per transition, 5 per cycle):
    t     = the time of the cycle's P→Q step (s)
    v_k   = (P of P→Q, Q→R, R→S, S→T, T→P) in cycle k         P = exp(−|ΔH/H|)
    r_k   = the rank vector of v_k (1 = lowest band): the path of the cycle
    c_k   = cos(v_k, v_k+1), the scalar product of two successive cycles (normalised)
    ret_k = (c_k - c_k-1) / c_k-1, its simple return (no log)

Usage
    python scripts/cycle_vectors.py mitdb mitdb100 25
        → mitdb/data/cycles_mitdb100_scale25.csv
          mitdb/figures/ska_mitdb100_scale25_cycle_cos.png, ska_mitdb100_scale25_cycle_cos_return.png
Requires: numpy, pandas, matplotlib
"""
import sys

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datasets import first_order_csv, folder, record

ORDER = ["P→Q", "Q→R", "R→S", "S→T", "T→P"]


def first_order(csv, rec, scale, inp="cdot_cos"):
    """The first-order steps of one run, with P."""
    d = pd.read_csv(csv, dtype={"record_id": str})
    d = d[(d.record_id == rec) & (d.input == inp) & (d.scale == scale)].sort_values("event_index")
    if d.empty:
        raise SystemExit(f"no run for {rec} at scale {scale:g}")
    d = d.reset_index(drop=True)
    H = d.entropy.to_numpy(float)
    d["P"] = np.r_[np.nan, np.exp(-np.abs(np.diff(H) / H[1:]))]
    d["tr"] = d.transition.str.replace("-", "→")
    return d.dropna(subset=["P"])


def cycles(d):
    """One row per complete cycle: v_k, r_k, c_k, ret_k."""
    W = d.pivot_table(index="k", columns="tr", values="P", aggfunc="first")[ORDER].dropna()
    w = W.to_numpy()
    out = W.rename(columns={t: "P_" + t.replace("→", "") for t in ORDER}).reset_index()
    t0 = d[d.tr == ORDER[0]].set_index("k").peak                  # cycle start: its P→Q step (ms)
    out.insert(1, "t", (t0.reindex(out.k).to_numpy() / 1000).round(3))
    out["rank"] = ["".join(map(str, r)) for r in W.rank(axis=1).astype(int).to_numpy()]
    c = (w[:-1] * w[1:]).sum(1) / (np.linalg.norm(w[:-1], axis=1) * np.linalg.norm(w[1:], axis=1))
    out["c"] = np.r_[c, np.nan]
    out["ret"] = np.r_[np.nan, c[1:] / c[:-1] - 1, np.nan]                 # simple return, no log
    return out


def plot(out, rec, scale, fig_dir):
    k = out.k.to_numpy()
    fig, ax = plt.subplots(2, 1, figsize=(11, 6), sharex=True)
    ax[0].plot(k, out.c, lw=.8, color="#3987e5")
    ax[0].set_ylabel(r"cos(v$_k$, v$_{k+1}$)")
    ax[1].semilogy(k, 1 - out.c, lw=.8, color="#e87ba4")
    ax[1].set_ylabel("1 − cos  (log)")
    ax[1].set_xlabel("cycle index k")
    ax[0].set_title(f"Record {rec}, scale {scale:g}: scalar product of two successive cycles (normalised), "
                    "v = (P of P→Q, Q→R, R→S, S→T, T→P)")
    for x in ax:
        x.grid(alpha=.3)
    fig.tight_layout()
    fig.savefig(fig_dir / f"ska_{rec}_scale{scale:g}_cycle_cos.png", dpi=130)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 3.6))
    ax.plot(k, out.ret, lw=.8, color="#1baf7a")
    ax.axhline(0, color="k", lw=.5)
    ax.set_xlabel("cycle index k")
    ax.set_ylabel(r"return  (c$_{k}$ − c$_{k-1}$) / c$_{k-1}$")
    ax.set_title(f"Record {rec}, scale {scale:g}: return of the scalar product c$_k$ = cos(v$_k$, v$_{{k+1}}$)")
    ax.grid(alpha=.3)
    fig.tight_layout()
    fig.savefig(fig_dir / f"ska_{rec}_scale{scale:g}_cycle_cos_return.png", dpi=130)
    plt.close(fig)


def main():
    ds, rec, scale = sys.argv[1], sys.argv[2], float(sys.argv[3])
    rec, f = record(ds, rec), folder(ds)
    out = cycles(first_order(first_order_csv(ds, rec), rec, scale))
    csv = f / "data" / f"cycles_{rec}_scale{scale:g}.csv"
    out.to_csv(csv, index=False, float_format="%.6g")
    plot(out, rec, scale, f / "figures")
    print(f"saved {csv}  ({len(out)} cycles, {out['rank'].nunique()} paths)")


if __name__ == "__main__":
    main()
