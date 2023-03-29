# Import necessary libraries 
from dash import html
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import requests
import time

dash.register_page(__name__, order = 3)

def description_card_descarga():
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H5("Dashboard FHIR - Pathlings Analytics", className="card-title"),
                    html.P(
                        "Este dashboard es a modo de prueba para visualizar y descargar datos sintéticos en formato FHIR. Seleccione más abajo las variables que desea descargar.",
                        className="card-text",
                    ),
                ],
            className = 'p-4')
        ],
        className = ''
    )


features = {
    'Patient': [
        ('gender', 'Género'),
        ('birthDate', 'Fecha de nacimiento'),
        ('maritalStatus.coding.display', 'Estado civil')
    ],
    'Observation': [
        ('code.coding.display', 'Código de observación'),
        ('valueQuantity.unit', 'Unidad de cantidad'),
        ('status', 'Estado')
    ],
    'Encounter': [
        ('class.code', 'Clase de encuentro'),
        ('type.coding.display', 'Tipo de encuentro'),
        ('status', 'Estado')
    ],
    'Procedure': [
        ('code.coding.display', 'Código de procedimiento'),
        ('status', 'Estado'),
        ('category.coding.display', 'Categoría de procedimiento')
    ],
    'MedicationRequest': [
        ('medicationCodeableConcept.coding.display', 'Código de medicación'),
        ('status', 'Estado'),
        ('intent', 'Intención')
    ],
    'Immunization': [
        ('vaccineCode.coding.display', 'Código de vacuna'),
        ('status', 'Estado'),
        ('doseQuantity.unit', 'Unidad de dosis')
    ],
    'AllergyIntolerance': [
        ('code.coding.display', 'Código de alergia/intolerancia'),
        ('clinicalStatus.coding.display', 'Estado clínico'),
        ('verificationStatus.coding.display', 'Estado de verificación')
    ]
}


def generate_control_card_descarga():
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Seleccione recurso", className="card-title"),
                    dcc.Dropdown(
                        id='resource-dropdown',
                        options=[{'label': key, 'value': key} for key in features.keys()],
                        value=list(features.keys())[0]
                    ),
                    dcc.Dropdown(
                        id='element-dropdown',
                        value=features[list(features.keys())[0]][0][0],
                        multi=True,
                        className = ''
                    ),

                    html.Div([
                        html.Button('Visualizar', id='toggle-button', className='btn btn-primary'),
                        ], 
                        className = 'p-2 d-flex justify-content-center align-items-center'),
                    dcc.Store(id='global-variable', data=False),
                ]
                
            )
        ],
        className = 'mt-3'
    )

@dash.callback(
    Output('element-dropdown', 'options'),
    Input('resource-dropdown', 'value')
)
def update_element_dropdown(selected_resource):
    options = features.get(selected_resource, [])
    return [{'label': option[1], 'value': option[0]} for option in options]


def get_extract(server, resource_type, columns, limit):      
    url = f'{server}/{resource_type}/$extract?'

    for column in columns:
        url = f'{url}column={column}&'
    
    url = f'{url}limit={limit}'
    resp = requests.get(url, headers={"Content-Type": "application/fhir+json"} )
    return resp.json()


@dash.callback(
        Output("tabla", "children")
    ,
    [
        Input("resource-dropdown", "value"),
        Input("element-dropdown", "value"),
        Input("toggle-button", "n_clicks"),
    ],
)

def get_data(resource_type, columns, n_clicks):

    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    
    server = 'http://pathling:8080/fhir'
    limit = 50
    resp = get_extract(server, resource_type, columns, limit)
    time.sleep(5)
    print(resp)
    url_to_download = resp['parameter'][0]['valueUrl']
    df = pd.read_csv(url_to_download)
    return [
            dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            page_size=10),
            html.Div(
            html.A(
                html.Button('Descargar', className='btn btn-primary'),
                id='download-link',
                download="data.csv",
                href=url_to_download.replace('pathling', 'localhost'),
                target="_blank"
                ),
                className='p-2 d-flex justify-content-center align-items-center'
                )
            ]
    

def download():
    return dbc.Container([
        dbc.Row([
            dbc.Col(
                children=[description_card_descarga(), generate_control_card_descarga()],
                width={"size": 3}
            ),
            dbc.Col(
                children=[
                    html.H4('Tabla a descargar', className="card-title text-center text-white"),
                    html.Div(id='tabla', className = 'm-4'),
                ],
                width={"size": 9},
                className='p-2'
            )
        ],
            className='g-0 m-2 d-flex justify-content-center align-items-center'),
        dbc.Row([
            dbc.Col(
                children=[
                    html.Div(id='download-link-container',
                            className='p-2 d-flex justify-content-center align-items-center')
                ],
                width={"size": 9, "offset": 3},
            )
        ],
            className='g-0 m-2 d-flex justify-content-center align-items-center'),
    ],
        fluid=True,
        className='g-0')



layout = html.Div(
    [download()],
    className = 'bg-dark'
)

