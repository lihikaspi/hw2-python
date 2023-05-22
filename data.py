import pandas as pd
from datetime import datetime


def load_data(path):
    """
    reads and returns the pandas DataFrame
    :param path:
    :return:
    """
    return pd.read_csv(path)


def add_new_columns(df):
    """
    adds columns to df and returns the new d
    :param df:
    :return:
    """
    df['season_name'] = df['season'].apply(convert_to_season)
    df['hour'] = df['timestamp'].apply(find_hour)
    df['day'] = df['timestamp'].apply(find_day)
    df['month'] = df['timestamp'].apply(find_month)
    df['year'] = df['timestamp'].apply(find_year)


def convert_to_season(season_num):
    seasons = ["spring", "summer", "fall", "winter"]
    return seasons[season_num]


def find_time_of_day(timestamp):
    if "AM" in timestamp:
        return 121
    elif "PM" in timestamp:
        return 122
    return 24


def get_time(timestamp):
    time_of_day = find_time_of_day(timestamp)
    if time_of_day == 24:
        return datetime.strptime(timestamp, '%d/%m/%y  %H:%M:%S.%f')

    elif time_of_day == 121:
        return datetime.strptime(timestamp, '%d/%m/%y  %I:%M:%S.%f %p')

    elif time_of_day == 122:
        return datetime.strptime(timestamp, '%d/%m/%y  %I:%M:%S.%f %p')


def find_hour(timestamp):
    time = get_time(timestamp)
    time_of_day = find_time_of_day(timestamp)
    if int(time_of_day/10) == 12:
        if time_of_day % 10 == 2:
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
