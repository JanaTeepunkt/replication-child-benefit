import numpy as np


def plot_data(data):
    """Create the data set ready for plotting.

    Args:
        data (pandas.DataFrame): The grouped data set.

    Returns:
        pandas.DataFrame: The data ready for plotting.

    """
    # create helping variable to group data bimonthly
    data["bimonthly"] = np.repeat(range(1, 61), 2)
    data = data.groupby(["bimonthly"]).mean().reset_index()
    data = data[["m", "conc", "month"]]
    # create variable for highlighting July-August months
    data["highlight"] = np.where(data["month"] == 7.5, 1, 0)
    # restrict plot to 30 months around cutoff
    data = data[(data["m"] > -31) & (data["m"] < 30)].reset_index(drop=True)

    return data
