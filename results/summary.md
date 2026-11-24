# Reproduction summary

Tasks completed: 72 / 72 (24 problems); fixed-version tasks: 72 / 72.

Statistics only use (problem, classifier) cells where every compared method has results.


## Protocol `per_fold`

### Table 3 — mean F1 (reproduced)

| method | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| Counterfactual SMOTE | 0.603 | 0.671 | 0.634 | 0.618 | 0.610 | 0.506 | 0.614 |
| K-means SMOTE | 0.395 | 0.461 | 0.480 | 0.438 | 0.364 | 0.427 | 0.433 |
| ADASYN | 0.495 | 0.486 | 0.524 | 0.514 | 0.493 | 0.417 | 0.516 |
| Borderline SMOTE 1 | 0.529 | 0.557 | 0.557 | 0.531 | 0.522 | 0.448 | 0.534 |
| Borderline SMOTE 2 | 0.536 | 0.568 | 0.565 | 0.534 | 0.511 | 0.443 | 0.538 |
| Random oversampling | 0.484 | 0.390 | 0.450 | 0.432 | 0.475 | 0.406 | 0.488 |
| Random undersampling | 0.462 | 0.383 | 0.417 | 0.465 | 0.422 | 0.410 | 0.446 |
| SMOTE | 0.511 | 0.493 | 0.519 | 0.511 | 0.503 | 0.422 | 0.517 |
| None | 0.296 | 0.407 | 0.432 | 0.398 | 0.311 | 0.400 | 0.371 |

### Table 3 — reproduced minus paper

| method | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| Counterfactual SMOTE | -0.012 | -0.034 | -0.014 | -0.024 | -0.007 | -0.018 | -0.033 |
| K-means SMOTE | +0.046 | -0.103 | +0.020 | -0.083 | -0.029 | -0.008 | -0.046 |
| ADASYN | -0.027 | -0.033 | -0.022 | -0.017 | -0.006 | -0.010 | -0.031 |
| Borderline SMOTE 1 | -0.010 | -0.030 | -0.007 | -0.031 | -0.003 | -0.014 | -0.033 |
| Borderline SMOTE 2 | -0.008 | -0.025 | -0.006 | -0.024 | -0.001 | -0.015 | -0.033 |
| Random oversampling | -0.028 | -0.031 | -0.037 | -0.032 | -0.016 | -0.020 | -0.041 |
| Random undersampling | -0.020 | -0.013 | -0.017 | -0.012 | -0.023 | -0.005 | -0.025 |
| SMOTE | -0.022 | -0.036 | -0.024 | -0.036 | -0.011 | -0.020 | -0.030 |
| None | -0.048 | -0.045 | -0.017 | -0.030 | -0.065 | -0.023 | -0.034 |

### Table 4 — mean rank (reproduced, average ranks; paper in parentheses)

| method | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| Counterfactual SMOTE | 1.38 (1.75) | 1.0 (1.48) | 1.31 (1.43) | 1.4 (1.57) | 1.04 (1.54) | 1.88 (1.74) | 1.44 (1.73) |
| K-means SMOTE | 6.35 (5.21) | 5.4 (3.7) | 5.52 (4.53) | 6.42 (3.39) | 6.73 (5.11) | 4.77 (3.72) | 5.79 (4.04) |
| ADASYN | 5.31 (3.94) | 5.15 (4.59) | 4.85 (3.52) | 4.65 (3.95) | 5.1 (4.61) | 5.79 (4.14) | 5.02 (4.06) |
| Borderline SMOTE 1 | 3.44 (3.13) | 3.06 (3.11) | 3.27 (2.82) | 3.44 (2.87) | 3.02 (3.27) | 3.48 (2.73) | 3.42 (3.01) |
| Borderline SMOTE 2 | 3.17 (3.55) | 2.88 (3.59) | 3.06 (3.13) | 3.15 (3.26) | 3.6 (3.78) | 3.5 (3.69) | 3.25 (3.41) |
| Random oversampling | 5.88 (4.25) | 7.94 (6.07) | 7.33 (4.77) | 7.35 (5.07) | 5.92 (4.54) | 6.69 (4.29) | 5.98 (4.4) |
| Random undersampling | 6.67 (5.37) | 7.08 (6.81) | 7.1 (6.21) | 5.88 (5.91) | 6.92 (5.6) | 6.5 (5.11) | 7.08 (5.97) |
| SMOTE | 4.12 (3.42) | 4.73 (4.26) | 4.81 (3.52) | 4.56 (3.55) | 4.19 (3.89) | 5.17 (3.29) | 4.77 (3.68) |
| None | 8.69 (5.94) | 7.77 (5.94) | 7.73 (4.8) | 8.17 (5.45) | 8.48 (5.44) | 7.23 (3.98) | 8.25 (5.67) |

