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
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': 'All Sites', 'value': 'ALL'},
                                                      {'label': 'CCAFS LC-40', 'value': 'site1'},
                                                      {'label': 'VAFB SLC-4E', 'value': 'site2'},
                                                      {'label': 'KSC LC-39A', 'value': 'site3'},
                                                      {'label': 'CCAFS SLC-40', 'value': 'site4'}],
                                             value='ALL',
                                             placeholder='Select a Site:',
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 1000:'1000', 2000:'2000', 3000:'3000', 4000:'4000', 5000: '5000', 
                                                    6000:'6000', 7000:'7000', 8000:'8000', 9000:'9000', 10000:'10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    
    if entered_site == 'ALL':
        filtered_df = spacex_df
        fig = px.pie(filtered_df, values='class',
        names='Launch Site', 
        title='Total Succes Launches by Site')
        return fig
    elif entered_site == 'site1':
        filtered_df = spacex_df[spacex_df['Launch Site'] == "CCAFS LC-40"]
        filtered_df= filtered_df.groupby('class').size().reset_index(name='counts')
        fig = px.pie(filtered_df, 
        values='counts',
        names='class', 
        title='Total Succes Launches for site CCAFS LC-40')
        return fig
    elif entered_site == 'site2':
        filtered_df = spacex_df[spacex_df['Launch Site'] == "VAFB SLC-4E"]
        filtered_df= filtered_df.groupby('class').size().reset_index(name='counts')
        fig = px.pie(filtered_df, 
        values='counts',
        names='class', 
        title='Total Succes Launches for site VAFB SLC-4E')
        return fig

    elif entered_site == 'site3':
        filtered_df = spacex_df[spacex_df['Launch Site'] == "KSC LC-39A"]
        filtered_df= filtered_df.groupby('class').size().reset_index(name='counts')
        fig = px.pie(filtered_df, 
        values='counts',
        names='class', 
        title='Total Succes Launches for site KSC LC-39A')
        return fig
    
    elif entered_site == 'site4':
        filtered_df = spacex_df[spacex_df['Launch Site'] == "CCAFS SLC-40"]
        filtered_df= filtered_df.groupby('class').size().reset_index(name='counts')
        fig = px.pie(filtered_df, 
        values='counts',
        names='class', 
        title='Total Succes Launches for site CCAFS SLC-40')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))

def get_scatter_chart(entered_site, payload_value):
    low, high = payload_value
    mask= (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df[mask],x= 'Payload Mass (kg)', y='class', title='Correlation Between Payload and Succes for all Sites',
                color= 'Booster Version Category', symbol='Booster Version Category')
        return fig
    else:
        if entered_site == "site1":
            filter_site='CCAFS LC-40'
        elif entered_site == "site2":
            filter_site='VAFB SLC-4E'
        elif entered_site == "site3":
            filter_site='KSC LC-39A'
        elif entered_site == "site4":
            filter_site='CCAFS SLC-40'
        filtered2_df = spacex_df[spacex_df['Launch Site'] == filter_site]
        fig = px.scatter(filtered2_df[mask],x= 'Payload Mass (kg)', y='class', title='Correlation Between Payload and Succes for: '+filter_site,
                color= 'Booster Version Category', symbol='Booster Version Category')
        return fig
        
            #else:

# Run the app
if __name__ == '__main__':
    app.run_server()
