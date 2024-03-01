import pandas as pd
import numpy as np
import glob
import zipfile
import shutil
from haversine import haversine, Unit
from datetime import datetime
import os
from itertools import islice

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
geo_df = data
geo_df['start_lng'] = data.groupby('start_station_name')['start_lng'].transform('mean')
geo_df['start_lat'] = data.groupby('start_station_name')['start_lat'].transform('mean')
geo_df['end_lng'] = data.groupby('end_station_name')['end_lng'].transform('mean')
geo_df['end_lat'] = data.groupby('end_station_name')['end_lat'].transform('mean')

start_counts = geo_df.groupby([pd.Grouper(key='started_at', freq='D'), pd.Grouper(key='started_at', freq='H'), 'start_station_name', 'start_lng','start_lat']).agg({'started_at': 'count'})
start_counts.rename(columns={'started_at': 'start_count'}, inplace=True)
start_counts.index = start_counts.index.set_names('day', level=0)
start_counts.index = start_counts.index.set_names('time', level=1)
start_counts.index = start_counts.index.set_names('station_name', level=2)
start_counts.index = start_counts.index.set_names('lng', level=3)
start_counts.index = start_counts.index.set_names('lat', level=4)

end_counts = geo_df.groupby([pd.Grouper(key='ended_at', freq='D'), pd.Grouper(key='ended_at', freq='H'), 'end_station_name', 'end_lng','end_lat']).agg({'ended_at': 'count'})
end_counts.rename(columns={'ended_at': 'end_count'}, inplace=True)
end_counts.index = end_counts.index.set_names('day', level=0)
end_counts.index = end_counts.index.set_names('time', level=1)
end_counts.index = end_counts.index.set_names('station_name', level=2)
end_counts.index = end_counts.index.set_names('lng', level=3)
end_counts.index = end_counts.index.set_names('lat', level=4)

station_map_counts = pd.merge(start_counts, end_counts, left_on=start_counts.index, right_on=end_counts.index, how='outer')

station_map_counts[['day', 'time', 'station_name', 'lng', 'lat']] = pd.DataFrame(station_map_counts['key_0'].tolist(), index=station_map_counts.index)
station_map_counts.drop(columns=['key_0'], inplace=True)
station_map_counts = station_map_counts.set_index(['day', 'time', 'station_name'])
station_map_counts = station_map_counts.fillna(0)

station_map_counts['start_count'] = station_map_counts['start_count'].astype(int)
station_map_counts['end_count'] = station_map_counts['end_count'].astype(int)

station_map_counts['count'] = station_map_counts['start_count'] + station_map_counts['end_count']
station_map_counts.sort_index(inplace=True)
station_map_counts.to_parquet('../data/processed/geo_station_map_df.parquet')


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