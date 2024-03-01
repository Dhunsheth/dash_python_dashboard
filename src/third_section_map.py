from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import altair as alt
import pandas as pd
import vegafusion
import folium
from itertools import islice

def get_third_section_map():
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
                                                    html.Th(scope='row', className='table-dark', children="Map of Stations"),
                                                ]
                                            ),
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
                    [
                        html.Iframe(
                            id='map-iframe',
                            srcDoc='',
                            style={'width': '100%', 'height':'80vh', 'border': '1px solid black'}
                        )
                    ]
                ),
            dbc.Row(
                dbc.Col(
                    html.Div( 
                        dcc.Dropdown(
                            id="num-stations",
                            options=[{'label': str(i), 'value': i} for i in [5, 10, 20, 50, 100, 250]],
                            value=50,
                            multi=False,
                            style={'text-align':'center', 'width': '100%'}  # Use 100% of the div's width
                        ), 
                        style={'max-width': '30%', 'margin': '0 auto'}  # Center the div within the column
                    ),
                    width=12  # Use all 12 columns of the grid for the Col, adjust as needed
                ),
                justify="center"  # This will center the column if the screen is wider than the content
            )
        ]

def get_map(num_stations, geo_station_map_df, start_date, end_date):
    
    filtered_df = geo_station_map_df.loc[(slice(start_date, end_date), slice(None), slice(None)), :]
    filtered_df = filtered_df.reset_index()
    filtered_df.drop(columns=['day'], inplace=True)
    
    aggregation_functions = {
        'count': 'sum',
        'start_count': 'sum',
        'end_count': 'sum',
        'lng': 'mean',
        'lat': 'mean',           
    }

    filtered_map_df = filtered_df.groupby('station_name').agg(aggregation_functions).sort_values(by='count', ascending=False)
    filtered_map_df.reset_index(inplace=True)
    
    points = [
        (row['lat'], row['lng'], row['station_name'], row['count']) 
        for index, row in islice(filtered_map_df.iterrows(), num_stations)
    ]
    
    map_chicago = folium.Map(location=[41.8781, -87.6298], zoom_start=12)
    
    for point in points[:num_stations]:
        tooltip_text = f"Rank: {filtered_map_df[filtered_map_df['station_name'] == point[2]].index[0] + 1} - {point[2]} - {point[3]}"  # Rank and station name
        folium.Marker(
            location=[point[0], point[1]],
            tooltip=tooltip_text
        ).add_to(map_chicago)
    
    map_html = map_chicago.get_root().render()
    
    return map_html
    