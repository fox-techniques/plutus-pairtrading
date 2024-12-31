# Demo 

## PLUTUS Pair Identification

In this section, we demonstrate how to identify cointegrated pairs using the PLUTUS package.

```py title="plutus_pair_identification_demo.py" linenums="1"
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

## PLUTUS Stationarity Tests

PLUTUS provides a comprehensive suite of statistical tests to assess the properties of financial time-series data, ensuring robust pair-trading strategies. These tests help evaluate stationarity:

- **Augmented Dickey-Fuller (ADF)** evaluates whether a series is stationary or contains a unit root.
- **Phillips-Perron (PP)** is a non-parametric test for stationarity.
- **Kwiatkowski-Phillips-Schmidt-Shin (KPSS)** checks if a series is stationary around a deterministic trend.

### Augmented Dickey-Fuller

=== "ADF"

    ```py title="plutus_stationarity_test_ADF_demo.py" linenums="1"

    import plutus_pairtrading.data_acquisitions as dacq
    import plutus_pairtrading.tests as tsts

    # Fetch stock data
    TSLA_df = dacq.fetch_yahoo_finance_data("TSLA", start_date="2020-01-01", end_date="2024-12-30")

    # Perform ADF Test
    ADF_result = tsts.augmented_dickey_fuller_test(
        data=TSLA_df,
        security="TSLA_close",
        trend="constant",
        significance_level=0.05,
    )

    print(ADF_result)
    ```


=== "Result"

    ```py
    {
        "Statistic": -1.93, 
        "p-Value": 0.318, 
        "Stationary": False, 
        "Lags": 10, 
        "Trend": "constant", 
        "Critical Values": {
            "1%": -3.44, 
            "5%": -2.86,
            "10%": -2.57
            }
    }
    ```
### Phillips-Perron

=== "PP"

    ```py title="plutus_stationarity_test_PP_demo.py" linenums="1"
    import plutus_pairtrading.data_acquisitions as dacq
    import plutus_pairtrading.tests as tsts

    # Fetch stock data
    TSLA_df = dacq.fetch_yahoo_finance_data("TSLA", start_date="2020-01-01", end_date="2024-12-30")

    # Perform PP Test
    PP_result = tsts.philips_perron_test(
        data=TSLA_df,
        security="TSLA_close",
        trend="constant",
        significance_level=0.05,
    )

    print(PP_result)
    ```
=== "Result"

    ```py
    {
        "Statistic": -0.49,
        "p-Value": 0.89,
        "Stationary": False,
        "Lags": 1255,
        "Trend": "constant",
        "Critical Values": {
            "1%": -3.44,
            "5%": -2.86,
            "10%": -2.57
        }
    }
    ```

### Kwiatkowski-Phillips-Schmidt-Shin

=== "KPSS"

    ```py title="plutus_stationarity_test_PP_demo.py" linenums="1"
    import plutus_pairtrading.data_acquisitions as dacq
    import plutus_pairtrading.tests as tsts

    # Fetch stock data 
    TSLA_df = dacq.fetch_yahoo_finance_data("TSLA", start_date="2020-01-01", end_date="2024-12-30")

    # Perform KPSS Test
    KPSS_result = tsts.KPSS_test(
        data=TSLA_df,
        security="TSLA_close",
        trend="constant",
        significance_level=0.05,
    )

    print(KPSS_result)
    ```
=== "Result"

    ```py
    {
        "Statistic": 1.51,
        "p-Value": 0.0002,
        "Stationary": False,
        "Lags": 20,
        "Trend": "constant",
        "Critical Values": {
            "1%": 0.743,
            "5%": 0.461,
            "10%": 0.348
        }
    }

    ```


## PLUTUS Cointegration Tests

PLUTUS provides a comprehensive suite of statistical tests to assess the properties of financial time-series data, ensuring robust pair-trading strategies. These tests help evaluate integration order, and cointegration between time-series. Available tests are:

- **Engle-Granger** performs test for cointegration between two time-series.
- **Phillips-Ouliaris** is another  method to assess cointegration between two series.
- **Johansen** evaluates cointegration among multiple time-series.

These tests are critical for identifying relationships between time-series and determining their suitability for pair-trading strategies.

### Engle-Granger

=== "Engle-Granger"

    ```py title="plutus_pairtrading_cointegration_EG_test.py" linenums="1"

    import plutus_pairtrading.data_acquisitions as dacq
    import plutus_pairtrading.tests as tsts

    # Fetch stock data for multiple securities
    TSLA_df = dacq.fetch_yahoo_finance_data("TSLA", start_date="2020-01-01", end_date="2024-12-30")
    GE_df = dacq.fetch_yahoo_finance_data("GE", start_date="2020-01-01", end_date="2024-12-30")

    # Combine the historical data of the stocks
    stock_df = dacq.combine_dataframes([TSLA_df, GE_df])

    # Perform Engle-Granger Test
    result = tsts.engle_granger_cointegration_test(
        data=stock_df,
        securities=["TSLA_close", "GE_close"],
        trend="constant",
        significance_level=0.05,
    )

    print(result)
    ```
=== "Result"

    ```py
    {
        "Cointegrated": False,
        "Cointegrated Vector": {
            "TSLA_close": 1.0,
            "GE_close": -0.48711,
            "const": -174.772825
        },
        "Critical Value": -3.34,
        "Statistic": -2.25,
        "Trend": "c",
        "p-Value": 0.3986,
        "spread_TSLA_close_GE_close": {
            "2020-01-02": -175.05,
            "2020-01-03": -174.30,
            "2020-01-06": -174.14,
            "2020-01-07": -172.76,
            "2020-01-08": -170.95,
            "...": "...",
            "2024-12-24": 203.97,
            "2024-12-26": 195.50,
            "2024-12-27": 174.04
        }
    }
    ```

### Phillips-Ouliaris

=== "Phillips-Ouliaris"

    ```py title="plutus_pairtrading_cointegration_PO_test.py" linenums="1"

    import plutus_pairtrading.data_acquisitions as dacq
    import plutus_pairtrading.tests as tsts

    # Fetch stock data for multiple securities
    TSLA_df = dacq.fetch_yahoo_finance_data("TSLA", start_date="2020-01-01", end_date="2024-12-30")
    GE_df = dacq.fetch_yahoo_finance_data("GE", start_date="2020-01-01", end_date="2024-12-30")

    # Combine the historical data of the stocks
    stock_df = dacq.combine_dataframes([TSLA_df, GE_df])

    # Perform Engle-Granger Test
    result = tsts.phillips_ouliaris_cointegration_test(
        data=stock_df,
        securities=["TSLA_close", "GE_close"],
        trend="constant",
        significance_level=0.05,
    )

    print(result)
    ```

=== "Result"

    ```py
    {
        "Statistic": -2.0986,
        "p-Value": 0.4757,
        "Critical Value": -3.3435,
        "Trend": "c",
        "Cointegrated Vector": {
            "TSLA_close": 1.0,
            "GE_close": -0.48711,
            "const": -174.772825
        },
        "Cointegrated": False,
        "spread_TSLA_close_GE_close": {
            "2020-01-02": -175.0528,
            "2020-01-03": -174.2999,
            "2020-01-06": -174.1439,
            "2020-01-07": -172.7574,
            "2020-01-08": -170.9517,
            "...": "...",
            "2024-12-24": 203.9726,
            "2024-12-26": 195.5012,
            "2024-12-27": 174.0395
        }
    }

    ```

### Johannes

=== "Johannes"

    ```py title="plutus_pairtrading_cointegration_J_test.py" linenums="1"

    import plutus_pairtrading.data_acquisitions as dacq
    import plutus_pairtrading.tests as tsts

    # Fetch stock data for multiple securities
    TSLA_df = dacq.fetch_yahoo_finance_data("TSLA", start_date="2020-01-01", end_date="2024-12-30")
    GE_df = dacq.fetch_yahoo_finance_data("GE", start_date="2020-01-01", end_date="2024-12-30")

    # Combine the historical data of the stocks
    stock_df = dacq.combine_dataframes([TSLA_df, GE_df])

    # Perform Engle-Granger Test
    result = tsts.phillips_ouliaris_cointegration_test(
        data=stock_df,
        securities=["TSLA_close", "GE_close"],
        trend="constant",
        significance_level=0.05,
    )

    print(result)
    ```

=== "Result"

    ```py
    {
        "Statistics and Critical Values": [
            {
                "Null Hypothesis": "r<=0",
                "Statistic": 20.9772,
                "Critical Value (95%)": 29.7961
            },
            {
                "Null Hypothesis": "r<=1",
                "Statistic": 6.7329,
                "Critical Value (95%)": 15.4943
            },
            {
                "Null Hypothesis": "r<=2",
                "Statistic": 0.0030,
                "Critical Value (95%)": 3.8415
            }
        ],
        "Eigenvalues": [0.0112948, 0.0053524, 0.0000024],
        "Eigenvectors": [
            [0.0187234, 0.0059437, -0.0072621],
            [0.0370668, -0.0278356, -0.0166753],
            [-0.0653901, 0.0167287, 0.0012695]
        ],
        "Trend": "constant",
        "#Cointegrated Vectors": 0,
        "Spread": {
            "2020-01-02": -2.1689,
            "2020-01-03": -2.0979,
            "2020-01-06": -2.0945,
            "2020-01-07": -2.0663,
            "2020-01-08": -2.1362,
            "...": "...",
            "2024-12-24": -1.8717,
            "2024-12-26": -2.0534,
            "2024-12-27": -2.3266
        }
    }

    ```




## PLUTUS Data Acquisition 

This section highlights how to acquire data using the PLUTUS package:

You can fetch historical financial data for multiple tickers using the fetch_yahoo_finance_data function.

=== "Code"

    ```py title="data_acquisition_demo.py" linenums="1"

    import plutus_pairtrading.data_acquisitions as dacq

    # Fetch stock data for AAPL, MSFT, and TSLA
    AAPL_df = dacq.fetch_yahoo_finance_data(
        "AAPL", start_date="2015-01-01", end_date="2021-01-01",
    )
    MSFT_df = dacq.fetch_yahoo_finance_data(
        "MSFT", start_date="2015-01-01", end_date="2021-01-01"
    )
    TSLA_df = dacq.fetch_yahoo_finance_data(
        "TSLA", start_date="2015-01-01", end_date="2021-01-01"
    )

    # Combine the data into a single DataFrame
    stock_df = dacq.combine_dataframes([AAPL_df, MSFT_df, TSLA_df])

    # Save the data to CSV files
    dacq.store_data_as_csv(AAPL_df, "data/tickers/AAPL.csv", )
    dacq.store_data_as_csv(MSFT_df, "data/tickers/MSFT.csv")
    dacq.store_data_as_csv(TSLA_df, "data/tickers/TSLA.csv")

    combined_df = dacq.read_and_combine_ticker_files(
        directory_path="data/tickers",
        tickers=["AAPL", "MSFT", "TSLA"],
        date_column="date",
        column_suffix=["close", "close_adj"],
        join_type="inner",
    )
    ```

=== "Combined DataFrame"

    | date       | AAPL_close_adj | AAPL_close | MSFT_close_adj | MSFT_close | TSLA_close_adj | TSLA_close |
    |------------|----------------|------------|----------------|------------|----------------|------------|
    | 2015-01-02 | 24.347172      | 27.332500  | 40.232841      | 46.759998  | 14.620667      | 14.620667  |
    | 2015-01-05 | 23.661276      | 26.562500  | 39.862869      | 46.330002  | 14.006000      | 14.006000  |
    | 2015-01-06 | 23.663506      | 26.565001  | 39.277802      | 45.650002  | 14.085333      | 14.085333  |
    | 2015-01-07 | 23.995310      | 26.937500  | 39.776840      | 46.230000  | 14.063333      | 14.063333  |
    | 2015-01-08 | 24.917269      | 27.972500  | 40.946987      | 47.590000  | 14.041333      | 14.041333  |


=== "Time-Series Plot"

    ![Demo plot_time_series_for_dacq](assets/dacq_plot_timeseries_screenshot.png){ width=800 }


## PLUTUS Data Visualization

[PLUTUS] has `data_visualizations` module. Here’s how each plot for pair-trading looks like:


=== "ACF and PACF"

    ![Demo plot_acf](assets/plot_acf_screenshot.png){ width=800 }

    ![Demo plot_pacf](assets/plot_pacf_screenshot.png){ width=800 }

    Here is the code to plot autocorrelation and partial-autocorrelation functions for a security:
    

    ```py title="plutus_plot_acf_pacf_demo.py" linenums="1"

    import plutus_pairtrading.data_acquisitions as dacq
    import plutus_pairtrading.data_visualizations as dviz

    # Fetch stock data
    AAPL_df = dacq.fetch_yahoo_finance_data("AAPL", start_date="2015-01-01", end_date="2021-01-01")   

    # Plot autocorrelation plot
    acf_fig = dviz.plot_acf(AAPL_df, security="AAPL_close")
    
    # Plot partial-autocorrelation plot
    pacf_fig = dviz.plot_pacf(AAPL_df, security="AAPL_close")

    #acf_fig.show() 
    pacf_fig.show()
    ```
    
=== "Correlation Matrix"

    ![Demo plot_correlation_matrix](assets/plot_correlation_matrix_screenshot.png){ width=800 }

    Here is the code to generate the correlation matrix plot: 
    

    ```py title="plutus_plot_correlation_matrix_demo.py" linenums="1"

    import plutus_pairtrading.data_acquisitions as dacq
    import plutus_pairtrading.data_visualizations as dviz

    # Fetch stock data
    AAPL_df = dacq.fetch_yahoo_finance_data("AAPL", start_date="2015-01-01", end_date="2021-01-01")   
    MSFT_df = dacq.fetch_yahoo_finance_data("MSFT", start_date="2015-01-01", end_date="2021-01-01")   
    GOOG_df = dacq.fetch_yahoo_finance_data("GOOG", start_date="2015-01-01", end_date="2021-01-01")

    stock_df = dacq.combine_dataframes([AAPL_df, MSFT_df, GOOG_df])

    # Plot correlation matrix
    fig = dviz.plot_correlation_matrix(
        data=stock_df,
        securities=["AAPL_close", "MSFT_close", "GOOG_close"],
    )

    fig.show() 
    ```

=== "Time-series Plot"

    ![Demo plot_timeseries](assets/plot_timeseries_screenshot.png){ width=800 }

    Here is the code to generate the time-series plot: 

    ```py title="plutus_plot_timeseries_demo.py" linenums="1"

    import plutus_pairtrading.data_acquisitions as dacq
    import plutus_pairtrading.data_visualizations as dviz

    # Fetch stock data
    AAPL_df = dacq.fetch_yahoo_finance_data("AAPL", start_date="2015-01-01", end_date="2021-01-01")   
    MSFT_df = dacq.fetch_yahoo_finance_data("MSFT", start_date="2015-01-01", end_date="2021-01-01")   
    GOOG_df = dacq.fetch_yahoo_finance_data("GOOG", start_date="2015-01-01", end_date="2021-01-01")

    stock_df = dacq.combine_dataframes([AAPL_df, MSFT_df, GOOG_df])

    # Plot time-series
    fig = dviz.plot_timeseries(
        data=stock_df,
        securities=["AAPL_close", "MSFT_close", "GOOG_close"],
        plot_title="Stock Prices",
        x_label="Date",
        y_label="Price",
        line_colors=["#6F5AD6", "#E28A37", "#328847"],
    )

    fig.show()   
    ```


=== "Dual Y-Axis Plot"

    ![Demo plot_dual_timeseries](assets/plot_dual_timeseries_screenshot.png){ width=800 }

    Here is the code to generate the dual y-axis time-series plot: 
    

    ```py title="plutus_plot_dual_timeseries_demo.py" linenums="1"

    import plutus_pairtrading.data_acquisitions as dacq
    import plutus_pairtrading.data_visualizations as dviz

    # Fetch stock data
    MSFT_df = dacq.fetch_yahoo_finance_data("MSFT", start_date="2015-01-01", end_date="2021-01-01")   
    GOOG_df = dacq.fetch_yahoo_finance_data("GOOG", start_date="2015-01-01", end_date="2021-01-01")

    stock_df = dacq.combine_dataframes([MSFT_df, GOOG_df])

    # Plot dual y-axis time-series
    fig = dviz.plot_dual_timeseries(
        data=stock_df,
        securities=["GOOG_close", "MSFT_close"],
        plot_title="Stock Prices",
        line_colors=["#3C8BE5", "#C93F8C"],
    )

    fig.show() 
    ```

Thank you for exploring our demo! We hope this example has given you a brief understanding of how to utilize our package and integrate its features into your projects. Whether you're just getting started or diving deeper, our goal is to make your experience as seamless and productive as possible.

Happy coding!

  [PLUTUS]: https://pypi.org/project/plutus-pairtrading/
  [virtual environment]: https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment