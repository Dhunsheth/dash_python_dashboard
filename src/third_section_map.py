from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import folium
from itertools import islice


def get_third_section_map():
    metric_color = '#8e0050'
    return [
        
        dbc.Row([
            dbc.Col([
                        dbc.Row(html.H4("KPI Summary"), style={'text-align':'center', 'padding-top':'40px'}),
                        dbc.Row(html.H5("Top Station", style={'text-align':'center', 'font-weight': 'bold',
                                                                    'padding-top':'40px', 'color':'#2B2D42'})),
                        dbc.Row(
                                dbc.Col(html.Div(id='output-geo-top-station'), 
                                width=12, className="text-center"),
                                style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                                ),
                        dbc.Row(html.H5("Total Rides", style={'text-align':'center', 'font-weight': 'bold',
                                                                    'padding-top':'20px', 'color':'#2B2D42'})),
                        dbc.Row(
                                dbc.Col(html.Div(id='output-geo-top-total-rides'), 
                                width=12, className="text-center"),
                                style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                                ),
                        dbc.Row(html.H5("Bottom Station", style={'text-align':'center', 'font-weight': 'bold',
                                                                    'padding-top':'40px', 'color':'#2B2D42'})),
                        dbc.Row(
                                dbc.Col(html.Div(id='output-geo-bot-station'), 
                                width=12, className="text-center"),
                                style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                                ),
                        dbc.Row(html.H5("Total Rides", style={'text-align':'center', 'font-weight': 'bold',
                                                                    'padding-top':'20px', 'color':'#2B2D42'})),
                        dbc.Row(
                                dbc.Col(html.Div(id='output-geo-bot-total-rides'), 
                                width=12, className="text-center"),
                                style={'font-weight': 'bold', 'color': metric_color, 'font-size':'18px'}
                                )
                        ], width=3, style={"text-align": "center", 'height':'530px','backgroundColor': '#eaeaec'},
                    className='justify-content-center'),
        dbc.Col([
            dbc.Row(
                dbc.Col(
                    html.Div( 
                        dcc.Dropdown(
                            id="num-stations",
                            options=[{'label': str(i), 'value': i} for i in [5, 10, 20, 50, 100, 250]],
                            value=20,
                            multi=False,
                            style={'text-align':'center', 'width': '100%'}
                        ), 
                        style={'max-width': '30%', 'margin': '0 auto'}  
                    ),
                    width=12  
                ),
                justify="center", style={'padding-top':'10px'}
            ),
            dbc.Row(
                    [
                        html.Iframe(
                            id='map-iframe',
                            srcDoc='',
                            style={'width': '100%', 'height':'475px', 'padding-top':'10px'}
                        )
                    ]
                )
        ], width=9)
    ])
 ]

def get_map(num_stations, geo_station_map_df):
    
    filtered_df = geo_station_map_df.reset_index()

    filtered_map_df = filtered_df.sort_values(by='count', ascending=False)
    filtered_map_df.reset_index(inplace=True)
    
    top_station = filtered_map_df['station_name'].values[0]
    top_metric = filtered_map_df['count'].values[0]
    bot_station = filtered_map_df['station_name'].values[num_stations-1]
    bot_metric = filtered_map_df['count'].values[num_stations-1]
    
    points = [
        (row['lat'], row['lng'], row['station_name'], row['count']) 
        for index, row in islice(filtered_map_df.iterrows(), num_stations)
    ]
    
    map_chicago = folium.Map(location=[41.895076, -87.627627], zoom_start=12)
    
    icon_image_a = 'point_a.png'
    icon_image_b = 'point_b.png'
    
    for point in points[:num_stations]:
        tooltip_text = f"Rank: {filtered_map_df[filtered_map_df['station_name'] == point[2]].index[0] + 1} - {point[2]} - {point[3]}"  # Rank and station name
        
        if point[2] == top_station or point[2] == bot_station:
            icon = folium.features.CustomIcon(icon_image_a, icon_size=(80, 80))
        else:
            icon = folium.features.CustomIcon(icon_image_b, icon_size=(80, 80))
        
        folium.Marker(
            location=[point[0], point[1]],
            tooltip=tooltip_text,
            icon=icon  # Specify the icon color here
        ).add_to(map_chicago)
    
    map_html = map_chicago.get_root().render()
    
    return [map_html, top_station, "{:,}".format(top_metric), bot_station, "{:,}".format(bot_metric)]
    