import os
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
from IPython.display import IFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.express as px
import vegafusion
import folium
from itertools import islice

from first_section import get_first_section
from first_section import plot_rider_trend
from second_section_heatmap import get_heatmap
from second_section_heatmap import plot_heatmap
from third_section_map import get_third_section_map
from third_section_map import get_map

# changing current directory to directory of app.py file
file_path = 'app.py'
full_file_path = os.path.abspath(file_path)
directory_path = os.path.dirname(full_file_path)
os.chdir(directory_path)


# Load data frames from parquet
data = pd.read_parquet('../data/processed/data.parquet')
rider_trend_df = pd.read_parquet('../data/processed/rider_trend_df.parquet')
heat_map_df = pd.read_parquet('../data/processed/heat_map_df.parquet')
geo_station_map_df = pd.read_parquet('../data/processed/geo_station_map_df.parquet')
#points_df = pd.read_parquet('../data/processed/points_df.parquet')

# num_station_to_show = 10

# points = [
#     (row['lat'], row['lng'], row['station_name'], row['count']) 
#     for index, row in islice(map_stations_df.iterrows(), num_station_to_show)
# ]

# map_chicago = folium.Map(location=[41.8781, -87.6298], zoom_start=12)

# for point in points:
#     tooltip_text = f"Rank: {map_stations_df[map_stations_df['station_name'] == point[2]].index[0] + 1} - {point[2]}"  # Rank and station name
#     folium.Marker(
#         location=[point[0], point[1]],
#         tooltip=tooltip_text
#     ).add_to(map_chicago)

# map_chicago
# map_chicago.save('map_chicago.html')
# IFrame(src='map_chicago.html', width=800, height=600)

start_date_min = str(data['started_at'].min())
end_date_max = str(data['ended_at'].max())

alt.data_transformers.enable('vegafusion')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

app.layout = html.Div([
    dbc.Container(
            get_first_section(start_date_min, end_date_max),
            className="mb-4"
        ),
    dbc.Container(
            get_heatmap(data),
            className="mb-4"
        
        ),
    dbc.Container(
            get_third_section_map(),
            className="mb-4"
        
        )
    
])
@app.callback(
    Output('rider-trend-bar', 'srcDoc'),
    [Input('rider-trend-radio', 'value'),
    Input('rider-trend-box', 'value'),
    Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def plot_rider_analysis(func, cat, start_date, end_date):
    p = plot_rider_trend(rider_trend_df, func, cat, start_date, end_date)
    return p

@app.callback(
    Output('heat', 'srcDoc'),
    [Input('station-select', 'value'),
    Input('heatmap-radio', 'value'),
    Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)

def plot_station_analysis(stations, heat_type, start_date, end_date):
    p = plot_heatmap(heat_map_df, stations, heat_type, start_date, end_date)
    return p

@app.callback(
    Output('map-iframe', 'srcDoc'),
    [Input('num-stations', 'value'),
     Input('date-picker-range', 'start_date'),
      Input('date-picker-range', 'end_date')]
)

def plot_map(num_stations, start_date, end_date):
    p = get_map(num_stations, geo_station_map_df, start_date, end_date)
    return p

if __name__ == '__main__':
    app.run_server(debug=True)

