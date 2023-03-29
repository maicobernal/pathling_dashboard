# Import necessary libraries 
from dash import html, get_asset_url
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
import subprocess

dash.register_page(__name__, order = 1, path = '/')

def generate_random():
        print('Generating random data...')

        # Set the path to your run_synthea.sh script
        script_path = "dash/random_generator.sh"

        # Run the script with default values
        subprocess.run(["bash", script_path])

        # If you want to provide custom values for SEED and AGE, you can pass them as arguments:
        # seed = "5678"
        # age = "30-50"
        # subprocess.run(["bash", script_path, seed, age])

@dash.callback(
        Output("output-exito", "children"),
        [Input("randomize-button", "n_clicks")],
)
def on_button_click(n_clicks):
        if n_clicks is not None:
                generate_random()
                return html.Div('Datos generados y cargados con éxito', className='alert alert-success')

def home():
        return dbc.Container([
                dbc.Row([
                        dbc.Col(
                        children=[
                
                                html.H3('Dashboard Pathling-FHIR', className="card-title text-center text-white pb-3"),
                                html.H5('Creación de data sintética en formato FHIR', className="card-title text-center text-white pb-2"),
                                html.H5('Visualización con Pathling y Dash', className="card-title text-center text-white"),
                                html.Img(src=get_asset_url('home.png'), className="p-3", style = {'width': '40%'}),
                                ],
                        width={"size": 12},
                        className = 'p-2 m-2 justify-content-center align-items-center text-center'
                )
                ],
                className = 'g-0 m-2 d-flex justify-content-center align-items-center'),
                dbc.Row([
                        dbc.Col(
                                [html.Button('Generar nuevos datos', className='btn btn-primary', id='randomize-button'),
                                html.Div(id='output-exito')],
                                width={"size": 12},
                                className = 'p-2 m-2 justify-content-center align-items-center text-center'
                                )
                ])
        ], 
        fluid=True,
        className = 'g-0')

layout = home()