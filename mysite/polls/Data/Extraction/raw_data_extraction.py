from ...models import MatchRawData
from enum import IntEnum
from datetime import datetime
import pandas as pd


class RawDataCols(IntEnum):
    DATE = 0
    HOME_TEAM = 1
    AWAY_TEAM = 2
    FTHG = 3
    HG = 4
    FTAG = 5
    AG = 6
    FTR = 7
    RES = 8
    HTHG = 9
    HTAG = 10
    HTR = 11
    ATTENDANCE = 12
    HS = 13
    AS = 14
    HST = 15
    AST = 16
    HHW = 17
    AHW = 18
    HC = 19
    AC = 20
    HF = 21
    AF = 22
    HFKC = 23
    AFKC = 24
    HO = 25
    AO = 26
    HY = 27
    AY = 28
    HR = 29
    AR = 30
    COUNT = 31


# Returns an array of the column names needed for our raw data table

def seed_db_raw_data():
    # Clear the database table if it has any logs
    if MatchRawData.objects.count != 0:
        return
        # MatchRawData.objects.all().delete()

    extract_raw_data('../raw_data/BPL_18_19.csv')
    extract_raw_data('../raw_data/BPL_17_18.csv')
    extract_raw_data('../raw_data/BPL_16_17.csv')
    extract_raw_data('../raw_data/BPL_15_16.csv')


def cols_to_extract():
    cols_to_use = [None] * RawDataCols.COUNT

    cols_to_use[RawDataCols.DATE] = 'Date'
    cols_to_use[RawDataCols.HOME_TEAM] = 'HomeTeam'
    cols_to_use[RawDataCols.AWAY_TEAM] = 'AwayTeam'
    cols_to_use[RawDataCols.FTHG] = 'FTHG'
    cols_to_use[RawDataCols.HG] = 'HG'
    cols_to_use[RawDataCols.FTAG] = 'FTAG'
    cols_to_use[RawDataCols.AG] = 'AG'

    cols_to_use[RawDataCols.FTR] = 'FTR'
    cols_to_use[RawDataCols.RES] = 'Res'

    cols_to_use[RawDataCols.HTHG] = 'HTHG'
    cols_to_use[RawDataCols.HTAG] = 'HTAG'
    cols_to_use[RawDataCols.HTR] = 'HTR'
    cols_to_use[RawDataCols.ATTENDANCE] = 'Attendance'
    cols_to_use[RawDataCols.HS] = 'HS'
    cols_to_use[RawDataCols.AS] = 'AS'
    cols_to_use[RawDataCols.HST] = 'HST'
    cols_to_use[RawDataCols.AST] = 'AST'
    cols_to_use[RawDataCols.HHW] = 'HHW'
    cols_to_use[RawDataCols.AHW] = 'AHW'
    cols_to_use[RawDataCols.HC] = 'HC'
    cols_to_use[RawDataCols.AC] = 'AC'
    cols_to_use[RawDataCols.HF] = 'HF'
    cols_to_use[RawDataCols.AF] = 'AF'
    cols_to_use[RawDataCols.HFKC] = 'HFKC'
    cols_to_use[RawDataCols.AFKC] = 'AFKC'
    cols_to_use[RawDataCols.HO] = 'HO'
    cols_to_use[RawDataCols.AO] = 'AO'
    cols_to_use[RawDataCols.HY] = 'HY'
    cols_to_use[RawDataCols.AY] = 'AY'
    cols_to_use[RawDataCols.HR] = 'HR'
    cols_to_use[RawDataCols.AR] = 'AR'

    return cols_to_use


# Extracts raw data from the raw data csv and populates the raw match data table in the
# database

def extract_raw_data(csv):
    cols_to_use = cols_to_extract()

    csv_tokens = csv.split("_")
    csv_tokens[-1] = csv_tokens[-1][:-4]

    # Read and parse the csv file
    parsed_csv = pd.read_csv(csv, sep=',', delim_whitespace=False, header=0)

    results_parser = {'H': 1, 'D': 0.5, 'A': 0}

    for index, row in parsed_csv.iterrows():
        match_data = MatchRawData()

        # pick one of two possible date formats - try catch it
        try:
            datetime_object = \
                datetime.strptime(row[cols_to_use[RawDataCols.DATE]], '%d/%m/%y')
        except ValueError:
            datetime_object = \
                datetime.strptime(row[cols_to_use[RawDataCols.DATE]], '%d/%m/%Y')

        match_data.date = datetime_object
        match_data.season = csv_tokens[2] + "/" + csv_tokens[3]

        match_data.home_team = get_col_value(row, cols_to_use[RawDataCols.HOME_TEAM])
        match_data.away_team = get_col_value(row, cols_to_use[RawDataCols.AWAY_TEAM])

        match_data.full_time_home_goals = \
            get_col_value(row, cols_to_use[RawDataCols.FTHG])
        match_data.full_time_away_goals = \
            get_col_value(row, cols_to_use[RawDataCols.FTAG])

        # pick one of two possible table names - try catch it
        try:
            match_data.full_time_result = \
                results_parser[row[cols_to_use[RawDataCols.FTR]]]
        except KeyError:
            match_data.full_time_result = \
                results_parser[get_col_value(row, cols_to_use[RawDataCols.RES])]

        match_data.half_time_home_goals = \
            get_col_value(row, cols_to_use[RawDataCols.HTHG])
        match_data.half_time_away_goals = \
            get_col_value(row, cols_to_use[RawDataCols.HTAG])

        match_data.half_time_result = results_parser[row[cols_to_use[RawDataCols.HTR]]]
        match_data.attendance = get_col_value(row, cols_to_use[RawDataCols.ATTENDANCE])

        match_data.home_shots = get_col_value(row, cols_to_use[RawDataCols.HS])
        match_data.away_shots = get_col_value(row, cols_to_use[RawDataCols.AS])

        match_data.home_woodwork_hits = get_col_value(row, cols_to_use[RawDataCols.HHW])
        match_data.away_woodwork_hits = get_col_value(row, cols_to_use[RawDataCols.AHW])

        match_data.home_corners = get_col_value(row, cols_to_use[RawDataCols.HC])
        match_data.away_corners = get_col_value(row, cols_to_use[RawDataCols.AC])
        match_data.home_fouls_commited = get_col_value(row, cols_to_use[RawDataCols.HF])
        match_data.away_fouls_commited = get_col_value(row, cols_to_use[RawDataCols.AF])

        match_data.home_offsides = get_col_value(row, cols_to_use[RawDataCols.HO])
        match_data.away_offsides = get_col_value(row, cols_to_use[RawDataCols.AC])
        match_data.home_red_cards = get_col_value(row, cols_to_use[RawDataCols.HR])
        match_data.away_red_cards = get_col_value(row, cols_to_use[RawDataCols.AR])
        match_data.home_yellow_cards = get_col_value(row, cols_to_use[RawDataCols.HY])
        match_data.away_yellow_cards = get_col_value(row, cols_to_use[RawDataCols.AY])

        match_data.save()

        print(match_data)
        print("---------------------------")


# An utility function that helps to get the value of the csv row and column. Returns None
# if no such column was found

def get_col_value(row, col):
    try:
        return row[col]
    except KeyError:
        return None
