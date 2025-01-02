"""Data Generation

This module covers feature engineering functions 
"""

import pandas as pd
import numpy as np
import re

from typing import List, Optional, Tuple

from ..tests.stationarity_tests import augmented_dickey_fuller_test
from ..tests.stationarity_tests import philips_perron_test
from ..tests.stationarity_tests import KPSS_test

from ..tests.cointegration_tests import engle_granger_cointegration_test
from ..tests.cointegration_tests import phillips_ouliaris_cointegration_test
from ..tests.cointegration_tests import johansen_cointegration_test

from ..utils.performance import _log_execution_time
import logging

logger = logging.getLogger(__name__)


@_log_execution_time
def validate_securities(data: pd.DataFrame, securities: List[str]) -> None:
    """
    Validates that all securities exist in the dataset.

    Args:
        data (pd.DataFrame): Input dataset.
        securities (List[str]): List of securities to validate.

    Raises:
        ValueError: If any securities are missing from the dataset.
    """
    missing = [sec for sec in securities if sec not in data.columns]
    if missing:
        raise ValueError(f"Securities not found in data: {missing}")


@_log_execution_time
def generate_random_stock_prices(
    ticker_label: str = "TICKER",
    start_price: float = 150,
    num_days: int = 100,
    mu: float = 0.0005,
    sigma: float = 0.01,
    start_date: str = "2023-01-01",
) -> pd.DataFrame:
    """
    Generate random stock prices using geometric Brownian motion.

    Args:
        ticker_label (str): Ticker label. Defaults to "TICKER"
        start_price (float): Initial stock price. Defaults to 150.
        num_days (int): Number of days to generate data for. Defaults to 100.
        mu (float): Expected daily return. Defaults to 0.0005 (0.05%).
        sigma (float): Daily volatility. Defaults to 0.01 (1%).
        start_date (str): Start date for the time series. Defaults to "2023-01-01".

    Returns:
        pd.DataFrame: DataFrame with a "date" index and "AAPL" column of prices.
    """
    np.random.seed(42)

    # Generate daily returns using random normal distribution
    daily_returns = np.random.normal(mu, sigma, num_days)

    # Simulate price changes using cumulative product
    prices = start_price * np.exp(np.cumsum(daily_returns))

    # Create a DataFrame with dates and prices
    dates = pd.date_range(start=start_date, periods=num_days, freq="D")
    return pd.DataFrame({ticker_label: prices}, index=dates)


@_log_execution_time
def compute_returns(
    data: pd.DataFrame, securities: List[str], return_period: str = "daily"
) -> pd.DataFrame:
    """
    Computes periodic returns for specified securities.

    Args:
        data (pd.DataFrame): Input dataset.
        securities (List[str]): List of securities to compute returns for.
        return_period (str, optional): Period for returns ('daily', 'weekly', 'monthly'). Defaults to 'daily'.

    Returns:
        pd.DataFrame: DataFrame with added return columns.
    """
    validate_securities(data, securities)

    period_map = {"daily": 1, "weekly": 5, "monthly": 20}
    if return_period.lower() not in period_map:
        raise ValueError(
            f"Invalid return period: {return_period}. Options are {list(period_map.keys())}."
        )
    period = period_map[return_period.lower()]
    suffix = return_period[0]

    returns = data.copy()
    for sec in securities:
        returns[f"r_{sec}_{suffix}"] = data[sec].pct_change(periods=period).fillna(0)

    return returns


@_log_execution_time
def return_logs(
    data: pd.DataFrame,
    securities: List[str],
    return_only_logs: bool = True,
    rename_logs: bool = False,
) -> pd.DataFrame:
    """
    Computes the logarithm of prices for specified securities.

    Args:
        data (pd.DataFrame): Input dataset.
        securities (List[str]): List of securities to compute logs for.
        return_only_logs (bool, optional): If True, retains only log-transformed columns. Defaults to True.
        rename_logs (bool, optional): If True, renames log columns to original names. Defaults to False.

    Returns:
        pd.DataFrame: DataFrame with log-transformed prices.
    """
    validate_securities(data, securities)
    data_log = data.copy()

    for sec in securities:
        data_log[f"log_{sec}"] = np.log(data[sec])

        if return_only_logs:
            data_log.drop(columns=[sec], inplace=True)
            if rename_logs:
                data_log.rename(columns={f"log_{sec}": sec}, inplace=True)

    return data_log


