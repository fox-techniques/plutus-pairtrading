"""Cointegration Tests

This module tests for cointegration which covers:
    * Engle-Granger test
    * Phillips-Ouliaris test
    * Johansen test

In the future, the cointegration tests with structural breaks will be included, such as:
    * The Gregory and Hansen (1996) test for cointegration with a single structural break
    * The Hatemi-J test (2009) for cointegration with two structural breaks
    * The Maki test for cointegration with multiple structural breaks
"""

from statsmodels.tsa.vector_ar.vecm import coint_johansen
from arch.unitroot.cointegration import engle_granger, phillips_ouliaris

import numpy as np
import pandas as pd

from typing import List, Optional

from ..utils.performance import _log_execution_time
import logging

logger = logging.getLogger(__name__)


@_log_execution_time
def validate_trend(trend: str) -> str:
    """
    Validates and converts the trend argument to a format accepted by the cointegration tests.

    Args:
        trend (str): Trend argument. Options are:
            - "no deterministic term"
            - "constant"
            - "constant and time trend"

    Returns:
        str: Converted trend option for use in cointegration tests.

    Raises:
        ValueError: If an invalid trend is provided.
    """
    trend = trend.lower()
    valid_trends = ["no deterministic term", "constant", "constant and time trend"]
    if trend not in valid_trends:
        raise ValueError(f"Invalid trend. Options are: {', '.join(valid_trends)}.")
    return {
        "no deterministic term": "n",
        "constant": "c",
        "constant and time trend": "ct",
    }[trend]


@_log_execution_time
def engle_granger_cointegration_test(
    data: pd.DataFrame,
    securities: List[str],
    trend: Optional[str] = "constant",
    selection_criterion: Optional[str] = "AIC",
    significance_level: Optional[float] = 0.05,
) -> dict:
    """
    Tests for cointegration using the Engle-Granger method.

    Args:
        data (pd.DataFrame): Pandas DataFrame containing time series data.
        securities (list): List of two securities to test, e.g., ["AAPL", "MSFT"].
        trend (str, optional): Trend assumption in the model. Options are:
            - "no deterministic term"
            - "constant"
            - "constant and time trend"
            Defaults to "constant".
        selection_criterion (str, optional): Selection criterion for lag order. Options are "AIC" or "BIC". Defaults to "AIC".
        significance_level (float, optional): Significance level for cointegration test. Defaults to 0.05.

    Returns:
        dict: Dictionary containing test results, including:
            - "Statistic": Test statistic.
            - "p-Value": p-value of the test.
            - "Critical Value": Critical value at the significance level.
            - "Trend": Trend used in the test.
            - "Cointegrated Vector": Cointegrating vector.
            - "Cointegrated": Boolean indicating if the series are cointegrated.
            - Spread between the two series.
    """
    trend = validate_trend(trend)
    if len(securities) != 2:
        raise ValueError("Engle-Granger test requires exactly two securities.")

    coint_result = engle_granger(
        data[securities[0]],
        data[securities[1]],
        trend=trend,
        method=selection_criterion.lower(),
    )
    return {
        "Statistic": coint_result.stat,
        "p-Value": coint_result.pvalue,
        "Critical Value": coint_result.critical_values[int(significance_level * 100)],
        "Trend": trend,
        "Cointegrated Vector": coint_result.cointegrating_vector,
        "Cointegrated": bool(coint_result.pvalue < significance_level),
        f"spread_{securities[0]}_{securities[1]}": coint_result.resid,
    }


@_log_execution_time
def phillips_ouliaris_cointegration_test(
    data: pd.DataFrame,
    securities: List[str],
    trend: Optional[str] = "constant",
    significance_level: Optional[float] = 0.05,
) -> dict:
    """
    Tests for cointegration using the Phillips-Ouliaris method.

    Args:
        data (pd.DataFrame): Pandas DataFrame containing time series data.
        securities (list): List of two securities to test, e.g., ["AAPL", "MSFT"].
        trend (str, optional): Trend assumption in the model. Options are:
            - "no deterministic term"
            - "constant"
            - "constant and time trend"
            Defaults to "constant".
        significance_level (float, optional): Significance level for cointegration test. Defaults to 0.05.

    Returns:
        dict: Dictionary containing test results, including:
            - "Statistic": Test statistic.
            - "p-Value": p-value of the test.
            - "Critical Value": Critical value at the significance level.
            - "Trend": Trend used in the test.
            - "Cointegrated Vector": Cointegrating vector.
            - "Cointegrated": Boolean indicating if the series are cointegrated.
            - Spread between the two series.
    """
    trend = validate_trend(trend)
    if len(securities) != 2:
        raise ValueError("Phillips-Ouliaris test requires exactly two securities.")

    coint_result = phillips_ouliaris(
        data[securities[0]], data[securities[1]], trend=trend
    )
    return {
        "Statistic": coint_result.stat,
        "p-Value": coint_result.pvalue,
        "Critical Value": coint_result.critical_values[int(significance_level * 100)],
        "Trend": trend,
        "Cointegrated Vector": coint_result.cointegrating_vector,
        "Cointegrated": bool(coint_result.pvalue < significance_level),
        f"spread_{securities[0]}_{securities[1]}": coint_result.resid,
    }


