"""Tasks for creating the data set for plotting."""

import pandas as pd
import pytask

from replication_child_benefit.config import BLD
from replication_child_benefit.data_management.plot_data import plot_data


@pytask.mark.depends_on(
    {
        "scripts": ["plot_data.py"],
        "data": BLD / "data" / "data_grouped.csv",
    },
)
@pytask.mark.produces({"data_plot": BLD / "data" / "data_plot.csv"})
def task_plot_data(depends_on, produces):
    """Create the data set for the plot."""
    data = pd.read_csv(depends_on["data"])
    data = plot_data(data)
    data.to_csv(produces["data_plot"], index=False)
