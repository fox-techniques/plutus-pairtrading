# Plutus Pair-Trading and Statistical Analysis Toolkit

Plutus is a Python-based toolkit for performing pair trading and statistical analysis. This project is designed for educational purposes and provides tools for:

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