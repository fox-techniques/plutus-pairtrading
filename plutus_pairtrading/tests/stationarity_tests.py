"""Stationarity Tests

This module tests for stationarity and order of integration which covers:
    * Augmented Dickey-Fuller test
    * Philips-Perron test
    * Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test 
"""

from typing import Optional, List
import pandas as pd
from arch.unitroot import ADF, PhillipsPerron, KPSS

from ..utils.performance import _log_execution_time
import logging

logger = logging.getLogger(__name__)


@_log_execution_time
def validate_trend(trend: str, allowed_trends: List[str]) -> str:
    """
    Validates the trend argument and converts it to the format required by the test functions.

    Args:
        trend (str): Trend argument provided by the user.
        allowed_trends (List[str]): List of allowed trends for the specific test.

    Returns:
        str: Validated trend argument.

    Raises:
        ValueError: If the trend is not in the allowed options.
    """
    trend = trend.lower()
    if trend not in allowed_trends:
        raise ValueError(
            f"Invalid trend: {trend}. Allowed options are: {', '.join(allowed_trends)}"
        )
    return {
        "no deterministic term": "n",
        "constant": "c",
        "constant and time trend": "ct",
    }[trend]


@_log_execution_time
def augmented_dickey_fuller_test(
    data: pd.DataFrame,
    security: str,
    trend: str = "constant",
    method: str = "AIC",
    max_lag_for_auto_detect: int = 20,
    num_lags: Optional[int] = None,
    significance_level: float = 0.05,
) -> dict:
    """
    Tests for stationarity using the Augmented Dickey-Fuller (ADF) test.

    Args:
        data (pd.DataFrame): DataFrame containing the time series data.
        security (str): Name of the security column to test.
        trend (str, optional): Trend assumption. Options: "no deterministic term", "constant", "constant and time trend".
            Defaults to "constant".
        method (str, optional): Criterion for lag selection. Options: "AIC", "BIC". Defaults to "AIC".
        max_lag_for_auto_detect (int, optional): Maximum number of lags for automatic selection. Defaults to 20.
        num_lags (Optional[int], optional): Fixed number of lags to use. If None, lags are automatically selected.
        significance_level (float, optional): Significance level for the test. Defaults to 0.05.

    Returns:
        dict: Test results, including statistic, p-value, stationarity status, and critical values.
    """
    adf_trend = validate_trend(
        trend, ["no deterministic term", "constant", "constant and time trend"]
    )

    if security not in data.columns:
        raise ValueError(f"Security '{security}' not found in the DataFrame.")
    clean_data = data[security].dropna()

    # Adjust max_lag based on data length
    max_lag = min(max_lag_for_auto_detect, len(clean_data) - 1)

    # Perform the ADF test
    adf = ADF(
        clean_data,
        method=method.lower(),
        lags=num_lags,
        max_lags=max_lag,
        trend=adf_trend,
    )
    return {
        "Statistic": adf.stat,
        "p-Value": adf.pvalue,
        "Stationary": bool(adf.pvalue < significance_level),
        "Lags": adf.lags,
        "Trend": trend,
        "Critical Values": adf.critical_values,
    }


@_log_execution_time
def philips_perron_test(
    data: pd.DataFrame,
    security: str,
    lags: Optional[int] = None,
    trend: str = "constant",
    significance_level: float = 0.05,
) -> dict:
    """
    Tests for stationarity using the Phillips-Perron (PP) test.

    Args:
        data (pd.DataFrame): DataFrame containing the time series data.
        security (str): Name of the security column to test.
        lags (Optional[int], optional): Number of lags to use. If None, automatic selection is performed. Defaults to None.
        trend (str, optional): Trend assumption. Options: "no deterministic term", "constant", "constant and time trend".
            Defaults to "constant".
        significance_level (float, optional): Significance level for the test. Defaults to 0.05.

    Returns:
        dict: Test results, including statistic, p-value, stationarity status, and critical values.
    """
    pp_trend = validate_trend(
        trend, ["no deterministic term", "constant", "constant and time trend"]
    )

    if security not in data.columns:
        raise ValueError(f"Security '{security}' not found in the DataFrame.")
    clean_data = data[security].dropna()

    # Ensure lags are feasible
    max_possible_lags = len(clean_data) - 1
    lags = lags if lags is not None else max_possible_lags

    pp = PhillipsPerron(clean_data, lags=lags, trend=pp_trend)
    return {
        "Statistic": pp.stat,
        "p-Value": pp.pvalue,
        "Stationary": bool(pp.pvalue < significance_level),
        "Lags": pp.lags,
        "Trend": trend,
        "Critical Values": pp.critical_values,
    }


@_log_execution_time
def KPSS_test(
    data: pd.DataFrame,
    security: str,
    lags: Optional[int] = None,
    trend: str = "constant",
    significance_level: float = 0.05,
) -> dict:
    """
    Tests for stationarity using the Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test.

    Args:
        data (pd.DataFrame): DataFrame containing the time series data.
        security (str): Name of the security column to test.
        lags (Optional[int], optional): Number of lags to use. If None, automatic selection is performed. Defaults to None.
        trend (str, optional): Trend assumption. Options: "constant", "constant and time trend". Defaults to "constant".
        significance_level (float, optional): Significance level for the test. Defaults to 0.05.

    Returns:
        dict: Test results, including statistic, p-value, stationarity status, and critical values.
    """
    kpss_trend = validate_trend(trend, ["constant", "constant and time trend"])

    if security not in data.columns:
        raise ValueError(f"Security '{security}' not found in the DataFrame.")
    clean_data = data[security].dropna()

    kpss = KPSS(clean_data, lags=lags, trend=kpss_trend)
    return {
        "Statistic": kpss.stat,
        "p-Value": kpss.pvalue,
        "Stationary": bool(kpss.pvalue >= significance_level),
        "Lags": kpss.lags,
        "Trend": trend,
        "Critical Values": kpss.critical_values,
    }
