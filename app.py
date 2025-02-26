import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd

# Initialize Dash App
app = dash.Dash(__name__)

# App Layout
app.layout = html.Div([
    html.H1("Crypto Liveliness Dashboard", style={"textAlign": "center"}),

    # Dropdown to Select Crypto
    dcc.Dropdown(
        id="crypto-dropdown",
        options=[{"label": row["name"], "value": row["name"]} for _, row in crypto_df.iterrows()],
        value=crypto_df["name"].iloc[0],  # Default value
        multi=False,
        style={"width": "50%", "margin": "auto"}
    ),

    # Line Chart for Price Trend
    dcc.Graph(id="crypto-price-chart"),

    # Bar Chart for Liveliness Scores
    dcc.Graph(
        id="crypto-liveliness-chart",
        figure=px.bar(
            crypto_df,
            x="name",
            y="liveliness_score",
            title="Liveliness Score of Top 15 Cryptos",
            labels={"name": "Crypto", "liveliness_score": "Liveliness Score"},
            text_auto=True
        )
    ),

    # Table for Crypto Rankings
    dash_table.DataTable(
        id="crypto-table",
        columns=[{"name": col, "id": col} for col in ["name", "symbol", "price", "market_cap", "volume", "liveliness_score"]],
        data=crypto_df.to_dict("records"),
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "center", "padding": "10px"},
        style_header={"backgroundColor": "black", "color": "white", "fontWeight": "bold"}
    )
])

# Callback to Update Line Chart Based on Selected Crypto
@app.callback(
    Output("crypto-price-chart", "figure"),
    Input("crypto-dropdown", "value")
)
def update_chart(selected_crypto):
    df = crypto_df[crypto_df["name"] == selected_crypto]
    
    # Ensure sparkline data exists
    if len(df) == 0 or not isinstance(df["sparkline"].values[0], list):
        return px.line(title=f"Price Trend for {selected_crypto} (No Data)")

    fig = px.line(
        x=list(range(len(df["sparkline"].values[0]))),
        y=df["sparkline"].values[0],
        title=f"7-Day Price Trend for {selected_crypto}",
        labels={"x": "Time", "y": "Price (USD)"}
    )
    
    return fig

# Run Dash App
if __name__ == "__main__":
    app.run_server(debug=True)
