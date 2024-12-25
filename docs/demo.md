# Demo 

## PLUTUS Demo

[PLUTUS] has three main modules `data_acquisitions`, `data_generations`, and  `data_visualizations`. Here’s how each `data_visualization` plot looks like:


=== "Time-series Plot"

    ![Demo plot_timeseries](assets/plot_timeseries_screenshot.png){ width=800 }

=== "Dual Y-Axis Plot"

    ![Demo plot_dual_timeseries](assets/plot_dual_timeseries_screenshot.png){ width=800 }

=== "Correlation Matrix"

    ![Demo plot_correlation_matrix](assets/plot_correlation_matrix_screenshot.png){ width=800 }

=== "ACF and PACF"

    ![Demo plot_acf](assets/plot_acf_screenshot.png){ width=800 }

    ![Demo plot_pacf](assets/plot_pacf_screenshot.png){ width=800 }

## How to Use

Once the PLUTUS package is installed, you can use it in your projects. Here’s the code of the demo: 

```py title="plutus_pairtrading_demo.py" linenums="1"
import pandas as pd
from irene_sankey.core.traverse import traverse_sankey_flow
from irene_sankey.plots.sankey import plot_irene_sankey_diagram

# Sample data to test the functionality
input_df = pd.DataFrame(
    {
        "country": ["NL","NL","NL","DE","DE","FR","FR","FR","US","US","US"],
        "industry": [
            "Technology","Finance","Healthcare",
            "Automotive","Engineering",
            "Technology","Agriculture","Healthcare",
            "Manufacturing","Technology","Finance"],
        "field": [
            "Software","Banking","Pharmaceuticals",
            "Car Manufacturing","Mechanical Engineering",
            "Software","Crop Science","Medical Devices",
            "Electronics","AI & Robotics","Investment Banking"],
    }
)

# Generate source-target pair, node map and link for Sankey diagrams
flow_df, node_map, link = traverse_sankey_flow(input_df, ["", "country", "industry", "field"])

# Plot Sankey diagram 
fig = plot_irene_sankey_diagram(node_map, link, title = "Irene-Sankey Demo", node_config={
        "pad": 10,
        "line": dict(color="black", width=1),
    }
)
fig.show()
```
!!! tip

    You can use `node_map` and `link` with your own Plotly’s Sankey diagram functions.


Thank you for exploring our demo! We hope this example has given you a clear understanding of how to utilize our package and integrate its features into your projects. Whether you're just getting started or diving deeper, our goal is to make your experience as seamless and productive as possible.

Happy coding!

  [PLUTUS]: https://pypi.org/project/plutus-pairtrading/
  [virtual environment]: https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment