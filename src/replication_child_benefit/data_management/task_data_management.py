"""Tasks for managing the data."""

import pandas as pd
import pytask

from replication_child_benefit.config import BLD, SRC
from replication_child_benefit.data_management import clean_data
from replication_child_benefit.utilities import read_yaml


@pytask.mark.depends_on(
    {
        "scripts": ["clean_data.py", "group_data.py", "plot_data.py"],
        "data_info": SRC / "data_management" / "data_info.yaml",
        "data": SRC / "data" / "data_births_20110196.dta",
    },
)
@pytask.mark.produces(
    {
        "data_clean": BLD / "data" / "data_clean.csv",
    },
)
def task_clean_data(depends_on, produces):
    """Clean the data."""
    data_info = read_yaml(depends_on["data_info"])
    data = pd.read_stata(depends_on["data"])
    data = clean_data(data, data_info)
    data.to_csv(produces["data_clean"], index=False)
