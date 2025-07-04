import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fredapi import Fred
from datetime import datetime

# Streamlit page config
st.set_page_config(page_title="Interest Rate Chart", layout="wide")
st.title("Interactive US Interest Rate Comparison")
st.caption("Prime Rate, 30-Year Treasury, and Fed Funds Rate")

# Define date range
start_date = "2024-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')  # Automatically update to today

# Load FRED API key
fred = Fred(api_key=st.secrets["fred_api_key"])

# Define FRED series
series = {
    "Prime Rate": "MPRIME",
    "30 Yr Treasury": "GS30",
    "Fed Funds Rate": "FEDFUNDS"
}

# Pull data for each series
data = {}
for label, ticker in series.items():
    df = fred.get_series(ticker, start_date, end_date)
    df = df.to_frame(name=label)
    data[label] = df

# Combine into one DataFrame
df_all = pd.concat(data.values(), axis=1)

# Tick marks for annotations
monthly_ticks = pd.date_range(start=start_date, end=end_date, freq='MS')
quarterly_ticks = pd.date_range(start=start_date, end=end_date, freq='QS')
yearly_ticks = pd.date_range(start=start_date, end=end_date, freq='AS')

# Create Plotly chart
fig = go.Figure()

# Add each interest rate line
for column in df_all.columns:
    fig.add_trace(go.Scatter(
        x=df_all.index,
        y=df_all[column],
        mode='lines',
        name=column
    ))

# Quarter lines and annotations
for date in quarterly_ticks:
    fig.add_vline(x=date, line_width=1, line_dash="dash", line_color="gray")
    fig.add_annotation(
        x=date,
        y=max(df_all.max()),
        text=f"Q{((date.month - 1) // 3) + 1}",
        showarrow=False,
        yshift=20,
        font=dict(color="white", size=12)
    )

# Year lines and annotations
for date in yearly_ticks:
    fig.add_vline(x=date, line_width=2, line_dash="dot", line_color="white")
    fig.add_annotation(
        x=date,
        y=max(df_all.max()),
        text=str(date.year),
        showarrow=False,
        yshift=40,
        font=dict(color="white", size=14)
    )

# Final layout
fig.update_layout(
    title=dict(
        text="US Interest Rates: Prime, Fed Funds, and 30-Year Treasury",
        font=dict(size=20, color="white"),
        x=0.5
    ),
    xaxis=dict(
        title=dict(text="Date", font=dict(size=14, color='white')),
        tickmode='array',
        tickvals=monthly_ticks,
        tickformat="%b\n%Y",
        tickangle=0,
        tickfont=dict(size=12, color='white')
    ),
    yaxis=dict(
        title=dict(text="Yield (%)", font=dict(size=14, color='white')),
        tickfont=dict(size=12, color='white')
    ),
    legend=dict(
        title="Rate Type",
        font=dict(size=12, color="white"),
        bgcolor="black",
        bordercolor="gray"
    ),
    template="plotly_dark",
    hovermode="x unified",
    plot_bgcolor='black',
    paper_bgcolor='black'
)

# Show chart
st.plotly_chart(fig, use_container_width=True)
