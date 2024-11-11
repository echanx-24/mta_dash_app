from flask_app.dashboard.mta._mta import MTA
from dash import Output, Input, no_update

def init_callback(app):

    mta = MTA()
    df, df_group, df_current, df_historical = mta.historical_data()

    @app.callback([Output("mta-monthly-chart", "figure"),
                   Output("current-month-chart", "figure")],
                   Input("mta-dropwdown", "value"))
    def update_chart(value):
        if value is None:
            return no_update
        fig_monthly = mta.historical_monthly_chart(df_group, value)
        fig_current = mta.current_month_chart(df_current, value)

        return fig_monthly, fig_current
    
    @app.callback([Output("current-month", "children"),
                   Output("avg-riders", "children")],
                   Input("mta-dropwdown", "value"))
    def update_metric(value):
        if value is None:
            return no_update, no_update
        x = mta.fetch_current(df_current, value)
        y = mta.fetch_average(df_current, value)

        return f"{x:,d}", f"{y:,d}"