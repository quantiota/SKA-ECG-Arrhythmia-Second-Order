#!/usr/bin/env python3
"""3D cube (HTML, Three.js, WebXR) of a second-order run: one point per cycle.

Axes: z₂ = ‖Z₂‖, ż₂ = dz₂/dt₂ (1/s), P₂ = exp(−|ΔH₂/H₂|) of the second-order learner.
Colour = the sign of the return it learned. With dt, the vertical axis is Δt₂ (ms), the time
between two cycles, instead of P₂. Open the HTML file in a browser.

Usage
    python scripts/build_cube2.py mitdb mitdb100 25 25    # → mitdb/vr/ska2_ecg_mitdb100_scale25_scale25_vr.html
    python scripts/build_cube2.py mitdb mitdb100 25 25 dt # → mitdb/vr/ska2_ecg_mitdb100_scale25_scale25_dt_vr.html
Requires: <dataset>/data/ska2_<record>_scale<s1>_scale<s2>.csv (learn_second_order.py), pandas
"""
import json
import sys

import pandas as pd

from datasets import ROOT, folder, record, source

NAMES = ["return ≥ 0", "return < 0"]
COLORS = ["#e8604c", "#3987e5"]


def main():
    ds, rec, s1, s2 = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
    dt = len(sys.argv) > 5 and sys.argv[5] == "dt"                    # vertical axis = dt2 (ms), not P2
    rec, f = record(ds, rec), folder(ds)
    d = pd.read_csv(f / "data" / f"ska2_{rec}_scale{s1:g}_scale{s2:g}.csv").dropna(subset=["P2", "zdot2"])
    D = dict(z=d.z2.round(3).tolist(), zd=d.zdot2.round(4).tolist(), p=d.P2.round(4).tolist(),
             t=[0 if r >= 0 else 1 for r in d.ret], names=NAMES, colors=COLORS,
             zmax=float(d.z2.max()), zdmax=float(d.zdot2.max()))
    if dt:
        D["p"] = (1000 * d.dt2).round(1).tolist()
        D["ymax"] = float(1000 * d.dt2.max())
    desc = (f"{source(ds, rec)}. Second-order SKA learning, {len(d):,} steps, one per cycle. "
            f"Input: the return of c_k = cos(v_k, v_k+1), v_k = (P of P→Q, Q→R, R→S, S→T, T→P) of the "
            f"first-order run at scale {s1:g}; second-order scale {s2:g}. Horizontal axes: z₂ = ‖Z₂‖ and "
            f"ż₂ = dz₂/dt₂ (1/s), dt₂ = the time between two cycles; "
            + ("vertical axis: Δt₂, the time between two cycles (ms). " if dt else "vertical axis: P₂ = exp(−|ΔH₂/H₂|). ")
            + "2 colours = the sign of the return.")
    s = (ROOT / "scripts" / ("ska_ecg_vr_template_dt.html" if dt else "ska_ecg_vr_template.html")).read_text(encoding="utf-8")
    s = s.replace("__DATA__", json.dumps(D, separators=(",", ":"), ensure_ascii=False)).replace("__DESCRIPTION__", desc)
    out = f / "vr" / f"ska2_ecg_{rec}_scale{s1:g}_scale{s2:g}{'_dt' if dt else ''}_vr.html"
    out.write_text(s, encoding="utf-8")
    print(f"saved {out}  ({len(d):,} steps)")


if __name__ == "__main__":
    main()