### Tables 5–6 — Friedman p-value and Holm-adjusted Wilcoxon p (CF-SMOTE vs each)

|  | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| friedman | 2.5e-23 | 5.4e-28 | 1.8e-23 | 4.3e-23 | 3.0e-25 | 3.1e-15 | 4.9e-21 |
| wilcoxon_holm[K-means SMOTE] | 1.1e-04 | 9.5e-07 | 1.4e-04 | 1.9e-04 | 9.5e-07 | 1.1e-03 | 1.9e-04 |
| wilcoxon_holm[ADASYN] | 1.9e-06 | 9.5e-07 | 5.8e-06 | 1.9e-04 | 9.5e-07 | 2.2e-04 | 1.9e-04 |
| wilcoxon_holm[Borderline SMOTE 1] | 1.1e-04 | 9.5e-07 | 1.4e-04 | 1.9e-04 | 9.5e-07 | 1.1e-03 | 1.9e-04 |
| wilcoxon_holm[Borderline SMOTE 2] | 1.1e-04 | 9.5e-07 | 1.4e-04 | 1.9e-04 | 9.5e-07 | 3.4e-04 | 1.9e-04 |
| wilcoxon_holm[Random oversampling] | 2.5e-06 | 9.5e-07 | 1.4e-04 | 1.9e-04 | 9.5e-07 | 2.2e-04 | 1.9e-04 |
| wilcoxon_holm[Random undersampling] | 2.5e-06 | 9.5e-07 | 5.0e-05 | 8.4e-05 | 9.5e-07 | 2.6e-04 | 1.9e-06 |
| wilcoxon_holm[SMOTE] | 3.0e-06 | 9.5e-07 | 4.8e-06 | 1.9e-04 | 9.5e-07 | 2.3e-04 | 2.6e-04 |
| wilcoxon_holm[None] | 1.1e-04 | 9.5e-07 | 1.4e-04 | 1.9e-04 | 9.5e-07 | 2.2e-04 | 1.9e-04 |

### CF-SMOTE wins (out of 24 problems)

|  | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| CF_wins[K-means SMOTE] | 22 | 24 | 23 | 23 | 23 | 18 | 22 |
| CF_wins[ADASYN] | 23 | 24 | 23 | 22 | 24 | 22 | 22 |
| CF_wins[Borderline SMOTE 1] | 22 | 24 | 22 | 22 | 24 | 19 | 21 |
| CF_wins[Borderline SMOTE 2] | 22 | 24 | 23 | 22 | 24 | 20 | 22 |
| CF_wins[Random oversampling] | 23 | 24 | 23 | 23 | 24 | 22 | 23 |
| CF_wins[Random undersampling] | 23 | 24 | 23 | 21 | 24 | 22 | 23 |
| CF_wins[SMOTE] | 23 | 24 | 23 | 23 | 24 | 21 | 22 |
| CF_wins[None] | 23 | 24 | 23 | 23 | 24 | 23 | 23 |

### Table 7 — % of runs where each CF-SMOTE value was best

| param | value | pct |
|---|---|---|
| k_neighbors | 2 | 70.4 |
| k_neighbors | 3 | 18.2 |
| k_neighbors | 5 | 11.3 |
| opt_steps | 3 | 57.3 |
| opt_steps | 5 | 23.3 |
| opt_steps | 10 | 19.4 |
| n_iter | 3 | 46.4 |
| n_iter | 10 | 20.8 |
| n_iter | 5 | 17.1 |
| n_iter | 15 | 15.8 |
| strategy | strict | 58.3 |
| strategy | flexible | 41.7 |