@_log_execution_time
def return_exps(
    data: pd.DataFrame,
    securities: List[str],
    return_only_exps: bool = True,
    rename_exps: bool = True,
    drop_exp_logs_prefix: bool = True,
) -> pd.DataFrame:
    """
    Computes the exponential transformation of prices for specified securities.

    Args:
        data (pd.DataFrame): Input dataset.
        securities (List[str]): List of securities to compute exponentials for.
        return_only_exps (bool, optional): If True, retains only exponential-transformed columns. Defaults to True.
        rename_exps (bool, optional): If True, renames exponential columns to original names. Defaults to True.
        drop_exp_logs_prefix (bool, optional): If True, renames columns with prefix 'exp_log_<ticker>' back to '<ticker>'. Defaults to True.

    Returns:
        pd.DataFrame: DataFrame with exponential-transformed prices.
    """
    validate_securities(data, securities)  # Validate securities exist in the data
    data_exps = data.copy()
    transformed_columns = {}

    # Compute exponential transformation for each security
    for sec in securities:
        if sec not in data.columns:
            raise ValueError(f"Column '{sec}' not found in the data.")

        exp_col = f"exp_{sec}"
        data_exps[exp_col] = np.exp(data[sec])
        transformed_columns[sec] = exp_col

    # Retain only exponential-transformed columns if specified
    if return_only_exps:
        data_exps = data_exps[list(transformed_columns.values())]

        # Rename exponential columns back to original names if specified
        if rename_exps:
            data_exps.rename(
                columns={v: k for k, v in transformed_columns.items()}, inplace=True
            )

    # Rename columns with 'exp_log_' prefix to the ticker name if specified
    if drop_exp_logs_prefix:
        data_exps.columns = [
            col.replace("exp_log_", "") if col.startswith("exp_log_") else col
            for col in data_exps.columns
        ]

    return data_exps


@_log_execution_time
def get_date_range(data: pd.DataFrame) -> Tuple[str, str]:
    """
    Returns the start and end dates of the dataset.

    Args:
        data (pd.DataFrame): Input dataset.

    Returns:
        Tuple[str, str]: Start and end dates of the dataset.
    """
    if data.index.isnull().any():
        raise ValueError("Data contains null indices, which are not allowed.")

    start_date = data.index[0].strftime("%Y-%m-%d")
    end_date = data.index[-1].strftime("%Y-%m-%d")

    return start_date, end_date


@_log_execution_time
def compute_correlation_matrix(
    data: pd.DataFrame, securities: List[str], method: str = "spearman"
) -> pd.DataFrame:
    """
    Computes the correlation matrix for specified securities.

    Args:
        data (pd.DataFrame): Input dataset.
        securities (List[str]): List of securities to compute correlations for.
        method (str, optional): Correlation method ('pearson', 'kendall', 'spearman'). Defaults to 'spearman'.

    Returns:
        pd.DataFrame: Correlation matrix.
    """
    validate_securities(data, securities)
    return data[securities].corr(method=method)


