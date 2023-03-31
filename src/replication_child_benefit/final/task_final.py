"""Tasks running the results formatting (tables, figures)."""

import pandas as pd
import pytask

from replication_child_benefit.analysis.model import load_model
from replication_child_benefit.config import BLD
from replication_child_benefit.final.plot import plot_bimonthly_conc


@pytask.mark.depends_on(
    {
        "data_grouped": BLD / "data" / "data_grouped.csv",
        "data_plot": BLD / "data" / "data_plot.csv",
    },
)
@pytask.mark.produces(BLD / "figures" / "bimonthly_conc.png")
def task_plot_bimonthly_conc(depends_on, produces):
    """Plot the bimonthly average conception rate."""
    data_grouped = pd.read_csv(depends_on["data_grouped"])
    data_plot = pd.read_csv(depends_on["data_plot"])
    fig = plot_bimonthly_conc(data_grouped, data_plot)
    fig.write_image(produces)


for models in range(0, 5):
    kwargs = {
        "models": models,
        "produces": BLD / "tables" / f"rdd_results_{models}.tex",
        "depends_on": BLD / "models" / f"rdd_model_{models}.pickle",
    }

    @pytask.mark.task(id=models, kwargs=kwargs)
    def task_create_results_table(depends_on, produces, models):
        """Store a table in LaTeX format with the estimation results for each regression."""
        model = load_model(depends_on)
        table = model.summary().as_latex()
        with open(produces, "w") as f:
            f.writelines(table)
