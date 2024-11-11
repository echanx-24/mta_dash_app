import plotly.graph_objects as go
import plotly.subplots as sbp
from datetime import date
import pandas as pd
import numpy as np
import calendar

class MTA:

    today = date.today()
    current_month = date(today.year, today.month, calendar.monthrange(today.year, today.month)[1]).strftime("%m/%d/%Y")

    col_map = {
        "Subways": "Subways: Total Estimated Ridership",
        "Buses": "Buses: Total Estimated Ridership",
        "LIRR": "LIRR: Total Estimated Ridership",
        "Metro-North": "Metro-North: Total Estimated Ridership",
        "Access-A-Ride": "Access-A-Ride: Total Scheduled Trips",
        "Bridges and Tunnels": "Bridges and Tunnels: Total Traffic",
        "Staten Island Railway": "Staten Island Railway: Total Estimated Ridership"
    }

    def historical_data(self):
        df = pd.read_csv("flask_app/dashboard/mta/data.csv")
        df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
        df["month_end"] = df["Date"] + pd.tseries.offsets.MonthEnd(0)
        df["year"] = df["Date"].dt.year
        df["month"] = df["Date"].dt.month
        df["current_month_flag"] = np.where(df["month_end"] == self.current_month, 1, 0)
        df["date_str"] = df["Date"].dt.strftime("%b-%d-%Y")

        cols = ["Subways: Total Estimated Ridership", "Buses: Total Estimated Ridership", "LIRR: Total Estimated Ridership",
                "Metro-North: Total Estimated Ridership", "Access-A-Ride: Total Scheduled Trips", "Bridges and Tunnels: Total Traffic",
                "Staten Island Railway: Total Estimated Ridership"]
        
        df_group = df.groupby(["month_end", "current_month_flag"], as_index=False)[cols].agg(["sum", "mean"])
        df_group = df_group.rename(columns={"('month-end',     '')": "month_end"})
        df_current = df[df["current_month_flag"] == 1]
        df_historical = df[df["current_month_flag"] == 0]

        return df, df_group, df_current, df_historical
    
    def historical_monthly_chart(self, df: pd.DataFrame, key: str) -> go.Figure:
        col = self.col_map[key]
        df = df[df["current_month_flag"] == 0]
        n = df["month_end"].count()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["month_end"], y=df[(col, "sum")], name=f"<b>{col}</b>", hovertemplate="%{y:,d}", mode="lines", line=dict(width=3, color="#3459e6")))

        fig.update_xaxes(gridcolor="#D2D2D2", showline=False, rangeslider_visible=False, range=[df["month_end"][0], df["month_end"][n-1]])
        fig.update_yaxes(gridcolor="#D2D2D2", side="right", tickformat=",", zerolinewidth=1, zerolinecolor="#D2D2D2")
        fig.update_layout(hovermode="x", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", dragmode=False, showlegend=False,
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right",x=1, font=dict(size=18, color="black", family="Arial")),
                          title=dict(text=f"<b>Historical Monthly MTA Ridership by {key}</b>", font=dict(size=20, color="black", family="Arial")))
        
        return fig
    
    def current_month_chart(self, df: pd.DataFrame, key: str) -> go.Figure:
        col = self.col_map[key]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=df["date_str"], y=df[col], name=f"<b>{col}</b>", hovertemplate="%{y:,d}", marker_color="#3459e6"))
        fig.update_xaxes(gridcolor="#D2D2D2", showline=False, rangeslider_visible=False)
        fig.update_yaxes(gridcolor="#D2D2D2", side="right", tickformat=",")
        fig.update_layout(hovermode="x", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", dragmode=False,
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right",x=1, font=dict(size=18, color="black", family="Arial")),
                          title=dict(text=f"<b>Current Month MTA Ridership by {key}</b>", font=dict(size=20, color="black", family="Arial")))
        
        return fig
    
    def fetch_current(self, df: pd.DataFrame, key: str) -> int:
        return int(df[self.col_map[key]].sum())
    
    def fetch_average(self, df: pd.DataFrame, key: str) -> int:
        return int(df[self.col_map[key]].mean())
    
    @classmethod
    def empty_chart(cls):
        fig = go.Figure()
        fig.add_trace(go.Bar())
        fig.update_xaxes(showline=False, showgrid=False, visible=False)
        fig.update_yaxes(showline=False, showgrid=False, visible=False)
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", dragmode=False)
        return fig