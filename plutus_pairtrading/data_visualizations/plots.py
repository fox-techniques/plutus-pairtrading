"""Data Visualization

This module covers data visualization functions 
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as sp


def plot_timeseries(
    data: pd.DataFrame,
    securities: list,
    plot_title: str = "Time-series Plot",
    legend_location: str = "bottom center",
) -> None:
    """
    Plots the time-series of given securities using Plotly.

    Args:
        data (pd.DataFrame): Input dataset.
        securities (list): List of securities to plot.
        plot_title (str, optional): Title of the plot. Defaults to "Time-series Plot".
        legend_location (str, optional): Location of the legend. Defaults to "bottom center".

    Returns:
        None: Displays the interactive plot.
    """
    fig = go.Figure()
    for sec in securities:
        fig.add_trace(go.Scatter(x=data.index, y=data[sec], mode="lines", name=sec))

    fig.update_layout(
        title=plot_title,
        xaxis_title="Date",
        yaxis_title="Value",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
    )
    fig.show()


def plot_dual_timeseries(
    data: pd.DataFrame,
    securities: list,
    plot_title: str = "Dual Time-series Plot",
) -> None:
    """
    Plots two time-series with dual Y-axes using Plotly.

    Args:
        data (pd.DataFrame): Input dataset.
        securities (list): List of two securities to plot.
        plot_title (str, optional): Title of the plot. Defaults to "Dual Time-series Plot".

    Returns:
        None: Displays the interactive plot.
    """
    if len(securities) != 2:
        raise ValueError("Dual time-series plot requires exactly two securities.")

    fig = sp.make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=data.index, y=data[securities[0]], name=securities[0]),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=data.index, y=data[securities[1]], name=securities[1]),
        secondary_y=True,
    )

    fig.update_layout(
        title=plot_title,
        xaxis_title="Date",
        yaxis_title_left=f"{securities[0]}",
        yaxis_title_right=f"{securities[1]}",
    )
    fig.show()


def plot_correlation_matrix(
    data: pd.DataFrame,
    securities: list,
    plot_title: str = "Correlation Matrix",
    method: str = "spearman",
) -> None:
    """
    Plots the correlation matrix for given securities using Plotly.

    Args:
        data (pd.DataFrame): Input dataset.
        securities (list): List of securities to include in the correlation matrix.
        plot_title (str, optional): Title of the plot. Defaults to "Correlation Matrix".
        method (str, optional): Method for computing correlation. Defaults to "spearman".

    Returns:
        None: Displays the interactive plot.
    """
    corr_matrix = data[securities].corr(method=method)
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        title=plot_title,
    )
    fig.show()


def plot_acf(
    data: pd.DataFrame,
    security: str,
    num_of_lags: int = 20,
    plot_title: str = "Autocorrelation Plot",
) -> None:
    """
    Plots the autocorrelation function for a given security using Plotly.

    Args:
        data (pd.DataFrame): Input dataset.
        security (str): Security to compute autocorrelation for.
        num_of_lags (int, optional): Number of lags to compute. Defaults to 20.
        plot_title (str, optional): Title of the plot. Defaults to "Autocorrelation Plot".

    Returns:
        None: Displays the interactive plot.
    """
    from statsmodels.graphics.tsaplots import acf

    acf_values = acf(data[security], nlags=num_of_lags)
    fig = px.bar(
        x=list(range(len(acf_values))),
        y=acf_values,
        labels={"x": "Lag", "y": "Autocorrelation"},
        title=plot_title,
    )
    fig.show()


def plot_pacf(
    data: pd.DataFrame,
    security: str,
    num_of_lags: int = 20,
    plot_title: str = "Partial-Autocorrelation Plot",
) -> None:
    """
    Plots the partial autocorrelation function for a given security using Plotly.

    Args:
        data (pd.DataFrame): Input dataset.
        security (str): Security to compute partial autocorrelation for.
        num_of_lags (int, optional): Number of lags to compute. Defaults to 20.
        plot_title (str, optional): Title of the plot. Defaults to "Partial-Autocorrelation Plot".

    Returns:
        None: Displays the interactive plot.
    """
    from statsmodels.graphics.tsaplots import pacf

    pacf_values = pacf(data[security], nlags=num_of_lags)
    fig = px.bar(
        x=list(range(len(pacf_values))),
        y=pacf_values,
        labels={"x": "Lag", "y": "Partial Autocorrelation"},
        title=plot_title,
    )
    fig.show()
