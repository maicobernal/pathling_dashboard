# Import necessary libraries 
from dash import html
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html, dcc
from dash.dependencies import Input, Output
import pathlib
import plotly.express as px
import requests
import pandas as pd

dash.register_page(__name__, order = 2)

def get_aggregate(server, resource_type, element_path, filter_path=None):
    url = f'{server}/{resource_type}/$aggregate?aggregation=count()&grouping={element_path}'

    if filter_path is not None:
        url = f'{url}&filter={filter_path}'
    
    resp = requests.get(url, headers={"Content-Type": "application/fhir+json"} )
    return resp.json()

def plot_aggregate(resp, title, limit, size=[12,8], rotation=90, ascending=True, skip_missing=False):
    parameters = resp['parameter']
    list_label = []
    list_value = []
    for parameter in parameters:
        if (len(parameter['part'][0]) == 2):
            label_val = list(parameter['part'][0].values())[1]
        elif skip_missing:
            continue
        else:
            label_val = 'WITHOUT'
        list_label.append(label_val)
        list_value.append(parameter['part'][1]['valueUnsignedInt'])

    df = pd.DataFrame({'label': list_label, 'value': list_value})
    df_sorted = df.sort_values(by=['value'], ascending=ascending).iloc[-limit:]

    fig = px.bar(df_sorted, x='value', y='label', orientation='h')
    fig.update_layout(
        xaxis=dict(tickangle=rotation),
        #width=size[0] * 100,
        #height=size[1] * 100,
        #margin={"r":0,"t":0,"l":0,"b":0},
        #title = {""}
    )
    return fig

def description_card():
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H5("Dashboard FHIR - Pathlings Analytics", className="card-title"),
                    html.P(
                        "Este dashboard es a modo de prueba para visualizar datos sintéticos almacenados con el estándar HL-7 FHIR R4.",
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
        ('maritalStatus.coding.display', 'Estado civil')
    ],
    'Encounter': [
        ('class.code', 'Clase de encuentro'),
        ('type.coding.display', 'Tipo de encuentro')
    ],
    'Procedure': [
        ('code.coding.display', 'Código de procedimiento'),
        ('category.coding.display', 'Categoría de procedimiento')
    ],
    'Condition': [
        ('code.coding.display', 'Código de diagnóstico')
    ],
    'MedicationRequest': [
        ('medicationCodeableConcept.coding.display', 'Código de medicación')
    ],
    'Immunization': [
        ('vaccineCode.coding.display', 'Código de vacuna')
    ],
    'AllergyIntolerance': [
        ('code.coding.display', 'Código de alergia/intolerancia')
    ]
}


tags = [element[1] for resource, elements in features.items() for element in elements]
values = [f"{resource}: {element[0]}" for resource, elements in features.items() for element in elements]
tags_and_values = list(zip(tags, values))
options = [{"label": label, "value": value} for label, value in tags_and_values]

def generate_control_card():
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Seleccione variable", className="card-title"),
                    dcc.Dropdown(
                        id="features-select",
                        options = options,
                        value = options[0]['value'],
                        className = ''
                    ),
                ]
                
            )
        ],
        className = 'mt-3'
    )


@dash.callback(
        Output("grafico", "figure")
    ,
    [
        Input("features-select", "value"),
    ],
)
def get_data(input):
    server = 'http://pathling:8080/fhir'
    resource_type = input.split(':')[0].strip()
    element_path = input.split(':')[1].strip()
    title = f'{resource_type}: {element_path}'
    limit = 10
    resp = get_aggregate(server, resource_type, element_path)
    return plot_aggregate(resp, title, limit)



@dash.callback(
    Output("selected-indicador", "children"),
    [Input("features-select", "value")]
)
def update_selected_indicador(selected_value):
    location = values.index(selected_value)
    return html.P(f"Variable seleccionada: {tags[location]}", className="card-text text-center mt-3 text-white")


def poblacion():
        return dbc.Container([
                dbc.Row([
                    dbc.Col(
                        children = [description_card(),generate_control_card()],
                        width={"size": 3}
                    ),
                    dbc.Col(
                        children=[
                                html.H4('Gráfico de agregación', className="card-title text-center text-white"),
                                html.Div(id="selected-indicador", className = 'mb-2'),
                                dcc.Graph(id="grafico")
                                ],
                        width={"size": 9},
                        className = 'p-5 mt-1'
                    )
                    ],
                    className = 'g-0 m-2 d-flex justify-content-center align-items-center')
            ], 
            fluid=True,
            className = 'g-0')


layout = poblacion()