from dash import html, dcc

def summary_tab(summary_totals, summary_avg):

    tab = \
    html.Div([
        html.Div([
            dcc.Graph(figure=summary_totals, id="summary-stacked", className="chart", config={"displayModeBar": False})
        ], className="chart-div"),
        html.Div([
            dcc.Graph(figure=summary_avg, id="summary-avg", className="chart", config={"displayModeBar": False})
        ], className="chart-div")
    ], className="mta-chart-div")

    return tab