@_log_execution_time
def johansen_cointegration_test(
    data: pd.DataFrame,
    securities: List[str],
    trend: Optional[str] = "constant",
    statistic: Optional[str] = "trace",
    num_lag_diff: Optional[int] = 1,
    significance_level: Optional[float] = 0.05,
) -> dict:
    """
    Tests for cointegration using the Johansen method.

    Args:
        data (pd.DataFrame): Pandas DataFrame containing time series data.
        securities (list): List of securities to test, e.g., ["AAPL", "MSFT", "GOOG"].
        trend (str, optional): Trend assumption in the model. Options are:
            - "no deterministic term"
            - "constant"
            - "constant and time trend"
            Defaults to "constant".
        statistic (str, optional): Test statistic to use. Options are "trace" or "eigenvalue". Defaults to "trace".
        num_lag_diff (int, optional): Number of lag differences to include in the model. Defaults to 1.
        significance_level (float, optional): Significance level for cointegration test. Defaults to 0.05.

    Returns:
        dict: Dictionary containing test results, including:
            - "Statistics and Critical Values": DataFrame with test statistics and critical values.
            - "Eigenvalues": Eigenvalues of the cointegration matrix.
            - "Eigenvectors": Eigenvectors of the cointegration matrix.
            - "Trend": Trend used in the test.
            - "Spread": Linear combination representing the spread.
            - "#Cointegrated Vectors": Number of cointegrated vectors.
    """
    # Map trend to deterministic order
    trend_mapping = {
        "no deterministic term": -1,
        "constant": 0,
        "constant and time trend": 1,
    }
    if trend.lower() not in trend_mapping:
        raise ValueError(
            "Invalid trend. Options are: 'no deterministic term', 'constant', 'constant and time trend'."
        )
    det_order = trend_mapping[trend.lower()]

    # Perform Johansen test
    coint = coint_johansen(
        data[securities], det_order=det_order, k_ar_diff=num_lag_diff
    )

    # Prepare results DataFrame
    coint_df = pd.DataFrame(
        {
            "Null Hypothesis": [f"r<={i}" for i in range(len(securities))],
        }
    )

    # Handle Trace or Eigenvalue statistic
    if statistic.lower() == "trace":
        coint_df["Statistic"] = coint.lr1
        critical_values = coint.cvt
    elif statistic.lower() == "eigenvalue":
        coint_df["Statistic"] = coint.lr2
        critical_values = coint.cvm
    else:
        raise ValueError("Invalid statistic. Options are: 'trace', 'eigenvalue'.")

    # Add critical values to the DataFrame
    significance_col_index = {0.1: 0, 0.05: 1, 0.01: 2}.get(significance_level)
    if significance_col_index is None:
        raise ValueError("Significance level must be one of 0.1, 0.05, or 0.01.")
    coint_df[f"Critical Value ({int((1 - significance_level) * 100)}%)"] = (
        critical_values[:, significance_col_index]
    )

    # Determine number of cointegrated vectors
    H0_rejected = (
        coint_df["Statistic"]
        > coint_df[f"Critical Value ({int((1 - significance_level) * 100)}%)"]
    )
    num_cointegrated_vectors = H0_rejected.sum()

    # Calculate spread using eigenvectors
    eigenvectors = coint.evec
    spread = np.dot(data[securities].values, eigenvectors[:, 0])

    # Compile results into a dictionary
    return {
        "Statistics and Critical Values": coint_df,
        "Eigenvalues": coint.eig,
        "Eigenvectors": eigenvectors,
        "Trend": trend,
        "#Cointegrated Vectors": num_cointegrated_vectors,
        "Spread": pd.Series(spread, index=data.index, name="Spread"),
    }
