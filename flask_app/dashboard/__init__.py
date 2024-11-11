from dash import Dash, dcc, html,Input, Output, State, no_update
import dash_bootstrap_components as dbc
from flask_app.dashboard.data._mta import MTA

def create_dash(server):

    mta = MTA()

    app = Dash(
        server=server,
        routes_pathname_prefix="/dashboard/",
        suppress_callback_exceptions=False,
        external_stylesheets=[dbc.themes.MINTY, "assets/stylesheet.css"]
    )

    app.layout = \
    html.Div([
        dbc.NavbarSimple(brand="Welcome", dark=True, color="primary"),
        dbc.Tabs([
            dbc.Tab(label="Monthly",
                    children=[
                        dbc.Card(
                            dbc.CardBody([
                                html.Div([
                                    dcc.Dropdown(options=["Subways", "Buses", "LIRR", "Metro-North", "Access-A-Ride","Bridges and Tunnels", "Staten Island Railway"], 
                                                 value="Subways", multi=False, id="mta-dropwdown"),
                                    dcc.Graph(id="mta-monthly-chart", figure=MTA.empty_chart()),
                                    dcc.Graph(id="current-month-chart", figure=MTA.empty_chart())
                                ], className="mta-chart-div")
                            ])
                        )
                    ])
        ])
    ])

    @app.callback([Output("mta-monthly-chart", "figure"),
                   Output("current-month-chart", "figure")],
                   Input("mta-dropwdown", "value"))
    def update_chart(value):
        if value is None:
            return no_update
        df, df_month = mta.historical_data()
        fig_monthly = mta.historical_monthly_chart(df_month.copy(), value)
        fig_current = mta.current_month_chart(df.copy(), value)

        return fig_monthly, fig_current

    return app.server