### Fixed vs original Counterfactual SMOTE (`per_fold`)

|  | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| F1 original | 0.603 | 0.671 | 0.634 | 0.618 | 0.610 | 0.506 | 0.614 |
| F1 fixed | 0.601 | 0.652 | 0.622 | 0.615 | 0.591 | 0.503 | 0.613 |
| F1 SMOTE | 0.511 | 0.493 | 0.519 | 0.511 | 0.503 | 0.422 | 0.517 |

|  | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| fixed > original (problems) | 10 | 6 | 7 | 6 | 4 | 10 | 7 |
| fixed < original (problems) | 13 | 18 | 17 | 17 | 19 | 13 | 16 |

|  | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| Wilcoxon p (fixed vs original) | 6.3e-01 | 2.5e-03 | 6.9e-02 | 2.0e-01 | 6.8e-03 | 3.8e-01 | 1.6e-01 |

#### Table 3 with the fixed version in place of the original (mean F1)

| method | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| Counterfactual SMOTE (fixed) | 0.601 | 0.652 | 0.622 | 0.615 | 0.591 | 0.503 | 0.613 |
| K-means SMOTE | 0.395 | 0.461 | 0.480 | 0.438 | 0.364 | 0.427 | 0.433 |
| ADASYN | 0.495 | 0.486 | 0.524 | 0.514 | 0.493 | 0.417 | 0.516 |
| Borderline SMOTE 1 | 0.529 | 0.557 | 0.557 | 0.531 | 0.522 | 0.448 | 0.534 |
| Borderline SMOTE 2 | 0.536 | 0.568 | 0.565 | 0.534 | 0.511 | 0.443 | 0.538 |
| Random oversampling | 0.484 | 0.390 | 0.450 | 0.432 | 0.475 | 0.406 | 0.488 |
| Random undersampling | 0.462 | 0.383 | 0.417 | 0.465 | 0.422 | 0.410 | 0.446 |
| SMOTE | 0.511 | 0.493 | 0.519 | 0.511 | 0.503 | 0.422 | 0.517 |
| None | 0.296 | 0.407 | 0.432 | 0.398 | 0.311 | 0.400 | 0.371 |

#### Table 4 with the fixed version (mean rank; paper in parentheses)

| method | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| Counterfactual SMOTE (fixed) | 1.29 (1.75) | 1.04 (1.48) | 1.25 (1.43) | 1.27 (1.57) | 1.04 (1.54) | 1.58 (1.74) | 1.25 (1.73) |
| K-means SMOTE | 6.38 (5.21) | 5.35 (3.7) | 5.5 (4.53) | 6.38 (3.39) | 6.73 (5.11) | 4.79 (3.72) | 5.81 (4.04) |
| ADASYN | 5.31 (3.94) | 5.15 (4.59) | 4.88 (3.52) | 4.69 (3.95) | 5.1 (4.61) | 5.85 (4.14) | 5.06 (4.06) |
| Borderline SMOTE 1 | 3.5 (3.13) | 3.06 (3.11) | 3.31 (2.82) | 3.48 (2.87) | 3.02 (3.27) | 3.5 (2.73) | 3.46 (3.01) |
| Borderline SMOTE 2 | 3.19 (3.55) | 2.88 (3.59) | 3.02 (3.13) | 3.19 (3.26) | 3.6 (3.78) | 3.56 (3.69) | 3.23 (3.41) |
| Random oversampling | 5.88 (4.25) | 7.94 (6.07) | 7.35 (4.77) | 7.35 (5.07) | 5.92 (4.54) | 6.71 (4.29) | 6.0 (4.4) |
| Random undersampling | 6.67 (5.37) | 7.08 (6.81) | 7.1 (6.21) | 5.92 (5.91) | 6.92 (5.6) | 6.5 (5.11) | 7.12 (5.97) |
| SMOTE | 4.08 (3.42) | 4.73 (4.26) | 4.83 (3.52) | 4.56 (3.55) | 4.19 (3.89) | 5.25 (3.29) | 4.79 (3.68) |
| None | 8.71 (5.94) | 7.77 (5.94) | 7.75 (4.8) | 8.17 (5.45) | 8.48 (5.44) | 7.25 (3.98) | 8.27 (5.67) |

