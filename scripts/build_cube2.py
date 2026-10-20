#!/usr/bin/env python3
"""3D cube (HTML, Three.js, WebXR) of a second-order run: one point per cycle.

Axes: z₂ = ‖Z₂‖, ż₂ = dz₂/dt₂ (1/s), P₂ = exp(−|ΔH₂/H₂|) of the second-order learner.
Colour = the sign of the return it learned. With dt, the vertical axis is Δt₂ (ms), the time
between two cycles, instead of P₂. Open the HTML file in a browser.

With label, each point also carries the MIT-BIH labels of its interval, from cycle k to the next
(e.g. N→V), shown on click; the title gives the label counts of the cycles and of the intervals.

Usage
    python scripts/build_cube2.py mitdb mitdb100 25 25    # → mitdb/vr/ska2_ecg_mitdb100_scale25_scale25_vr.html
    python scripts/build_cube2.py mitdb mitdb100 25 25 dt # → mitdb/vr/ska2_ecg_mitdb100_scale25_scale25_dt_vr.html
    python scripts/build_cube2.py mitdb mitdb100 25 25 label     # → ..._scale25_label_vr.html
    python scripts/build_cube2.py mitdb mitdb100 25 25 dt label  # → ..._scale25_dt_label_vr.html
Requires: <dataset>/data/ska2_<record>_scale<s1>_scale<s2>.csv (learn_second_order.py), the record's .atr, pandas
"""
import json
import sys

import pandas as pd

from datasets import BEATS, ROOT, folder, labels, record, source

NAMES = ["return ≥ 0", "return < 0"]
COLORS = ["#e8604c", "#3987e5"]


def main():
    ds, rec, s1, s2 = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
    dt = "dt" in sys.argv[5:]                                          # vertical axis = dt2 (ms), not P2
    label = "label" in sys.argv[5:]                                    # MIT-BIH labels in the title and on click
    rec, f = record(ds, rec), folder(ds)
    d = pd.read_csv(f / "data" / f"ska2_{rec}_scale{s1:g}_scale{s2:g}.csv")
    lab = labels(ds, rec, s1) if label else {}
    nxt = dict(zip(d.k[:-1], d.k[1:]))                                  # step k = the interval from cycle k to the next
    d["pair"] = [f"{lab.get(k, '?')}→{lab.get(nxt.get(k), '?')}" for k in d.k]
    d = d.dropna(subset=["P2", "zdot2"])
    D = dict(z=d.z2.round(3).tolist(), zd=d.zdot2.round(4).tolist(), p=d.P2.round(4).tolist(),
             t=[0 if r >= 0 else 1 for r in d.ret], names=NAMES, colors=COLORS,
             zmax=float(d.z2.max()), zdmax=float(d.zdot2.max()))
    if label:
        D.update(lb=d.pair.tolist(), lbn={**{b[0]: b[1] for b in BEATS.values()}, "?": "no annotation"},
                 k=d.k.tolist(), dt=(1000 * d.dt2).round(0).tolist(), x=d.x.round(4).tolist(), r=d.ret.round(5).tolist())
    labs = ""
    if label:
        cnt, pairs = pd.Series(list(lab.values())).value_counts(), d.pair.value_counts()
        labs = ("cycles: " + ", ".join(f"{n} {b} {D['lbn'][b]}" for b, n in cnt.items())
                + "; intervals between cycles: " + ", ".join(f"{n} {p}" for p, n in pairs.items()) + ". ")
    if dt:
        D["p"] = (1000 * d.dt2).round(1).tolist()
        D["ymax"] = float(1000 * d.dt2.max())
    desc = (f"{source(ds, rec)}. " + labs + f"Second-order SKA learning, {len(d):,} steps, one per cycle. "
            f"Input: the return of c_k = cos(v_k, v_k+1), v_k = (P of P→Q, Q→R, R→S, S→T, T→P) of the "
            f"first-order run at scale {s1:g}; second-order scale {s2:g}. Horizontal axes: z₂ = ‖Z₂‖ and "
            f"ż₂ = dz₂/dt₂ (1/s), dt₂ = the time between two cycles; "
            + ("vertical axis: Δt₂, the time between two cycles (ms). " if dt else "vertical axis: P₂ = exp(−|ΔH₂/H₂|). ")
            + "2 colours = the sign of the return.")
    tpl = "ska_ecg_vr_template" + ("_dt" if dt else "") + ("_label" if label else "") + ".html"
    s = (ROOT / "scripts" / tpl).read_text(encoding="utf-8")
    s = s.replace("__DATA__", json.dumps(D, separators=(",", ":"), ensure_ascii=False)).replace("__DESCRIPTION__", desc)
    out = f / "vr" / f"ska2_ecg_{rec}_scale{s1:g}_scale{s2:g}{'_dt' if dt else ''}{'_label' if label else ''}_vr.html"
    out.write_text(s, encoding="utf-8")
    print(f"saved {out}  ({len(d):,} steps)")


if __name__ == "__main__":
    main()
