import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import dash_bootstrap_components as dbc

# cargamos el documen to en un data frame
df = pd.read_csv('Base_de_datos.csv')
df_precio= pd.read_csv('Base_de_tarifas.csv')

def operar():
    global df_nuevo
    global df_precio
    #aqui se va a realizar el calculo de los precios segun el mes
    df_precio['Date'] = pd.to_datetime(df_precio['Date'], format='%m/%d/%Y', errors='coerce')
    df_nuevo = pd.DataFrame({'Mes': monthly_consumption.index, 'Consumo_Energetico': monthly_consumption.values, 'Precio_Mes': df_precio['Value']})
    df_nuevo['Nombre_Mes'] = [meses[int(date.split('-')[1])] for date in df_nuevo['Mes']]
    df_nuevo['Consumo_Energetico'] = df_nuevo['Consumo_Energetico'].round(0)
    df_nuevo['Precio_Mes'] = df_nuevo['Precio_Mes'].round(0)
    df_nuevo['Total_Costo'] = df_nuevo['Consumo_Energetico'] * df_nuevo['Precio_Mes']
    
def diccionarios():
    global meses
    global horas

    meses = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }

    horas = {
        1: "1 am",
        2: "2 am",
        3: "3 am",
        4: "4 am",
        5: "5 am",
        6: "6 am",
        7: "7 am",
        8: "8 am",
        9: "9 am",
        10: "10 am",
        11: "11 am",
        12: "12 pm",
        13: "1 pm",
        14: "2 pm",
        15: "3 pm",
        16: "4 pm",
        17: "5 pm",
        18: "6 pm",
        19: "7 pm",
        20: "8 pm",
        21: "9 pm",
        22: "10 pm",
        23: "11 pm",
        24: "12 am",
    }

def filtrar():
    global max_value
    global monthly_consumption
    global fecha

    # Agrupa los datos por mes y suma el consumo de cada mes
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
     # Suma el consumo de todas las horas en cada mes y crea una columna "Total" en el DataFrame
    df['Total'] = df[['H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13', 'H14', 'H15', 'H16', 'H17', 'H18', 'H19', 'H20', 'H21', 'H22', 'H23']].sum(axis=1)
    # Agrupa los datos por mes y muestra el consumo general por meses
    monthly_consumption = df.groupby(df['Date'].dt.strftime('%Y-%m'))['Total'].sum()
    #Valor del consumo maximo
    max_month = monthly_consumption.idxmax()
    partes = max_month.split('-')
    partes=int(partes[1])
    fecha=(meses[partes])
    max_value = monthly_consumption[max_month].round(2)

def fecha_max():

    global max_row
    global nombre_mes
    global max_column
    global max_day
    global hora
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
    max_row, max_column = df.iloc[:, 1:].stack().idxmax()

    # Obtiene la fecha correspondiente
    max_date = df['Date'].iloc[max_row]

    # Desglosa la fecha en día, mes y año
    max_day = max_date.day
    max_month = max_date.month
    nombre_mes=meses[max_month]

    # Obtiene la hora correspondiente
    max_hour = int(max_column[1:])  # Extrae el número de la columna "H#"
    max_hour = (max_hour + 1) % 24  # Convierte la hora en un rango de 0 a 24
    hora=horas[max_hour]

def graficar():
    global month_labels
    global sizes

    # Datos de 'monthly_consumption'
    labels = monthly_consumption.index
    sizes = monthly_consumption.values

    month_labels = [meses[int(date.split('-')[1])] for date in labels]

    # Crear una figura con dos subplots, uno para el diagrama de torta y otro para el diagrama de barras
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    # Diagrama de torta
    ax1.pie(sizes, labels=month_labels, autopct='%1.1f%%', startangle=90)
    ax1.set_title("Distribución de demanda Mensual en 2022")

    # Diagrama de barras
    ax2.bar(month_labels, sizes)
    ax2.set_xticklabels(month_labels, rotation=45)
    ax2.set_xlabel("Fecha")
    ax2.set_ylabel("kWhD")
    ax2.set_title("Demanda mensual de energia por la plata en 2022")

    # Gráfica de líneas
    ax3.plot(df_nuevo['Nombre_Mes'], df_nuevo['Total_Costo'], marker='o', linestyle='-', color='b')
    ax3.set_xlabel('Mes')
    ax3.set_ylabel('Total Costo')
    ax3.set_title('Total Costo por Mes')
    ax3.tick_params(axis='x', rotation=45)

    # Ajustar el espaciado entre subplots
    plt.tight_layout()

    # Mostrar la gráfica con ambos subplots al mismo tiempo
    ##plt.show()