#### Holm-adjusted Wilcoxon p (fixed CF-SMOTE vs each baseline)

|  | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| wilcoxon_holm[K-means SMOTE] | 1.7e-06 | 9.5e-07 | 3.6e-06 | 1.9e-04 | 9.5e-07 | 3.0e-04 | 1.8e-06 |
| wilcoxon_holm[ADASYN] | 1.4e-06 | 9.5e-07 | 8.1e-05 | 1.9e-04 | 9.5e-07 | 9.5e-07 | 9.1e-06 |
| wilcoxon_holm[Borderline SMOTE 1] | 9.5e-07 | 9.5e-07 | 3.3e-05 | 1.9e-04 | 9.5e-07 | 3.0e-04 | 9.1e-06 |
| wilcoxon_holm[Borderline SMOTE 2] | 1.4e-06 | 9.5e-07 | 1.1e-04 | 1.9e-04 | 9.5e-07 | 3.3e-05 | 1.3e-05 |
| wilcoxon_holm[Random oversampling] | 1.4e-06 | 9.5e-07 | 9.5e-07 | 1.9e-04 | 9.5e-07 | 1.2e-06 | 9.5e-07 |
| wilcoxon_holm[Random undersampling] | 1.4e-06 | 9.5e-07 | 2.0e-05 | 1.8e-05 | 9.5e-07 | 1.3e-04 | 9.5e-07 |
| wilcoxon_holm[SMOTE] | 1.4e-06 | 9.5e-07 | 8.1e-05 | 1.9e-04 | 9.5e-07 | 9.5e-07 | 1.3e-05 |
| wilcoxon_holm[None] | 9.5e-07 | 9.5e-07 | 9.5e-07 | 1.9e-04 | 9.5e-07 | 9.5e-07 | 9.5e-07 |


## Protocol `mean_cv`

### Table 3 — mean F1 (reproduced)

| method | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| Counterfactual SMOTE | 0.550 | 0.539 | 0.557 | 0.551 | 0.536 | 0.470 | 0.564 |
| K-means SMOTE | 0.378 | 0.438 | 0.460 | 0.423 | 0.349 | 0.417 | 0.421 |
| ADASYN | 0.487 | 0.443 | 0.494 | 0.487 | 0.480 | 0.412 | 0.505 |
| Borderline SMOTE 1 | 0.508 | 0.477 | 0.516 | 0.500 | 0.497 | 0.435 | 0.514 |
| Borderline SMOTE 2 | 0.516 | 0.499 | 0.525 | 0.505 | 0.489 | 0.429 | 0.519 |
| Random oversampling | 0.484 | 0.390 | 0.450 | 0.432 | 0.475 | 0.406 | 0.488 |
| Random undersampling | 0.462 | 0.383 | 0.417 | 0.465 | 0.422 | 0.410 | 0.446 |
| SMOTE | 0.501 | 0.448 | 0.490 | 0.493 | 0.489 | 0.418 | 0.508 |
| None | 0.296 | 0.407 | 0.432 | 0.398 | 0.311 | 0.400 | 0.371 |

### Table 3 — reproduced minus paper

| method | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| Counterfactual SMOTE | -0.065 | -0.166 | -0.091 | -0.091 | -0.081 | -0.054 | -0.083 |
| K-means SMOTE | +0.029 | -0.126 | +0.000 | -0.098 | -0.044 | -0.018 | -0.058 |
| ADASYN | -0.035 | -0.076 | -0.052 | -0.044 | -0.019 | -0.015 | -0.042 |
| Borderline SMOTE 1 | -0.031 | -0.110 | -0.048 | -0.062 | -0.028 | -0.027 | -0.053 |
| Borderline SMOTE 2 | -0.028 | -0.094 | -0.046 | -0.053 | -0.023 | -0.029 | -0.052 |
| Random oversampling | -0.028 | -0.031 | -0.037 | -0.032 | -0.016 | -0.020 | -0.041 |
| Random undersampling | -0.020 | -0.013 | -0.017 | -0.012 | -0.023 | -0.005 | -0.025 |
| SMOTE | -0.032 | -0.081 | -0.053 | -0.054 | -0.025 | -0.024 | -0.039 |
| None | -0.048 | -0.045 | -0.017 | -0.030 | -0.065 | -0.023 | -0.034 |

