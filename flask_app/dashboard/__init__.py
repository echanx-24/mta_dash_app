from flask_app.dashboard.callbacks.data_backbacks import init_callback
from flask_app.dashboard.components.SummaryTab import summary_tab
from flask_app.dashboard.components.MonthlyTab import monthly_tab
from flask_app.dashboard._mta import MTA
import dash_bootstrap_components as dbc
from dash import Dash, html

def create_dash(server):

    mta = MTA()
    df, df_group, df_current = mta.historical_data()
    summary_total = mta.summary_chart_totals(df_group.copy())
    summary_avg = mta.summary_chart_avg(df.copy())

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
            dbc.Tab(label="Summary", tab_class_name="tab-custom", children=[summary_tab(summary_total, summary_avg)]),
            dbc.Tab(label="Monthly", tab_class_name="tab-custom", children=[monthly_tab()])
        ])
    ], className="dashboard-container")

    init_callback(app, mta, df, df_group, df_current)

    return app.server