from flask_app.dashboard.callbacks.data_backbacks import init_callback
from flask_app.dashboard.mta._mta import MTA
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

def create_dash(server):

    app = Dash(
        server=server,
        routes_pathname_prefix="/dashboard/",
        suppress_callback_exceptions=False,
        external_stylesheets=[dbc.themes.ZEPHYR, "/static/stylesheet.css"]
    )

    app.layout = \
    html.Div([
        dbc.Navbar(
            html.Div([
                html.H3("Welcome", className="titles")
            ], className="title-container"), 
            dark=True, color="primary", className="navigation"
        ),
        dbc.Tabs([
            dbc.Tab(
                label="Monthly",
                children=[
                    html.Div([

                        dcc.Dropdown(options=["Subways", "Buses", "LIRR", "Metro-North", "Access-A-Ride","Bridges and Tunnels", "Staten Island Railway"], 
                                     value="Subways", multi=False, id="mta-dropwdown"),

                        html.Div([
                            html.Div([
                                html.Div(children="-", id="current-month", className="metric-value"),
                                html.H3(children="Current Month", className="metric-title")
                            ], className="metric-card first-card"),
                            html.Div([
                                html.Div(children="-", id="avg-riders", className="metric-value"),
                                html.H3("Avg. Daily Riders", className="metric-title")
                            ], className="metric-card")
                        ], className="metric-parent"),

                        html.Div([
                            dcc.Graph(id="mta-monthly-chart", figure=MTA.empty_chart(), config={"displayModeBar": False})
                        ], className="chart-div"),
                        html.Div([
                            dcc.Graph(id="current-month-chart", figure=MTA.empty_chart(), config={"displayModeBar": False})
                        ], className="chart-div")

                    ], className="mta-chart-div")
                ]
            )
        ])
    ], className="dashboard-container")

    init_callback(app)

    return app.server