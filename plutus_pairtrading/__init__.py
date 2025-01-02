from .data_acquisitions.data_acquisition import (
    load_csv_data,
    store_data_as_csv,
    fetch_yahoo_finance_data,
    combine_dataframes,
    fetch_and_store_tickers,
    read_and_combine_ticker_files,
)

from .data_generations.data_generation import (
    compute_returns,
    return_logs,
    return_exps,
    generate_random_stock_prices,
    get_date_range,
    compute_correlation_matrix,
    compute_correlation_dataframe,
    slice_data_with_dates,
    pairs_identification,
)

from .data_visualizations.plots import (
    plot_timeseries,
    plot_dual_timeseries,
    plot_correlation_matrix,
    plot_acf,
    plot_pacf,
)

from .tests.stationarity_tests import (
    augmented_dickey_fuller_test,
    philips_perron_test,
    KPSS_test,
)

from .tests.cointegration_tests import (
    engle_granger_cointegration_test,
    phillips_ouliaris_cointegration_test,
    johansen_cointegration_test,
)

from .utils.performance import _log_execution_time

import logging


# Set up default logging configuration
@_log_execution_time
def setup_logging(level=logging.INFO):
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=level
    )


# Initialize logging with INFO level by default
setup_logging()


# Package-level imports
__all__ = [
    "load_csv_data",
    "store_data_as_csv",
    "fetch_yahoo_finance_data",
    "combine_dataframes",
    "fetch_and_store_tickers",
    "read_and_combine_ticker_files",
    "compute_returns",
    "return_logs",
    "return_exps",
    "generate_random_stock_prices",
    "get_date_range",
    "compute_correlation_matrix",
    "compute_correlation_dataframe",
    "slice_data_with_dates",
    "pairs_identification",
    "plot_timeseries",
    "plot_dual_timeseries",
    "plot_correlation_matrix",
    "plot_acf",
    "plot_pacf",
    "augmented_dickey_fuller_test",
    "philips_perron_test",
    "KPSS_test",
    "engle_granger_cointegration_test",
    "phillips_ouliaris_cointegration_test",
    "johansen_cointegration_test",
]

__version__ = "0.1.0"
