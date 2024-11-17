from flask_app.dashboard._mta import MTA
from dash import html, dcc

def monthly_tab():

    empty = MTA.empty_chart()

    tab = \
    html.Div([
                        
        html.Div([
            dcc.Dropdown(options=["Subways", "Buses", "LIRR", "Metro-North", "Access-A-Ride","Bridges and Tunnels", "Staten Island Railway"], 
                            value="Subways", multi=False, id="mta-dropwdown"),
            html.Button("Run", id="mta-btn")
        ], className="dropdown-container"),

        html.Div([
            html.Div([
                html.Div(children="-", id="avg-monthly-riders", className="metric-value"),
                html.H3("6 Month Avg. Monthly Riders", className="metric-title")
            ], className="metric-card first-card"),
            html.Div([
                html.Div(children="-", id="avg-daily-riders", className="metric-value"),
                html.H3("6 Month Avg. Daily Riders", className="metric-title")
            ], className="metric-card"),
            html.Div([
                html.Div(children="-", id="avg-growth", className="metric-value"),
                html.H3("6 Month Avg. Growth (M)", className="metric-title")
            ], className="metric-card"),
            html.Div([
                html.Div(children="-", id="growth", className="metric-value"),
                html.H3("Growth Since Pandemic", className="metric-title")
            ], className="metric-card"),
            html.Div([
                html.Div(children="-", id="percent-total", className="metric-value"),
                html.H3("% of Total", className="metric-title")
            ], className="metric-card")
        ], className="metric-parent"),

        html.Div([
            html.Div([
                dcc.Graph(id="mta-monthly-chart", figure=empty, className="chart", config={"displayModeBar": False})
            ], className="chart-child first-card"),
            html.Div([
                dcc.Graph(id="mta-moving-avg", figure=empty, className="chart", config={"displayModeBar": False})
            ], className="chart-child")
        ], className="chart-combined"),
        html.Div([
            dcc.Graph(id="percent-pre-pandemic", figure=empty, className="chart", config={"displayModeBar": False})
        ], className="chart-div")

    ], className="mta-chart-div")

    return tab