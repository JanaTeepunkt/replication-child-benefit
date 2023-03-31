"""Tests for the regression model."""

import pandas as pd
import pytest
from replication_child_benefit.analysis.model import fit_rdd_model
from replication_child_benefit.config import TEST_DIR
from replication_child_benefit.data_management.group_data import group_data
from replication_child_benefit.data_management.model_info import create_model_info

# test whether formula is given in the dictionary for model infos

@pytest.fixture()
def data():
    data_group = pd.read_csv(TEST_DIR / "data_management" / "data_fixture_grouped.csv")
    data = group_data(data_group)
    return data


@pytest.fixture()
def data_dict_false():
    ddf = {
        "data": [
            "data",
            "data[data['yearc']>=2005])",
            "data[(data['m']>=-12) & (data['m']<12)])",
            "data[(data['m']>=-9) & (data['m']<9)])",
            "data[(data['m']>=-3) & (data['m']<3)]",
        ],
    }
    return ddf

# test whether formula is a string

@pytest.fixture()
def data_dict():
    dd = {
        "formula": [1, 2, 3, 4, 5],
        "data": [
            "data",
            "data[data['yearc']>=2005])",
            "data[(data['m']>=-12) & (data['m']<12)])",
            "data[(data['m']>=-9) & (data['m']<9)])",
            "data[(data['m']>=-3) & (data['m']<3)]",
        ],
    }
    return dd


def test_create_model_info(data_dict_false):
    with pytest.raises(KeyError) as excinfo:
        create_model_info(data_dict_false)

    assert str(excinfo.value) == "'Formula is missing in dictionary.'"


def test_fit_rdd_reg(data_dict, data):
    df = create_model_info(data_dict)
    formula = df["formula"]
    with pytest.raises(TypeError) as excinfo:
        fit_rdd_model(formula, data)
    assert (
        str(excinfo.value) == "Invalid form: 'formula' must be 'string'"
    )
