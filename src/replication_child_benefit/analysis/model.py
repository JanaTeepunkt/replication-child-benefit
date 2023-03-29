"""Functions for fitting the regression model."""

import statsmodels.formula.api as smf
from statsmodels.iolib.smpickle import load_pickle


def fit_rdd_model(formula, data):
    """Fit rdd models
    Args:
        formula: String variable from data frame (model_info).
        data (pandas.DataFrame): The data set for the regression.

    Returns:
        Fitted rdd model.
    """
    fit = smf.ols(formula=formula, data=data).fit(cov_type="HC1")

    return fit


def load_model(path):
    """Load statsmodels model.

    Args:
        path (str or pathlib.Path): Path to model file.

    Returns:
        statsmodels.base.model.Results: The stored model.

    """
    return load_pickle(path)
