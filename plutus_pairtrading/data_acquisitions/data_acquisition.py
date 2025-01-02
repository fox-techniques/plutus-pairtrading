import os
import pandas as pd
import yfinance as yf
from datetime import date
from typing import List, Optional, Tuple, Dict
from functools import reduce

from ..utils.performance import _log_execution_time
import logging

logger = logging.getLogger(__name__)


@_log_execution_time
def ensure_directory_exists(dir_path: str) -> None:
    """
    Ensure the given directory exists, creating it if necessary.

    Args:
        dir_path (str): Path to the directory to check or create.
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


@_log_execution_time
def load_csv_data(
    file_path: str, date_column: str = "date", time_series: bool = True
) -> pd.DataFrame:
    """
    Load CSV data into a DataFrame.

    Args:
        file_path (str): Path to the CSV file.
        date_column (str, optional): Name of the date column to set as index. Defaults to "date".
        time_series (bool, optional): If True, parse the date column and set it as index. Defaults to True.

    Returns:
        pd.DataFrame: Loaded DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")
    parse_dates = [date_column] if time_series else None
    index_col = date_column if time_series else None
    return pd.read_csv(file_path, parse_dates=parse_dates, index_col=index_col)


@_log_execution_time
def store_data_as_csv(
    data: pd.DataFrame, file_path: str, include_index: bool = True
) -> None:
    """
    Save a DataFrame as a CSV file.

    Args:
        data (pd.DataFrame): DataFrame to save.
        file_path (str): Destination file path.
        include_index (bool, optional): Whether to include the DataFrame index. Defaults to True.
    """
    ensure_directory_exists(os.path.dirname(file_path))
    data.to_csv(file_path, index=include_index)


@_log_execution_time
def fetch_yahoo_finance_data(
    ticker: str,
    start_date: str = "2010-01-01",
    end_date: Optional[str] = None,
    ticker_prefix: bool = True,
    column_mapping: Dict[str, str] = None,
) -> pd.DataFrame:
    """
    Fetch historical data for a ticker from Yahoo Finance.

    Args:
        ticker (str): Stock ticker symbol.
        start_date (str, optional): Start date for the data. Defaults to "2010-01-01".
        end_date (Optional[str], optional): End date for the data. Defaults to None (current date).
        ticker_prefix (bool, optional): If True, prefixes columns with the ticker name. Defaults to True.
        column_mapping (Dict[str, str], optional): Mapping of Yahoo Finance's column names to desired names.
            Example: {"Adj Close": "close_adj", "Close": "close", "High": "high", "Low": "low", "Open": "open", "Volume": "volume"}.

    Returns:
        pd.DataFrame: DataFrame containing historical data.

    Raises:
        ValueError: If none of the expected columns are found in the data.
    """
    if end_date is None:
        end_date = date.today().strftime("%Y-%m-%d")

    # Default column mapping
    if column_mapping is None:
        column_mapping = {
            "Close": "close",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Volume": "volume",
        }

    # Fetch data from Yahoo Finance
    raw_data = yf.download(ticker, start=start_date, end=end_date, progress=False)

    # Handle MultiIndex columns
    if isinstance(raw_data.columns, pd.MultiIndex):
        raw_data.columns = raw_data.columns.get_level_values(0)

    # Map and filter columns based on `column_mapping`
    available_columns = {
        yahoo_col: column_mapping[yahoo_col]
        for yahoo_col in raw_data.columns
        if yahoo_col in column_mapping
    }

    if not available_columns:
        raise ValueError(
            f"None of the expected columns ({list(column_mapping.keys())}) were found in the data."
        )

    # Rename and reorder columns based on the mapping
    renamed_data = raw_data.rename(columns=available_columns)
    renamed_data = renamed_data[list(available_columns.values())]

    # Add ticker prefix if required
    if ticker_prefix:
        renamed_data.columns = [f"{ticker}_{col}" for col in renamed_data.columns]

    renamed_data.index.name = "date"
    return renamed_data


@_log_execution_time
def combine_dataframes(
    dataframes: List[pd.DataFrame],
    join_type: str = "inner",
    suffixes: Tuple[str, str] = ("_left", "_right"),
) -> pd.DataFrame:
    """
    Combine multiple DataFrames by joining on their indices.

    Args:
        dataframes (List[pd.DataFrame]): List of DataFrames to combine.
        join_type (str, optional): Type of join to perform ('inner', 'outer', etc.). Defaults to "inner".
        suffixes (Tuple[str, str], optional): Suffixes to apply to overlapping columns. Defaults to ("_left", "_right").

    Returns:
        pd.DataFrame: Combined DataFrame.
    """
    if not dataframes:
        return pd.DataFrame()

    # Ensure all DataFrames use the same index
    for df in dataframes:
        if not df.index.name:
            df.index.name = "date"

    # Combine dataframes using reduce and join
    combined = reduce(
        lambda left, right: left.join(
            right, how=join_type, lsuffix=suffixes[0], rsuffix=suffixes[1]
        ),
        dataframes,
    )

    return combined


