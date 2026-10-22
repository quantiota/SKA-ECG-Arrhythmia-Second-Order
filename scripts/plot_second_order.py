#!/usr/bin/env python3
"""Figure of a second-order run: the cube (z₂, ż₂, P₂) and P₂ along the cycle index,
coloured by the return learned.

Usage
    python scripts/plot_second_order.py mitdb mitdb100 25 25
        → mitdb/figures/ska2_mitdb100_scale25_scale25.png
Requires: <dataset>/data/ska2_<record>_scale<s1>_scale<s2>.csv (the second-order learning results), pandas, matplotlib
"""
import sys

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datasets import folder, record


def main():
    ds, rec, s1, s2 = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
    rec, f = record(ds, rec), folder(ds)
    d = pd.read_csv(f / "data" / f"ska2_{rec}_scale{s1:g}_scale{s2:g}.csv").dropna(subset=["P2", "zdot2"])
    v = max(abs(d.ret.quantile(.02)), abs(d.ret.quantile(.98)))
    kw = dict(c=d.ret, cmap="coolwarm", vmin=-v, vmax=v, s=6)
    fig = plt.figure(figsize=(13, 5.5))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    sc = ax.scatter(d.z2, d.zdot2, d.P2, **kw)
    ax.set_xlabel("z₂"); ax.set_ylabel("ż₂ (1/s)"); ax.set_zlabel("P₂")
    fig.colorbar(sc, ax=ax, shrink=.6, label="return")
    b = fig.add_subplot(1, 2, 2)
    b.scatter(d.k, d.P2, **kw)
    b.set_xlabel("cycle index k"); b.set_ylabel("P₂"); b.grid(alpha=.3)
    fig.suptitle(f"Record {rec}: second-order SKA learning of the return of c$_k$ "
                 f"(first order scale {s1:g}, second order scale {s2:g})")
    fig.tight_layout()
    out = f / "figures" / f"ska2_{rec}_scale{s1:g}_scale{s2:g}.png"
    fig.savefig(out, dpi=120)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
