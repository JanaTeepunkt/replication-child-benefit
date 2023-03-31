"""Function for cleaning the data set."""

import numpy as np


def clean_data(data, data_info):
    """Clean data set.

    Information on data columns is stored in ``data_management/data_info.yaml``.

    Args:
        data (pandas.DataFrame): The data set.
        data_info (dict): Information on data set stored in data_info.yaml. The
            following keys can be accessed:
            - 'columns_to_drop': Names of columns that are dropped in data cleaning step
            - 'categorical_columns': Names of columns that are converted to categorical

            - 'url': URL to data set

    Returns:
        pandas.DataFrame: The cleaned data set.

    """
    for cat_col in data_info["categorical_columns"]:
        data[cat_col] = data[cat_col].astype("category")

    # transformations:
    # create running variable for month
    for year in range(2000, 2011):
        data.loc[data["year"] == year, "month"] = data["mesp"] + (year - 2008) * 12 + 5

    ## create conception variable
    # replace nas in semanas with 0
    data["semanas"] = data["semanas"].fillna(0)

    # prematurity equals 2 what means yes, 10 months if gestation weeks greater than 43 weeks and nine months in other cases.

    data["m"] = np.where(
        (data["semanas"] <= 38) & (data["semanas"] > 0) | (data["prem"] == 2),
        data["month"] - 8,
        np.where(data["semanas"] >= 44, data["month"] - 10, data["month"] - 9),
    )
    return data
