"""Aggregate results/raw/*.csv into the paper's Tables 3-7 and compare with the published values.

Two hyperparameter-selection protocols are reported:
  per_fold : for every fold keep the config with the best test F1 (literal reading of Sec. 4.4:
             "the scores corresponding to the best combination of hyperparameters are stored").
             Optimistic, and favours methods with large grids.
  mean_cv  : one config per (problem, seed, method, classifier), chosen by mean F1 over the
             5 folds. Still selected on test folds, but much less optimistic.
Scores are averaged over folds, then over seeds -> one score per (problem, method, classifier).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, wilcoxon

ROOT = Path(__file__).resolve().parent.parent
RAW, OUT = ROOT / "results" / "raw", ROOT / "results"

METHODS = ["Counterfactual SMOTE", "K-means SMOTE", "ADASYN", "Borderline SMOTE 1",
           "Borderline SMOTE 2", "Random oversampling", "Random undersampling", "SMOTE", "None"]
CLFS = ["LR", "DT", "XGBoost", "RF", "KNN", "GNB", "MLP"]
CF = "Counterfactual SMOTE"
FIX = "Counterfactual SMOTE (fixed)"
RAW_FIXED = ROOT / "results" / "raw_fixed"

# Published values (Table 3: mean F1, Table 4: mean rank), rows in METHODS order.
PAPER_F1 = pd.DataFrame({
    "LR": [.615, .349, .522, .539, .544, .512, .482, .533, .344],
    "DT": [.705, .564, .519, .587, .593, .421, .396, .529, .452],
    "XGBoost": [.648, .460, .546, .564, .571, .487, .434, .543, .449],
    "RF": [.642, .521, .531, .562, .558, .464, .477, .547, .428],
    "KNN": [.617, .393, .499, .525, .512, .491, .445, .514, .376],
    "GNB": [.524, .435, .427, .462, .458, .426, .415, .442, .423],
    "MLP": [.647, .479, .547, .567, .571, .529, .471, .547, .405]}, index=METHODS)
PAPER_RANK = pd.DataFrame({
    "LR": [1.75, 5.21, 3.94, 3.13, 3.55, 4.25, 5.37, 3.42, 5.94],
    "DT": [1.48, 3.70, 4.59, 3.11, 3.59, 6.07, 6.81, 4.26, 5.94],
    "XGBoost": [1.43, 4.53, 3.52, 2.82, 3.13, 4.77, 6.21, 3.52, 4.80],
    "RF": [1.57, 3.39, 3.95, 2.87, 3.26, 5.07, 5.91, 3.55, 5.45],
    "KNN": [1.54, 5.11, 4.61, 3.27, 3.78, 4.54, 5.60, 3.89, 5.44],
    "GNB": [1.74, 3.72, 4.14, 2.73, 3.69, 4.29, 5.11, 3.29, 3.98],
    "MLP": [1.73, 4.04, 4.06, 3.01, 3.41, 4.40, 5.97, 3.68, 5.67]}, index=METHODS)

KEY = ["dataset", "pct", "seed", "method", "classifier"]


def select(df, protocol):
    if protocol == "per_fold":
        best = df.loc[df.groupby(KEY + ["fold"])["f1"].idxmax()]
    else:
        cfg_mean = df.groupby(KEY + ["config_id"])["f1"].mean().reset_index()
        best_cfg = cfg_mean.loc[cfg_mean.groupby(KEY)["f1"].idxmax(), KEY + ["config_id"]]
        best = df.merge(best_cfg, on=KEY + ["config_id"])
    per_seed = best.groupby(KEY)["f1"].mean().reset_index()
    scores = per_seed.groupby(["dataset", "pct", "method", "classifier"])["f1"].mean().reset_index()
    return best, scores


def fmt_pm(mean, std):
    return mean.round(3).astype(str) + " ± " + std.round(2).astype(str)


def tables(scores, cf=CF):
    """Tables 3-6 for the 9-method comparison, with `cf` as the Counterfactual SMOTE variant."""
    methods = [cf] + METHODS[1:]
    wide = scores.pivot_table(index=["dataset", "pct", "classifier"], columns="method", values="f1")
    wide = wide[[m for m in methods if m in wide.columns]].dropna()
    methods = list(wide.columns)
    f1_mean = wide.groupby("classifier").mean().T[CLFS]
    f1_std = wide.groupby("classifier").std().T[CLFS]
    ranks = wide.rank(axis=1, ascending=False, method="average")
    rank_mean = ranks.groupby("classifier").mean().T[CLFS]
    rank_std = ranks.groupby("classifier").std().T[CLFS]
    stats = {}
    for c in CLFS:
        w = wide.xs(c, level="classifier")
        fried_p = friedmanchisquare(*[w[m] for m in methods]).pvalue
        raw_p = {m: wilcoxon(w[cf], w[m]).pvalue if (w[cf] != w[m]).any() else 1.0
                 for m in methods if m != cf}
        # Holm step-down adjustment over the 8 comparisons.
        order = sorted(raw_p, key=raw_p.get)
        adj, running = {}, 0.0
        for i, m in enumerate(order):
            running = max(running, min(1.0, (len(order) - i) * raw_p[m]))
            adj[m] = running
        stats[c] = dict(friedman=fried_p, **{f"wilcoxon_holm[{m}]": adj[m] for m in methods if m != cf},
                        **{f"CF_wins[{m}]": int((w[cf] > w[m]).sum()) for m in methods if m != cf})
    f1_mean.index.name = rank_mean.index.name = "method"
    return f1_mean, f1_std, rank_mean, rank_std, pd.DataFrame(stats)


def fixed_section(scores, protocol):
    """Original vs fixed Counterfactual SMOTE: head-to-head, plus the paper tables with the fix swapped in."""
    if FIX not in set(scores["method"]):
        return []
    wide = scores.pivot_table(index=["dataset", "pct", "classifier"], columns="method", values="f1").dropna()
    h2h = {}
    for c in CLFS:
        w = wide.xs(c, level="classifier")
        h2h[c] = {"F1 original": w[CF].mean(), "F1 fixed": w[FIX].mean(), "F1 SMOTE": w["SMOTE"].mean(),
                  "fixed > original (problems)": int((w[FIX] > w[CF]).sum()),
                  "fixed < original (problems)": int((w[FIX] < w[CF]).sum()),
                  "Wilcoxon p (fixed vs original)": wilcoxon(w[FIX], w[CF]).pvalue
                  if (w[FIX] != w[CF]).any() else 1.0}
    h2h = pd.DataFrame(h2h)
    f1m, _, rkm, _, st = tables(scores, cf=FIX)
    return [f"\n### Fixed vs original Counterfactual SMOTE (`{protocol}`)\n",
            md(h2h.loc[[i for i in h2h.index if i.startswith("F1")]]), "",
            md(h2h.loc[[i for i in h2h.index if "problems" in i]].astype(int)), "",
            md(h2h.loc[["Wilcoxon p (fixed vs original)"]], "{:.1e}"), "",
            "#### Table 3 with the fixed version in place of the original (mean F1)\n", md(f1m), "",
            "#### Table 4 with the fixed version (mean rank; paper in parentheses)\n",
            md(rkm.round(2).astype(str) + " (" + PAPER_RANK.rename(index={CF: FIX}).loc[rkm.index].astype(str) + ")"),
            "", "#### Holm-adjusted Wilcoxon p (fixed CF-SMOTE vs each baseline)\n",
            md(st.loc[[i for i in st.index if i.startswith("wilcoxon")]], "{:.1e}"), ""]


def md(df, floatfmt="{:.3f}"):
    df = df.copy()
    for c in df.columns:
        if pd.api.types.is_float_dtype(df[c]):
            df[c] = df[c].map(floatfmt.format)
    head = "| " + " | ".join([df.index.name or ""] + list(map(str, df.columns))) + " |"
    sep = "|" + "---|" * (len(df.columns) + 1)
    body = ["| " + " | ".join([str(i)] + list(map(str, r))) + " |" for i, r in zip(df.index, df.values)]
    return "\n".join([head, sep] + body)


def main():
    files = sorted(RAW.glob("*.csv"))
    # keep_default_na=False: otherwise the method name "None" is parsed as NaN.
    df = pd.concat([pd.read_csv(f, keep_default_na=False) for f in files], ignore_index=True)
    fixed_files = sorted(RAW_FIXED.glob("*.csv"))
    if fixed_files:
        df = pd.concat([df] + [pd.read_csv(f, keep_default_na=False) for f in fixed_files], ignore_index=True)
    n_tasks = df[df.method == CF].groupby(["dataset", "pct", "seed"]).ngroups
    n_fixed = df[df.method == FIX].groupby(["dataset", "pct", "seed"]).ngroups
    lines = [f"# Reproduction summary\n\nTasks completed: {n_tasks} / 72 "
             f"({df.groupby(['dataset', 'pct']).ngroups} problems); fixed-version tasks: {n_fixed} / 72.\n",
             "Statistics only use (problem, classifier) cells where every compared method has results.\n"]
    if n_tasks < 72 or 0 < n_fixed < 72:
        lines.append("**Partial results** — statistics below cover only finished tasks.\n")

    for protocol in ["per_fold", "mean_cv"]:
        best, scores = select(df, protocol)
        scores.to_csv(OUT / f"scores_{protocol}.csv", index=False)
        f1m, f1s, rkm, rks, st = tables(scores)
        lines += [f"\n## Protocol `{protocol}`\n",
                  "### Table 3 — mean F1 (reproduced)\n", md(f1m), "",
                  "### Table 3 — reproduced minus paper\n", md(f1m - PAPER_F1, "{:+.3f}"), "",
                  "### Table 4 — mean rank (reproduced, average ranks; paper in parentheses)\n",
                  md(rkm.round(2).astype(str) + " (" + PAPER_RANK.astype(str) + ")"), "",
                  "### Tables 5–6 — Friedman p-value and Holm-adjusted Wilcoxon p (CF-SMOTE vs each)\n",
                  md(st.loc[[i for i in st.index if not i.startswith("CF_wins")]], "{:.1e}"), "",
                  f"### CF-SMOTE wins (out of {scores.groupby(['dataset', 'pct']).ngroups} problems)\n",
                  md(st.loc[[i for i in st.index if i.startswith("CF_wins")]].astype(int)), ""]
        if protocol == "per_fold":
            cf = best[best.method == CF].copy()
            cfg = cf["config"].map(eval).apply(pd.Series)
            t7 = pd.concat([(cfg[p].value_counts(normalize=True) * 100).rename("pct").to_frame()
                            .assign(param=p) for p in ["k_neighbors", "opt_steps", "n_iter", "strategy"]])
            t7.index.name = "value"
            lines += ["### Table 7 — % of runs where each CF-SMOTE value was best\n",
                      md(t7.reset_index().set_index("param"), "{:.1f}"), ""]
        lines += fixed_section(scores, protocol)
    fail = df.groupby("method")["failed"].mean().mul(100).round(1).rename("failed configs (%)")
    lines += ["\n## Resampler failures (fell back to unresampled data)\n", md(fail.to_frame(), "{:.1f}")]
    (OUT / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    sys.exit(main())
