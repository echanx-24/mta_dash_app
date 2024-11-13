from flask_app.dashboard.mta._mta import MTA
from dash import Output, Input, no_update
import numpy as np

def init_callback(app):

    mta = MTA()
    df, df_group, df_current = mta.historical_data()

    total = 0
    for col in df.columns:
        if df[col].dtype == np.int64 or df[col].dtype == np.float64:
            total += df[col].sum()

    @app.callback([Output("mta-monthly-chart", "figure"),
                   Output("mta-moving-avg", "figure"),
                   Output("percent-pre-pandemic", "figure")],
                   Input("mta-dropwdown", "value"))
    def update_chart(value):
        if value is None:
            return no_update
        fig_monthly = mta.historical_monthly_chart(df_group.copy(), value)
        fig_sma = mta.moving_average(df.copy(), value)
        fig_current = mta.pre_pandemic_percent(df.copy(), value)

        return fig_monthly, fig_sma, fig_current
    
    @app.callback([Output("current-month", "children"),
                   Output("avg-daily-riders", "children"),
                   Output("avg-monthly-riders", "children"),
                   Output("percent-total", "children")],
                   Input("mta-dropwdown", "value"))
    def update_metric(value):
        if value is None:
            return no_update, no_update
        x = mta.fetch_current(df_current, value)
        y = mta.fetch_average(df_current, value)
        z = mta.fetch_average_month(df_group, value)
        percent = f"{mta.fetch_total(df, value) / total:.2%}"

        return f"{x:,d}", f"{y:,d}", f"{z:,d}",percent