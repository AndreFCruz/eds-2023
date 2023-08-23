import numpy as np
import pandas as pd

import seaborn as sns
from matplotlib import pyplot as plt

from .postprocessing import compute_inner_and_outer_adjustment_ci, get_envelope_of_postprocessing_frontier


def plot_postprocessing_frontier(
        postproc_results_df: pd.DataFrame,
        perf_metric: str,
        disp_metric: str,
        show_data_type: str,
        model_name: str,
        constant_clf_accuracy: float,
        color: str = "black",
    ):
    """Helper to plot the given post-processing frontier results with 95% confidence intervals.
    """

    # Get envelope of postprocessing adjustment frontier
    postproc_frontier = get_envelope_of_postprocessing_frontier(
        postproc_results_df,
        perf_col=f"{perf_metric}_mean_{show_data_type}",
        disp_col=f"{disp_metric}_mean_{show_data_type}",
        constant_clf_accuracy=constant_clf_accuracy,
    )

    # Get inner and outer confidence intervals
    postproc_frontier_xticks, interior_frontier_yticks, outer_frontier_yticks = \
        compute_inner_and_outer_adjustment_ci(
            postproc_results_df,
            perf_metric=perf_metric,
            disp_metric=disp_metric,
            data_type=show_data_type,
            constant_clf_accuracy=constant_clf_accuracy,
        )

    # Draw upper right portion of the line (dominated but not feasible)
    upper_right_frontier = np.array([
        postproc_frontier[-1],
        (postproc_frontier[-1, 0] - 1e-6, 1.0),
    ])

    sns.lineplot(
        x=upper_right_frontier[:, 0],
        y=upper_right_frontier[:, 1],
        linestyle=":",
        # label=r"dominated",
        color="grey",
    )

    # Plot postprocessing frontier
    sns.lineplot(
        x=postproc_frontier[:, 0],
        y=postproc_frontier[:, 1],
        label=f"post-processing of {model_name}",
        linestyle="-.",
        color=color,
    )

    # Draw confidence intervals (shaded area)
    ax = plt.gca()
    ax.fill_between(
        x=postproc_frontier_xticks,
        y1=interior_frontier_yticks,
        y2=outer_frontier_yticks,
        interpolate=True,
        color=color,
        alpha=0.1,
        label=r"$95\%$ conf. interv.",
    )
