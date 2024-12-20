"""Data Visualization

This module covers data visualization functions 
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as sp


import plotly.graph_objects as go
from typing import List
import pandas as pd

DEFAULT_LINE_COLORS = [
    "#001219",
    "#005f73",
    "#0a9396",
    "#94d2bd",
    "#e9d8a6",
    "#ee9b00",
    "#ca6702",
    "#bb3e03",
    "#ae2012",
    "#9b2226",
]


def plot_timeseries(
    data: pd.DataFrame,
    securities: List[str],
    plot_title: str = "Time-series Plot",
    x_label: str = "Time",
    y_label: str = "Value",
    legend_horizontal: str = "right",
    legend_vertical: str = "middle",
    legend_orientation: str = "v",
    legend_inside: bool = False,
    fig_xsize: int = 1000,
    fig_ysize: int = 600,
    background_color: str = "#F1F1F1",
    line_colors: List[str] = None,
    grid_color: str = "lightgray",
    grid_width: int = 1,
    grid_dash: str = "solid",
) -> go.Figure:
    """
    Plots the time-series of given securities using Plotly with flexible legend positioning.

    Args:
        data (pd.DataFrame): Pandas dataframe with time-series data.
        securities (List[str]): List of securities to plot.
        plot_title (str, optional): Title of the plot. Defaults to "Time-series Plot".
        x_label (str, optional): Label for the X-axis. Defaults to "Time".
        y_label (str, optional): Label for the Y-axis. Defaults to "Value".
        legend_horizontal (str, optional): Horizontal position of the legend ("left", "center", "right").
        legend_vertical (str, optional): Vertical position of the legend ("top", "middle", "bottom").
        legend_orientation (str, optional): Orientation of the legend ("v" for vertical, "h" for horizontal). Defaults to "v".
        legend_inside (bool, optional): Whether to place the legend inside the plot area. Defaults to False (outside).
        fig_xsize (int, optional): Width of the figure in pixels. Defaults to 1000.
        fig_ysize (int, optional): Height of the figure in pixels. Defaults to 600.
        background_color (str, optional): Background color of the plot area. Defaults to #F1F1F1.
        line_colors (List[str], optional): List of custom line colors for the securities. Defaults to None.
        grid_color (str, optional): Gridline color. Defaults to "lightgray".
        grid_width (int, optional): Gridline width. Defaults to 1.
        grid_dash (str, optional): Gridline style ("solid", "dot", "dash"). Defaults to "solid".

    Returns:
        go.Figure: Plotly Figure object.
    """

    # Define default line colors
    if line_colors is None:
        line_colors = DEFAULT_LINE_COLORS * (
            len(securities) // len(DEFAULT_LINE_COLORS) + 1
        )

    fig = go.Figure()

    # Add each security as a line plot
    for i, sec in enumerate(securities):
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data[sec],
                mode="lines",
                name=sec,
                line=dict(color=line_colors[i], width=2),
            )
        )

    # Configure legend position
    legend_x = {"left": 0, "center": 0.5, "right": 1.01}[legend_horizontal]
    legend_y = {"bottom": 0, "middle": 0.5, "top": 1.01}[legend_vertical]

    if legend_inside:
        # Adjust legend inside the plot
        legend_x = legend_x * 0.8 + 0.1  # Keep it slightly away from the edge
        legend_y = legend_y * 0.8 + 0.1
    else:
        # Legend outside the plot area
        if legend_vertical == "bottom":
            legend_y = -0.2  # Place below the plot
        elif legend_vertical == "top":
            legend_y = 1.2  # Place above the plot

    fig.update_layout(
        title=dict(text=plot_title, x=0.5, xanchor="center", font=dict(size=20)),
        xaxis=dict(
            title=x_label,
            showgrid=True,
            gridcolor=grid_color,
            gridwidth=grid_width,
            griddash=grid_dash,
            zeroline=False,
        ),
        yaxis=dict(
            title=y_label,
            showgrid=True,
            gridcolor=grid_color,
            gridwidth=grid_width,
            griddash=grid_dash,
            zeroline=False,
        ),
        legend=dict(
            x=legend_x,
            y=legend_y,
            bgcolor=(
                "rgba(255, 255, 255, 0.7)"
                if legend_inside
                else "rgba(255, 255, 255, 0)"
            ),
            bordercolor="gray",
            borderwidth=1,
            orientation=legend_orientation,
            traceorder="normal",
        ),
        plot_bgcolor=background_color,
        width=fig_xsize,
        height=fig_ysize,
    )

    return fig


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
