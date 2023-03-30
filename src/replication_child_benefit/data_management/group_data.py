import numpy as np


def group_data(data):
    """Create grouped data set by month and variables necessary for regression.

    Args:
        data(pandas.DataFrame): The cleaned data set.

    Returns:
        pandas.DataFrame: The grouped data set with regression variables.

    """
    # group dataset by month of conc ('m') to get cumulated conception rates per month
    data = data.groupby("m").size().reset_index(name="conc")
    # create post dummy
    data["post"] = np.where(data["m"] >= 0, 1, 0)

    # restrict dataset to years 2000 (m=-90) until 2009 (m=29)
    data = data[(data["m"] > -91) & (data["m"] < 30)]

    # create month of conception within a year variable
    data["month"] = np.tile(range(1, 13), 10)

    ## create days in a month variable
    # leap years: 2000, 2004, 2008 -> m=-89, m=-41,m=7
    data["days"] = np.where(
        (data["month"] == 4)
        | (data["month"] == 6)
        | (data["month"] == 9)
        | (data["month"] == 11),
        30,
        np.where((data["month"] == 2), 28, 31),
    )

    data["days"] = np.where(
        (data["m"] == -89) | (data["m"] == -41) | (data["m"] == 7),
        29,
        data["days"],
    )

    # create year of conception variable
    data["yearc"] = np.repeat(range(2000, 2010), 12)

    # add log(conc)
    data["log_conc"] = np.log(data["conc"])
    # add m^2 and m^3 for quadratic and cubic trend in running variable
    data["m_2"] = np.square(data["m"])
    data["m_3"] = np.power(data["m"], 3)

    return data
