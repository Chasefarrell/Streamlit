# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📅 Two-Year Life Plan: Gantt Chart")

# Google Sheet URLs (CSV export format)
sheet_id = "1lH4Q3z_rBq66_KrzwXOgcekn38o1QIFMvh0c9o7r0aA"
timeline_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Timeline"
markers_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Specific%20Dates"

# Load data
try:
    df = pd.read_csv(timeline_url, parse_dates=["Start", "Finish"])
    markers = pd.read_csv(markers_url, parse_dates=["Date"])
except Exception as e:
    st.error("❌ Failed to load data. Please check sheet access or column names.")
    st.stop()

# Build the Gantt chart
fig = px.timeline(
    df,
    x_start="Start",
    x_end="Finish",
    y="Task",
    color="Category",
    text="Task",
    title="Your Joint 2-Year Plan"
)

fig.update_traces(textposition="inside")
fig.update_yaxes(autorange="reversed")

# Add milestone lines from the second sheet
for _, row in markers.iterrows():
    fig.add_shape(
        type="line",
        x0=row["Date"],
        x1=row["Date"],
        y0=-0.5,
        y1=len(df) - 0.5,
        line=dict(color="red", width=2, dash="dash"),
        xref="x",
        yref="y"
    )
    fig.add_annotation(
        x=row["Date"],
        y=-0.5,
        text=row["Label"],
        showarrow=False,
        yshift=-10,
        font=dict(color="red", size=12)
    )

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("🔄 This chart updates live from [this Google Sheet](https://docs.google.com/spreadsheets/d/1lH4Q3z_rBq66_KrzwXOgcekn38o1QIFMvh0c9o7r0aA). Just update the **Timeline** or **Specific Dates** sheets.")
