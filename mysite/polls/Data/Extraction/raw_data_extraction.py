from ...models import MatchRawData
from enum import IntEnum

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


# Extracts raw data from the raw data csv and populates the raw match data table in the database

def extract_raw_data(csv):
    # Clear the database table if it has any logs
    # if MatchRawData.objects.count != 0:
    # MatchRawData.objects.delete()

    cols_to_use = cols_to_extract()
    #
    # cols_to_use=['HomeTeam', 'Div','Date', 'AwayTeam']
    # Read and parse the csv file
    parsed_csv = pd.read_csv(csv, sep=',', delim_whitespace=False, names=cols_to_use, usecols=cols_to_use, header=0)

    # match_data = MatchRawData(date='2018-12-12', home_team='Home', away_team='Away',
    #                           full_time_home_goals=5, full_time_away_goals=0,
    #                           full_time_result=-1)
    # match_data.save()
    #

    # print(parsed_csv[parsed_csv["Date"] == 14])

    for col in cols_to_use:
        values = parsed_csv[col].values
        for val in values:
            print(str(col) + ' --------> ' + str(val))
