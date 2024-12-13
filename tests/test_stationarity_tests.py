import pytest
import pandas as pd
from plutus_pairtrading.tests.stationarity_tests import (
    validate_trend,
    augmented_dickey_fuller_test,
    philips_perron_test,
    KPSS_test,
)

from plutus_pairtrading.data_generations.data_generation import (
    generate_random_stock_prices,
)


@pytest.fixture
def sample_data():
    """Fixture to provide sample data for testing."""
    df = generate_random_stock_prices()
    return df


def test_validate_trend():
    """Test trend validation."""
    # Valid trends
    assert (
        validate_trend(
            "constant", ["no deterministic term", "constant", "constant and time trend"]
        )
        == "c"
    )
    assert (
        validate_trend(
            "constant and time trend",
            ["no deterministic term", "constant", "constant and time trend"],
        )
        == "ct"
    )

    # Invalid trend
    with pytest.raises(ValueError, match="Invalid trend: invalid_trend."):
        validate_trend(
            "invalid_trend",
            ["no deterministic term", "constant", "constant and time trend"],
        )


def test_augmented_dickey_fuller_test(sample_data):
    """Test ADF stationarity test."""
    result = augmented_dickey_fuller_test(
        sample_data,
        security="TICKER",
        trend="constant",
        method="AIC",
        max_lag_for_auto_detect=20,
        significance_level=0.05,
    )
    assert "Statistic" in result
    assert "p-Value" in result
    assert "Stationary" in result
    assert "Critical Values" in result
    assert result["Trend"] == "constant"
    assert isinstance(result["Stationary"], bool)

    # Invalid security
    with pytest.raises(ValueError, match="Security 'MSFT' not found in the DataFrame."):
        augmented_dickey_fuller_test(sample_data, security="MSFT")


def test_philips_perron_test(sample_data):
    """Test Phillips-Perron stationarity test."""
    result = philips_perron_test(
        sample_data,
        security="TICKER",
        trend="constant",
        lags=10,
        significance_level=0.05,
    )

    print(result["Stationary"] == bool)
    assert "Statistic" in result
    assert "p-Value" in result
    assert "Stationary" in result
    assert "Critical Values" in result
    assert result["Trend"] == "constant"
    assert isinstance(result["Stationary"], bool)

    # Invalid security
    with pytest.raises(ValueError, match="Security 'GOOG' not found in the DataFrame."):
        philips_perron_test(sample_data, security="GOOG")


def test_KPSS_test(sample_data):
    """Test KPSS stationarity test."""
    result = KPSS_test(
        sample_data,
        security="TICKER",
        trend="constant",
        lags=5,
        significance_level=0.05,
    )
    assert "Statistic" in result
    assert "p-Value" in result
    assert "Stationary" in result
    assert "Critical Values" in result
    assert result["Trend"] == "constant"
    assert isinstance(result["Stationary"], bool)

    # Invalid security
    with pytest.raises(ValueError, match="Security 'TSLA' not found in the DataFrame."):
        KPSS_test(sample_data, security="TSLA")
