from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import altair as alt
import pandas as pd
import vegafusion

def get_first_section(start_date_min, end_date_max):
    return [
        html.H1("Bike Sharing Analysis", className="text-primary", style={'text-align': 'center', 'padding-top': '20px'}),
            dbc.Row(
                [
                    dbc.Col(
                        [ 
                            html.Div(
                                [
                                    dcc.DatePickerRange(
                                        id='date-picker-range',
                                        start_date=start_date_min,
                                        end_date=end_date_max,
                                        display_format='YYYY-MM-DD',
                                        className="mt-3",
                                        min_date_allowed=start_date_min, 
                                        max_date_allowed=end_date_max
                                    )
                                ], style = {'padding-bottom': '15px'}
                            )
                        ],
                        style={'display': 'flex', 'flexDirection': 'column',  'alignItems': 'center', 'border': '1px solid black'}
                    )
                ]
            ),
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
                                                    html.Th(scope='row', className='table-dark', children="Rider Trends"),
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
                    html.Iframe(
                        id='rider-trend-bar',
                        srcDoc='',
                        style={'width': '100%', 'height':'540px', 'margin': 'auto', 'border': '1px solid black'}
                    )
            ),
            dbc.Row(
                dbc.Col(
                        [
                            dcc.Checklist(
                                id='rider-trend-box',
                                options=[
                                    {'label': "Classic Bike", 'value': 'classic_bike'},
                                    {'label': "Docked Bike", 'value': 'docked_bike'},
                                    {'label': "Electric Bike", 'value': 'electric_bike'}
                                ],
                                value=['classic_bike', 'docked_bike', 'electric_bike'],
                                labelStyle={'display': 'inline-block', 'margin-right': '20px', 'margin-left': '20px'},
                                inputClassName="form-check-input",
                                labelClassName="form-check-label",
                                className="form-check",
                                style={'border': '1px solid black', 'text-align': 'center'}
                            )
                        ], 
                        width=4, 
                        style={'margin': 'auto'}
                    )
                ),
            dbc.Row(
                [
                    dcc.RadioItems(
                        id='rider-trend-radio',
                        options=[
                            {'label': "Number of Rides", 'value': 'count'},
                            {'label': "Average Duration", 'value': 'mean'}
                        ],
                        value='count',
                        labelStyle={'display': 'inline-block', 'margin-left': '20px', 'margin-right': '20px'},
                        inputClassName="form-check-input",
                        labelClassName="form-check-label",
                        className="form-check",
                        style={'text-align': 'center', 'margin': 'auto', 'width': 'fit-content', 'border': '1px solid black'}
                    )
                ], 
                style={'text-align': 'center'}
            )
        ]

alt.data_transformers.enable('vegafusion')
def plot_rider_trend(df, func, cat, start_date, end_date):
    
    filtered_df = df.loc[(slice(start_date, end_date), slice(None), slice(None)), :]
    filtered_df = filtered_df.reset_index()
    filtered_df.drop(columns=['day'], inplace=True)

    if func == "mean":
        by_hour = alt.Chart(filtered_df).mark_line(point=True).encode(
        x=alt.X('hours(time):O', title=None),
        y=alt.Y('mean(ride_duration):Q', axis=alt.Axis(ticks=False), title=None),
        color=alt.Color('rideable_type:N', title=None, scale=alt.Scale(scheme='viridis')),
        tooltip=[
            alt.Tooltip('rideable_type:N', title='Ride Type'),
            alt.Tooltip('mean(ride_duration):Q', title='Average Ride Duration')
        ]
        ).transform_filter(alt.FieldOneOfPredicate(field='rideable_type', oneOf=cat)).properties(height=480, width=500)
    
        by_day = alt.Chart(filtered_df).mark_line(point=True).encode(
            x=alt.X('day(time):O', title=None),
            y=alt.Y('mean(ride_duration):Q', axis=alt.Axis(ticks=False), title=None),
            color=alt.Color('rideable_type:N', scale=alt.Scale(scheme='viridis')),
            tooltip=[
                alt.Tooltip('rideable_type:N', title='Ride Type'),
                alt.Tooltip('mean(ride_duration):Q', title='Average Ride Duration')
            ]
        ).transform_filter(alt.FieldOneOfPredicate(field='rideable_type', oneOf=cat)).properties(height=480, width=200)
        
        by_month = alt.Chart(filtered_df).mark_line(point=True).encode(
            x=alt.X('month(time):O', title=None),
            y=alt.Y('mean(ride_duration):Q', axis=alt.Axis(ticks=False), title=None),
            color=alt.Color('rideable_type:N', scale=alt.Scale(scheme='viridis')),
            tooltip=[
                alt.Tooltip('rideable_type:N', title='Ride Type'),
                alt.Tooltip('mean(ride_duration):Q', title='Average Ride Duration')
            ]
        ).transform_filter(alt.FieldOneOfPredicate(field='rideable_type', oneOf=cat)).properties(height=480, width=200)
    else:
        by_hour = alt.Chart(filtered_df).mark_bar().encode(
            x=alt.X('hours(time):O', title=None),
            y=alt.Y('sum(count):Q', axis=alt.Axis(ticks=False), title=None),
            color=alt.Color('rideable_type:N', title=None, scale=alt.Scale(scheme='viridis')),
            tooltip=[
                alt.Tooltip('rideable_type:N', title='Ride Type'),
                alt.Tooltip('sum(count):Q', title="Number of Rides")
            ]
        ).transform_filter(alt.FieldOneOfPredicate(field='rideable_type', oneOf=cat)).properties(height=480, width=500)
        
        by_day = alt.Chart(filtered_df).mark_bar().encode(
            x=alt.X('day(time):O', title=None),
            y=alt.Y('sum(count):Q', axis=alt.Axis(ticks=False), title=None),
            color=alt.Color('rideable_type:N', scale=alt.Scale(scheme='viridis')),
            tooltip=[
                alt.Tooltip('rideable_type:N', title='Ride Type'),
                alt.Tooltip('sum(count):Q', title="Number of Rides")
            ]
        ).transform_filter(alt.FieldOneOfPredicate(field='rideable_type', oneOf=cat)).properties(height=480, width=200)
        
        by_month = alt.Chart(filtered_df).mark_bar().encode(
            x=alt.X('month(time):O', title=None),
            y=alt.Y('sum(count):Q', axis=alt.Axis(ticks=False), title=None),
            color=alt.Color('rideable_type:N', title=None, scale=alt.Scale(scheme='viridis')),
            tooltip=[
                alt.Tooltip('rideable_type:N', title='Ride Type'),
                alt.Tooltip('sum(count):Q', title="Number of Rides")
            ]
        ).transform_filter(alt.FieldOneOfPredicate(field='rideable_type', oneOf=cat)).properties(height=480, width=200)
        
    chart_1 = alt.concat(by_hour | by_day | by_month, spacing=50).configure_view(stroke=None)
    vega_lite_json = chart_1.to_json(format='vega')

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