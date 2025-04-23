import pandas as pd
import datetime
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# === Load and prepare the data ===
df = pd.read_csv("formatted_sales_data.csv")
df["date"] = pd.to_datetime(df["date"])
regions = ["all"] + sorted(df["region"].unique())

# === Initialize Dash app ===
app = dash.Dash(__name__)
app.title = "Pink Morsel Sales Visualiser"

# === App layout with custom styling ===
app.layout = html.Div(
    style={
        "background": "linear-gradient(to right, #f8f9fa, #ffffff)",
        "minHeight": "100vh",
        "padding": "40px",
        "fontFamily": "'Segoe UI', sans-serif",
        "color": "#333"
    },
    children=[
        html.Div([
            html.H1(
                "🌸 Pink Morsel Sales Dashboard",
                style={
                    "textAlign": "center",
                    "color": "#d6336c",
                    "marginBottom": "10px",
                    "fontSize": "42px"
                }
            ),
            html.P(
                "Track how Pink Morsel sales changed before and after the Jan 15, 2021 price increase.",
                style={
                    "textAlign": "center",
                    "fontSize": "18px",
                    "color": "#6c757d",
                    "marginBottom": "40px"
                }
            )
        ]),

        html.Div(
            children=[
                html.Label("🔍 Filter by Region:", style={
                    "fontWeight": "bold",
                    "fontSize": "18px",
                    "marginRight": "20px",
                    "color": "#343a40"
                }),
                dcc.RadioItems(
                    id="region-radio",
                    options=[{"label": r.title(), "value": r} for r in regions],
                    value="all",
                    labelStyle={
                        "display": "inline-block",
                        "marginRight": "20px",
                        "fontSize": "16px",
                        "color": "#495057"
                    },
                    inputStyle={"marginRight": "8px"}
                )
            ],
            style={
                "textAlign": "center",
                "marginBottom": "30px",
                "padding": "10px",
                "backgroundColor": "#f1f3f5",
                "borderRadius": "10px",
                "boxShadow": "0 0 10px rgba(0,0,0,0.05)",
                "maxWidth": "700px",
                "margin": "0 auto"
            }
        ),

        html.Div([
            dcc.Graph(id="sales-line-chart", style={"height": "600px"})
        ],
        style={
            "boxShadow": "0 4px 15px rgba(0,0,0,0.1)",
            "borderRadius": "15px",
            "padding": "20px",
            "backgroundColor": "#ffffff"
        })
    ]
)

# === Callback for interactivity ===
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-radio", "value")
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered_df = df.copy()
    else:
        filtered_df = df[df["region"] == selected_region]

    daily_sales = filtered_df.groupby("date", as_index=False)["sales"].sum()

    fig = px.line(
        daily_sales,
        x="date",
        y="sales",
        title=f"Pink Morsel Sales in {selected_region.title() if selected_region != 'all' else 'All Regions'}",
        labels={"date": "Date", "sales": "Sales ($)"}
    )

    price_increase_date = datetime.datetime(2021, 1, 15)
    max_sales = daily_sales["sales"].max() if not daily_sales.empty else 0

    fig.add_shape(
        type="line",
        x0=price_increase_date,
        y0=0,
        x1=price_increase_date,
        y1=max_sales,
        line=dict(color="#e64980", dash="dash"),
    )

    fig.add_annotation(
        x=price_increase_date,
        y=max_sales,
        text="💰 Price Increase",
        showarrow=False,
        yanchor="bottom",
        font=dict(color="#e64980")
    )

    fig.update_layout(
        plot_bgcolor="#fff",
        paper_bgcolor="#fff",
        font=dict(color="#212529"),
        title_font=dict(size=24, color="#d6336c"),
        margin=dict(l=40, r=40, t=80, b=40),
        hovermode="x unified"
    )

    return fig

# === Run the app ===
if __name__ == "__main__":
    app.run(debug=True)
