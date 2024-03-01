from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import altair as alt
import pandas as pd
import vegafusion


def get_heatmap(df):
    top20_start = df['start_station_name'].value_counts()[:20].index.values
    return [
        dbc.Row(
            [
                html.Div(
                    [
                        dbc.Table(
                            # Table header
                            children=[
                                html.Tbody(
                                    [
                                        html.Tr(
                                            [
                                                html.Th(scope='row', className='table-dark', children="Station Analysis"),
                                            ]
                                        )
                                    ]
                                )
                            ], 
                            style={'text-align':'center', 'padding':'0vh', 'margin':'0vh'}
                        )
                    ]
                )
            ]
        ),
        dbc.Row(
                html.Iframe(
                    id='heat',
                    style={'width': '100%', 'height':'550px', 'border': '1px solid black'}
                    )
        ),
        dbc.Row(
                dcc.RadioItems(
                    id='heatmap-radio',
                    options=[
                        {'label': "Start Station", 'value': 'start'},
                        {'label': "End Station", 'value': 'end'},
                        {'label': "Net Bikes", 'value': 'net'}
                    ],
                    value='start',
                    labelStyle={'display': 'inline-block', 'margin-left': '20px', 'margin-right': '20px'},
                    inputClassName="form-check-input",
                    labelClassName="form-check-label",
                    className="form-check",
                    style={'text-align': 'center', 'margin': 'auto', 'width': 'fit-content', 'border': '1px solid black'}
                        )
        ),
        dbc.Row(
                # dropdown to select the stations to visualize
                dcc.Dropdown(
                            id="station-select",
                            options=[{"label": i, "value": i} for i in top20_start],
                            value=top20_start[:10],
                            multi=True,
                            style = {'padding-top': '10px', 'padding-bottom': '10px', 'padding-right': '5px'}
                )
        )
        
    ]

alt.data_transformers.enable('vegafusion')
def plot_heatmap(heat_map_df, stations, heat_type, start_date, end_date):
    
    filtered_df = heat_map_df.loc[(slice(start_date, end_date), slice(None), stations), :]
    filtered_df = filtered_df.reset_index()
    filtered_df.drop(columns=['day'], inplace=True)
    
    if heat_type == 'start':
        heatmap = alt.Chart(filtered_df).mark_rect().encode(
            x=alt.X('hours(time):O', title=None),
            y=alt.Y('station_name:N', title=None),
            color='sum(start_count)',
            tooltip=[
                alt.Tooltip('station_name:N', title='Station'),
                alt.Tooltip('hours(time):O', title='Hour'),
                alt.Tooltip('sum(start_count)', title='# of Rides Started')
                ]
            )
    elif heat_type == 'end':
        heatmap = alt.Chart(filtered_df).mark_rect().encode(
            x=alt.X('hours(time):O', title=None),
            y=alt.Y('station_name:N', title=None),
            color='sum(end_count)',
            tooltip=[
                alt.Tooltip('station_name:N', title='Station'),
                alt.Tooltip('hours(time):O', title='Hour'),
                alt.Tooltip('sum(end_count)', title='# of Rides Ended')
                ]
            )   
    elif heat_type == 'net':

        heatmap = alt.Chart(filtered_df).mark_rect().encode(
            x=alt.X('hours(time):O', title=None),
            y=alt.Y('station_name:N', title=None),
            color=alt.Color('sum(net):Q', scale=alt.Scale(range=['#D4322C', 'white', '#4A74B4'], domainMid=0)).title("Net Bikes at Station"),
            tooltip= [alt.Tooltip('station_name:N', title="Station Name"), alt.Tooltip('hours(time):O', title="Time of Day"), alt.Tooltip('sum(net):Q', title='Net Bikes')]
        )
    
    heatmap = heatmap.properties(height=500, width = 800)
    vega_lite_json = heatmap.to_json(format='vega')

    chart_obj = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
            <script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
            <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
        </head>
        <body>
        <center>
            <div id="altair-chart-container"></div>
            <script>
                var spec = {vega_lite_json};
                vegaEmbed('#altair-chart-container', spec);
            </script>
        </center>
        </body>
        </html>
    """
    return chart_obj
    