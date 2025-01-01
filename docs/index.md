---
title: PLUTUS Pair-Trading Toolkit
---

# PLUTUS: Pair-Trading Toolkit

![PLUTUS Flyer](assets/plutus-flyer.png){ width=200 }

[![Python](https://img.shields.io/badge/Python-3.10%2B-darkcyan)](https://pypi.org/project/plutus-pairtrading/)
[![PyPI - Version](https://img.shields.io/pypi/v/plutus-pairtrading?label=PyPI%20Version&color=green)](https://pypi.org/project/plutus-pairtrading/)
[![License: MIT](https://img.shields.io/badge/License-MIT-orange.svg)](https://github.com/fox-techniques/plutus-pairtrading/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-plutus--pairtrading-181717?logo=github)](https://github.com/fox-techniques/plutus-pairtrading)

PLUTUS is a Python-based toolkit for performing pair-trading analysis. This project is designed for educational purposes and provides analysis tools for:

- Fetching and processing financial data.
- Conducting statistical tests (stationarity and cointegration).
- Performing feature engineering.
- Visualizing financial time-series data.


## Key Features

**1. Data Acquisition**

   - Fetch historical financial data using Yahoo Finance API.
   - Store and manage time-series data in a structured format.
   - Combine and preprocess data for analysis.

**2. Statistical Tests**

   - Stationarity Tests
  
     - *Augmented Dickey-Fuller Test (ADF)* tests whether a time series is stationary.
     - *Phillips-Perron Test (PP)* handles autocorrelations and heteroskedasticity.
     - *KPSS* tests for trend stationarity.

   - Cointegration Tests
  
       - *Engle-Granger* identifies long-term equilibrium relationships.
       - *Phillips-Ouliaris* handles residual-based cointegration testing.
       - *Johansen Test* detects multiple cointegration vectors.

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
  
--- 

## Quick Links

- [PyPI](https://pypi.org/project/plutus-pairtrading)
- [GitHub Repository](https://github.com/fox-techniques/plutus-pairtrading)
- [License](https://github.com/fox-techniques/plutus-pairtrading/blob/main/LICENSE)

Explore the documentation to learn how to customize and make the most of **PLUTUS Pair-Trading Toolkit** for your project!
