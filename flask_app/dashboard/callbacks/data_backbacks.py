from dash import Output, Input, State, no_update
from flask_app.dashboard._mta import MTA
import numpy as np

def init_callback(app, mta: MTA, df, df_group, df_current):

    total = 0
    for col in df.columns:
        if df[col].dtype == np.int64 or df[col].dtype == np.float64:
            total += df[col].sum()

    @app.callback([Output("mta-monthly-chart", "figure"),
                   Output("mta-moving-avg", "figure"),
                   Output("avg-growth", "children"),
                   Output("growth", "children"),
                   Output("percent-pre-pandemic", "figure")],
                   Input("mta-btn", "n_clicks"),
                   State("mta-dropwdown", "value"))
    def update_chart(n_clicks, value):
        if value is None:
            return no_update

        fig_monthly, avg_growth, growth = mta.historical_monthly_chart(df_group, value)
        fig_sma = mta.moving_average(df, value)
        fig_current = mta.pre_pandemic_percent(df, value)

        return fig_monthly, fig_sma, avg_growth, growth, fig_current
    
    @app.callback([Output("current-month", "children"),
                   Output("avg-daily-riders", "children"),
                   Output("avg-monthly-riders", "children"),
                   Output("percent-total", "children")],
                   Input("mta-btn", "n_clicks"),
                   State("mta-dropwdown", "value"))
    def update_metric(n_clicks, value):
        if value is None:
            return no_update, no_update
        current_total = mta.fetch(df_current, value, "sum")
        avg_daily = mta.fetch(df_current, value, "mean")
        z = mta.fetch_average_month(df_group, value)
        percent_total = f"{mta.fetch(df, value, "sum") / total:.2%}"

        return f"{current_total:,d}", f"{avg_daily:,d}", f"{z:,d}", percent_total