# Import necessary libraries 
from dash import html
import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__)

def error():
        return dbc.Container([
                dbc.Row([
                        dbc.Col(
                        children=[
                
                                html.H3('Dashboard Pathling-FHIR', className="card-title text-center text-white pb-3"),
                                html.H5('Creación de data sintética en formato FHIR', className="card-title text-center text-white pb-2"),
                                html.H5('Visualización con Pathling y Dash', className="card-title text-center text-white pb-4"),
                                html.H1('ERROR 404', className="card-title text-center text-white pb-3"),
                                html.H3('Página no encontrada', className="card-title text-center text-white pb-3"),
                                ],
                        width={"size": 12},
                        className = 'p-2 m-2 justify-content-center align-items-center text-center'
                        )
                        ],
                        className = 'g-0 m-2 d-flex justify-content-center align-items-center')
                ], 
                fluid=True,
                className = 'g-0')

layout = error()