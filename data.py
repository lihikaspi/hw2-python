import numpy as np
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
    new_df['is_weekend_holiday'] = df.apply(lambda feat: is_weekend_holiday(feat.is_holiday, feat.is_weekend), axis = 1)
    new_df['t_diff'] = df.apply(lambda t: t.t2 - t.t1, axis = 1)
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

    corr_dict = sort_corr_dict(corr)
    print("Highest correlated are:")
    for i in range(1, 6):
        print(str(i) + ". " + str(corr_dict[-i][1]) + " with %.6f" % corr_dict[-i][0])

    print()
    print("Lowest correlated are:")
    for i in range(5):
        print(str(i+1) + ". " + str(corr_dict[i][1]) + " with %.6f" % corr_dict[i][0])

    df_season = df.groupby(['season_name']).mean()

    fall_mean = filter_season(df, 2)['t_diff'].mean()
    spring_mean = filter_season(df, 0)['t_diff'].mean()
    summer_mean = filter_season(df, 1)['t_diff'].mean()
    winter_mean = filter_season(df, 3)['t_diff'].mean()
    print()
    print("fall average t_diff is %.2f" % fall_mean)
    print("spring average t_diff is %.2f" % spring_mean)
    print("summer average t_diff is %.2f" % summer_mean)
    print("winter average t_diff is %.2f" % winter_mean)
    all_seasons = df['t_diff'].mean()
    print("All average t_diff is %.2f" % all_seasons)


def filter_season(df, szn_num):
    new_df = df[df['season'] == szn_num]
    return new_df

def to_dict(corr):
    corr_dict = {}
    for feat1 in corr.keys():
        for feat2 in corr.keys():
            corr_dict[(feat1, feat2)] = absolute(corr[feat1][feat2])
    return corr_dict


def absolute(corr):
    if corr < 0:
        return -corr
    return corr

def sort_corr_dict(corr):
    corr_dict = to_dict(corr)
    values = []
    for key in corr_dict.keys():
        values.append((corr_dict[key], key))

    sorted_corr_doubles = sorted(values, key=lambda tup: tup[0])
    sorted_corr = []
    for i in range(len(values)):
        if sorted_corr_doubles[i][0] == 1:
            continue
        if sorted_corr_doubles[i][0] == sorted_corr_doubles[i+1][0] \
                and sorted_corr_doubles[i][1][0] == sorted_corr_doubles[i+1][1][1] \
                and sorted_corr_doubles[i][1][1] == sorted_corr_doubles[i+1][1][0]:
            sorted_corr.append(sorted_corr_doubles[i])
            i += 1

    return sorted_corr


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
        return datetime.strptime(timestamp, '%d/%m/%Y %H:%M')  #:%S.%f

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
    #holiday = holiday_weekend[0]
    #weekend = holiday_weekend[1]
    if holiday == 0 and weekend == 0:
        return 0
    if holiday == 0 and weekend == 1:
        return 1
    if holiday == 1 and weekend == 0:
        return 2
    if holiday == 1 and weekend == 1:
        return 3
