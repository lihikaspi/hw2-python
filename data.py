import pandas as pd
from datetime import datetime


def load_data(path):
    """reads and returns the pandas DataFrame"""
    return pd.read_csv(path)


def add_new_columns(df):
    """adds columns to df and returns the new df"""
    new_df = df
    new_df['season_name'] = df['season'].apply(convert_to_season)
    new_df['hour'] = df['timestamp'].apply(find_hour)
    new_df['day'] = df['timestamp'].apply(find_day)
    new_df['month'] = df['timestamp'].apply(find_month)
    new_df['year'] = df['timestamp'].apply(find_year)
    new_df['is_weekend_holiday'] = df['is_holiday', 'is_weekend'].apply(is_weekend_holiday)
    new_df['t_diff'] = df['t1', 't2'].apply(lambda t1, t2: t2 - t1)
    return new_df


def data_analysis(df):
    """prints statistics on the transformed df"""
    print("describe output:")
    print(df.describe().to_string())
    print()
    print("corr output:")
    corr = df.corr()
    print(corr.to_string())
    print()

    corr_dict = to_dict(df)
    print("Highest correlated are:")

    print()
    print("Lowest correlated are:")


def to_dict(df):
    corr_dict = {}
    for feat1 in df.keys():
        for feat2 in df.keys():
            corr_dict[(feat1, feat2)] = df[feat1].corr(df[feat2])
    return corr_dict


def sort_corr_dict(corr_dict):


def convert_to_season(season_num):
    seasons = ["spring", "summer", "fall", "winter"]
    return seasons[season_num]


def find_time_of_day(timestamp):
    if "AM" in timestamp:
        return 121
    if "PM" in timestamp:
        return 122
    return 24


def get_time(timestamp):
    time_of_day = find_time_of_day(timestamp)
    if time_of_day == 24:
        return datetime.strptime(timestamp, '%d/%m/%y  %H:%M:%S.%f')

    if time_of_day == 121 or time_of_day == 122:
        return datetime.strptime(timestamp, '%d/%m/%y  %I:%M:%S.%f %p')


def find_hour(timestamp):
    time = get_time(timestamp)
    time_of_day = find_time_of_day(timestamp)
    if int(time_of_day/10) == 12 and time_of_day % 10 == 2:
            return time.hour+12
    else:
        return time.hour


def find_day(timestamp):
    time = get_time(timestamp)
    return time.day


def find_month(timestamp):
    time = get_time(timestamp)
    return time.month


def find_year(timestamp):
    time = get_time(timestamp)
    return time.year


def is_weekend_holiday(holiday, weekend):
    if holiday == 0 and weekend == 0:
        return 0
    if holiday == 0 and weekend == 1:
        return 1
    if holiday == 1 and weekend == 0:
        return 2
    if holiday == 1 and weekend == 1:
        return 3
