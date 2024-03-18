from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import altair as alt
import calendar

def get_first_section():
    metric_color = '#8e0050'
    return [
    dbc.Row([
        dbc.Col([
                    dbc.Row(html.H4("KPI Summary"), style={'text-align':'center', 'padding-top':'40px'}),
                    dbc.Row(html.H5("Most Popular Hour", style={'text-align':'center', 'font-weight': 'bold',
                                                                'padding-top':'40px', 'color':'#2B2D42'})),
                    dbc.Row(
                        dbc.Col(html.Div(id='output-hour'), 
                        width=12, className="text-center"),
                        style={'font-weight': 'bold', 'color': metric_color, 'font-size':'22px'}
                        ),
                    dbc.Row(html.H6("Total Number of Rides"), style={'text-align':'center', 'font-style': 'italic', 'padding-top':'15px'}),
                    dbc.Row(
                            dbc.Col(html.Div(id='output-hour-count'), 
                            width=12, className="text-center"),
                            style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                            ),
                    dbc.Row(html.H6("Average Duration of Rides"), style={'text-align':'center', 'font-style': 'italic', 'padding-top':'15px'}),
                    dbc.Row(
                            dbc.Col(html.Div(id='output-hour-duration'), 
                            width=12, className="text-center"),
                            style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                            ),
                    dbc.Row(html.H5("Most Popular Day", style={'text-align':'center', 'font-weight': 'bold',
                                                                'padding-top':'40px', 'color':'#2B2D42'})),
                    dbc.Row(
                            dbc.Col(html.Div(id='output-day'), 
                            width=12, className="text-center"),
                            style={'font-weight': 'bold', 'color': metric_color, 'font-size':'22px'}
                            ),
                    dbc.Row(html.H6("Total Number of Rides"), style={'text-align':'center', 'font-style': 'italic', 'padding-top':'15px'}),
                    dbc.Row(
                            dbc.Col(html.Div(id='output-day-count'), 
                            width=12, className="text-center"),
                            style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                            ),
                    dbc.Row(html.H6("Average Duration of Rides"), style={'text-align':'center', 'font-style': 'italic', 'padding-top':'15px'}),
                    dbc.Row(
                            dbc.Col(html.Div(id='output-day-duration'), 
                            width=12, className="text-center"),
                            style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                            ),
                    dbc.Row(html.H5("Most Popular Month", style={'text-align':'center', 'font-weight': 'bold',
                                                                'padding-top':'40px', 'color':'#2B2D42'})),
                    dbc.Row(
                            dbc.Col(html.Div(id='output-month'), 
                            width=12, className="text-center"),
                            style={'font-weight': 'bold', 'color': metric_color, 'font-size':'22px'}
                            ),
                    dbc.Row(html.H6("Total Number of Rides"), style={'text-align':'center', 'font-style': 'italic', 'padding-top':'15px'}),
                    dbc.Row(
                            dbc.Col(html.Div(id='output-month-count'), 
                            width=12, className="text-center"),
                            style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                            ),
                    dbc.Row(html.H6("Average Duration of Rides"), style={'text-align':'center', 'font-style': 'italic', 'padding-top':'15px'}),
                    dbc.Row(
                            dbc.Col(html.Div(id='output-month-duration'), 
                            width=12, className="text-center"),
                            style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                            )
                    ], width=3, style={"text-align": "center", 'height':'1250px','backgroundColor': '#eaeaec'},
                className='justify-content-center'),
    dbc.Col([
                dbc.Row(
                    [
                        dbc.Col(
                            html.H4("Trend Graph Filters:"),
                            align='center',
                            style={"text-align": "right", 'padding-right':'20px'},
                            width=5),
                        dbc.Col([
                            dbc.Row(
                                dcc.Checklist(
                                    id='rider-trend-box',
                                    options=[
                                        {'label': "Classic Bike", 'value': 'Classic Bike'},
                                        {'label': "Docked Bike", 'value': 'Docked Bike'},
                                        {'label': "Electric Bike", 'value': 'Electric Bike'}
                                    ],
                                    value=['Classic Bike', 'Docked Bike', 'Electric Bike'],
                                    labelStyle={'display': 'inline-block', 'margin-right': '20px', 'margin-left': '20px'},
                                    inputClassName="form-check-input",
                                    labelClassName="form-check-label",
                                    className="form-check",
                                    style={'text-align': 'center'}
                                ), style={'padding-bottom':'10px'}
                                ),
                            dbc.Row(
                                dcc.RadioItems(
                                    id='rider-trend-radio',
                                    options=[
                                        {'label': "Number of Rides Started", 'value': 'count'},
                                        {'label': "Average Duration", 'value': 'mean'}
                                    ],
                                    value='count',
                                    labelStyle={'display': 'inline-block', 'margin-left': '20px', 'margin-right': '20px'},
                                    inputClassName="form-check-input",
                                    labelClassName="form-check-label",
                                    className="form-check",
                                    style={'text-align': 'center', 'margin': 'auto', 'width': 'fit-content'}
                                )
                                )
                            ], width=5)
                    ], style={'padding-top':'20px', 'padding-bottom':'10px'}
                ),
                dbc.Row([
                    dbc.Col([
                    html.H6("Hour of Day", style={'text-align': 'center', 'margin-bottom':'0px'}),
                    html.Iframe(
                        id='rider-trend-hour',
                        srcDoc='',
                        style={'width': '100%', 'height':'540px', 'margin': 'auto'}
                    )],width=12)
                    ], style={'padding-top':'10px'}),
                dbc.Row([
                    dbc.Col([
                        html.H6("Day of Week", style={'text-align': 'center', 'margin-bottom':'0px'}),
                        html.Iframe(
                            id='rider-trend-day',
                            srcDoc='',
                            style={'width': '100%', 'height':'540px', 'margin': 'auto'}
                        )
                        ]),
                    dbc.Col([
                        html.H6("Month of Year", style={'text-align': 'center', 'margin-bottom':'0px'}),
                        html.Iframe(
                            id='rider-trend-month',
                            srcDoc='',
                            style={'width': '100%', 'height':'540px', 'margin': 'auto'}
                        )
                        ])
                    ], style={'padding-top':'10px'})
                ], width=9)
    ])
        ]

