"""Utils for evaluating model metrics.

Based on: https://github.com/socialfoundations/error-parity/blob/supp-materials/scripts/utils/metrics.py
"""

import statistics

import numpy as np
from numpy.random import default_rng
from hpt.evaluation import evaluate_predictions

from .commons import join_dictionaries


def bootstrap_results(
        y_true: np.ndarray,
        y_pred_scores: np.ndarray,
        sensitive_attr: np.ndarray,
        k: int = 200,
        confidence_pct: float = 95,
        seed: int = 42,
    ) -> tuple[dict, dict]:
    assert len(y_true) == len(y_pred_scores)
    rng = default_rng(seed=seed)

    # Draw k bootstrap samples with replacement
    results = []
    for _ in range(k):

        # Indices of current bootstrap sample
        indices = rng.choice(len(y_true), replace=True, size=len(y_true))

        # Evaluate predictions on this bootstrap sample
        results.append(evaluate_predictions(
            y_true=y_true[indices],
            y_pred_scores=y_pred_scores[indices],
            sensitive_attribute=sensitive_attr[indices],
            threshold=0.50,
        ))

    # Compute statistics from bootstrapped results
    all_metrics = set(results[0].keys())

    bt_mean = {}
    bt_stdev = {}
    bt_percentiles = {}

    low_percentile = (100 - confidence_pct) / 2
    confidence_percentiles = [low_percentile, 100 - low_percentile]

    for m in all_metrics:
        metric_values = [r[m] for r in results]

        bt_mean[m] = statistics.mean(metric_values)
        bt_stdev[m] = statistics.stdev(metric_values)
        bt_percentiles[m] = tuple(np.percentile(metric_values, confidence_percentiles))

    return bt_mean, bt_stdev, bt_percentiles


def evaluate_predictions_bootstrap(*args, **kwargs) -> dict:
    """Helper to make `bootstrap_results` return similar to that of
    `hpt.evaluate_predictions`, i.e., a dict of metric->value.
    """

    bt_mean, bt_stdev, bt_percentiles = bootstrap_results(*args, **kwargs)

    return join_dictionaries(*(
        {
            f"{metric}_bootstrap": bt_mean[metric],
            f"{metric}_stdev_bootstrap": bt_stdev[metric],
            f"{metric}_low-percentile_bootstrap": bt_percentiles[metric][0],
            f"{metric}_high-percentile_bootstrap": bt_percentiles[metric][1],
        }
        for metric in sorted(bt_mean.keys())
    ))
