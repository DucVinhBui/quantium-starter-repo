import pandas as pd
import datetime
import dash
from dash import dcc, html
import plotly.express as px

# Step 1: Load the formatted sales data
df = pd.read_csv("formatted_sales_data.csv")

# Ensure 'date' column is datetime
df["date"] = pd.to_datetime(df["date"])

# Step 2: Aggregate sales by date
daily_sales = df.groupby("date", as_index=False)["sales"].sum()

# Step 3: Initialize Dash app
app = dash.Dash(__name__)
app.title = "Pink Morsel Sales Visualiser"

# Step 4: Create the line chart
fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Daily Sales of Pink Morsels",
    labels={"date": "Date", "sales": "Sales ($)"}
)

# Step 5: Add vertical line and annotation for price increase
price_increase_date = datetime.datetime(2021, 1, 15)
max_sales = daily_sales["sales"].max()

fig.add_shape(
    type="line",
    x0=price_increase_date,
    y0=0,
    x1=price_increase_date,
    y1=max_sales,
    line=dict(color="red", dash="dash"),
)

fig.add_annotation(
    x=price_increase_date,
    y=max_sales,
    text="Price Increase",
    showarrow=False,
    yanchor="bottom",
    font=dict(color="red")
)

# Step 6: Build layout
app.layout = html.Div(children=[
    html.H1("Pink Morsel Sales Dashboard", style={'textAlign': 'center'}),
    dcc.Graph(
        id='sales-line-chart',
        figure=fig
    )
])

# Step 7: Run the app
if __name__ == '__main__':
    app.run(debug=True)