alt.data_transformers.enable('vegafusion')
# classic, docked, electric
color = ['#2B2D42', '#626797', '#5D2E46']
def plot_rider_trend_hour(df, func, cat):
    """
    This function creates the hourly rider trend graph and hourly KPI's. 
    
    Args:
        df: data frame for hourly data
        func (str): Value of radio filter to select either "count" or "mean".
        cat (str): Value from check-boxes to select bike type to plot. 
    
    Returns:
        chart_obj: chart object
        top_hour: hour with the highest count or mean
        total_rides_hour: total number of rides on hourly graph
        total_avg_hour: average number of rides on hourly graph
    """
    
    filtered_df = df.loc[(slice(None), cat), :]
    hour = filtered_df.groupby(['hour']).agg({'count':'sum','ride_duration':'mean'}) 
    filtered_df = filtered_df.reset_index()

    if func == "mean":
        top_hour = hour['ride_duration'].argmax()
        total_rides_hour = "{:,}".format(hour.loc[top_hour,'count'])
        total_avg_hour = round(hour.loc[top_hour,'ride_duration'],2)
        
        by_hour = alt.Chart(filtered_df).mark_line(point=True).encode(
        x=alt.X('hour:O', title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y('ride_duration:Q', axis=alt.Axis(ticks=False), title=None),
        color=alt.Color('rideable_type:N', title=None, scale=alt.Scale(
            domain=['Classic Bike', 'Docked Bike', 'Electric Bike'],
                            range=color)
            ),
        tooltip=[
            alt.Tooltip('hour:O', title='Time'),
            alt.Tooltip('rideable_type:N', title='Ride Type'),
            alt.Tooltip('ride_duration:Q', title='Average Ride Duration', format='.2f')
        ]
        ).properties(height=480, width=800)

    else:
        top_hour = hour['count'].argmax()
        total_rides_hour = "{:,}".format(hour.loc[top_hour,'count'])
        total_avg_hour = round(hour.loc[top_hour,'ride_duration'],2)
        
        by_hour = alt.Chart(filtered_df).mark_bar().encode(
            x=alt.X('hour:O', title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y('count:Q', axis=alt.Axis(ticks=False), title=None),
            color=alt.Color('rideable_type:N', title=None, scale=alt.Scale(
                domain=['Classic Bike', 'Docked Bike', 'Electric Bike'],
                                range=color)
                ),
            tooltip=[
                alt.Tooltip('hour:O', title='Time'),
                alt.Tooltip('rideable_type:N', title='Ride Type'),
                alt.Tooltip('count:Q', title="Number of Rides", format=',')
            ]
        ).properties(height=480, width=950)
        
    chart_1 = (by_hour).configure_axis(
    gridColor='#eaeaec').configure_axis(labelColor='#2B2D42', 
                                         tickColor='#2B2D42', domainColor='#2B2D42').configure_view(stroke=None)
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
                vegaEmbed('#altair-chart-container', spec, {{actions: false}});
            </script>
        </center>
        </body>
        </html>
    """
    return [chart_obj, top_hour, total_rides_hour, total_avg_hour]

def plot_rider_trend_day(df, func, cat):
    """
    This function creates the daily rider trend graph and KPI's. 
    
    Args:
        df: data frame for daily data
        func (str): Value of radio filter to select either "count" or "mean".
        cat (str): Value from check-boxes to select bike type to plot. 
    
    Returns:
        chart_obj: chart object
        top_day: day with the highest count or mean
        total_rides_day: total number of rides on daily graph
        total_avg_day: average number of rides on daily graph
    """

    filtered_df = df.loc[(slice(None), cat), :]
    day = filtered_df.groupby(['day']).agg({'count':'sum','ride_duration':'mean'}) 
    filtered_df = filtered_df.reset_index()

    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    if func == "mean":
        top_day = day.index[day['ride_duration'].argmax()]
        total_rides_day = "{:,}".format(day.loc[top_day,'count'])
        total_avg_day = round(day.loc[top_day,'ride_duration'],2)
        
        by_day = alt.Chart(filtered_df).mark_line(point=True).encode(
        x=alt.X('day:O', title=None, axis=alt.Axis(labelAngle=0), sort=days_order),
        y=alt.Y('ride_duration:Q', axis=alt.Axis(ticks=False), title=None),
        color=alt.Color('rideable_type:N', legend=None, title=None, scale=alt.Scale(
            domain=['Classic Bike', 'Docked Bike', 'Electric Bike'],
                            range=color)
            ),
        tooltip=[
            alt.Tooltip('day:O', title='Day'),
            alt.Tooltip('rideable_type:N', title='Ride Type'),
            alt.Tooltip('ride_duration:Q', title='Average Ride Duration', format='.2f')
        ]
        ).properties(height=480, width=400)
    else:
        top_day = day.index[day['count'].argmax()]
        total_rides_day = "{:,}".format(day.loc[top_day,'count'])
        total_avg_day = round(day.loc[top_day,'ride_duration'],2)
        
        by_day = alt.Chart(filtered_df).mark_bar().encode(
            x=alt.X('day:O', title=None, axis=alt.Axis(labelAngle=0), sort=days_order),
            y=alt.Y('count:Q', axis=alt.Axis(ticks=False), title=None),
            color=alt.Color('rideable_type:N', legend=None, title=None, scale=alt.Scale(
                domain=['Classic Bike', 'Docked Bike', 'Electric Bike'],
                                range=color)
                ),
            tooltip=[
                alt.Tooltip('day:O', title='Day'),
                alt.Tooltip('rideable_type:N', title='Ride Type'),
                alt.Tooltip('count:Q', title="Number of Rides", format=',')
            ]
        ).properties(height=480, width=400)
        
        
    chart_1 = (by_day).configure_axis(
    gridColor='#eaeaec').configure_axis(labelColor='#2B2D42', 
                                         tickColor='#2B2D42', domainColor='#2B2D42').configure_view(stroke=None)
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
                vegaEmbed('#altair-chart-container', spec, {{actions: false}});
            </script>
        </center>
        </body>
        </html>
    """
    return [chart_obj, top_day, total_rides_day, total_avg_day]

def plot_rider_trend_month(df, func, cat):
    """
    This function creates the monthly rider trend graph and KPI's. 
    
    Args:
        df: data frame for monthly data
        func (str): Value of radio filter to select either "count" or "mean".
        cat (str): Value from check-boxes to select bike type to plot. 
    
    Returns:
        chart_obj: chart object
        top_month: month with the highest count or mean
        total_rides_month: total number of rides on monthly graph
        total_avg_month: average number of rides on monthly graph
    """
    
    filtered_df = df.loc[(slice(None), cat), :]
    month = filtered_df.groupby(['month']).agg({'count':'sum','ride_duration':'mean'}) 
    filtered_df = filtered_df.reset_index()

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_abbr_to_full = {month: calendar.month_name[i] for i, month in enumerate(calendar.month_abbr) if month}

    if func == "mean":
        top_month = month.index[month['ride_duration'].argmax()]
        total_rides_month = "{:,}".format(month.loc[top_month,'count'])
        total_avg_month = round(month.loc[top_month,'ride_duration'],2)
        top_month = month_abbr_to_full[top_month]
        
        by_month = alt.Chart(filtered_df).mark_line(point=True).encode(
        x=alt.X('month:O', title=None, axis=alt.Axis(labelAngle=0), sort=month_order),
        y=alt.Y('ride_duration:Q', axis=alt.Axis(ticks=False), title=None),
        color=alt.Color('rideable_type:N', legend=None, title=None, scale=alt.Scale(
            domain=['Classic Bike', 'Docked Bike', 'Electric Bike'],
                            range=color)
            ),
        tooltip=[
            alt.Tooltip('month:O', title='Month'),
            alt.Tooltip('rideable_type:N', title='Ride Type'),
            alt.Tooltip('ride_duration:Q', title='Average Ride Duration', format='.2f')
        ]
        ).properties(height=480, width=400)
    else:
        top_month = month.index[month['count'].argmax()]
        total_rides_month = "{:,}".format(month.loc[top_month,'count'])
        total_avg_month = round(month.loc[top_month,'ride_duration'],2)
        top_month = month_abbr_to_full[top_month]
        
        by_month = alt.Chart(filtered_df).mark_bar().encode(
            x=alt.X('month:O', title=None, axis=alt.Axis(labelAngle=0), sort=month_order),
            y=alt.Y('count:Q', axis=alt.Axis(ticks=False), title=None),
            color=alt.Color('rideable_type:N', legend=None, title=None, scale=alt.Scale(
                domain=['Classic Bike', 'Docked Bike', 'Electric Bike'],
                                range=color)
                ),
            tooltip=[
                alt.Tooltip('month:O', title='Month'),
                alt.Tooltip('rideable_type:N', title='Ride Type'),
                alt.Tooltip('count:Q', title="Number of Rides", format=',')
            ]
        ).properties(height=480, width=400)
        
        
    chart_1 = (by_month).configure_axis(
    gridColor='#eaeaec').configure_axis(labelColor='#2B2D42', 
                                         tickColor='#2B2D42', domainColor='#2B2D42').configure_view(stroke=None)
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
                vegaEmbed('#altair-chart-container', spec, {{actions: false}});
            </script>
        </center>
        </body>
        </html>
    """
    return [chart_obj, top_month, total_rides_month, total_avg_month]