from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import altair as alt


def get_second_section(df):
    top_100_start = df['station_name'].values
    metric_color = '#8e0050'
    return [
        
    dbc.Row([
        dbc.Col([
                    dbc.Row(html.H4("KPI Summary"), style={'text-align':'center', 'padding-top':'40px'}),
                    dbc.Row(html.H5("Station A", style={'text-align':'center', 'font-weight': 'bold',
                                                                'padding-top':'40px', 'color':'#2B2D42'})),
                    dbc.Row(html.H6("Most Popular Day"), style={'text-align':'center', 'font-style': 'italic'}),
                    dbc.Row(
                            dbc.Col(html.Div(id='output-station-a-day'), 
                            width=12, className="text-center"),
                            style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                            ),
                    dbc.Row(html.H6("Most Popular Hour"), style={'text-align':'center', 'font-style': 'italic', 'padding-top':'15px'}),
                    dbc.Row(
                            dbc.Col(html.Div(id='output-station-a-hour'), 
                            width=12, className="text-center"),
                            style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                            ),
                    dbc.Row(html.H6("Largest Comparison Metric"), style={'text-align':'center', 'font-style': 'italic', 'padding-top':'15px'}),
                    dbc.Row(
                            dbc.Col(html.Div(id='output-station-a-metric'), 
                            width=12, className="text-center"),
                            style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                            ),
                    dbc.Row(html.H5("Station B", style={'text-align':'center', 'font-weight': 'bold',
                                                                'padding-top':'40px', 'color':'#2B2D42'})),
                    dbc.Row(html.H6("Most Popular Day"), style={'text-align':'center', 'font-style': 'italic'}),
                    dbc.Row(
                            dbc.Col(html.Div(id='output-station-b-day'), 
                            width=12, className="text-center"),
                            style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                            ),
                    dbc.Row(html.H6("Most Popular Hour"), style={'text-align':'center', 'font-style': 'italic', 'padding-top':'15px'}),
                    dbc.Row(
                            dbc.Col(html.Div(id='output-station-b-hour'), 
                            width=12, className="text-center"),
                            style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                            ),
                    dbc.Row(html.H6("Largest Comparison Metric"), style={'text-align':'center', 'font-style': 'italic', 'padding-top':'15px'}),
                    dbc.Row(
                            dbc.Col(html.Div(id='output-station-b-metric'), 
                            width=12, className="text-center"),
                            style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                            ),
                    dbc.Row(html.H5("Busiest Station", style={'text-align':'center', 'font-weight': 'bold',
                                                                'padding-top':'40px', 'color':'#2B2D42'})),
                    dbc.Row(
                            dbc.Col(html.Div(id='output-busiest-station'), 
                            width=12, className="text-center"),
                            style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                            ),
                    dbc.Row(html.H5("Busiest Time", style={'text-align':'center', 'font-weight': 'bold',
                                                                'padding-top':'20px', 'color':'#2B2D42'})),
                    dbc.Row(
                            dbc.Col(html.Div(id='output-busiest-time'), 
                            width=12, className="text-center"),
                            style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                            ),
                    dbc.Row(html.H5("Busiest Metric", style={'text-align':'center', 'font-weight': 'bold',
                                                                'padding-top':'20px', 'color':'#2B2D42'})),
                    dbc.Row(
                            dbc.Col(html.Div(id='output-busiest-metric'), 
                            width=12, className="text-center"),
                            style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                            )
                    ], width=3, style={"text-align": "center", 'height':'1350px','backgroundColor': '#eaeaec'},
                className='justify-content-center'),
    dbc.Col([
                dbc.Row(
                    [
                        dbc.Col(
                            html.H4("Station Comparison", style={'text-align':'center', 'margin-bottom':'0'}),
                            align='center',
                            style={"text-align": "center"},
                            width=12, className='justify-content-center')
                    ], style={'padding-top':'20px', 'padding-bottom':'10px'}
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H6("Comparison Metric:", style={'margin-bottom':'0'}),
                            align='center',
                            style={"text-align": "right", 'margin-left':'130px', 'padding-right':'0px'},
                            width=3, className='justify-content-center'),
                        dbc.Col(
                                dcc.RadioItems(
                                    id='station-comparison-metric',
                                    options=[
                                        {'label': "Rides Started", 'value': 'start'},
                                        {'label': "Rides Ended", 'value': 'end'},
                                        {'label': "Total Rides", 'value': 'total'},
                                        {'label': "Net Rides", 'value': 'net'}
                                    ],
                                    value='total',
                                    labelStyle={'display': 'inline-block', 'margin-left': '20px', 'margin-right': '20px'},
                                    inputClassName="form-check-input",
                                    labelClassName="form-check-label",
                                    className="form-check",
                                    style={'padding-left':'2px','text-align': 'left','margin-right':'85px', 'margin-left':'0', 'width': 'fit-content'}
                                ), align='center', width=7)
                    ], style={'padding-top':'10px', 'padding-bottom':'10px'}
                ),
                dbc.Row([
                    dbc.Col([
                        html.H5("Station A", style={'text-align': 'center'}),
                        dcc.Dropdown(
                                    id="station-a-list",
                                    options=[{'label': str(i), 'value': i} for i in top_100_start],
                                    value=top_100_start[0],
                                    multi=False,
                                    style={'text-align':'center', 'width': '100%'}  # Use 100% of the div's width
                                ),
                    html.Iframe(
                            id='station-a-graph',
                            style={'margin-top':'0','margin-bottom':'0','margin-right':'0','margin-left':'0',
                                   'width': '100%', 'height':'450px'}
                        )
                        ]),
                    dbc.Col([
                        html.H5("Station B", style={'text-align': 'center'}),
                        dcc.Dropdown(
                                    id="station-b-list",
                                    options=[{'label': str(i), 'value': i} for i in top_100_start],
                                    value=top_100_start[1],
                                    multi=False,
                                    style={'text-align':'center', 'width': '100%'}  # Use 100% of the div's width
                                ),
                        html.Iframe(
                            id='station-b-graph',
                            srcDoc='',
                            style={'width': '100%', 'height':'450px', 'margin': 'auto'}
                        )
                        ])
                    ], style={'padding-top':'10px'}
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H4("Multi-Station Comparison by Hour", style={'text-align':'center', 'margin-bottom':'0'}),
                            align='center',
                            style={"text-align": "center"},
                            width=12, className='justify-content-center')
                    ], style={'padding-top':'20px'}
                ),
                dbc.Row(
                dcc.Dropdown(
                            id="station-select",
                            options=[{"label": i, "value": i} for i in top_100_start],
                            value=top_100_start[:4],
                            multi=True,
                            style = {'padding-top': '10px', 'padding-bottom': '10px', 'padding-right': '5px'}
                            )
                ),
                dbc.Row(
                        html.Iframe(
                            id='heat',
                            style={'width': '100%', 'height':'550px'}
                            )
                )
                ], width=9)
    ])
        ]

