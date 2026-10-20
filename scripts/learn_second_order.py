#!/usr/bin/env python3
"""Second-order SKA learning: the learner reads the return of the scalar product of two
successive cycles, one step per cycle.

    input  x_k = sigmoid(SCALE2 * ret_k),   ret_k = (c_k - c_k-1) / c_k-1,   c_k = cos(v_k, v_k+1)

ret_k is known when cycle k+1 starts, so the step carries that time and the learner's
dt2 is the time between two cycles. Output, per cycle:
    z2 = ‖Z₂‖,  dt2,  zdot2 = dz2/dt2 (1/s),  P2 = exp(−|ΔH₂/H₂|)
The SKA learner is not included in this repository: set SKA_ENGINE to the folder holding
ska_core.py (default: ../SKA-ECG-Heart-Rate-Variability/ecg-ska-engine).

Usage
    python scripts/learn_second_order.py mitdb mitdb100 25 25    # first-order scale 25, second-order scale 25
        → mitdb/data/ska2_mitdb100_scale25_scale25.csv
Requires: <dataset>/data/cycles_<record>_scale<s>.csv (cycle_vectors.py), numpy, pandas, torch
"""
import datetime as dt
import os
import pathlib
import sys

import numpy as np
import pandas as pd

from datasets import PROJECT, folder, record

ENGINE = pathlib.Path(os.getenv("SKA_ENGINE", PROJECT / "SKA-ECG-Heart-Rate-Variability" / "ecg-ska-engine"))
sys.path.insert(0, str(ENGINE))
from ska_core import SKALearner                                   # noqa: E402


def main():
    ds, rec, s1, s2 = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
    rec, f = record(ds, rec), folder(ds)
    cyc = pd.read_csv(f / "data" / f"cycles_{rec}_scale{s1:g}.csv")
    d = pd.DataFrame({"k": cyc.k, "ret": cyc.ret, "t": cyc.t.shift(-1)}).dropna().reset_index(drop=True)
    d["x"] = 1.0 / (1.0 + np.exp(-np.clip(s2 * d.ret, -500, 500)))
    t0 = dt.datetime(2000, 1, 1)
    L, rows = SKALearner(init_std=0.01), []
    for e in d.itertuples():
        r = L.step(float(e.x), t0 + dt.timedelta(milliseconds=round(1000 * e.t)), int(e.k))
        Z, D = r["Z"], r["D"]
        rows.append({"k": e.k, "t": e.t, "ret": e.ret, "x": e.x, "z2": float(np.linalg.norm(Z)),
                     "decision2": float(D[-1]) if len(D) else 0.5, "entropy2": r["entropy"],
                     "dt2": r.get("delta_t")})
    out = pd.DataFrame(rows)
    H = out.entropy2.to_numpy(float)
    out["P2"] = np.r_[np.nan, np.exp(-np.abs(np.diff(H) / H[1:]))]
    out["zdot2"] = np.gradient(out.z2.to_numpy(float)) / out.dt2.to_numpy(float)
    csv = f / "data" / f"ska2_{rec}_scale{s1:g}_scale{s2:g}.csv"
    out.to_csv(csv, index=False, float_format="%.6g")
    print(f"saved {csv}  ({len(out)} steps, x {d.x.min():.4f}..{d.x.max():.4f})")


if __name__ == "__main__":
    main()