### Table 4 — mean rank (reproduced, average ranks; paper in parentheses)

| method | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| Counterfactual SMOTE | 1.62 (1.75) | 1.08 (1.48) | 1.56 (1.43) | 1.6 (1.57) | 1.58 (1.54) | 2.02 (1.74) | 1.5 (1.73) |
| K-means SMOTE | 6.73 (5.21) | 5.19 (3.7) | 5.52 (4.53) | 6.33 (3.39) | 7.23 (5.11) | 4.96 (3.72) | 6.29 (4.04) |
| ADASYN | 5.4 (3.94) | 5.4 (4.59) | 5.08 (3.52) | 4.92 (3.95) | 4.96 (4.61) | 5.75 (4.14) | 5.06 (4.06) |
| Borderline SMOTE 1 | 3.48 (3.13) | 3.5 (3.11) | 3.6 (2.82) | 3.67 (2.87) | 3.44 (3.27) | 3.81 (2.73) | 3.73 (3.01) |
| Borderline SMOTE 2 | 3.38 (3.55) | 2.83 (3.59) | 3.15 (3.13) | 3.44 (3.26) | 3.52 (3.78) | 3.75 (3.69) | 3.25 (3.41) |
| Random oversampling | 5.38 (4.25) | 7.65 (6.07) | 7.04 (4.77) | 7.02 (5.07) | 5.38 (4.54) | 6.31 (4.29) | 5.56 (4.4) |
| Random undersampling | 6.46 (5.37) | 6.79 (6.81) | 6.6 (6.21) | 5.54 (5.91) | 6.5 (5.6) | 6.25 (5.11) | 6.88 (5.97) |
| SMOTE | 3.92 (3.42) | 5.04 (4.26) | 4.88 (3.52) | 4.31 (3.55) | 3.96 (3.89) | 5.27 (3.29) | 4.48 (3.68) |
| None | 8.65 (5.94) | 7.52 (5.94) | 7.56 (4.8) | 8.17 (5.45) | 8.44 (5.44) | 6.88 (3.98) | 8.25 (5.67) |

### Tables 5–6 — Friedman p-value and Holm-adjusted Wilcoxon p (CF-SMOTE vs each)

|  | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| friedman | 1.3e-21 | 6.7e-24 | 1.5e-18 | 1.3e-19 | 8.9e-22 | 2.9e-11 | 5.4e-20 |
| wilcoxon_holm[K-means SMOTE] | 1.2e-04 | 2.4e-06 | 1.6e-04 | 2.2e-04 | 1.7e-06 | 2.5e-03 | 1.9e-04 |
| wilcoxon_holm[ADASYN] | 1.8e-05 | 9.5e-07 | 2.4e-05 | 2.2e-04 | 1.6e-05 | 2.8e-04 | 3.5e-04 |
| wilcoxon_holm[Borderline SMOTE 1] | 8.4e-04 | 9.5e-07 | 7.5e-04 | 2.2e-04 | 3.2e-04 | 9.7e-03 | 3.5e-04 |
| wilcoxon_holm[Borderline SMOTE 2] | 8.4e-04 | 2.4e-06 | 7.5e-04 | 6.4e-04 | 6.0e-05 | 4.7e-03 | 3.5e-04 |
| wilcoxon_holm[Random oversampling] | 9.5e-06 | 9.5e-07 | 1.6e-04 | 2.2e-04 | 4.2e-06 | 2.8e-04 | 1.9e-04 |
| wilcoxon_holm[Random undersampling] | 1.2e-05 | 9.5e-07 | 1.6e-04 | 6.4e-04 | 2.1e-06 | 1.1e-03 | 2.9e-06 |
| wilcoxon_holm[SMOTE] | 3.3e-05 | 9.5e-07 | 3.6e-05 | 2.2e-04 | 6.0e-05 | 4.0e-04 | 3.5e-04 |
| wilcoxon_holm[None] | 1.1e-04 | 9.5e-07 | 1.6e-04 | 2.2e-04 | 9.5e-07 | 2.2e-04 | 1.9e-04 |

