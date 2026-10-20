"""The dataset: where the first-order results are, where the second order is written."""
import pathlib

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT = ROOT.parent
MITDB_RESULTS = PROJECT / "SKA-ECG-Arrhythmia" / "ska-ecg-engine" / "results"
MITDB_DATA = PROJECT / "SKA-ECG-Arrhythmia" / "ecg-data-validation" / "data"
FS = 360.0
BEATS = {1: ("N", "normal"), 2: ("L", "left bundle branch block"), 3: ("R", "right bundle branch block"),
         4: ("a", "aberrated atrial premature"), 5: ("V", "premature ventricular contraction"),
         6: ("F", "fusion of ventricular and normal"), 7: ("J", "nodal (junctional) premature"),
         8: ("A", "atrial premature"), 9: ("S", "supraventricular premature"), 10: ("E", "ventricular escape"),
         11: ("j", "nodal (junctional) escape"), 12: ("/", "paced"), 13: ("Q", "unclassifiable"),
         31: ("!", "ventricular flutter wave"), 34: ("e", "atrial escape"), 35: ("n", "supraventricular escape"),
         38: ("f", "fusion of paced and normal")}


def folder(ds):
    """mitdb/, with data/, figures/, vr/."""
    if ds != "mitdb":
        raise SystemExit("dataset: mitdb")
    f = ROOT / ds
    for sub in ("data", "figures", "vr"):
        (f / sub).mkdir(parents=True, exist_ok=True)
    return f


def first_order_csv(ds, rec):
    """The file holding the first-order run of this record."""
    return MITDB_RESULTS / rec / f"ska_{rec}_runs.csv"


def record(ds, rec):
    return rec


def source(ds, rec):
    """The database line of a description."""
    return f"Record {rec}, PhysioNet MIT-BIH Arrhythmia Database (lead MLII, 360 Hz)"


def read_atr(path):
    """MIT-BIH .atr -> (time in ms, symbol) of every beat annotation."""
    w = np.fromfile(path, dtype="<u2")
    i, s, out = 0, 0, []
    while i < len(w):
        t, v = int(w[i]) >> 10, int(w[i]) & 0x3FF
        i += 1
        if t == 0 and v == 0:
            break
        if t == 59:                                        # SKIP: 32-bit interval in the next two words
            s += (int(w[i]) << 16 | int(w[i + 1])); i += 2
            continue
        if t == 63:                                        # AUX: v bytes
            i += (v + 1) // 2
            continue
        if t in (60, 61, 62):                              # NUM, SUB, CHN
            continue
        s += v
        if t in BEATS:
            out.append((s * 1000.0 / FS, BEATS[t][0]))
    return np.array([o[0] for o in out]), np.array([o[1] for o in out])


def labels(ds, rec, scale):
    """{cycle k: MIT-BIH label}: the beat annotation nearest the cycle's R peak (within 150 ms), else "?"."""
    d = pd.read_csv(first_order_csv(ds, rec), usecols=["input", "scale", "event", "k", "peak"])
    d = d[(d.input == "cdot_cos") & (d.scale == scale)]
    R = d[d.event == "R"].groupby("k").peak.first()                    # R peak of each cycle (ms)
    at, sym = read_atr(MITDB_DATA / f"{rec.removeprefix('mitdb')}.atr")
    j = np.clip(np.searchsorted(at, R.values), 1, len(at) - 1)
    j = np.where(np.abs(at[j - 1] - R.values) < np.abs(at[j] - R.values), j - 1, j)
    return dict(zip(R.index, np.where(np.abs(at[j] - R.values) <= 150, sym[j], "?")))
