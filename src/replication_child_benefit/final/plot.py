"""Functions plotting conception rates."""

import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression


def plot_bimonthly_conc(data_grouped, data_plot):
    """Plot bimonthly conceptions rates with trend line before and after the cutoff date.

    Args:
        data_grouped (pandas.DataFrame): The grouped data set.
        data_plot (pandas.DataFrame): The data for plotting containing aid variables for the plot.

    Returns:
        plotly.graph_objects.Figure: The figure.

    """
    ## regressions for trend lines
    # regression before cutoff
    data1 = data_grouped[(data_grouped["m"] >= -30) & (data_grouped["m"] < 0)]
    x_data1 = np.array(data1["m"]).reshape((-1, 1))
    y_data1 = np.array(data1["conc"])
    model1 = LinearRegression().fit(x_data1, y_data1)
    X1_predict = np.array(data_plot.m[data_plot["m"] < 0]).reshape((-1, 1))
    y1_predict = model1.predict(X1_predict)

    # regression after cutoff
    data2 = data_grouped[(data_grouped["m"] <= 30) & (data_grouped["m"] >= 0)]
    x_data2 = np.array(data2["m"]).reshape((-1, 1))
    y_data2 = np.array(data2["conc"])
    model2 = LinearRegression().fit(x_data2, y_data2)
    X2_predict = np.array(data_plot.m[data_plot["m"] >= 0]).reshape((-1, 1))
    y2_predict = model2.predict(X2_predict)

    # data_grouped
    x = data_plot.m
    y = data_plot.conc

    # dots
    trace = go.Scatter(x=x, y=y, mode="markers", marker={"color": data_plot.highlight})

    # layout
    layout = go.Layout(
        title="Number of Conceptions by month, 2005 - 2009",
        title_x=0.5,
        yaxis={
            "range": [35000, 45000],
            "showline": True,
            "linecolor": "black",
            "nticks": 6,
            "title": go.layout.yaxis.Title(
                text="Conceptions",
                font={"size": 14, "color": "black"},
            ),
            "tickformat": "000",
        },
        xaxis={
            "range": [-30, 30],
            "showline": True,
            "linecolor": "black",
            "title": go.layout.xaxis.Title(
                text="Month of conception (0=July 2007)",
                font={"size": 14, "color": "black"},
            ),
        },
        plot_bgcolor="rgb(255,255,255)",
        showlegend=False,
    )

    fig = go.Figure(data=[trace], layout=layout)

    # add vertical line at cutoff
    fig.add_vline(x=0, line_dash="solid", line_color="black")
    # add regression lines at both sides of cutoff
    fig.add_trace(
        go.Scatter(x=data_plot.m[data_plot["m"] < 0], y=y1_predict, mode="lines"),
    )
    fig.add_trace(
        go.Scatter(x=data_plot.m[data_plot["m"] >= 0], y=y2_predict, mode="lines"),
    )
    fig.show()

    return fig
