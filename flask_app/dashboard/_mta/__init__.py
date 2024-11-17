from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go
from datetime import date
import pandas as pd
import numpy as np
import calendar

class MTA:

    today = date.today()
    current_month = date(today.year, today.month, calendar.monthrange(today.year, today.month)[1]).strftime("%m/%d/%Y")

    col_map = {
        "Subways": ("Subways: Total Estimated Ridership", "Subways: % of Comparable Pre-Pandemic Day"),
        "Buses": ("Buses: Total Estimated Ridership", "Subways: % of Comparable Pre-Pandemic Day"),
        "LIRR": ("LIRR: Total Estimated Ridership", "LIRR: % of Comparable Pre-Pandemic Day"),
        "Metro-North": ("Metro-North: Total Estimated Ridership", "Metro-North: % of Comparable Pre-Pandemic Day"),
        "Access-A-Ride": ("Access-A-Ride: Total Scheduled Trips", "Access-A-Ride: % of Comparable Pre-Pandemic Day"),
        "Bridges and Tunnels": ("Bridges and Tunnels: Total Traffic", "Bridges and Tunnels: % of Comparable Pre-Pandemic Day"),
        "Staten Island Railway": ("Staten Island Railway: Total Estimated Ridership", "Staten Island Railway: % of Comparable Pre-Pandemic Day")
    }

    def historical_data(self):
        df = pd.read_csv("flask_app/dashboard/_mta/data.csv")
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
        
        df_group = df[df["current_month_flag"] == 0].groupby("month_end", as_index=False)[cols].agg(["sum", "mean"])
        df_group = df_group.rename(columns={"('month-end',     '')": "month_end"})
        df_current = df[df["current_month_flag"] == 1]

        return df, df_group, df_current
    
    def historical_monthly_chart(self, df: pd.DataFrame, key: str) -> go.Figure:
        col = self.col_map[key][0]
        n = df["month_end"].count()
        avg_growth = f"{sum(df[(col, "sum")].pct_change().fillna(0)) / (n-1):.2%}"
        growth_since_pan = f"{(df[(col, "sum")][n-1]/df[(col, "sum")][0]) - 1:.2%}"

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
        
        return fig, avg_growth, growth_since_pan
    
    def moving_average(self, df: pd.DataFrame, key: str) -> go.Figure:
        col = self.col_map[key][0]
        df["SMA"] = df[col].rolling(window=30, min_periods=1).mean()
        df = df[df["EOM"] == True].reset_index()
        n = df["month_end"].count()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Date"], y=df["SMA"], name=f"<b>SMA</b>", hovertemplate="<b>%{y:,d}</b>", mode="lines", line=dict(color="#a30000", width=2.5)))
        fig.add_hline(y=df["SMA"][0], line_dash="dash", line_width=2.5, line_color="black")

        fig.update_xaxes(gridcolor="#D2D2D2", showline=False, rangeslider_visible=False, range=[df["month_end"][0], df["month_end"][n-1]], 
                         tickfont=dict(size=16, color="black", family="Arial"), tickformat="%b<br>'%y")
        fig.update_yaxes(gridcolor="#D2D2D2", side="right", tickformat=",", zerolinewidth=1, zerolinecolor="#D2D2D2", tickfont=dict(size=16, color="black", family="Arial"))
        fig.update_layout(hovermode="x", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", dragmode=False, showlegend=False, margin=dict(b=50),
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right",x=1, font=dict(size=18, color="black", family="Arial")),
                          title=dict(text=f"<b>{key} 30 Day Trending Daily Riders</b>", font=dict(size=20, color="black", family="Arial")),
                          hoverlabel=dict(font=dict(size=16, family="Arial")))
        
        return fig
    
    def pre_pandemic_percent(self, df: pd.DataFrame, key: str) -> go.Figure:
        col = self.col_map[key][1]
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
        col = self.col_map[key][0]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=df["date_str"], y=df[col], name=f"<b>{col}</b>", hovertemplate="%{y:,d}", marker_color="#3459e6"))
        fig.update_xaxes(gridcolor="#D2D2D2", showline=False, rangeslider_visible=False, tickfont=dict(size=16, color="black", family="Arial"))
        fig.update_yaxes(gridcolor="#D2D2D2", side="right", tickformat=",", tickfont=dict(size=16, color="black", family="Arial"))
        fig.update_layout(hovermode="x", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", dragmode=False, hoverlabel=dict(font=dict(size=16, family="Arial")),
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right",x=1, font=dict(size=18, color="black", family="Arial")),
                          title=dict(text=f"<b>Current Month {key} Riders</b>", font=dict(size=20, color="black", family="Arial")))
        
        return fig
    
    def summary_chart_totals(self, df: pd.DataFrame) -> go.Figure:
        cols, colors = list(df.columns[1::2]), ("#264653", "#287271", "#2A9D8F", "#8AB17D", "#E9C46A", "#F4A261", "#E76F51")
        base = df[cols[0]]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=df["month_end"], y=df[cols[0]], marker_color=colors[0], name=f"<b>{cols[0][0].split(":")[0]}</b>", hovertemplate="%{y:,d}", offsetgroup=1))
        for col, color in zip(cols[1:], colors[1:]):
            fig.add_trace(go.Bar(x=df["month_end"], y=df[col], customdata=df[col], marker_color=color, name=f"<b>{col[0].split(":")[0]}</b>", hovertemplate="%{customdata:,d}", 
                                 offsetgroup=1, base=base))
            base += df[col]

        fig.update_xaxes(gridcolor="#D2D2D2", showline=False, tickfont=dict(size=16, color="black", family="Arial"))
        fig.update_yaxes(gridcolor="#D2D2D2", side="right", tickformat=".3s", zerolinewidth=1, zerolinecolor="#D2D2D2", tickfont=dict(size=16, color="black", family="Arial"))
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right",x=1, font=dict(size=16, color="black", family="Arial")),
                          title=dict(text=f"<b>Monthly Totals Summary</b>", font=dict(size=20, color="black", family="Arial")), hovermode="x unified", 
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", dragmode=False, margin=dict(l=50, b=50))
        
        return fig
    
    def summary_chart_avg(self, df: pd.DataFrame) -> go.Figure:

        fig = go.Figure()
        cols, colors = list(df.columns[1::2]), ("#264653", "#287271", "#2A9D8F", "#8AB17D", "#E9C46A", "#F4A261", "#E76F51")
        for col, color in zip(cols, colors):
            col_name = f"{col.split(":")[0]} MoM %"
            df[col_name] = df[col].rolling(window=90, min_periods=1).mean()
            fig.add_trace(go.Scatter(x=df["Date"], y=df[col_name], name=f"<b>{col.split(":")[0]}</b>", line=dict(color=color, width=2.5), hovertemplate="%{y:.2s}"))

        fig.update_xaxes(gridcolor="#D2D2D2", showline=False, tickfont=dict(size=16, color="black", family="Arial"), rangeslider_visible=True)
        fig.update_yaxes(gridcolor="#D2D2D2", side="right", tickformat=".2s", zerolinewidth=1, zerolinecolor="#D2D2D2", tickfont=dict(size=16, color="black", family="Arial"))
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right",x=1, font=dict(size=16, color="black", family="Arial")),
                          title=dict(text=f"<b>T90 Trending Daily Avg. Riders</b>", font=dict(size=20, color="black", family="Arial")), hovermode="x unified", 
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", dragmode=False, margin=dict(l=50, b=50))
        
        return fig
    
    def fetch(self, df: pd.DataFrame, key: str, agg="sum") -> int:
        n = df["month_end"].count()
        if agg == "sum":
            return int(df[df["month_end"] >= str(self.today - relativedelta(months=6))][self.col_map[key][0]].sum())
        elif agg == "mean":
            return int(df[df["month_end"] >= str(self.today - relativedelta(months=6))][self.col_map[key][0]].mean())
        else:
            return 0
    
    def fetch_average_month(self, df: pd.DataFrame, key: str) -> int:
        n = df["month_end"].count()
        return int(df[df["month_end"] >= str(self.today - relativedelta(months=6))][(self.col_map[key][0], "sum")].mean())
    
    @classmethod
    def empty_chart(cls):
        fig = go.Figure()
        fig.add_trace(go.Bar())
        fig.update_xaxes(showline=False, showgrid=False, visible=False)
        fig.update_yaxes(showline=False, showgrid=False, visible=False)
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", dragmode=False)
        return fig