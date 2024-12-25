"""Data Visualization

This module covers data visualization functions 
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from typing import List, Optional
from statsmodels.tsa.stattools import acf, pacf

from ..utils.performance import _log_execution_time
import logging

logger = logging.getLogger(__name__)

DEFAULT_LINE_COLORS = [
    "#636EFA",
    "#EF553B",
    "#00CC96",
    "#AB63FA",
    "#FFA15A",
    "#19D3F3",
    "#FF6692",
    "#B6E880",
    "#FF97FF",
    "#FECB52",
    "#1F77B4",
    "#FF7F0E",
    "#2CA02C",
    "#D62728",
    "#9467BD",
    "#8C564B",
    "#E377C2",
    "#7F7F7F",
    "#BCBD22",
    "#17BECF",
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


@_log_execution_time
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
    date_format: str = "%d-%m-%Y",
    date_angle: int = -45,
) -> go.Figure:
    """
    Plots the time-series of given securities using Plotly with flexible legend positioning and date formatting.

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
        date_format (str, optional): Format for x-axis date labels. Defaults to "%d-%m-%Y".
        date_angle (int, optional): Angle for the date labels. Defaults to -45.

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
            tickformat=date_format,
            tickangle=date_angle,
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


@_log_execution_time
def plot_dual_timeseries(
    data: pd.DataFrame,
    securities: List[str],
    plot_title: str = "Dual Time-series Plot",
    x_label: str = "Time",
    y_left_label: str = "",
    y_right_label: str = "",
    fig_xsize: int = 1000,
    fig_ysize: int = 600,
    background_color: str = "#F1F1F1",
    line_colors: Optional[List[str]] = None,
    date_format: str = "%d-%m-%Y",
    date_angle: int = -45,
) -> go.Figure:
    """
    Plots two time-series with dual Y-axes using Plotly, removing the legend and coloring Y-axes to match line colors.

    Args:
        data (pd.DataFrame): Input dataset.
        securities (List[str]): List of two securities to plot.
        plot_title (str, optional): Title of the plot. Defaults to "Dual Time-series Plot".
        x_label (str, optional): Label for the X-axis. Defaults to "Time".
        y_left_label (str, optional): Label for the left Y-axis. Defaults to the first security.
        y_right_label (str, optional): Label for the right Y-axis. Defaults to the second security.
        fig_xsize (int, optional): Width of the figure in pixels. Defaults to 1000.
        fig_ysize (int, optional): Height of the figure in pixels. Defaults to 600.
        background_color (str, optional): Background color of the plot area. Defaults to #F1F1F1.
        line_colors (Optional[List[str]], optional): List of custom line colors for the securities. Defaults to None.
        date_format (str, optional): Format for x-axis date labels. Defaults to "%d-%m-%Y".
        date_angle (int, optional): Angle for the date labels. Defaults to -45.

    Returns:
        go.Figure: Plotly Figure object.
    """
    if len(securities) != 2:
        raise ValueError("Dual time-series plot requires exactly two securities.")

    # Default line colors
    if line_colors is None:
        line_colors = DEFAULT_LINE_COLORS

    # Assign default Y-axis labels
    if y_left_label == "":
        y_left_label = str(securities[0])
    if y_right_label == "":
        y_right_label = str(securities[1])

    fig = go.Figure()

    # Left Y-axis plot
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data[securities[0]],
            mode="lines",
            line=dict(color=line_colors[0], width=2),
            yaxis="y1",
        )
    )

    # Right Y-axis plot
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data[securities[1]],
            mode="lines",
            line=dict(color=line_colors[1], width=2),
            yaxis="y2",
        )
    )

    # Update layout
    fig.update_layout(
        title=dict(text=plot_title, x=0.5, xanchor="center", font=dict(size=20)),
        xaxis=dict(
            title=x_label,
            tickformat=date_format,
            tickangle=date_angle,
        ),
        yaxis=dict(
            title=y_left_label,
            titlefont=dict(color=line_colors[0]),
            tickfont=dict(color=line_colors[0]),
            showgrid=True,
        ),
        yaxis2=dict(
            title=y_right_label,
            titlefont=dict(color=line_colors[1]),
            tickfont=dict(color=line_colors[1]),
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        plot_bgcolor=background_color,
        width=fig_xsize,
        height=fig_ysize,
        showlegend=False,  # Remove legend
    )

    return fig


@_log_execution_time
def plot_correlation_matrix(
    data: pd.DataFrame,
    securities: List[str],
    plot_title: str = "Correlation Matrix",
    method: str = "spearman",
    fig_xsize: int = 800,
    fig_ysize: int = 600,
) -> go.Figure:
    """
    Plots the correlation matrix for given securities using Plotly.

    Args:
        data (pd.DataFrame): Input dataset.
        securities (List[str]): List of securities to include in the correlation matrix.
        plot_title (str, optional): Title of the plot. Defaults to "Correlation Matrix".
        method (str, optional): Method for computing correlation. Defaults to "spearman".
        fig_xsize (int, optional): Width of the figure in pixels. Defaults to 800.
        fig_ysize (int, optional): Height of the figure in pixels. Defaults to 600.

    Returns:
        go.Figure: Plotly Figure object.
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

    fig.update_layout(
        width=fig_xsize,
        height=fig_ysize,
        title=dict(text=plot_title, x=0.5, xanchor="center", font=dict(size=20)),
    )

    return fig


@_log_execution_time
def plot_acf(
    data: pd.DataFrame,
    security: str,
    num_of_lags: int = 20,
    plot_title: str = "Autocorrelation Plot",
    x_label: str = "Lag",
    y_label: str = "Autocorrelation",
    bar_color: str = "#00CC96",
    fig_xsize: int = 800,
    fig_ysize: int = 300,
    background_color: str = "#F1F1F1",
) -> go.Figure:
    """
    Plots the autocorrelation function for a given security using Plotly.

    Args:
        data (pd.DataFrame): Input dataset.
        security (str): Security to compute autocorrelation for.
        num_of_lags (int, optional): Number of lags to compute. Defaults to 20.
        plot_title (str, optional): Title of the plot. Defaults to "Autocorrelation Plot".
        x_label (str, optional): Label for the X-axis. Defaults to "Lag".
        y_label (str, optional): Label for the Y-axis. Defaults to "Autocorrelation".
        bar_color (str, optional): Color of the bars in the plot. Defaults to "#00CC96".
        fig_xsize (int, optional): Width of the figure in pixels. Defaults to 800.
        fig_ysize (int, optional): Height of the figure in pixels. Defaults to 300.
        background_color (str, optional): Background color of the plot area. Defaults to "#F1F1F1".

    Returns:
        go.Figure: Plotly Figure object.
    """
    acf_values = acf(data[security], nlags=num_of_lags)

    fig = go.Figure(
        data=[
            go.Bar(
                x=list(range(len(acf_values))),
                y=acf_values,
                marker=dict(color=bar_color),
            )
        ]
    )

    fig.update_layout(
        title=dict(text=plot_title, x=0.5, xanchor="center", font=dict(size=20)),
        xaxis=dict(title=x_label),
        yaxis=dict(title=y_label),
        plot_bgcolor=background_color,
        width=fig_xsize,
        height=fig_ysize,
    )

    return fig


def plot_pacf(
    data: pd.DataFrame,
    security: str,
    num_of_lags: int = 20,
    plot_title: str = "Partial-Autocorrelation Plot",
    x_label: str = "Lag",
    y_label: str = "Partial Autocorrelation",
    bar_color: str = "#1B705A",
    fig_xsize: int = 800,
    fig_ysize: int = 300,
    background_color: str = "#F1F1F1",
) -> go.Figure:
    """
    Plots the partial autocorrelation function for a given security using Plotly.

    Args:
        data (pd.DataFrame): Input dataset.
        security (str): Security to compute partial autocorrelation for.
        num_of_lags (int, optional): Number of lags to compute. Defaults to 20.
        plot_title (str, optional): Title of the plot. Defaults to "Partial-Autocorrelation Plot".
        x_label (str, optional): Label for the X-axis. Defaults to "Lag".
        y_label (str, optional): Label for the Y-axis. Defaults to "Partial Autocorrelation".
        bar_color (str, optional): Color of the bars in the plot. Defaults to "#1B705A".
        fig_xsize (int, optional): Width of the figure in pixels. Defaults to 800.
        fig_ysize (int, optional): Height of the figure in pixels. Defaults to 300.
        background_color (str, optional): Background color of the plot area. Defaults to "#F1F1F1".

    Returns:
        go.Figure: Plotly Figure object.
    """
    pacf_values = pacf(data[security], nlags=num_of_lags)

    fig = go.Figure(
        data=[
            go.Bar(
                x=list(range(len(pacf_values))),
                y=pacf_values,
                marker=dict(color=bar_color),
            )
        ]
    )

    fig.update_layout(
        title=dict(text=plot_title, x=0.5, xanchor="center", font=dict(size=20)),
        xaxis=dict(title=x_label),
        yaxis=dict(title=y_label),
        plot_bgcolor=background_color,
        width=fig_xsize,
        height=fig_ysize,
    )

    return fig