@_log_execution_time
def compute_correlation_dataframe(
    data: pd.DataFrame,
    securities: List[str],
    method: str = "spearman",
    plus_threshold: float = 0.8,
    minus_threshold: float = -0.8,
) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Computes correlations and filters results based on thresholds.

    Args:
        data (pd.DataFrame): Input dataset.
        securities (List[str]): List of securities to include.
        method (str, optional): Correlation method ('pearson', 'kendall', 'spearman'). Defaults to 'spearman'.
        plus_threshold (float, optional): Positive correlation threshold. Defaults to 0.8.
        minus_threshold (float, optional): Negative correlation threshold. Defaults to -0.8.

    Returns:
        Tuple[pd.DataFrame, np.ndarray]: Filtered correlation DataFrame and unique correlated securities.
    """
    validate_securities(data, securities)
    corr_mat = data[securities].corr(method=method)

    corr_df = corr_mat.stack().reset_index(name=f"{method}_correlation")
    corr_df = corr_df[corr_df["level_0"] != corr_df["level_1"]]
    corr_df = corr_df[
        (corr_df[f"{method}_correlation"] > plus_threshold)
        | (corr_df[f"{method}_correlation"] < minus_threshold)
    ].sort_values(by=f"{method}_correlation", ascending=False)

    unique_securities = np.unique(corr_df[["level_0", "level_1"]].values.ravel())
    return corr_df, unique_securities


@_log_execution_time
def slice_data_with_dates(
    data: pd.DataFrame, cut_start_date: str, cut_end_date: str
) -> pd.DataFrame:
    """
    Slices the data based on the requested start and end dates.

    Args:
        data (pd.DataFrame): Input DataFrame with a DatetimeIndex.
        cut_start_date (str): Start date for slicing (inclusive).
        cut_end_date (str): End date for slicing (inclusive).

    Returns:
        pd.DataFrame: Sliced DataFrame.

    Raises:
        ValueError: If the sliced DataFrame is empty or indices are not valid dates.
    """
    if not isinstance(data.index, pd.DatetimeIndex):
        raise ValueError("Data must have a DatetimeIndex for slicing by dates.")

    try:
        sliced_data = data.loc[cut_start_date:cut_end_date]
    except KeyError as e:
        raise ValueError(f"Error slicing data: {e}")

    if sliced_data.empty:
        raise ValueError(
            f"No data available in the range {cut_start_date} to {cut_end_date}."
        )

    return sliced_data


@_log_execution_time
def pairs_identification(
    data,
    stationarity_method="augmented dickey-fuller",
    cointegration_method="phillips-ouliaris",
    stationarity_significance_level=0.01,
    coint_significance_level=0.01,
    stationarity_trend="constant",
    cointegration_trend="constant",
):
    """
    This function identifies the pairs with cointegration method. The process is as follows:

    * Check if both candidates have integration order of one with stationarity test
    * Check if both candidates are cointegrated with Phillips-Ouliaris cointegration test

    Args:
        data (DataFrame): Pandas dataframe
        stationarity_method (str, optional): Stationarity test method. Options are ['Augmented Dickey-Fuller', 'Philips-Perron', 'Kwiatkowski-Phillips-Schmidt-Shin'] - for short: ["ADF", "PP", "KPSS"]. Defaults to 'ADF'
        cointegration_method (str, optional): Method of cointegration. Options are ['phillips-ouliaris', 'engle-granger']. Defaults to 'phillips-ouliaris'
        stationarity_significance_level (float, optional): Significance level of stationarity test. Defaults to 0.01
        coint_significance_level (float, optional): Significance level of cointegration test. Defaults to 0.01
        stationarity_trend (str, optional): Time trend for statioarity test can be set. Options are ['no deterministic term', 'constant', 'constant and time trend]. Defaults to 'constant'
        cointegration_trend (str, optional): Time trend for cointegration test can be set. Options are ['no deterministic term', 'constant', 'constant and time trend']. Defaults to 'constant'

    Returns:
        DataFrame: Dataframe of the cointegrated pairs
    """

    # Check for I(1)
    securities = data.columns
    nonstationary_securities = []

    for sec in securities:

        if stationarity_method.lower() == "adf":
            stationarity_report = augmented_dickey_fuller_test(
                data,
                security=sec,
                trend=stationarity_trend,
                significance_level=stationarity_significance_level,
            )
        elif stationarity_method.lower() == "pp":
            stationarity_report = philips_perron_test(
                data,
                security=sec,
                trend=stationarity_trend,
                significance_level=stationarity_significance_level,
            )
        elif stationarity_method.lower() == "kpss":
            stationarity_report = KPSS_test(
                data,
                security=sec,
                trend=stationarity_trend,
                significance_level=stationarity_significance_level,
            )
        else:
            logger.error(
                "Method of stationarity is not supported please select from ['ADF', 'PP', 'KPSS']"
            )

        if stationarity_report["Stationary"] == False:
            nonstationary_securities.append(sec)

    # Pairs identification
    pairs_identification_summary = []

    for sec_i in nonstationary_securities:

        for sec_j in nonstationary_securities:
            if sec_i != sec_j:
                securities = [sec_i, sec_j]

                if cointegration_method.lower() == "engle-granger":
                    cointegration_report = engle_granger_cointegration_test(
                        data,
                        securities=securities,
                        trend=cointegration_trend,
                        significance_level=coint_significance_level,
                    )
                elif cointegration_method.lower() == "phillips-ouliaris":
                    cointegration_report = phillips_ouliaris_cointegration_test(
                        data,
                        securities=securities,
                        trend=cointegration_trend,
                        significance_level=coint_significance_level,
                    )
                elif cointegration_method.lower() == "johansen":
                    cointegration_report = johansen_cointegration_test(
                        data,
                        securities=securities,
                        trend=cointegration_trend,
                        significance_level=coint_significance_level,
                    )
                else:
                    logger.error(
                        "Method of cointegration is not supported please select from ['Engle-Granger', 'Phillips-Ouliaris', 'Johansen']"
                    )

                if cointegration_report["Cointegrated"] == True:
                    pairs_identification_summary.append(
                        {
                            "security_a": sec_i,
                            "security_b": sec_j,
                            f"cointegration_vector_{int(coint_significance_level*100)}perc": cointegration_report[
                                "Cointegrated Vector"
                            ],
                        }
                    )

    coint_pairs_df = pd.DataFrame(pairs_identification_summary)

    return coint_pairs_df
