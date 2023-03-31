"""Create df with model infos."""
import pandas as pd


def create_model_info(dict):
    """Create a data frame with informations about the models.

    Args:
        dict (dictionary): A dictionary containing formulas and data set restrictions in string format.

    Returns:
        pandas.DataFrame: The data frame containing formulas as strings.

    """
    if "formula" in dict:
        data_dict = {"formula": dict["formula"], "data": dict["data"]}
        df = pd.DataFrame(data_dict)
        df["model"] = range(0, 5)
        return df

    else:
        raise KeyError(
            'Formula is missing in dictionary.'
            )
