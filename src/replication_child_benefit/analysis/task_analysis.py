"""Tasks running the core analyses."""

import pandas as pd
import pytask

from replication_child_benefit.analysis.model import fit_rdd_model
from replication_child_benefit.config import BLD

for models in range(0, 5):

    kwargs = {
        "models": models,
        "produces": BLD / "models" / f"rdd_model_{models}.pickle",
        "depends_on": {"data": BLD / "data" / f"data_grouped_{models}.csv"},
    }

    @pytask.mark.depends_on(
        {"formula": BLD / "data" / "model_info.csv"},
    )
    @pytask.mark.task(id=models, kwargs=kwargs)
    def task_rdd_regressions(depends_on, models, produces):
        """Estimate different rdd regressions and store model."""
        data = pd.read_csv(depends_on["data"])
        df_formula = pd.read_csv(depends_on["formula"])
        form = df_formula.loc[models, "formula"]
        regression = fit_rdd_model(formula=form, data=data)

        regression.save(produces)
