import pandas as pd
import glob
import zipfile
import shutil
from haversine import haversine, Unit
import os

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


## Data frame for rider trend graphs
type_mapping = {'classic_bike': 'Classic Bike', 'docked_bike': 'Docked Bike', 'electric_bike': 'Electric Bike'}

rider_trend_hour = data.groupby([data['started_at'].dt.hour, 'rideable_type']).agg({'started_at': 'count', 'ride_duration':'mean'})
rider_trend_hour.rename(columns={'started_at':'count'}, inplace=True)
rider_trend_hour.index = rider_trend_hour.index.set_names('hour', level=0)
rider_trend_hour.index = rider_trend_hour.index.set_levels([rider_trend_hour.index.levels[0],
                                                            rider_trend_hour.index.levels[1].map(type_mapping)])
rider_trend_hour.to_parquet('../data/processed/rider_trend_hour.parquet')

rider_trend_day = data.groupby([data['started_at'].dt.day_name(), 'rideable_type']).agg({'started_at': 'count', 'ride_duration':'mean'})
rider_trend_day.rename(columns={'started_at':'count'}, inplace=True)
rider_trend_day.index = rider_trend_day.index.set_names('day', level=0)
rider_trend_day.index = rider_trend_day.index.set_levels([rider_trend_day.index.levels[0],
                                                            rider_trend_day.index.levels[1].map(type_mapping)])
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
rider_trend_day = rider_trend_day.reindex(days_order, level=0)
rider_trend_day.to_parquet('../data/processed/rider_trend_day.parquet')

month_abbreviations = {
    'January': 'Jan',
    'February': 'Feb',
    'March': 'Mar',
    'April': 'Apr',
    'May': 'May',
    'June': 'Jun',
    'July': 'Jul',
    'August': 'Aug',
    'September': 'Sep',
    'October': 'Oct',
    'November': 'Nov',
    'December': 'Dec'
}
custom_month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
rider_trend_month = data.groupby([data['started_at'].dt.month_name(), 'rideable_type']).agg({'started_at': 'count', 'ride_duration':'mean'})
rider_trend_month.rename(columns={'started_at':'count'}, inplace=True)
rider_trend_month.index = rider_trend_month.index.set_names('month', level=0)
rider_trend_month.index = rider_trend_month.index.set_levels([rider_trend_month.index.levels[0].map(month_abbreviations),
                                                            rider_trend_month.index.levels[1].map(type_mapping)])
rider_trend_month = rider_trend_month.reindex(custom_month_order, level=0)
rider_trend_month.to_parquet('../data/processed/rider_trend_month.parquet')

# Data frame for Geo-Map of bike station locations
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
station_map_counts.reset_index(inplace=True)
station_map_counts.drop(columns=['day', 'time'], inplace=True)
station_map_counts = station_map_counts.groupby(['station_name']).agg({'start_count':'sum','end_count':'sum', 'lng':'mean', 'lat':'mean'})
station_map_counts = station_map_counts.fillna(0)

station_map_counts['start_count'] = station_map_counts['start_count'].astype(int)
station_map_counts['end_count'] = station_map_counts['end_count'].astype(int)

station_map_counts['count'] = station_map_counts['start_count'] + station_map_counts['end_count']
station_map_counts.sort_index(inplace=True)
station_map_counts.to_parquet('../data/processed/geo_station_map_df.parquet')

## Data frame for heatmap
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

start_station_comparison = data.groupby([data['started_at'].dt.day_name(), data['started_at'].dt.hour, 'start_station_name']).agg({'started_at': 'count'})
start_station_comparison.rename(columns={'started_at':'start_count'}, inplace=True)
start_station_comparison.index = start_station_comparison.index.set_names('day', level=0)
start_station_comparison.index = start_station_comparison.index.set_names('hour', level=1)
start_station_comparison = start_station_comparison.reindex(days_order, level=0)
start_station_comparison.index = start_station_comparison.index.set_names('station_name', level=2)

end_station_comparison = data.groupby([data['ended_at'].dt.day_name(), data['ended_at'].dt.hour, 'end_station_name']).agg({'ended_at': 'count'})
end_station_comparison.rename(columns={'ended_at':'end_count'}, inplace=True)
end_station_comparison.index = end_station_comparison.index.set_names('day', level=0)
end_station_comparison.index = end_station_comparison.index.set_names('hour', level=1)
end_station_comparison = end_station_comparison.reindex(days_order, level=0)
end_station_comparison.index = end_station_comparison.index.set_names('station_name', level=2)

station_comparison = pd.merge(start_station_comparison, end_station_comparison, left_on=start_station_comparison.index, right_on=end_station_comparison.index, how='outer')
station_comparison[['day', 'hour', 'station_name']] = pd.DataFrame(station_comparison['key_0'].tolist(), index=station_comparison.index)
station_comparison.drop(columns=['key_0'], inplace=True)
station_comparison = station_comparison.set_index(['day', 'hour', 'station_name'])
station_comparison = station_comparison.fillna(0)
station_comparison['start_count'] = station_comparison['start_count'].astype(int)
station_comparison['end_count'] = station_comparison['end_count'].astype(int)
station_comparison['net'] = station_comparison['end_count'] - station_comparison['start_count']
station_comparison['total'] = station_comparison['end_count'] + station_comparison['start_count']
station_comparison.to_parquet('../data/processed/station_comparison.parquet')

stations = station_comparison.reset_index().groupby(['station_name']).agg({'total':'sum'}).reset_index().sort_values(by='total', ascending=False)
stations.to_parquet('../data/processed/station_list.parquet')