@_log_execution_time
def fetch_and_store_tickers(
    tickers: List[str],
    output_dir: str,
    start_date: str = "2010-01-01",
    end_date: Optional[str] = None,
    ticker_prefix: bool = True,
    column_mapping: Dict[str, str] = None,
    join_type: str = "inner",
) -> tuple[pd.DataFrame, List[str]]:
    """
    Fetch historical data for a list of tickers, save them as CSV files, and return combined data and failed tickers.

    Args:
        tickers (List[str]): List of ticker symbols to fetch.
        output_dir (str): Directory to save CSV files.
        start_date (str, optional): Start date for fetching data. Defaults to "2010-01-01".
        end_date (Optional[str], optional): End date for fetching data. Defaults to None (current date).
        ticker_prefix (bool, optional): If True, prefixes columns with ticker names. Defaults to True.
        column_mapping (Dict[str, str], optional): Mapping of Yahoo Finance's column names to desired names.
            Example: {"Close": "close", "Open": "open", "High": "high", "Low": "low", "Volume": "volume"}.
        join_type (str, optional): Type of join operation for combining data ('inner', 'outer'). Defaults to "inner".

    Returns:
        tuple[pd.DataFrame, List[str]]:
            - Combined DataFrame of successfully fetched tickers.
            - List of tickers that failed to fetch data.
    """
    if end_date is None:
        end_date = date.today().strftime("%Y-%m-%d")

    # Ensure the output directory exists
    ensure_directory_exists(output_dir)

    failed_tickers = []
    dataframes = []

    for ticker in tickers:
        try:
            # Fetch data for the ticker
            data = fetch_yahoo_finance_data(
                ticker=ticker,
                start_date=start_date,
                end_date=end_date,
                ticker_prefix=ticker_prefix,
                column_mapping=column_mapping,
            )

            # Save to CSV
            file_path = os.path.join(output_dir, f"{ticker}.csv")
            data.to_csv(file_path)
            logger.info(f"Data for {ticker} saved to {file_path}")

            # Append to the list of DataFrames
            dataframes.append(data)
        except Exception as e:
            logger.warning(f"Failed to fetch data for {ticker}: {e}")
            failed_tickers.append(ticker)

    # Combine all DataFrames
    combined_data = combine_dataframes(dataframes, join_type=join_type)
    return combined_data, failed_tickers


@_log_execution_time
def read_and_combine_ticker_files(
    directory_path: str,
    tickers: List[str],
    date_column: str = "date",
    column_mapping: Optional[Dict[str, str]] = None,
    join_type: str = "inner",
) -> pd.DataFrame:
    """
    Read and combine data files for specified tickers from a directory, selecting columns based on mapping.

    Args:
        directory_path (str): Path to the directory containing CSV files.
        tickers (List[str]): List of ticker symbols to combine.
        date_column (str, optional): Name of the date column to set as index. Defaults to "date".
        column_mapping (Optional[Dict[str, str]], optional): Mapping of column names to desired names. If None, uses all columns.
            Example: {"Close": "close", "Open": "open", "High": "high", "Low": "low", "Volume": "volume"}.
        join_type (str, optional): Type of join operation ('inner', 'outer', etc.). Defaults to "inner".

    Returns:
        pd.DataFrame: Combined DataFrame from the specified ticker files.

    Raises:
        FileNotFoundError: If the directory does not exist or no files are found for the specified tickers.
        ValueError: If no valid data could be read from the files or if no matching columns are found.
    """
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Directory {directory_path} does not exist.")

    ticker_files = [os.path.join(directory_path, f"{ticker}.csv") for ticker in tickers]
    valid_files = [file for file in ticker_files if os.path.exists(file)]
    if not valid_files:
        raise FileNotFoundError(
            f"No CSV files found for specified tickers in {directory_path}."
        )

    dataframes = []
    for file_path in valid_files:
        try:
            data = pd.read_csv(
                file_path, parse_dates=[date_column], index_col=date_column
            )
            if column_mapping:
                # Dynamically map and filter columns based on column_mapping
                available_columns = {
                    orig_col: new_col
                    for orig_col, new_col in column_mapping.items()
                    if orig_col in data.columns
                }
                if not available_columns:
                    raise ValueError(
                        f"No columns matching the mapping {list(column_mapping.keys())} found in {file_path}."
                    )
                data = data.rename(columns=available_columns)
                data = data[list(available_columns.values())]
            dataframes.append(data)
        except Exception as e:
            logger.warning(f"Error reading {file_path}: {e}")

    if not dataframes:
        raise ValueError("No valid data could be read from the specified files.")

    # Combine dataframes
    combined_data = combine_dataframes(dataframes, join_type=join_type)
    return combined_data
