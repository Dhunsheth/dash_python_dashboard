import pandas as pd
import numpy as np
import glob
import zipfile
import shutil
from haversine import haversine, Unit
from datetime import datetime
import os

## Reading all ZIP files and compiling main data frame
def calculate_distance(row):
    start_coords = (row['start_lat'], row['start_lng'])
    end_coords = (row['end_lat'], row['end_lng'])
    return round(haversine(start_coords, end_coords, unit=Unit.KILOMETERS)*1000,2)

zip_path = '../data/raw/*.zip'
files = glob.glob(zip_path)
for zip_file in files:
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        temp_dir = 'temp_extracted'
        zip_ref.extractall(temp_dir)
path = os.path.join(temp_dir, '*.csv')
csv_files = glob.glob(path)
data = pd.DataFrame()
for file in csv_files:
    df = pd.read_csv(file, parse_dates=['started_at','ended_at'])
    df.head()
    data = pd.concat([data, df], ignore_index=True)
shutil.rmtree(temp_dir, ignore_errors=True)

data.dropna(subset=['end_lat', 'end_lng'], inplace=True)
data['ride_duration'] = round((data['ended_at'] - data['started_at']).dt.total_seconds()/60, 2) # in minutes
data['ride_distance'] = data.apply(calculate_distance, axis=1) # in meters
data.drop(data[data['ride_duration'] < 0].index, inplace=True)

# Write to Parquet
data.to_parquet('../data/processed/data.parquet', index=False)

## Data frame for Geo-Map of bike station locations
# start_stations = data['start_station_name'].dropna().unique()
# end_stations = data['end_station_name'].dropna().unique()
# unique_stations = np.concatenate((start_stations, end_stations))
# unique_stations = np.unique(unique_stations)
# number_of_stations = len(unique_stations) # Number of bike stations we want to show.


map_stations_df = data['start_station_name'].value_counts()
map_stations_df = map_stations_df.reset_index()
map_stations_df.columns = ['station_name', 'start_count']
map_stations_df = map_stations_df.merge(data, left_on='station_name', right_on='start_station_name', how='left')
map_stations_df.drop(['ride_id', 'rideable_type', 'started_at',
       'ended_at', 'start_station_name', 'start_station_id',
       'end_station_name', 'end_station_id', 'end_lat', 'end_lng', 'member_casual', 'ride_duration',
       'ride_distance'], axis=1, inplace=True)
map_stations_df.drop_duplicates(subset=['station_name'], keep='first', inplace=True)

end_stations_df = data['end_station_name'].value_counts()
end_stations_df = end_stations_df.reset_index()
end_stations_df.columns = ['station_name', 'end_count']
end_stations_df = end_stations_df.merge(data, left_on='station_name', right_on='end_station_name', how='left')
end_stations_df.drop(['ride_id', 'rideable_type', 'started_at',
       'ended_at', 'start_station_name', 'start_station_id',
       'end_station_name', 'end_station_id', 'start_lat', 'start_lng', 'member_casual', 'ride_duration',
       'ride_distance'], axis=1, inplace=True)
end_stations_df.drop_duplicates(subset=['station_name'], keep='first', inplace=True)

map_stations_df = map_stations_df.merge(end_stations_df, how='outer').fillna(0)

map_stations_df.drop(columns=['end_lat', 'end_lng'], inplace=True)
map_stations_df.rename(columns={'start_lng': 'lng', 'start_lat':'lat'}, inplace=True)
map_stations_df['count'] = map_stations_df['start_count'] + map_stations_df['end_count']


map_stations_df.to_parquet('../data/processed/geo_map_stations.parquet', index=False)

## Data frame for rider trend graphs
rider_trend = data.groupby([pd.Grouper(key='started_at', freq='D'), pd.Grouper(key='started_at', freq='H'), 'rideable_type']).agg({'started_at': 'count', 'ride_duration':'mean'})
rider_trend.rename(columns={'started_at': 'count'}, inplace=True)
rider_trend.index = rider_trend.index.set_names('day', level=0)
rider_trend.index = rider_trend.index.set_names('time', level=1)
rider_trend.to_parquet('../data/processed/rider_trend_df.parquet')


## Data frame for heatmap
heat_map_start = data.groupby([pd.Grouper(key='started_at', freq='D'), pd.Grouper(key='started_at', freq='H'), 'start_station_name']).agg({'started_at': 'count'})
heat_map_start.rename(columns={'started_at': 'start_count'}, inplace=True)
heat_map_start.index = heat_map_start.index.set_names('day', level=0)
heat_map_start.index = heat_map_start.index.set_names('time', level=1)
heat_map_start.index = heat_map_start.index.set_names('station_name', level=2)

heat_map_end = data.groupby([pd.Grouper(key='ended_at', freq='D'), pd.Grouper(key='ended_at', freq='H'), 'end_station_name']).agg({'ended_at': 'count'})
heat_map_end.rename(columns={'ended_at': 'end_count'}, inplace=True)
heat_map_end.index = heat_map_end.index.set_names('day', level=0)
heat_map_end.index = heat_map_end.index.set_names('time', level=1)
heat_map_end.index = heat_map_end.index.set_names('station_name', level=2)

heat_map = pd.merge(heat_map_start, heat_map_end, left_on=heat_map_start.index, right_on=heat_map_end.index, how='outer')

heat_map[['day', 'time', 'station_name']] = pd.DataFrame(heat_map['key_0'].tolist(), index=heat_map.index)
heat_map.drop(columns=['key_0'], inplace=True)
heat_map = heat_map.set_index(['day', 'time', 'station_name'])
heat_map = heat_map.fillna(0)
heat_map['start_count'] = heat_map['start_count'].astype(int)
heat_map['end_count'] = heat_map['end_count'].astype(int)
heat_map['net'] = heat_map['end_count'] - heat_map['start_count']
heat_map.sort_index(inplace=True)
heat_map.to_parquet('../data/processed/heat_map_df.parquet')