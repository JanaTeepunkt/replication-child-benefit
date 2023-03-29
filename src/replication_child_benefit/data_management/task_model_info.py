"""Tasks for creating an informational data set for the regressions."""

import pytask

from replication_child_benefit.config import BLD
from replication_child_benefit.data_management.model_info import create_model_info

data_dict = {
    "formula": [
        "log_conc ~ post + m*post + m_2*post + m_3*post + days",
        "log_conc ~ post + m*post + m_2*post + days",
        "log_conc ~ post + m*post + m_2*post + days",
        "log_conc ~ post + m*post + days",
        "log_conc ~ post + days",
    ],
    "data": [
        "data",
        "data[data['yearc']>=2005])",
        "data[(data['m']>=-12) & (data['m']<12)])",
        "data[(data['m']>=-9) & (data['m']<9)])",
        "data[(data['m']>=-3) & (data['m']<3)]",
    ],
}


@pytask.mark.produces(BLD / "data" / "model_info.csv")
def task_model_info(produces):
    """Creates a data frame including the formulas for the models."""
    df = create_model_info(data_dict)
    df.to_csv(produces)
