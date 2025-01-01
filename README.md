# PLUTUS: Pair-Trading Toolkit

[![Python](https://img.shields.io/badge/Python-3.10%2B-darkcyan)](https://pypi.org/project/irene-sankey/)
[![PyPI - Version](https://img.shields.io/pypi/v/plutus-pairtrading?label=PyPI%20Version&color=green)](https://pypi.org/project/plutus-pairtrading/)
[![License: MIT](https://img.shields.io/badge/License-MIT-orange.svg)](https://github.com/fox-techniques/plutus-pairtrading/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-plutus--pairtrading-181717?logo=github)](https://github.com/fox-techniques/plutus-pairtrading)

PLUTUS is a Python-based toolkit for performing pair-trading analysis. This project is designed for educational purposes and provides tools for:

- Fetching and processing financial data.
- Conducting statistical tests (stationarity and cointegration).
- Performing feature engineering.
- Visualizing financial time-series data.


## Table of Contents

- [PLUTUS: Pair-Trading Toolkit](#plutus-pair-trading-toolkit)
  - [Table of Contents](#table-of-contents)
  - [Documentation](#documentation)
  - [Key Features](#key-features)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
  - [Contribution](#contribution)
  - [License](#license)
  
## Documentation

The full documentation is available on **[GitHub Pages](https://fox-techniques.github.io/plutus-pairtrading/)**.

## Key Features

**1. Data Acquisition**

   - Fetch historical financial data using Yahoo Finance API.
   - Store and manage time-series data in a structured format.
   - Combine and preprocess data for analysis.

**2. Statistical Tests**
   - Stationarity Tests

     - Augmented Dickey-Fuller Test (ADF): Tests whether a time series is stationary.
     - Phillips-Perron Test (PP): Handles autocorrelations and heteroskedasticity.
     - KPSS Test: Tests for trend stationarity.

   - Cointegration Tests

       - Engle-Granger Test: Identifies long-term equilibrium relationships.
       - Phillips-Ouliaris Test: Handles residual-based cointegration testing.
       - Johansen Test: Detects multiple cointegration vectors.

**3. Feature Engineering**

  - Compute periodic returns (daily, weekly, monthly).
  - Apply logarithmic and exponential transformations.
  - Calculate correlation matrices and filter securities based on thresholds.
  - Identify cointegrated pairs for pair trading.

**4. Data Visualization**

  - Plot financial time-series data.
  - Generate dual-axis plots for comparing securities.
  - Visualize correlation matrices.
  - Plot autocorrelation and partial autocorrelation.


## Installation

Install **Plutus Pair-Trading Toolkit** using pip:

```bash
pip install plutus-pairtrading
```

> **Note**: Requires Python 3.10 or above.


## Quick Start

Here’s a quick example to use **PLUTUS** pair-trading tookit.

```python
  import plutus_pairtrading.data_acquisitions as dacq
  import plutus_pairtrading.data_generations as dgen
  import plutus_pairtrading.data_visualizations as dviz

  # Fetch stock data for multiple securities
  AAPL_df = dacq.fetch_yahoo_finance_data("AAPL", start_date="2015-01-01", end_date="2021-01-01")
  MSFT_df = dacq.fetch_yahoo_finance_data("MSFT", start_date="2015-01-01", end_date="2021-01-01")
  GOOG_df = dacq.fetch_yahoo_finance_data("GOOG", start_date="2015-01-01", end_date="2021-01-01")
  TSLA_df = dacq.fetch_yahoo_finance_data("TSLA", start_date="2015-01-01", end_date="2021-01-01")

  # Combine the data into a single DataFrame
  stock_df = dacq.combine_dataframes([AAPL_df, MSFT_df, GOOG_df, TSLA_df])

  # Perform pair identification
  pairs_df = dgen.pairs_identification(
      data=stock_df,
      stationarity_method="ADF",
      cointegration_method="phillips-ouliaris",
      stationarity_significance_level=0.05,
      coint_significance_level=0.05,
  )

  # Display the identified pairs
  print(pairs_df)
```

## Contribution

We welcome contributions! Visit our [Github](https://github.com/fox-techniques/plutus-pairtrading) repository, and to contribute:

1. Fork the repository.
2. Create a branch (`git checkout -b feature/NewFeature`).
3. Commit your changes (`git commit -m 'Add NewFeature'`).
4. Push to the branch (`git push origin feature/NewFeature`).
5. Open a Pull Request.


## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/fox-techniques/plutus-pairtrading/blob/main/LICENSE) file for details.
