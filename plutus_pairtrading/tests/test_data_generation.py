import pandas as pd
import pytest
from plutus_pairtrading.data_generations.data_generation import (
    validate_securities,
    compute_returns,
    return_logs,
    return_exps,
    get_date_range,
    compute_correlation_matrix,
    compute_correlation_dataframe,
    slice_data_with_dates,
    pairs_identification,
)


@pytest.fixture
def sample_data():
    """Fixture to provide sample data for testing."""
    data = {
        "date": pd.date_range(start="2023-01-01", periods=10, freq="D"),
        "AAPL": [150 + i for i in range(10)],
        "MSFT": [200 + i * 2 for i in range(10)],
    }
    df = pd.DataFrame(data)
    df.set_index("date", inplace=True)
    return df


def test_validate_securities(sample_data):
    """Test securities validation."""
    with pytest.raises(ValueError, match="Securities not found in data"):
        validate_securities(sample_data, ["AAPL", "GOOG"])

    # Should pass without exception
    validate_securities(sample_data, ["AAPL", "MSFT"])


def test_compute_returns(sample_data):
    """Test periodic returns computation."""
    result = compute_returns(
        sample_data, securities=["AAPL", "MSFT"], return_period="daily"
    )
    assert "r_AAPL_d" in result.columns
    assert "r_MSFT_d" in result.columns
    assert result["r_AAPL_d"].iloc[0] == 0  # First return should be 0 (filled)


def test_return_logs(sample_data):
    """Test logarithmic transformation."""
    result = return_logs(sample_data, securities=["AAPL"], return_only_logs=True)
    assert "log_AAPL" in result.columns
    assert "AAPL" not in result.columns


def test_return_exps(sample_data):
    """Test exponential transformation."""
    log_data = return_logs(sample_data, securities=["AAPL"], return_only_logs=True)
    result = return_exps(log_data, securities=["log_AAPL"], return_only_exps=True)
    assert "log_AAPL" in result.columns


def test_get_date_range(sample_data):
    """Test retrieving date range."""
    start_date, end_date = get_date_range(sample_data)
    assert start_date == "2023-01-01"
    assert end_date == "2023-01-10"


def test_compute_correlation_matrix(sample_data):
    """Test correlation matrix computation."""
    corr_matrix = compute_correlation_matrix(
        sample_data, securities=["AAPL", "MSFT"], method="pearson"
    )
    assert corr_matrix.shape == (2, 2)  # 2 securities
    assert corr_matrix.loc["AAPL", "MSFT"] != 0  # Correlation should be valid


def test_compute_correlation_dataframe(sample_data):
    """Test correlation dataframe computation and filtering."""
    corr_df, correlated_securities = compute_correlation_dataframe(
        sample_data, securities=["AAPL", "MSFT"], method="pearson", plus_threshold=0.5
    )
    assert not corr_df.empty
    assert "AAPL" in correlated_securities
    assert "MSFT" in correlated_securities


def test_slice_data_with_dates(sample_data):
    """Test slicing data by date range."""
    sliced_data = slice_data_with_dates(sample_data, "2023-01-03", "2023-01-05")
    assert sliced_data.index[0] == pd.Timestamp("2023-01-03")
    assert sliced_data.index[-1] == pd.Timestamp("2023-01-05")


@pytest.mark.skip(
    reason="Stationarity and cointegration tests require more mock setup."
)
def test_pairs_identification(sample_data):
    """Test pairs identification."""
    pairs = pairs_identification(
        sample_data,
        stationarity_method="ADF",
        cointegration_method="phillips-ouliaris",
    )
    assert isinstance(pairs, pd.DataFrame)
    assert "security_a" in pairs.columns
    assert "security_b" in pairs.columns