diccionarios()
fecha_max()
filtrar()
operar()
graficar()

#dash board
# Configuración de Dash
app = dash.Dash(__name__, external_stylesheets=['styles.css'])

def mostrar_informacion_demanda_maxima():
    return dbc.Card(
        dbc.CardBody([
            html.H2("Información de Demanda Máxima", className="card-title", style={'fontFamily': 'Arial'}),
            html.P(f"Demanda máximo: {df.at[max_row, max_column].round(2)}", className="card-text", style={'fontFamily': 'Arial'}),
            html.P(f"Fecha de demanda máxima: Dia {max_day}, mes: {nombre_mes}", className="card-text", style={'fontFamily': 'Arial'}),
            html.P(f"Hora del demanda máximo: {hora}", className="card-text", style={'fontFamily': 'Arial'})
        ]),
        style={'backgroundColor': 'white', 'border': '2px solid black', 'borderRadius': '15px', 'margin': '20px'}
    )

# Función para mostrar la información del mes con mayor consumo en el Dash
def mostrar_informacion_mes_maximo():
    return dbc.Card(
        dbc.CardBody([
            html.H2("Información del Mes con Mayor Consumo", className="card-title", style={'fontFamily': 'Arial'}),
            html.P(f"Mes con mayor consumo: {fecha}", className="card-text", style={'fontFamily': 'Arial'}),
            html.P(f"Consumo máximo en ese mes: {max_value}", className="card-text", style={'fontFamily': 'Arial'})
        ]),
        style={'backgroundColor': 'white', 'border': '2px solid black', 'borderRadius': '15px', 'margin': '20px'}
    )

def mostrar_tarjeta_datos():
    return dbc.Card(
        dbc.CardBody([
            html.H2("Datos Mensuales en pesos", className="card-title", style={'fontFamily': 'Arial'}),
            dbc.Table.from_dataframe(df_nuevo[['Nombre_Mes', 'Total_Costo']].round(2), striped=True, bordered=True, hover=True,
                                     style={'margin': 'auto', 'textAlign': 'center', 'fontFamily': 'Arial'})
        ]),
        style={'backgroundColor': 'white', 'border': '2px solid black', 'borderRadius': '15px', 'margin': '20px', 'width': '20%'}
    )
# Layout
app.layout = html.Div(style={'backgroundColor': 'rgb(240, 240, 240)', 'textAlign': 'center'}, children=[
    html.H1(children='Energia requerida por la planta la Petar', style={'color': 'black', 'fontFamily': 'Arial'}),

    html.Div([  # Div para el gráfico de torta y la información de demanda máxima
        dcc.Graph(
            id='pie-chart',
            figure={
                'data': [
                    {'labels': month_labels, 'values': sizes, 'type': 'pie', 'name': 'Distribución Mensual'},
                ],
                'layout': {
                    'title': 'Distribución de demanda Mensual', 'font': {'weight': 'bold'}
                }
            },
            style={'height': '400px', 'width': '50%', 'margin': 'auto', 'border': '2px solid black', 'borderRadius': '15px',
                   'padding': '8px', 'marginBottom': '20px'}
        ),
        mostrar_informacion_demanda_maxima(),  # Mostrar información de demanda máxima
        mostrar_informacion_mes_maximo()
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'margin': 'auto'}),

    dcc.Graph(
        id='bar-chart',
        figure={
            'data': [
                {'x': month_labels, 'y': sizes, 'type': 'bar', 'name': 'Demanda Mensual'},
            ],
            'layout': {
                'title': 'Demanda mensual de energia por la plata en Kwh durante el 2022'
            }
        },
        style={'height': '400px', 'width': '80%', 'margin': 'auto', 'border': '2px solid black', 'borderRadius': '15px',
               'padding': '8px', 'marginBottom': '20px'}
    ),

    html.Div([  # Div para la última gráfica y la tarjeta de datos
        mostrar_tarjeta_datos(),
        dcc.Graph(
            id='line-chart',
            figure={
                'data': [
                    {'x': df_nuevo['Nombre_Mes'], 'y': df_nuevo['Total_Costo'], 'type': 'line', 'name': 'Total Costo por Mes'},
                ],
                'layout': {
                    'title': 'Total Costo por Mes'
                }
            },
            style={'height': '400px', 'width': '60%', 'margin': 'auto', 'border': '2px solid black', 'borderRadius': '15px',
                   'padding': '8px', 'marginBottom': '20px'},
            config={'displayModeBar': False}
        )
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'margin': 'auto'}),
])


if __name__ == '__main__':
    app.run_server(debug=True)