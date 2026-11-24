"""Counterfactual SMOTE with the binary-search return bug fixed.

In the authors' `_binary_search` (Counterfactual_SMOTE.py:65-69), the point is only kept when the
LAST search step landed on the majority side; if the last step landed on the minority side the
function returns the hard-coded label "majority" and `fit_resample` discards a perfectly valid
sample. The paper (Sec. 3.2) says the method keeps the last point found inside the minority
safe region and only discards the sample when no step ever reached it. This subclass does that;
everything else (search, safe-region test, sampling loop) is inherited unchanged.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from Counterfactual_SMOTE import CounterfactualSMOTE  # noqa: E402


class CounterfactualSMOTEFixed(CounterfactualSMOTE):

    def _binary_search(self, minority_sample, majority_neighbor):
        direction = minority_sample - majority_neighbor
        low, high = 0.0, 1.0
        last_valid = None
        boundary = self.k_neighbors // 2 + 1 if self.strategy == "flexible" else 1

        for _ in range(self.opt_steps):
            mid = 0.5 * (low + high)
            current_point = majority_neighbor + mid * direction
            d_maj, _ = self.majority_neighbors_model.kneighbors(current_point.reshape(1, -1), self.k_neighbors)
            d_min, _ = self.minority_neighbors_model.kneighbors(current_point.reshape(1, -1), self.k_neighbors)
            distances = np.concatenate([d_maj.ravel(), d_min.ravel()])
            n_majority = np.sum(np.argsort(distances)[: self.k_neighbors] < self.k_neighbors)

            if n_majority >= boundary:   # not minority-safe -> move toward the minority sample
                low = mid
            else:                        # minority-safe -> remember it, move toward the boundary
                high = mid
                last_valid = current_point

        if last_valid is None:
            return None, "majority"      # never reached the safe region -> discard
        return last_valid, "minority"    # closest-to-boundary safe point found
