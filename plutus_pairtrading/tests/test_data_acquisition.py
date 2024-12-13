import os
import shutil
import pandas as pd
import pytest
from plutus_pairtrading.data_acquisitions.data_acquisition import (
    ensure_directory_exists,
    load_csv_data,
    store_data_as_csv,
    fetch_yahoo_finance_data,
    combine_dataframes,
    fetch_and_store_tickers,
    read_and_combine_ticker_files,
)

TEST_DATA_DIR = "data/unittest"


@pytest.fixture(scope="module")
def setup_test_env():
    """Set up a temporary directory and test data for tests."""
    test_file1 = os.path.join(TEST_DATA_DIR, "TICKER1.csv")
    test_file2 = os.path.join(TEST_DATA_DIR, "TICKER2.csv")
    combined_file = os.path.join(TEST_DATA_DIR, "combined.csv")

    ensure_directory_exists(TEST_DATA_DIR)

    # Sample data for testing
    test_data1 = {
        "date": pd.date_range(start="2023-01-01", periods=5, freq="D"),
        "TICKER1": [100, 101, 102, 103, 104],
    }

    test1_df = pd.DataFrame(test_data1)
    test1_df.set_index("date", inplace=True)
    test1_df.to_csv(test_file1)

    test_data2 = {
        "date": pd.date_range(start="2023-01-01", periods=5, freq="D"),
        "TICKER2": [200, 201, 202, 203, 204],
    }

    test2_df = pd.DataFrame(test_data2)
    test2_df.set_index("date", inplace=True)
    test2_df.to_csv(test_file2)

    combined_data = {
        "date": pd.date_range(start="2023-01-01", periods=5, freq="D"),
        "TICKER1": [100, 101, 102, 103, 104],
        "TICKER2": [200, 201, 202, 203, 204],
    }

    combined_df = pd.DataFrame(combined_data)
    combined_df.set_index("date", inplace=True)

    yield test_file1, test_file2, combined_file, test1_df, test2_df, combined_df

    # Clean up after tests
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR)


def test_ensure_directory_exists(setup_test_env):
    """Test directory creation."""

    test_path = os.path.join(TEST_DATA_DIR, "testing_folder_creation")
    ensure_directory_exists(test_path)
    assert os.path.exists(test_path)


def test_load_csv_data(setup_test_env):
    """Test loading data from a CSV file."""
    test_file, _, _, test_df, _, _ = setup_test_env
    loaded_df = load_csv_data(test_file)
    pd.testing.assert_frame_equal(loaded_df, test_df)


def test_store_data_as_csv(setup_test_env):
    """Test storing data as a CSV file."""
    _, _, combined_file, _, _, combined_df = setup_test_env
    print(combined_df)
    store_data_as_csv(combined_df, combined_file)
    assert os.path.exists(combined_file)
    stored_df = pd.read_csv(combined_file, parse_dates=["date"], index_col="date")
    pd.testing.assert_frame_equal(stored_df, combined_df)


@pytest.mark.skip(
    reason="This test fetches live data; uncomment for integration testing."
)
def test_fetch_yahoo_finance_data():
    """Test fetching data from Yahoo Finance."""
    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2023-01-05"
    df = fetch_yahoo_finance_data(ticker, start_date, end_date)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_combine_dataframes(setup_test_env):
    """Test combining multiple DataFrames."""
    _, _, _, test1_df, test2_df, combined_df = setup_test_env
    combined = combine_dataframes([test1_df, test2_df], join_type="inner")
    expected = combined_df
    pd.testing.assert_frame_equal(combined, expected)


@pytest.mark.skip(
    reason="This test fetches live data; uncomment for integration testing."
)
def test_fetch_and_store_tickers(setup_test_env):
    """Test fetching and storing multiple tickers."""
    _, _, _, _, _, _ = setup_test_env
    tickers = ["AAPL", "MSFT"]
    combined_data, failed_tickers = fetch_and_store_tickers(tickers, TEST_DATA_DIR)
    assert isinstance(combined_data, pd.DataFrame)
    assert not combined_data.empty
    assert isinstance(failed_tickers, list)


def test_read_and_combine_ticker_files(setup_test_env):
    """Test reading and combining ticker files."""
    _, _, _, test1_df, test2_df, combined_df = setup_test_env

    tickers = ["TICKER1", "TICKER2"]
    combined_data = read_and_combine_ticker_files(TEST_DATA_DIR, tickers)
    assert isinstance(combined_data, pd.DataFrame)
    assert not combined_data.empty
    expected = combined_df
    pd.testing.assert_frame_equal(combined_data, expected)
