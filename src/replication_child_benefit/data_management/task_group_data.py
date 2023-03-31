"""Tasks for creating the grouped data for regressions."""

import pandas as pd
import pytask

from replication_child_benefit.config import BLD
from replication_child_benefit.data_management.group_data import group_data


@pytask.mark.depends_on(
    {
        "scripts": ["group_data.py"],
        "data": BLD / "data" / "data_clean.csv",
    },
)
@pytask.mark.produces(BLD / "data" / "data_grouped.csv")
def task_group_data(depends_on, produces):
    """Group the cleaned data set by month."""
    data = pd.read_csv(depends_on["data"])
    data = group_data(data)

    data.to_csv(produces, index=False)


# Create data sets for rdd-regressions
for models in range(0, 5):

    kwargs = {
        "models": models,
        "produces": BLD / "data" / f"data_grouped_{models}.csv",
    }

    @pytask.mark.depends_on(
        {
            "data": BLD / "data" / "data_grouped.csv",
        },
    )
    @pytask.mark.task(id=models, kwargs=kwargs)
    def task_reg_data(depends_on, produces, models):
        """Create different data frames for the five regression models."""
        data = pd.read_csv(depends_on["data"])

        if models == 0:
            data = data
        elif models == 1:
            data = data[data["yearc"] >= 2005]
        elif models == 2:
            data = data[(data["m"] >= -12) & (data["m"] < 12)]
        elif models == 3:
            data = data[(data["m"] >= -9) & (data["m"] < 9)]
        else:
            data = data[(data["m"] >= -3) & (data["m"] < 3)]

        data.to_csv(produces, index=False)
