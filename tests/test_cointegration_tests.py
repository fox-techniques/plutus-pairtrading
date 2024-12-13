import pytest
import pandas as pd
import numpy as np
from plutus_pairtrading.tests.cointegration_tests import (
    engle_granger_cointegration_test,
    phillips_ouliaris_cointegration_test,
    johansen_cointegration_test,
    validate_trend,
)


@pytest.fixture
def sample_cointegrated_data():
    """Fixture to generate cointegrated sample data."""
    np.random.seed(42)
    n = 100
    x = np.cumsum(np.random.normal(0, 1, n))
    y = 0.5 * x + np.random.normal(0, 0.5, n)
    data = pd.DataFrame({"X": x, "Y": y}, index=pd.date_range("2023-01-01", periods=n))
    return data


@pytest.fixture
def non_cointegrated_data():
    """Fixture to generate non-cointegrated sample data."""
    np.random.seed(42)
    n = 100
    x = np.cumsum(np.random.normal(0, 1, n))
    y = np.cumsum(np.random.normal(0, 1, n))
    data = pd.DataFrame({"X": x, "Y": y}, index=pd.date_range("2023-01-01", periods=n))
    return data


def test_validate_trend():
    """Test validate_trend function with valid and invalid inputs."""
    assert validate_trend("constant") == "c"
    assert validate_trend("no deterministic term") == "n"
    assert validate_trend("constant and time trend") == "ct"

    with pytest.raises(ValueError):
        validate_trend("invalid trend")


def test_engle_granger_cointegration_test(
    sample_cointegrated_data, non_cointegrated_data
):
    """Test Engle-Granger cointegration test."""
    # Test with cointegrated data
    result = engle_granger_cointegration_test(
        sample_cointegrated_data, ["X", "Y"], trend="constant"
    )
    assert "Statistic" in result
    assert "p-Value" in result
    assert "Cointegrated" in result
    assert result["Cointegrated"] is True

    # Test with non-cointegrated data
    result = engle_granger_cointegration_test(
        non_cointegrated_data, ["X", "Y"], trend="constant"
    )
    assert result["Cointegrated"] is False


def test_phillips_ouliaris_cointegration_test(
    sample_cointegrated_data, non_cointegrated_data
):
    """Test Phillips-Ouliaris cointegration test."""
    # Test with cointegrated data
    result = phillips_ouliaris_cointegration_test(
        sample_cointegrated_data, ["X", "Y"], trend="constant"
    )
    assert "Statistic" in result
    assert "p-Value" in result
    assert "Cointegrated" in result
    assert result["Cointegrated"] is True

    # Test with non-cointegrated data
    result = phillips_ouliaris_cointegration_test(
        non_cointegrated_data, ["X", "Y"], trend="constant"
    )
    assert result["Cointegrated"] is False


def test_johansen_cointegration_test(sample_cointegrated_data, non_cointegrated_data):
    """Test Johansen cointegration test."""
    # Test with cointegrated data
    result = johansen_cointegration_test(
        sample_cointegrated_data, ["X", "Y"], trend="constant", statistic="trace"
    )
    assert "Statistics and Critical Values" in result
    assert "Eigenvalues" in result
    assert "Eigenvectors" in result
    assert "Trend" in result
    assert result["#Cointegrated Vectors"] > 0

    # Test with non-cointegrated data
    result = johansen_cointegration_test(
        non_cointegrated_data, ["X", "Y"], trend="constant", statistic="trace"
    )
    assert result["#Cointegrated Vectors"] == 0

    # Test with invalid statistic
    with pytest.raises(ValueError):
        johansen_cointegration_test(
            sample_cointegrated_data, ["X", "Y"], trend="constant", statistic="invalid"
        )

    # Test with invalid trend
    with pytest.raises(ValueError):
        johansen_cointegration_test(
            sample_cointegrated_data, ["X", "Y"], trend="invalid", statistic="trace"
        )
