import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

# Load SpaceX launch data into a DataFrame
spacex_df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # Dropdown to select a launch site
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}
                                             ],
                                             value='ALL',
                                             placeholder="Select a launch site",
                                             searchable=True
                                             ),
                                html.Br(),

                                # Pie chart showing the total successful launches
                                html.Div(dcc.Graph(id='success-pie-chart')),

                                html.Br(),

                                # Slider for selecting payload range
                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                                value=[0, 10000]
                                                ),

                                # Scatter plot for showing the correlation between payload and success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# Callback function to update pie chart based on dropdown selection
@app.callback(Output('success-pie-chart', 'figure'),
              [Input('site-dropdown', 'value')])
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        pie_fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches By Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        pie_fig = px.pie(filtered_df, names='class', title=f'Total Success Launches for Site {selected_site}')
    return pie_fig


# Callback function to update scatter plot based on dropdown and slider selection
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'),
               Input('payload-slider', 'value')])
def update_scatter_chart(selected_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    if selected_site == 'ALL':
        scatter_fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                                 title='Correlation between Payload and Success for All Sites')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        scatter_fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                                 title=f'Correlation between Payload and Success for Site {selected_site}')
    return scatter_fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8054)
    
