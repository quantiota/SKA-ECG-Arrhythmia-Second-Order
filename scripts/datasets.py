"""The dataset: where the first-order results are, where the second order is written."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT = ROOT.parent
MITDB_RESULTS = PROJECT / "SKA-ECG-Arrhythmia" / "ska-ecg-engine" / "results"


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
