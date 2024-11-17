from flask_app.dashboard._mta import MTA
from dash import html, dcc

def summary_tab(summary):
    empty = MTA.empty_chart()

    tab = \
    html.Div([
        html.Div([
            dcc.Graph(figure=summary, id="summary-stacked", className="chart", config={"displayModeBar": False})
        ], className="chart-div"),
        html.Div([
            dcc.Graph(figure=empty, id="summary-growth", className="chart", config={"displayModeBar": False})
        ], className="chart-div")
    ], className="mta-chart-div")

    return tab