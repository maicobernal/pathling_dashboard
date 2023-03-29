# Import libraries
import dash_bootstrap_components as dbc
from dash import html

# Make a reusable copyright notice for the footer
def Copyright():
    return [html.P(
        "2023 Dashboard FHIR Pathling",
        className="mb-0 text-center",
        style={"color": "white"}
        
    ),
    html.P(
        "Creado por Maico Bernal",
        className="mb-0 text-center",
        style={"color": "white"}
    )
    ]

# Make a reusable social media icons row for the footer
def SocialMediaIcons():
    return dbc.Row(
        [
            dbc.Col(html.A(html.I(className="bi bi-twitter p-2", style={"font-size": "20px"}), href="https://twitter.com/BernalMaico"), width="auto"),
            dbc.Col(html.A(html.I(className="bi bi-linkedin p-2", style={"font-size": "20px"}), href="https://www.linkedin.com/in/maicobernal/"), width="auto")
        ],
        className="mb-2 g-1 justify-content-center",
    )

def Citations():
    return html.Div(
        [
            html.P("Using open-source technologies:", className="mb-0", style={"color": "white"}),
            html.P([
                html.A("Synthea", href="https://synthetichealth.github.io/synthea/"), ", ",
                html.A("HL7-FHIR", href="http://hl7.org/fhir/index.html"), ", ",
                html.A("Pathling", href="https://pathling.csiro.au/"), ", ",
                html.A("Dash", href="https://dash.plotly.com/"),
                html.A("MIMIC-IV-FHIR", href="https://physionet.org/content/mimic-iv-fhir-demo/2.0/"),
            ],
            className="mb-0"),
        ],
        className="text-center",
    )

# Footer layout
def Footer():
    layout = html.Div(
        [
            dbc.Container(
                [
                    dbc.Row(SocialMediaIcons(), className="mt-4"),
                    dbc.Row(Copyright(), className="mt-2"),
                    dbc.Row(Citations(), className="mt-2"),

                ],
                className="text-center justify-content-center align-items-center",
            ),
        ],
    
        style={
            "backgroundColor": "#0F0A0A",
            "width": "100%",
            "bottom": "0",
        },
    )
    return layout
