"""Loaders for the 8 UCI healthcare datasets used in Almeida & Bacao (2025), Table 1.

Each base loader returns (X: DataFrame of numeric features, y: Series with 1 = positive/minority
outcome, 0 = negative). `make_imbalanced` then undersamples the positive class to a fixed
percentage, following the `preprocess_liver` function in the authors' demo notebook.
"""
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from scipy.io import arff

warnings.filterwarnings("ignore")

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
CACHE = Path(__file__).resolve().parent.parent / "data" / "cache"


def _uci(uci_id):
    """Fetch a UCI dataset via ucimlrepo, cached locally as pickle."""
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"uci_{uci_id}.pkl"
    if path.exists():
        return pd.read_pickle(path)
    from ucimlrepo import fetch_ucirepo
    d = fetch_ucirepo(id=uci_id)
    out = (d.data.features.copy(), d.data.targets.iloc[:, 0].copy())
    pd.to_pickle(out, path)
    return out


def _finish(X, y):
    """Drop rows with missing values and non-numeric (categorical) columns (paper Sec. 4.4)."""
    X = X.select_dtypes(include=[np.number])
    keep = X.notna().all(axis=1)
    X, y = X[keep], y[keep]
    return X.reset_index(drop=True), y.astype(int).reset_index(drop=True)


def breast_wisconsin_diagnostic():
    X, y = _uci(17)
    return _finish(X, (y == "M").astype(int))


def breast_wisconsin_prognostic():
    X, y = _uci(16)
    # Table 1 reports 31 features and keeps all 47 recurrences, so the column holding the
    # missing values (lymph_node_status) must have been dropped rather than the rows.
    # 'Time' (time to recurrence / follow-up) is dropped too: it leaks the outcome and
    # dropping it gives the 31 features of Table 1.  -> assumption, not stated in the paper.
    X = X.drop(columns=["lymph_node_status", "Time"])
    return _finish(X, (y == "R").astype(int))


def breast_coimbra():
    X, y = _uci(451)
    return _finish(X, (y == 2).astype(int))  # 2 = patient, 1 = healthy control


def arcene():
    base = RAW / "arcene"
    Xtr = pd.read_csv(base / "ARCENE" / "arcene_train.data", sep=r"\s+", header=None)
    ytr = pd.read_csv(base / "ARCENE" / "arcene_train.labels", header=None)[0]
    Xva = pd.read_csv(base / "ARCENE" / "arcene_valid.data", sep=r"\s+", header=None)
    yva = pd.read_csv(base / "arcene_valid.labels", header=None)[0]
    X = pd.concat([Xtr, Xva], ignore_index=True)
    y = pd.concat([ytr, yva], ignore_index=True)
    return _finish(X, (y == 1).astype(int))  # 1 = cancer (88 of 200)


def pima_diabetes():
    data, _ = arff.loadarff(RAW / "pima.arff")
    df = pd.DataFrame(data)
    y = df.pop("class").str.decode("utf-8") == "tested_positive"
    return _finish(df.astype(float), y.astype(int))


def hepatitis_c():
    X, y = _uci(571)
    # The paper text says hepatitis/fibrosis/cirrhosis were merged and uncertain outcomes
    # discarded. That gives 56 positives after dropping NaN rows, but Table 1 (6/15/31
    # minority at 10/25/50%) needs 62-63. Treating everything except '0=Blood Donor' as
    # positive (i.e. keeping the 7 'suspect blood donors' as positives) gives exactly 63
    # and reproduces Table 1, so that is what is used here.
    pos = (y.astype(str) != "0=Blood Donor").astype(int)
    return _finish(X, pos)


def parkinsons():
    df = pd.read_csv(RAW / "parkinson+s+disease+classification" / "pd_speech_features.csv", header=1)
    y = df.pop("class")
    df = df.drop(columns=["id", "gender"])  # id + categorical -> 752 features (Table 1)
    return _finish(df, (y == 1).astype(int))  # 1 = Parkinson's (564), 0 = healthy (192)


def indian_liver():
    X, y = _uci(225)
    X = X.drop(columns=["Gender"])
    return _finish(X, (y == 1).astype(int))  # Selector 1 = liver patient


BASE = {
    "breast_wisconsin_diag": breast_wisconsin_diagnostic,
    "breast_wisconsin_prog": breast_wisconsin_prognostic,
    "breast_coimbra": breast_coimbra,
    "arcene": arcene,
    "pima": pima_diabetes,
    "hepatitis_c": hepatitis_c,
    "parkinsons": parkinsons,
    "indian_liver": indian_liver,
}

# (base dataset, percentage of positives kept) -> the 24 problems of Table 1.
# Note: Table 1 labels the middle Arcene problem "15%", but its 22 minority instances
# correspond to 25% of the 88 positives, so 0.25 is used here.
CONFIGS = (
    [(n, p) for n in ["breast_wisconsin_diag", "breast_wisconsin_prog", "breast_coimbra",
                      "pima", "hepatitis_c"] for p in (0.10, 0.25, 0.50)]
    + [("arcene", p) for p in (0.10, 0.25, 0.50)]
    + [(n, p) for n in ["parkinsons", "indian_liver"] for p in (0.05, 0.10, 0.15)]
)


def make_imbalanced(X, y, percentage, seed):
    """Keep every negative and int(percentage * n_pos) randomly chosen positives (demo notebook logic)."""
    n_keep = int(percentage * (y == 1).sum())
    pos_idx = y[y == 1].sample(n_keep, random_state=seed).index
    idx = np.sort(np.concatenate([y[y == 0].index.values, pos_idx.values]))
    return X.loc[idx].to_numpy(dtype=float), y.loc[idx].to_numpy()


def load(name, percentage, seed):
    X, y = BASE[name]()
    return make_imbalanced(X, y, percentage, seed)


if __name__ == "__main__":
    print(f"{'dataset':<28}{'rows':>6}{'minority':>10}{'features':>10}{'IR':>8}")
    for name, p in CONFIGS:
        X, y = load(name, p, seed=0)
        n_min = int(y.sum())
        print(f"{name + f' {int(p*100)}%':<28}{len(y):>6}{n_min:>10}{X.shape[1]:>10}{(len(y)-n_min)/n_min:>8.2f}")