alt.data_transformers.enable('vegafusion')

def plot_station(df, func, station):
    filtered_df = df.loc[(slice(None), slice(None), station), :]
    filtered_df = filtered_df.reset_index()
    
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    color_a = '#eaeaec'
    color_b = '#8e0050'
    
    if func == 'start':
        mp_day = filtered_df['day'].values[filtered_df['start_count'].idxmax()]
        mp_hour = filtered_df['hour'].values[filtered_df['start_count'].idxmax()]
        mp_metric = filtered_df['start_count'].max()
        station_map = alt.Chart(filtered_df).mark_rect().encode(
            x=alt.X('hour:O', title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y('day:O', title=None, sort=days_order),
            color=alt.Color('sum(start_count)', scale=alt.Scale(range=[color_a, color_b]), legend=None),
            tooltip=[
                alt.Tooltip('station_name:N', title='Station'),
                alt.Tooltip('day:O', title='Day'),
                alt.Tooltip('hour:O', title='Hour'),
                alt.Tooltip('sum(start_count)', title='# of Rides Started')
                ]
            )
    elif func == 'end':
        mp_day = filtered_df['day'].values[filtered_df['end_count'].idxmax()]
        mp_hour = filtered_df['hour'].values[filtered_df['end_count'].idxmax()]
        mp_metric = filtered_df['end_count'].max()
        station_map = alt.Chart(filtered_df).mark_rect().encode(
            x=alt.X('hour:O', title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y('day:O', title=None, sort=days_order),
            color=alt.Color('sum(end_count)', scale=alt.Scale(range=[color_a, color_b]), legend=None),
            tooltip=[
                alt.Tooltip('station_name:N', title='Station'),
                alt.Tooltip('day:O', title='Day'),
                alt.Tooltip('hour:O', title='Hour'),
                alt.Tooltip('sum(end_count)', title='# of Rides Ended')
                ]
            )
    elif func == 'total':
        mp_day = filtered_df['day'].values[filtered_df['total'].idxmax()]
        mp_hour = filtered_df['hour'].values[filtered_df['total'].idxmax()]
        mp_metric = filtered_df['total'].max()
        station_map = alt.Chart(filtered_df).mark_rect().encode(
            x=alt.X('hour:O', title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y('day:O', title=None, sort=days_order),
            color=alt.Color('sum(total)', scale=alt.Scale(range=[color_a, color_b]), legend=None),
            tooltip=[
                alt.Tooltip('station_name:N', title='Station'),
                alt.Tooltip('day:O', title='Day'),
                alt.Tooltip('hour:O', title='Hour'),
                alt.Tooltip('sum(total)', title='# of Total Rides')
                ]
            )
    else:
        mp_day = filtered_df['day'].values[filtered_df['net'].abs().idxmax()]
        mp_hour = filtered_df['hour'].values[filtered_df['net'].abs().idxmax()]
        mp_metric = filtered_df['net'].values[filtered_df['net'].abs().idxmax()]
        station_map = alt.Chart(filtered_df).mark_rect().encode(
            x=alt.X('hour:O', title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y('day:O', title=None, sort=days_order),
            color=alt.Color('sum(net)', scale=alt.Scale(range=['#d8315b', '#eaeaec','#0a2463'], domainMid=0), legend=None),
            tooltip=[
                alt.Tooltip('station_name:N', title='Station'),
                alt.Tooltip('day:O', title='Day'),
                alt.Tooltip('hour:O', title='Hour'),
                alt.Tooltip('sum(net)', title='# of Net Rides')
                ]
            )
    station_map = station_map.properties(height=400, width = 450).configure_axis(
    gridColor='#eaeaec').configure_axis(labelColor='#2B2D42', 
                                         tickColor='#2B2D42', domainColor='#2B2D42').configure_view(stroke=None)
    vega_lite_json = station_map.to_json(format='vega')

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
                vegaEmbed('#altair-chart-container', spec, {{actions: false}});
            </script>
        </center>
        </body>
        </html>
    """
    return [chart_obj, mp_day, mp_hour, "{:,}".format(mp_metric)]

def plot_multi_station(df, func, stations):
    
    filtered_df = df.loc[(slice(None), slice(None), stations), :]
    filtered_df = filtered_df.reset_index()
    filtered_df.drop(columns=['day'], inplace=True)
    filtered_df = filtered_df.groupby(['hour','station_name']).sum().reset_index()
    
    color_a = '#eaeaec'
    color_b = '#8e0050'
    
    if func == 'start':
        mp_station = filtered_df['station_name'].values[filtered_df['start_count'].idxmax()]
        mp_time = filtered_df['hour'].values[filtered_df['start_count'].idxmax()]
        mp_metric = filtered_df['start_count'].max()
        multi_station_map = alt.Chart(filtered_df).mark_rect().encode(
            x=alt.X('hour:O', title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y('station_name:N', title=None),
            color=alt.Color('start_count', scale=alt.Scale(range=[color_a, color_b]), legend=None),
            tooltip=[
                alt.Tooltip('station_name:N', title='Station'),
                alt.Tooltip('hour:O', title='Hour'),
                alt.Tooltip('start_count', title='# of Rides Started')
                ]
            )
    elif func == 'end':
        mp_station = filtered_df['station_name'].values[filtered_df['end_count'].idxmax()]
        mp_time = filtered_df['hour'].values[filtered_df['end_count'].idxmax()]
        mp_metric = filtered_df['end_count'].max()
        multi_station_map = alt.Chart(filtered_df).mark_rect().encode(
            x=alt.X('hour:O', title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y('station_name:N', title=None),
            color=alt.Color('end_count', scale=alt.Scale(range=[color_a, color_b]), legend=None),
            tooltip=[
                alt.Tooltip('station_name:N', title='Station'),
                alt.Tooltip('hour:O', title='Hour'),
                alt.Tooltip('end_count', title='# of Rides Ended')
                ]
            )
    elif func == 'total':
        mp_station = filtered_df['station_name'].values[filtered_df['total'].idxmax()]
        mp_time = filtered_df['hour'].values[filtered_df['total'].idxmax()]
        mp_metric = filtered_df['total'].max()
        multi_station_map = alt.Chart(filtered_df).mark_rect().encode(
            x=alt.X('hour:O', title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y('station_name:N', title=None),
            color=alt.Color('total', scale=alt.Scale(range=[color_a, color_b]), legend=None),
            tooltip=[
                alt.Tooltip('station_name:N', title='Station'),
                alt.Tooltip('hour:O', title='Hour'),
                alt.Tooltip('total', title='# of Total Rides')
                ]
            )
    else:
        mp_station = filtered_df['station_name'].values[filtered_df['net'].abs().idxmax()]
        mp_time = filtered_df['hour'].values[filtered_df['net'].abs().idxmax()]
        mp_metric = filtered_df['net'].values[filtered_df['net'].abs().idxmax()]
        multi_station_map = alt.Chart(filtered_df).mark_rect().encode(
            x=alt.X('hour:O', title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y('station_name:N', title=None),
            color=alt.Color('net', scale=alt.Scale(range=['#d8315b', '#eaeaec','#0a2463'], domainMid=0), legend=None),
            tooltip=[
                alt.Tooltip('station_name:N', title='Station'),
                alt.Tooltip('hour:O', title='Hour'),
                alt.Tooltip('net', title='# of Net Rides')
                ]
            )
    multi_station_map = multi_station_map.properties(height=500, width = 900).configure_axis(
    gridColor='#eaeaec').configure_axis(labelColor='#2B2D42', 
                                         tickColor='#2B2D42', domainColor='#2B2D42').configure_view(stroke=None)
    vega_lite_json = multi_station_map.to_json(format='vega')

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
                vegaEmbed('#altair-chart-container', spec, {{actions: false}});
            </script>
        </center>
        </body>
        </html>
    """
    return [chart_obj, mp_station, mp_time, "{:,}".format(mp_metric)]
    