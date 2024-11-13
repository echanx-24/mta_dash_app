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

    col_map_percent = {
        "Subways": "Subways: % of Comparable Pre-Pandemic Day",
        "Buses": "Subways: % of Comparable Pre-Pandemic Day",
        "LIRR": "LIRR: % of Comparable Pre-Pandemic Day",
        "Metro-North": "Metro-North: % of Comparable Pre-Pandemic Day",
        "Access-A-Ride": "Access-A-Ride: % of Comparable Pre-Pandemic Day",
        "Bridges and Tunnels": "Bridges and Tunnels: % of Comparable Pre-Pandemic Day",
        "Staten Island Railway": "SStaten Island Railway: % of Comparable Pre-Pandemic Day"
    }

    def historical_data(self):
        df = pd.read_csv("flask_app/dashboard/mta/data.csv")
        df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
        df = df.sort_values(by="Date")
        df["month_end"] = df["Date"] + pd.tseries.offsets.MonthEnd(0)
        df["year"] = df["Date"].dt.year
        df["month"] = df["Date"].dt.month
        df["current_month_flag"] = np.where(df["month_end"] == self.current_month, 1, 0)
        df["date_str"] = df["Date"].dt.strftime("%b-%d-%Y")
        df["EOM"] = df["Date"].dt.is_month_end

        cols = ["Subways: Total Estimated Ridership", "Buses: Total Estimated Ridership", "LIRR: Total Estimated Ridership",
                "Metro-North: Total Estimated Ridership", "Access-A-Ride: Total Scheduled Trips", "Bridges and Tunnels: Total Traffic",
                "Staten Island Railway: Total Estimated Ridership"]
        
        df_group = df.groupby(["month_end", "current_month_flag"], as_index=False)[cols].agg(["sum", "mean"])
        df_group = df_group.rename(columns={"('month-end',     '')": "month_end"})
        df_current = df[df["current_month_flag"] == 1]

        return df, df_group, df_current
    
    def historical_monthly_chart(self, df: pd.DataFrame, key: str) -> go.Figure:
        col = self.col_map[key]
        df = df[df["current_month_flag"] == 0]
        n = df["month_end"].count()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["month_end"], y=df[(col, "sum")], name=f"<b>{col}</b>", hovertemplate="<b>%{y:,d}</b>", mode="lines", line=dict(width=3, color="#609967"), 
                                 showlegend=False))
        fig.add_hline(y=int(df[(col, "sum")][0]), line_dash="dash", line_width=2.5, line_color="black")

        fig.update_xaxes(gridcolor="#D2D2D2", showline=False, rangeslider_visible=False, range=[df["month_end"][0], df["month_end"][n-1]], 
                        tickfont=dict(size=16, color="black", family="Arial"), tickformat="%b<br>'%y")
        fig.update_yaxes(gridcolor="#D2D2D2", side="right", tickformat=",", zerolinewidth=1, zerolinecolor="#D2D2D2", tickfont=dict(size=16, color="black", family="Arial"))
        fig.update_layout(hovermode="x", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", dragmode=False, margin=dict(b=50),
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right",x=1, font=dict(size=18, color="black", family="Arial")),
                          title=dict(text=f"<b>Total Monthly {key} Riders</b>", font=dict(size=20, color="black", family="Arial")),
                          hoverlabel=dict(font=dict(size=16, family="Arial", color="white")))
        
        return fig
    
    def moving_average(self, df: pd.DataFrame, key: str) -> go.Figure:
        col = self.col_map[key]
        df = df[df["current_month_flag"] == 0]
        df["SMA"] = df[col].rolling(window=30, min_periods=1).mean()
        df = df[df["EOM"] == True].reset_index()
        n = df["month_end"].count()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Date"], y=df["SMA"], name=f"<b>SMA</b>", hovertemplate="<b>%{y:,d}</b>", mode="lines", line=dict(color="#a30000", width=2.5)))

        fig.update_xaxes(gridcolor="#D2D2D2", showline=False, rangeslider_visible=False, range=[df["month_end"][0], df["month_end"][n-1]], 
                         tickfont=dict(size=16, color="black", family="Arial"), tickformat="%b<br>'%y")
        fig.update_yaxes(gridcolor="#D2D2D2", side="right", tickformat=",", zerolinewidth=1, zerolinecolor="#D2D2D2", tickfont=dict(size=16, color="black", family="Arial"))
        fig.update_layout(hovermode="x", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", dragmode=False, showlegend=False, margin=dict(b=50),
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right",x=1, font=dict(size=18, color="black", family="Arial")),
                          title=dict(text=f"<b>{key} 30 Day Trending Daily Riders</b>", font=dict(size=20, color="black", family="Arial")),
                          hoverlabel=dict(font=dict(size=16, family="Arial")))
        
        return fig
    
    def pre_pandemic_percent(self, df: pd.DataFrame, key: str) -> go.Figure:
        col = self.col_map_percent[key]
        df[col] = df[col] / 100
        n = df["Date"].count()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Date"], y=df[col], name=f"<b>{col}</b>", hovertemplate="<b>%{y:.0%}</b>", mode="lines", line=dict(color="#432d8a", width=2.5)))

        fig.update_xaxes(gridcolor="#D2D2D2", showline=False, rangeslider=dict(visible=True, bgcolor="#432d8a", thickness=0.085), range=[df["Date"][0], df["Date"][n-1]], 
                         tickfont=dict(size=16, color="black", family="Arial"), tickformat="%b<br>'%y")
        fig.update_yaxes(gridcolor="#D2D2D2", side="right", tickformat=".0%", zerolinewidth=1, zerolinecolor="#D2D2D2", tickfont=dict(size=16, color="black", family="Arial"))
        fig.update_layout(hovermode="x", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", dragmode=False, showlegend=False, margin=dict(b=25),
                          title=dict(text=f"<b>{key} Pre-Pandemic Percent</b>", font=dict(size=20, color="black", family="Arial")), hoverlabel=dict(font=dict(size=16, family="Arial")))
        return fig
    
    def current_month_chart(self, df: pd.DataFrame, key: str) -> go.Figure:
        col = self.col_map[key]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=df["date_str"], y=df[col], name=f"<b>{col}</b>", hovertemplate="%{y:,d}", marker_color="#3459e6"))
        fig.update_xaxes(gridcolor="#D2D2D2", showline=False, rangeslider_visible=False, tickfont=dict(size=16, color="black", family="Arial"))
        fig.update_yaxes(gridcolor="#D2D2D2", side="right", tickformat=",", tickfont=dict(size=16, color="black", family="Arial"))
        fig.update_layout(hovermode="x", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", dragmode=False, hoverlabel=dict(font=dict(size=16, family="Arial")),
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right",x=1, font=dict(size=18, color="black", family="Arial")),
                          title=dict(text=f"<b>Current Month {key} Riders</b>", font=dict(size=20, color="black", family="Arial")))
        
        return fig
    
    def fetch_current(self, df: pd.DataFrame, key: str) -> int:
        return int(df[self.col_map[key]].sum())
    
    def fetch_average(self, df: pd.DataFrame, key: str) -> int:
        return int(df[self.col_map[key]].mean())
    
    def fetch_average_month(self, df: pd.DataFrame, key: str) -> int:
        return int(df[(self.col_map[key], "sum")].mean())
    
    def fetch_total(self, df: pd.DataFrame, key: str) -> str:
        return df[self.col_map[key]].sum()
    
    @classmethod
    def empty_chart(cls):
        fig = go.Figure()
        fig.add_trace(go.Bar())
        fig.update_xaxes(showline=False, showgrid=False, visible=False)
        fig.update_yaxes(showline=False, showgrid=False, visible=False)
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", dragmode=False)
        return fig