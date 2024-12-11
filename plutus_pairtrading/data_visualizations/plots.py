"""Data Visualization

This module covers data visualization functions 
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.graphics.tsaplots as timeseries_plots

from ..utils.performance import _log_execution_time
import logging

logger = logging.getLogger(__name__)


@_log_execution_time
def plot_timeseries(
    data: pd.DataFrame,
    securities: list,
    plot_title: str = "Time-series Plot",
    legend_location: str = "lower right",
    fig_xsize: int = 16,
    fig_ysize: int = 10,
) -> None:
    """
    Plots the time-series of given securities as a line plot.

    Args:
        data (pd.DataFrame): Input dataset.
        securities (list): List of securities to plot.
        plot_title (str, optional): Title of the plot. Defaults to "Time-series Plot".
        legend_location (str, optional): Location of the legend. Defaults to "lower right".
        fig_xsize (int, optional): Width of the figure. Defaults to 16.
        fig_ysize (int, optional): Height of the figure. Defaults to 10.

    Returns:
        None
    """
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=(fig_xsize, fig_ysize))

    for sec in securities:
        ax.plot(data.index, data[sec], label=sec)

    ax.set_title(plot_title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc=legend_location)
    plt.show()


@_log_execution_time
def plot_dual_timeseries(
    data: pd.DataFrame,
    securities: list,
    plot_title: str = "Dual Time-series Plot",
    legend_location: str = "lower right",
    fig_xsize: int = 16,
    fig_ysize: int = 10,
) -> None:
    """
    Plots two time-series with dual Y-axes.

    Args:
        data (pd.DataFrame): Input dataset.
        securities (list): List of two securities to plot.
        plot_title (str, optional): Title of the plot. Defaults to "Dual Time-series Plot".
        legend_location (str, optional): Location of the legend. Defaults to "lower right".
        fig_xsize (int, optional): Width of the figure. Defaults to 16.
        fig_ysize (int, optional): Height of the figure. Defaults to 10.

    Returns:
        None
    """
    if len(securities) != 2:
        raise ValueError("Dual time-series plot requires exactly two securities.")

    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax1 = plt.subplots(figsize=(fig_xsize, fig_ysize))
    ax2 = ax1.twinx()

    ax1.plot(data.index, data[securities[0]], label=securities[0], color="blue")
    ax2.plot(data.index, data[securities[1]], label=securities[1], color="orange")

    ax1.set_title(plot_title)
    ax1.set_xlabel("Date")
    ax1.set_ylabel(securities[0], color="blue")
    ax2.set_ylabel(securities[1], color="orange")

    ax1.grid(True, linestyle="--", alpha=0.5)

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc=legend_location)
    plt.show()


@_log_execution_time
def plot_correlation_matrix(
    data: pd.DataFrame,
    securities: list,
    plot_title: str = "Correlation Matrix",
    method: str = "spearman",
    fig_xsize: int = 8,
    fig_ysize: int = 6,
) -> None:
    """
    Plots the correlation matrix for given securities.

    Args:
        data (pd.DataFrame): Input dataset.
        securities (list): List of securities to include in the correlation matrix.
        plot_title (str, optional): Title of the plot. Defaults to "Correlation Matrix".
        method (str, optional): Method for computing correlation. Defaults to "spearman".
        fig_xsize (int, optional): Width of the figure. Defaults to 8.
        fig_ysize (int, optional): Height of the figure. Defaults to 6.

    Returns:
        None
    """
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=(fig_xsize, fig_ysize))

    corr_matrix = data[securities].corr(method=method)
    sns.heatmap(corr_matrix, annot=True, cmap="RdBu", center=0, linewidths=0.5, ax=ax)

    ax.set_title(plot_title)
    plt.show()


@_log_execution_time
def plot_acf(
    data: pd.DataFrame,
    security: str,
    num_of_lags: int = 20,
    plot_title: str = "Autocorrelation Plot",
    fig_xsize: int = 8,
    fig_ysize: int = 6,
) -> None:
    """
    Plots the autocorrelation function for a given security.

    Args:
        data (pd.DataFrame): Input dataset.
        security (str): Security to compute autocorrelation for.
        num_of_lags (int, optional): Number of lags to compute. Defaults to 20.
        plot_title (str, optional): Title of the plot. Defaults to "Autocorrelation Plot".
        fig_xsize (int, optional): Width of the figure. Defaults to 8.
        fig_ysize (int, optional): Height of the figure. Defaults to 6.

    Returns:
        None
    """
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=(fig_xsize, fig_ysize))

    timeseries_plots.plot_acf(data[security], lags=num_of_lags, ax=ax)

    ax.set_title(f"{plot_title} ({security})")
    plt.show()


@_log_execution_time
def plot_pacf(
    data: pd.DataFrame,
    security: str,
    num_of_lags: int = 20,
    plot_title: str = "Partial-Autocorrelation Plot",
    fig_xsize: int = 8,
    fig_ysize: int = 6,
) -> None:
    """
    Plots the partial autocorrelation function for a given security.

    Args:
        data (pd.DataFrame): Input dataset.
        security (str): Security to compute partial autocorrelation for.
        num_of_lags (int, optional): Number of lags to compute. Defaults to 20.
        plot_title (str, optional): Title of the plot. Defaults to "Partial-Autocorrelation Plot".
        fig_xsize (int, optional): Width of the figure. Defaults to 8.
        fig_ysize (int, optional): Height of the figure. Defaults to 6.

    Returns:
        None
    """
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=(fig_xsize, fig_ysize))

    timeseries_plots.plot_pacf(data[security], lags=num_of_lags, method="ywm", ax=ax)

    ax.set_title(f"{plot_title} ({security})")
    plt.show()
