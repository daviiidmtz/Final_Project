# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Dropdown para seleccionar el sitio de lanzamiento
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] + 
                [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    
    html.Br(),

    # TASK 2: Pie chart para mostrar los lanzamientos exitosos
    html.Div(dcc.Graph(id='success-pie-chart')),
    
    html.Br(),

    html.P("Payload range (Kg):"),
    
    # TASK 3: Slider para seleccionar el rango de carga útil
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={int(min_payload): str(int(min_payload)), 
               int(max_payload): str(int(max_payload))},
        value=[min_payload, max_payload]
    ),
    
    # TASK 4: Gráfica de dispersión para mostrar la relación entre carga útil y éxito del lanzamiento
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback para actualizar la gráfica de pastel
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Mostrar el porcentaje de lanzamientos exitosos en todos los sitios
        fig = px.pie(spacex_df, names='Launch Site', values='class', 
                     title='Total Successful Launches by Site')
    else:
        # Mostrar el porcentaje de éxito y fracaso en el sitio seleccionado
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(site_data, names='class', 
                     title=f'Success vs. Failure at {selected_site}')
    return fig

# TASK 4: Callback para actualizar la gráfica de dispersión
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Filtrar datos por rango de carga útil
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]

    if selected_site == 'ALL':
        # Mostrar todos los sitios
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                         color='Launch Site',
                         title='Payload vs. Success for All Sites')
    else:
        # Filtrar por sitio específico
        site_data = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(site_data, x='Payload Mass (kg)', y='class', 
                         color='class',
                         title=f'Payload vs. Success at {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)