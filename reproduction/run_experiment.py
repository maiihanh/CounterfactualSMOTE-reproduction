"""Re-implementation of the experimental procedure of Almeida & Bacao (2025), Sec. 4.

The authors' repository only ships the CounterfactualSMOTE class and a demo notebook, so this
script rebuilds the benchmark from the paper's description:

  * 24 imbalanced problems (Table 1), each repeated with 3 seeds (seed drives the
    undersampling of positives, the CV split and every random_state).
  * 5-fold stratified CV; MinMax scaling fitted on the train fold.
  * 9 imbalance-handling methods x hyperparameter grids of Table 2 x 7 classifiers.
  * Every (method, config, classifier) is scored on every fold; raw fold-level results are
    written to results/raw/<dataset>_<pct>_seed<k>.csv (one file per task -> resumable).

Model selection ("scores corresponding to the best combination of hyperparameters are stored")
is done afterwards in aggregate.py.
"""
import argparse
import itertools
import os
import sys
import time
import warnings
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from imblearn.over_sampling import ADASYN, SMOTE, BorderlineSMOTE, KMeansSMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))   # the authors' original Counterfactual_SMOTE.py
sys.path.insert(0, str(HERE))
from Counterfactual_SMOTE import CounterfactualSMOTE  # noqa: E402
from cf_smote_fixed import CounterfactualSMOTEFixed  # noqa: E402
import datasets  # noqa: E402

OUT = HERE.parent / "results" / "raw"
CF_GRID = dict(k_neighbors=[2, 3, 5], strategy=["strict", "flexible"],
               opt_steps=[3, 5, 10], n_iter=[3, 5, 10, 15])


def grid(**params):
    keys = list(params)
    return [dict(zip(keys, vals)) for vals in itertools.product(*params.values())]


# Table 2 hyperparameter grids.
METHODS = {
    "None": (None, [{}]),
    "Random undersampling": (lambda s, **p: RandomUnderSampler(random_state=s, **p), [{}]),
    "Random oversampling": (lambda s, **p: RandomOverSampler(random_state=s, **p), [{}]),
    "SMOTE": (lambda s, **p: SMOTE(random_state=s, **p), grid(k_neighbors=[2, 3, 5])),
    "ADASYN": (lambda s, **p: ADASYN(random_state=s, **p), grid(n_neighbors=[2, 3, 5])),
    "Borderline SMOTE 1": (lambda s, **p: BorderlineSMOTE(kind="borderline-1", random_state=s, **p),
                           grid(k_neighbors=[2, 3, 5], m_neighbors=[5, 10, 15])),
    "Borderline SMOTE 2": (lambda s, **p: BorderlineSMOTE(kind="borderline-2", random_state=s, **p),
                           grid(k_neighbors=[2, 3, 5], m_neighbors=[5, 10, 15])),
    "K-means SMOTE": (lambda s, **p: KMeansSMOTE(
                          random_state=s, k_neighbors=p["k_neighbors"],
                          kmeans_estimator=p["n_clusters"],
                          cluster_balance_threshold=p["cluster_balance_threshold"],
                          density_exponent=p["density_exponent"]),
                      grid(k_neighbors=[2, 3, 5], n_clusters=[2, 50, 100],
                           cluster_balance_threshold=[1, "auto"], density_exponent=[0, 1, "auto"])),
    "Counterfactual SMOTE": (lambda s, **p: CounterfactualSMOTE(random_state=s, **p), grid(**CF_GRID)),
    # Not part of the paper: same method with the binary-search return bug fixed (cf_smote_fixed.py).
    "Counterfactual SMOTE (fixed)": (lambda s, **p: CounterfactualSMOTEFixed(random_state=s, **p),
                                     grid(**CF_GRID)),
}
PAPER_METHODS = [m for m in METHODS if m != "Counterfactual SMOTE (fixed)"]


