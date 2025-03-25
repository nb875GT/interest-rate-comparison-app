import streamlit as st
import pandas_datareader.data as web
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Streamlit page config
st.set_page_config(page_title="Interest Rate Chart", layout="wide")
st.title("Interactive US Interest Rate Comparison")
st.caption("Prime Rate, 30-Year Treasury, and Fed Funds Rate")

# Define date range
start_date = "2024-01-01"
end_date = "2025-03-21"

# Define FRED tickers
series = {
    "Prime Rate": "MPRIME",
    "30 Yr Treasury": "GS30",
    "Fed Funds Rate": "FEDFUNDS"
}

# Download data from FRED
data = {}
for label, ticker in series.items():
    df = web.DataReader(ticker, 'fred', start_date, end_date)
    data[label] = df.rename(columns={ticker: label})

# Combine data into one DataFrame
df_all = pd.concat(data.values(), axis=1)

# Generate tick marks
monthly_ticks = pd.date_range(start=start_date, end=end_date, freq='MS')
quarterly_ticks = pd.date_range(start=start_date, end=end_date, freq='QS')
yearly_ticks = pd.date_range(start=start_date, end=end_date, freq='AS')

# Interactive Plotly chart
fig = go.Figure()

# Add curves
for column in df_all.columns:
    fig.add_trace(go.Scatter(
        x=df_all.index,
        y=df_all[column],
        mode='lines',
        name=column
    ))

# Add quarter annotations
for date in quarterly_ticks:
    fig.add_vline(x=date, line_width=1, line_dash="dash", line_color="gray")
    fig.add_annotation(
        x=date,
        y=max(df_all.max()),
        text=f"Q{((date.month - 1) // 3) + 1}",
        showarrow=False,
        yshift=20,
        font=dict(color="white", size=12)  # Updated: brighter and larger
    )

# Add year annotations
for date in yearly_ticks:
    fig.add_vline(x=date, line_width=2, line_dash="dot", line_color="white")
    fig.add_annotation(
        x=date,
        y=max(df_all.max()),
        text=str(date.year),
        showarrow=False,
        yshift=40,
        font=dict(color="white", size=14)  # Updated
    )

# Style chart with true black background
fig.update_layout(
    title=dict(
        text="US Interest Rates: Prime, Fed Funds, and 30-Year Treasury",
        font=dict(size=20, color="white"),
        x=0.5
    ),
    xaxis_title="Date",
    yaxis_title="Yield (%)",
    template="plotly_dark",
    hovermode="x unified",
    legend_title="Rate Type",
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color="white"),  # Default font color for labels
    xaxis=dict(
        tickmode='array',
        tickvals=monthly_ticks,
        tickformat="%b\n%Y",
        tickangle=0,
        tickfont=dict(size=12, color='white'),  # Increase size
        titlefont=dict(size=14, color='white')
    ),
    yaxis=dict(
        tickfont=dict(size=12, color='white'),
        titlefont=dict(size=14, color='white')
    ),
    legend=dict(
        font=dict(size=12, color="white"),
        bgcolor="black",
        bordercolor="gray"
    )
)

# Display chart
st.plotly_chart(fig, use_container_width=True)
