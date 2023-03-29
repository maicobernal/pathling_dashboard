# Import libraries
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, get_asset_url

# Make a reuseable navitem for the different examples
def NavItem():
    return dbc.NavItem(dbc.NavLink("Home", href="/"))

# Make a reuseable dropdown for the different examples
def Dropdown():
    return dbc.DropdownMenu(
        children=[
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        #in_navbar=True,
        label="Menu",
    )

# Make a reuseable dropdown for the different examples
def Buttons ():
    return dbc.Row(
                [   
                dbc.Col(
                        dbc.Nav(
                            [NavItem(), Dropdown()],
                            className="ms-auto",
                            navbar=True,
                                )
                ),
                dbc.Col(
                    dbc.Input(type="search", placeholder="Búsqueda", style = {'width': '150px'})
                ),
                dbc.Col(
                    dbc.Button(
                        "Buscar", color="primary", className="ms-2"
                    ),
                    # set width of button column to auto to allow
                    # search box to take up remaining space.
                    width="auto",
                    className="ml-4",
                ),
                ],
                className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
                align="center",
            )

def Logo():
    return html.A(
        # Use row and col to control vertical alignment of logo / brand
        dbc.Row(
            [
                dbc.Col(html.Img(src=get_asset_url('logo.png'), height="30px")),
                dbc.Col(dbc.NavbarBrand("Dashboard FHIR Pathling", className="ms-2 font-weight-bold")),
            ],
            align="center",
            className="g-0",
        ),
        href="",
        style={"textDecoration": "none"},
        )

# This example that adds a logo to the navbar brand
def NavBarItem():
    return dbc.Navbar(
    dbc.Container(
                [
                Logo(),

                dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),

                dbc.Collapse(
                    Buttons(),
                    id="navbar-collapse2",
                    navbar=True,
                    ),
                ],
                ),
    color="#0F0A0A",
    dark=True,
    className="m-0"
)


def Navbar():
    layout = html.Div(
        [
        NavBarItem()
        ],
            style={"backgroundColor": "#595959"}
        )
    return layout