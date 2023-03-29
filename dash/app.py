import dash
import dash_bootstrap_components as dbc
from components.navbar import Navbar
from components.footer import Footer

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

app.layout = dbc.Container(
    [
        Navbar(),
        dash.page_container,
        Footer()
    ],
    className="dbc bg-dark",
    fluid=True
)

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)