### CF-SMOTE wins (out of 24 problems)

|  | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| CF_wins[K-means SMOTE] | 22 | 23 | 22 | 21 | 23 | 18 | 22 |
| CF_wins[ADASYN] | 23 | 24 | 22 | 22 | 21 | 22 | 22 |
| CF_wins[Borderline SMOTE 1] | 20 | 24 | 21 | 22 | 22 | 18 | 21 |
| CF_wins[Borderline SMOTE 2] | 19 | 23 | 21 | 20 | 22 | 18 | 21 |
| CF_wins[Random oversampling] | 23 | 24 | 23 | 23 | 22 | 22 | 23 |
| CF_wins[Random undersampling] | 23 | 24 | 22 | 20 | 23 | 21 | 23 |
| CF_wins[SMOTE] | 22 | 24 | 23 | 23 | 21 | 21 | 22 |
| CF_wins[None] | 23 | 24 | 23 | 23 | 24 | 23 | 23 |


### Fixed vs original Counterfactual SMOTE (`mean_cv`)

|  | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| F1 original | 0.550 | 0.539 | 0.557 | 0.551 | 0.536 | 0.470 | 0.564 |
| F1 fixed | 0.549 | 0.540 | 0.551 | 0.553 | 0.530 | 0.466 | 0.560 |
| F1 SMOTE | 0.501 | 0.448 | 0.490 | 0.493 | 0.489 | 0.418 | 0.508 |

|  | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| fixed > original (problems) | 10 | 10 | 11 | 10 | 8 | 8 | 8 |
| fixed < original (problems) | 13 | 14 | 13 | 13 | 16 | 16 | 16 |

|  | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| Wilcoxon p (fixed vs original) | 6.7e-01 | 6.4e-01 | 2.4e-01 | 9.8e-01 | 2.6e-01 | 1.5e-01 | 2.2e-01 |

#### Table 3 with the fixed version in place of the original (mean F1)

| method | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| Counterfactual SMOTE (fixed) | 0.549 | 0.540 | 0.551 | 0.553 | 0.530 | 0.466 | 0.560 |
| K-means SMOTE | 0.378 | 0.438 | 0.460 | 0.423 | 0.349 | 0.417 | 0.421 |
| ADASYN | 0.487 | 0.443 | 0.494 | 0.487 | 0.480 | 0.412 | 0.505 |
| Borderline SMOTE 1 | 0.508 | 0.477 | 0.516 | 0.500 | 0.497 | 0.435 | 0.514 |
| Borderline SMOTE 2 | 0.516 | 0.499 | 0.525 | 0.505 | 0.489 | 0.429 | 0.519 |
| Random oversampling | 0.484 | 0.390 | 0.450 | 0.432 | 0.475 | 0.406 | 0.488 |
| Random undersampling | 0.462 | 0.383 | 0.417 | 0.465 | 0.422 | 0.410 | 0.446 |
| SMOTE | 0.501 | 0.448 | 0.490 | 0.493 | 0.489 | 0.418 | 0.508 |
| None | 0.296 | 0.407 | 0.432 | 0.398 | 0.311 | 0.400 | 0.371 |

#### Table 4 with the fixed version (mean rank; paper in parentheses)

