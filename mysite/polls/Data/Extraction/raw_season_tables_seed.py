from ...models import SeasonTables
from enum import IntEnum
from datetime import datetime
import pandas as pd
from mysite.config import should_truncate_tables
from ...Data.data_mapping import team_names_map


class RawDataCols(IntEnum):
    SEASON = 0
    TEAM = 1
    ROUND_START = 2
    ROUND_END = 3
    WINS = 4
    DRAWS = 5
    LOSSES = 6
    POINTS = 7
    GOALS_SCORED = 8
    GOALS_RECEIVED = 9
    POSITION = 10
    COUNT = 11


def seed_raw_season_tables():
    # Clear the database table if it has any logs
    if SeasonTables.objects.count != 0:
        if should_truncate_tables:
            SeasonTables.objects.all().delete()
        else:
            return

    raw_data_list = []

    for i in range(1993, 2019):
        season_str = str(i)[2:] + "_" + str((i + 1))[2:]
        file_path = '../raw_data/standings_data/BPL_STANDINGS_' + season_str + '.csv'
        raw_data_list = raw_data_list + extract_raw_data(file_path)

    SeasonTables.objects.bulk_create(raw_data_list)


def cols_to_extract():
    cols_to_use = [None] * RawDataCols.COUNT

    cols_to_use[RawDataCols.SEASON] = 'season'
    cols_to_use[RawDataCols.TEAM] = 'team'
    cols_to_use[RawDataCols.ROUND_START] = 'round_start'
    cols_to_use[RawDataCols.ROUND_END] = 'round_end'
    cols_to_use[RawDataCols.WINS] = 'wins'
    cols_to_use[RawDataCols.DRAWS] = 'draws'
    cols_to_use[RawDataCols.LOSSES] = 'losses'

    cols_to_use[RawDataCols.POINTS] = 'points'
    cols_to_use[RawDataCols.GOALS_SCORED] = 'goals_scored'

    cols_to_use[RawDataCols.GOALS_RECEIVED] = 'goals_received'
    cols_to_use[RawDataCols.POSITION] = 'position'

    return cols_to_use


def extract_raw_data(csv):
    cols_to_use = cols_to_extract()

    csv_tokens = csv.split("_")
    csv_tokens[-1] = csv_tokens[-1][:-4]

    # Read and parse the csv file
    parsed_csv = pd.read_csv(csv, sep=',', delim_whitespace=False, header=0)

    raw_data_list = []

    for index, row in parsed_csv.iterrows():
        season_table = SeasonTables()

        datetime_object = datetime.strptime(row[cols_to_use[RawDataCols.ROUND_START]],
                                            "%Y-%m-%d")
        season_table.round_start = datetime_object

        datetime_object = datetime.strptime(row[cols_to_use[RawDataCols.ROUND_END]],
                                            "%Y-%m-%d")

        season_table.round_end = datetime_object

        season_table.season = get_col_value(row, cols_to_use[RawDataCols.SEASON])

        season_table.team = \
            team_names_map[get_col_value(row, cols_to_use[RawDataCols.TEAM])]

        season_table.wins = get_col_value(row, cols_to_use[RawDataCols.WINS])
        season_table.draws = get_col_value(row, cols_to_use[RawDataCols.DRAWS])
        season_table.losses = get_col_value(row, cols_to_use[RawDataCols.LOSSES])
        season_table.points = get_col_value(row, cols_to_use[RawDataCols.POINTS])

        season_table.goals_scored = \
            get_col_value(row, cols_to_use[RawDataCols.GOALS_SCORED])
        season_table.goals_received = \
            get_col_value(row, cols_to_use[RawDataCols.GOALS_RECEIVED])

        season_table.position = get_col_value(row, cols_to_use[RawDataCols.POSITION])

        raw_data_list.append(season_table)

        # print(season_table)
        # print("---------------------------")

    return raw_data_list


# An utility function that helps to get the value of the csv row and column. Returns None
# if no such column was found

def get_col_value(row, col):
    try:
        return row[col]
    except KeyError:
        return None