def classifiers(seed):
    # The paper does not list classifier hyperparameters -> library defaults.
    return {
        "LR": LogisticRegression(max_iter=1000),
        "DT": DecisionTreeClassifier(random_state=seed),
        "XGBoost": XGBClassifier(random_state=seed, n_jobs=1, verbosity=0),
        "RF": RandomForestClassifier(random_state=seed, n_jobs=1),
        "KNN": KNeighborsClassifier(),
        "GNB": GaussianNB(),
        "MLP": MLPClassifier(random_state=seed),
    }


def run_task(name, pct, seed, methods, out_dir=OUT):
    out = Path(out_dir) / f"{name}_{int(pct * 100)}_seed{seed}.csv"
    if out.exists():
        return str(out), 0.0
    warnings.filterwarnings("ignore")
    t0 = time.time()
    X, y = datasets.load(name, pct, seed)
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    rows = []
    for fold, (tr, te) in enumerate(skf.split(X, y)):
        scaler = MinMaxScaler().fit(X[tr])
        Xtr, Xte, ytr, yte = scaler.transform(X[tr]), scaler.transform(X[te]), y[tr], y[te]
        for method in methods:
            factory, configs = METHODS[method]
            for cfg_id, cfg in enumerate(configs):
                failed = 0
                n_before = len(ytr)
                try:
                    Xr, yr = (Xtr, ytr) if factory is None else factory(seed, **cfg).fit_resample(Xtr, ytr)
                    if len(np.unique(yr)) < 2:
                        raise ValueError("single class after resampling")
                except Exception:
                    # Config invalid for this fold (e.g. k_neighbors >= minority size, no
                    # K-means cluster found): fall back to the unresampled train fold.
                    Xr, yr, failed = Xtr, ytr, 1
                for clf_name, clf in classifiers(seed).items():
                    try:
                        pred = clf.fit(Xr, yr).predict(Xte)
                    except Exception:
                        pred = np.zeros_like(yte)
                    tn, fp, fn, tp = confusion_matrix(yte, pred, labels=[0, 1]).ravel()
                    f1 = 2 * tp / (2 * tp + fp + fn) if tp else 0.0
                    rows.append(dict(dataset=name, pct=pct, seed=seed, fold=fold, method=method,
                                     config_id=cfg_id, config=str(cfg), classifier=clf_name,
                                     f1=f1, tp=tp, fp=fp, fn=fn, tn=tn, failed=failed,
                                     n_synth=len(yr) - n_before))
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp")
    pd.DataFrame(rows).to_csv(tmp, index=False)
    tmp.replace(out)
    return str(out), time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--datasets", nargs="*", help="subset of base dataset names")
    ap.add_argument("--methods", nargs="*", default=PAPER_METHODS)
    ap.add_argument("--out", default=str(OUT), help="directory for per-task CSVs")
    ap.add_argument("--n-jobs", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    args = ap.parse_args()

    tasks = [(n, p, s) for (n, p) in datasets.CONFIGS for s in args.seeds
             if not args.datasets or n in args.datasets]
    # Spread the high-dimensional problems (Arcene: 10k features, Parkinson's: 752) through the
    # queue instead of starting them all at once, which exhausted RAM on a 14 GB machine.
    heavy = [t for t in tasks if t[0] in ("arcene", "parkinsons")]
    light = [t for t in tasks if t[0] not in ("arcene", "parkinsons")]
    step = max(1, len(light) // max(1, len(heavy)))
    tasks = []
    for i, h in enumerate(heavy):
        tasks += [h] + light[i * step:(i + 1) * step]
    tasks += light[len(heavy) * step:]
    print(f"{len(tasks)} tasks on {args.n_jobs} workers", flush=True)
    t0 = time.time()
    for i, (path, secs) in enumerate(Parallel(n_jobs=args.n_jobs, return_as="generator_unordered")(
            delayed(run_task)(n, p, s, args.methods, args.out) for n, p, s in tasks), 1):
        print(f"[{i}/{len(tasks)}] {Path(path).name} {secs:.0f}s (elapsed {time.time() - t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
