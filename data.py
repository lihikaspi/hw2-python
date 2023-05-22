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

    corr_dict = sort_corr_dict(df)
    print("Highest correlated are:")
    for i in range(5):
        print(str(i) + ". (" + corr_dict[i][1][0] + ", " +
              corr_dict[i][1][1] + ") with %.6f" % corr_dict[i][0])

    print()
    print("Lowest correlated are:")
    for i in range(5):
        print(str(i) + ". (" + corr_dict[-i][1][0] + ", " +
              corr_dict[-i][1][1] + ") with %.6f" % corr_dict[-i][0])

    df_season = df.groupby(['season_name']).mean()
    print("fall average t_diff is %.2f" % df_season['fall']['t_diff'])
    print("spring average t_diff is %.2f" % df_season['spring']['t_diff'])
    print("summer average t_diff is %.2f" % df_season['summer']['t_diff'])
    print("winter average t_diff is %.2f" % df_season['winter']['t_diff'])
    all_seasons = df['t_diff'].mean()
    print("All average t_diff is %.2f" % all_seasons)


def to_dict(df):
    corr_dict = {}
    for feat1 in df.keys():
        for feat2 in df.keys():
            corr_dict[(feat1, feat2)] = df[feat1].corr(df[feat2])
    return corr_dict


def sort_corr_dict(df):
    corr_dict = to_dict(df)
    count = [[]]
    i = 0
    for key in df.keys():
        count[i][0] = key
        count[i][1] = 0
        i += 1

    corr_vals = []
    j = 0
    for key, value in corr_dict.items():
        if key[0] == key[1]:
            continue
        k1 = find_feat_in_count(count, key[0])
        k2 = find_feat_in_count(count, key[1])
        if count[k1][1] == len(df.keys())-1 or count[k2][1] == len(df.keys())-1:
            continue
        corr_vals[j] = (value, key)
        j += 1

    return sorted(corr_vals)


def find_feat_in_count(count, feat):
    for i in range(len(count)):
        if count[i][0] == feat:
            return i

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
