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
                html.H3("MTA Transit Dashboard", className="titles")
            ], className="title-container"), 
            dark=True, color="primary", className="navigation"
        ),
        dbc.Tabs([
            dbc.Tab(
                label="Monthly", tab_class_name="tab-custom",
                children=[
                    html.Div([

                        dcc.Dropdown(options=["Subways", "Buses", "LIRR", "Metro-North", "Access-A-Ride","Bridges and Tunnels", "Staten Island Railway"], 
                                     value="Subways", multi=False, id="mta-dropwdown"),

                        html.Div([
                            html.Div([
                                html.Div(children="-", id="current-month", className="metric-value"),
                                html.H3(children="Current Month Riders", className="metric-title")
                            ], className="metric-card first-card"),
                            html.Div([
                                html.Div(children="-", id="avg-daily-riders", className="metric-value"),
                                html.H3("Avg. Daily Riders", className="metric-title")
                            ], className="metric-card"),
                            html.Div([
                                html.Div(children="-", id="avg-monthly-riders", className="metric-value"),
                                html.H3("Avg. Monthly Riders", className="metric-title")
                            ], className="metric-card"),
                            html.Div([
                                html.Div(children="-", id="percent-total", className="metric-value"),
                                html.H3("% of Total", className="metric-title")
                            ], className="metric-card")
                        ], className="metric-parent"),

                        html.Div([
                            html.Div([
                                dcc.Graph(id="mta-monthly-chart", figure=MTA.empty_chart(), className="chart", config={"displayModeBar": False})
                            ], className="chart-child first-card"),
                            html.Div([
                                dcc.Graph(id="mta-moving-avg", figure=MTA.empty_chart(), className="chart", config={"displayModeBar": False})
                            ], className="chart-child")
                        ], className="chart-combined"),
                        html.Div([
                            dcc.Graph(id="percent-pre-pandemic", figure=MTA.empty_chart(), className="chart", config={"displayModeBar": False})
                        ], className="chart-div")

                    ], className="mta-chart-div")
                ]
            )
        ])
    ], className="dashboard-container")

    init_callback(app)

    return app.server