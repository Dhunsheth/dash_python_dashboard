import os
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd

import requests
import pyarrow
from io import BytesIO

from first_section import get_first_section
from first_section import plot_rider_trend_hour
from first_section import plot_rider_trend_day
from first_section import plot_rider_trend_month
from second_section_heatmap import plot_station
from second_section_heatmap import get_second_section
from second_section_heatmap import plot_multi_station
from third_section_map import get_third_section_map
from third_section_map import get_map

# changing current directory to directory of app.py file
file_path = 'app.py'
full_file_path = os.path.abspath(file_path)
directory_path = os.path.dirname(full_file_path)
os.chdir(directory_path)

# Load data frames from parquet
rider_trend_hour = pd.read_parquet('../data/processed/rider_trend_hour.parquet')
rider_trend_day = pd.read_parquet('../data/processed/rider_trend_day.parquet')
rider_trend_month = pd.read_parquet('../data/processed/rider_trend_month.parquet')
stations_comparison = pd.read_parquet('../data/processed/station_comparison.parquet')
station_list = pd.read_parquet('../data/processed/station_list.parquet')
geo_station_map_df = pd.read_parquet('../data/processed/geo_station_map_df.parquet')


alt.data_transformers.enable('vegafusion')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(
                html.Div([
                html.Img(src="https://txt.1001fonts.net/img/txt/dHRmLjEyOC4yYjJkNDIuUTJocFkyRm5ieUJDYVd0bElGTm9ZWEpwYm1jLjA/brackley-demo.regular.webp", 
                             style={'width': '700px', 'height': '120px'}),
            html.Img(src="https://cdn.dribbble.com/users/594619/screenshots/2339770/media/a1cd8aed45626dc2c5f404bdcb222ffe.gif", 
                 style={'padding-left':'50px','width': '300px', 'height': '200px', 'object-fit': 'cover', 'overflow': 'hidden'})
            ], className="d-flex justify-content-center align-items-center"), style={'padding-left':'130px'})
        ])
    ], style={'maxWidth': '100%'}),
    dcc.Tabs([
            dcc.Tab(
                label='Rider Trend Analysis',
                children=[dbc.Container(get_first_section(), style={'maxWidth': '100%'})],
                style={'backgroundColor': '#2B2D42', 'color': '#edf2f4', 'fontSize': '18px', 'padding':'15px'},
                selected_style={'backgroundColor': '#8e0050', 'color': '#edf2f4', 'fontSize': '18px', 'padding':'15px'}
            ),
            dcc.Tab(
                label='Station Analysis',
                children=[dbc.Container(get_second_section(station_list), style={'maxWidth': '100%'})],
                style={'backgroundColor': '#2B2D42', 'color': '#edf2f4', 'fontSize': '18px', 'padding':'15px'},
                selected_style={'backgroundColor': '#8e0050', 'color': '#edf2f4', 'fontSize': '18px', 'padding':'15px'}
            ),
            dcc.Tab(
                label='Station Map',
                children=[dbc.Container(get_third_section_map(), style={'maxWidth': '100%'})],
                style={'backgroundColor': '#2B2D42', 'color': '#edf2f4', 'fontSize': '18px', 'padding':'15px'},
                selected_style={'backgroundColor': '#8e0050', 'color': '#edf2f4', 'fontSize': '18px', 'padding':'15px'}
            )
        ], style={'backgroundColor': '#2B2D42', 'color': '#2B2D42', 'fontSize': '24px'})  # Styles for the entire tab component 
])
@app.callback(
    [Output('rider-trend-hour', 'srcDoc'),
     Output('output-hour', 'children'),
     Output('output-hour-count', 'children'),
     Output('output-hour-duration', 'children')],
    [Input('rider-trend-radio', 'value'),
    Input('rider-trend-box', 'value')]
)
def plot_rider_hour(func, cat):
    chart_hour, kpi_hour, kpi_total_hours, kpi_avg_hours = plot_rider_trend_hour(rider_trend_hour, func, cat)
    return chart_hour, kpi_hour, kpi_total_hours, kpi_avg_hours

@app.callback(
    [Output('rider-trend-day', 'srcDoc'),
     Output('output-day', 'children'),
     Output('output-day-count', 'children'),
     Output('output-day-duration', 'children')],
    [Input('rider-trend-radio', 'value'),
    Input('rider-trend-box', 'value')]
)
def plot_rider_day(func, cat):
    chart_day, kpi_day, kpi_total_day, kpi_avg_day = plot_rider_trend_day(rider_trend_day, func, cat)
    return chart_day, kpi_day, kpi_total_day, kpi_avg_day

@app.callback(
    [Output('rider-trend-month', 'srcDoc'),
     Output('output-month', 'children'),
     Output('output-month-count', 'children'),
     Output('output-month-duration', 'children')],
    [Input('rider-trend-radio', 'value'),
    Input('rider-trend-box', 'value')]
)
def plot_rider_month(func, cat):
    chart_month, kpi_month, kpi_total_month, kpi_avg_month = plot_rider_trend_month(rider_trend_month, func, cat)
    return chart_month, kpi_month, kpi_total_month, kpi_avg_month

@app.callback(
    [Output('station-a-graph', 'srcDoc'),
     Output('output-station-a-day', 'children'),
     Output('output-station-a-hour', 'children'),
     Output('output-station-a-metric', 'children')],
    [Input('station-comparison-metric', 'value'),
     Input('station-a-list', 'value')]
)
def plot_station_A_map(func, station):
    chart, day, hour, metric = plot_station(stations_comparison, func, station)
    return chart, day, hour, metric

@app.callback(
    [Output('station-b-graph', 'srcDoc'),
     Output('output-station-b-day', 'children'),
     Output('output-station-b-hour', 'children'),
     Output('output-station-b-metric', 'children')],
    [Input('station-comparison-metric', 'value'),
     Input('station-b-list', 'value')]
)
def plot_station_B_map(func, station):
    chart, day, hour, metric = plot_station(stations_comparison, func, station)
    return chart, day, hour, metric

@app.callback(
    [Output('heat', 'srcDoc'),
     Output('output-busiest-station', 'children'),
     Output('output-busiest-time', 'children'),
     Output('output-busiest-metric', 'children')],
    [Input('station-comparison-metric', 'value'),
     Input('station-select', 'value')]
)
def plot_multi_station_map(func, stations):
    chart, mp_station, mp_time, mp_metric = plot_multi_station(stations_comparison, func, stations)
    return chart, mp_station, mp_time, mp_metric

@app.callback(
    [Output('map-iframe', 'srcDoc'),
     Output('output-geo-top-station', 'children'),
     Output('output-geo-top-total-rides', 'children'),
     Output('output-geo-bot-station', 'children'),
     Output('output-geo-bot-total-rides', 'children')],
    [Input('num-stations', 'value')]
)

def plot_map(num_stations):
    chart, top_station, top_metric, bot_station, bot_metric = get_map(num_stations, geo_station_map_df)
    return chart, top_station, top_metric, bot_station, bot_metric

if __name__ == '__main__':
    app.run_server()

