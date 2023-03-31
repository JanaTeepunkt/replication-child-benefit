"""Tests for the data management process."""

import pandas as pd
import pytest
from replication_child_benefit.config import TEST_DIR
from replication_child_benefit.data_management.clean_data import clean_data
from replication_child_benefit.data_management.group_data import group_data
from replication_child_benefit.data_management.plot_data import plot_data
from replication_child_benefit.utilities import read_yaml


@pytest.fixture()
def data():
    return pd.read_stata(TEST_DIR / "data_management" / "data_fixture.dta")


@pytest.fixture()
def data_grouped():
    return pd.read_csv(TEST_DIR / "data_management" / "data_fixture_grouped.csv")


@pytest.fixture()
def data_info():
    return read_yaml(TEST_DIR / "data_management" / "data_info_fixture.yaml")

# test whether all NAs were replaced by 0

def test_clean_data_repna(data, data_info):
    data_clean = clean_data(data, data_info)
    assert not data_clean.isna().any(axis=None)

# test whether all categorical variables are marked as "categorical"

def test_clean_data_categorical_columns(data, data_info):
    data_clean = clean_data(data, data_info)
    for cat_col in data_info["categorical_columns"]:
        assert data_clean[cat_col].dtype == "category"

# test whether data frame only contains obs. between 2000 and 2009

def test_obs_period(data_grouped):
    data = group_data(data_grouped)
    assert (data["yearc"] <= 2009).all()
    assert (data["yearc"] >= 2000).all()

# test wether the plot data are limited from -30 to 29

def test_plot_data_period(data_grouped):
    data = group_data(data_grouped)
    data_plot = plot_data(data)
    assert (data_plot["m"] <= 29).all()
    assert (data_plot["m"] >= -30).all()