| method | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| Counterfactual SMOTE (fixed) | 1.75 (1.75) | 1.12 (1.48) | 1.54 (1.43) | 1.73 (1.57) | 1.42 (1.54) | 2.0 (1.74) | 1.75 (1.73) |
| K-means SMOTE | 6.67 (5.21) | 5.19 (3.7) | 5.54 (4.53) | 6.33 (3.39) | 7.23 (5.11) | 4.9 (3.72) | 6.31 (4.04) |
| ADASYN | 5.35 (3.94) | 5.4 (4.59) | 5.15 (3.52) | 4.92 (3.95) | 5.0 (4.61) | 5.79 (4.14) | 5.02 (4.06) |
| Borderline SMOTE 1 | 3.46 (3.13) | 3.5 (3.11) | 3.56 (2.82) | 3.62 (2.87) | 3.44 (3.27) | 3.75 (2.73) | 3.62 (3.01) |
| Borderline SMOTE 2 | 3.44 (3.55) | 2.79 (3.59) | 3.1 (3.13) | 3.48 (3.26) | 3.56 (3.78) | 3.81 (3.69) | 3.15 (3.41) |
| Random oversampling | 5.38 (4.25) | 7.65 (6.07) | 7.06 (4.77) | 7.02 (5.07) | 5.38 (4.54) | 6.33 (4.29) | 5.54 (4.4) |
| Random undersampling | 6.42 (5.37) | 6.79 (6.81) | 6.6 (6.21) | 5.54 (5.91) | 6.54 (5.6) | 6.25 (5.11) | 6.92 (5.97) |
| SMOTE | 3.88 (3.42) | 5.04 (4.26) | 4.85 (3.52) | 4.19 (3.55) | 4.0 (3.89) | 5.27 (3.29) | 4.42 (3.68) |
| None | 8.67 (5.94) | 7.52 (5.94) | 7.58 (4.8) | 8.17 (5.45) | 8.44 (5.44) | 6.9 (3.98) | 8.27 (5.67) |

#### Holm-adjusted Wilcoxon p (fixed CF-SMOTE vs each baseline)

|  | LR | DT | XGBoost | RF | KNN | GNB | MLP |
|---|---|---|---|---|---|---|---|
| wilcoxon_holm[K-means SMOTE] | 1.1e-05 | 2.4e-06 | 5.0e-06 | 2.2e-04 | 1.4e-06 | 2.6e-03 | 3.6e-06 |
| wilcoxon_holm[ADASYN] | 7.2e-06 | 9.5e-07 | 1.4e-04 | 2.2e-04 | 4.2e-06 | 9.5e-07 | 1.9e-04 |
| wilcoxon_holm[Borderline SMOTE 1] | 2.5e-04 | 9.5e-07 | 3.5e-04 | 2.2e-04 | 9.1e-05 | 6.5e-03 | 3.5e-04 |
| wilcoxon_holm[Borderline SMOTE 2] | 3.7e-04 | 2.4e-06 | 2.8e-03 | 2.2e-04 | 2.6e-05 | 2.6e-03 | 1.8e-03 |
| wilcoxon_holm[Random oversampling] | 2.5e-06 | 9.5e-07 | 9.5e-07 | 2.2e-04 | 2.1e-05 | 2.1e-06 | 2.6e-05 |
| wilcoxon_holm[Random undersampling] | 1.2e-05 | 9.5e-07 | 1.4e-04 | 2.2e-04 | 9.5e-07 | 2.6e-03 | 9.5e-07 |
| wilcoxon_holm[SMOTE] | 2.0e-05 | 9.5e-07 | 1.4e-04 | 2.2e-04 | 2.1e-05 | 1.1e-05 | 1.2e-04 |
| wilcoxon_holm[None] | 9.5e-07 | 9.5e-07 | 9.5e-07 | 2.2e-04 | 9.5e-07 | 9.5e-07 | 9.5e-07 |


## Resampler failures (fell back to unresampled data)

| method | failed configs (%) |
|---|---|
| ADASYN | 5.3 |
| Borderline SMOTE 1 | 3.8 |
| Borderline SMOTE 2 | 0.0 |
| Counterfactual SMOTE | 1.9 |
| Counterfactual SMOTE (fixed) | 1.9 |
| K-means SMOTE | 79.8 |
| None | 0.0 |
| Random oversampling | 0.0 |
| Random undersampling | 0.0 |
| SMOTE | 5.3 |