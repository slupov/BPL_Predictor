from ....models import MatchRawData, SeasonTables
from urllib.request import urlopen
from datetime import datetime
from bs4 import BeautifulSoup
from enum import IntEnum

import csv
from os import listdir, path


class SeasonTableColumns(IntEnum):
    POSITION = 0
    TEAM_LOGO = 1
    TEAM = 2
    MATCHES_PLAYED = 3
    WINS = 4
    DRAWS = 5
    LOSSES = 6
    GOALS = 7
    GOAL_DIFF = 8
    POINTS = 9
    COUNT = 10


def format_season_string(seasons_str):
    years = seasons_str.split('/')
    years[0] = int(years[0])
    years[1] = int(years[1])

    # check if used for last century
    if years[0] > 90:
        years[0] += 1900
    else:
        years[0] += 2000

    if years[1] > 90:
        years[1] += 1900
    else:
        years[1] += 2000

    return str(years[0]) + "-" + str(years[1])


def get_original_seasons_string(formatted_str):
    years = formatted_str.split('-')
    years[0] = int(years[0])
    years[1] = int(years[1])

    # check if used for last century
    if years[0] < 2000:
        years[0] -= 1900
    else:
        years[0] -= 2000

    if years[1] < 2000:
        years[1] -= 1900
    else:
        years[1] -= 2000

    return str(years[0]).zfill(2) + "/" + str(years[1]).zfill(2)


def get_start_end_dates(fixtures_table_rows):
    # get start date and end date
    # iterate all table rows and get first column value

    start_date = None
    end_date = None

    for row in fixtures_table_rows:
        date = row.find_all("td")[0].get_text()

        if date != "":
            if start_date is None:
                start_date = datetime.strptime(date, "%d/%m/%Y")
            else:
                end_date = datetime.strptime(date, "%d/%m/%Y")

    if end_date is None:
        end_date = start_date

    return [start_date, end_date]


def get_round_team_statistics(standings_table_rows):
    # get standings
    # iterate all table rows and get first column value (standing) and third column value
    # (team name)

    res = []

    last_read_position = 0
    for row in standings_table_rows:
        team_table = SeasonTables()
        columns = row.find_all("td")

        goals = columns[SeasonTableColumns.GOALS].get_text().split(':')

        team_table.team = columns[SeasonTableColumns.TEAM].get_text().strip()
        team_table.wins = int(columns[SeasonTableColumns.WINS].get_text())
        team_table.draws = int(columns[SeasonTableColumns.DRAWS].get_text())
        team_table.losses = int(columns[SeasonTableColumns.LOSSES].get_text())
        team_table.points = int(columns[SeasonTableColumns.POINTS].get_text())

        team_table.goals_scored = int(goals[0])
        team_table.goals_received = int(goals[1])

        # handle fixed space or hard space, &nbsp; (non-breaking space)
        if columns[SeasonTableColumns.POSITION].get_text() != "\xa0":
            team_table.position = int(columns[0].get_text())
            last_read_position = team_table.position
        else:
            # same position as last read team
            team_table.position = last_read_position

        res.append(team_table)

    return res


def scrape_round(round, season, writer):
    url = "https://www.worldfootball.net/schedule/eng-premier-league-%s-spieltag/%s/" \
          % (season, str(round))

    html_page = urlopen(url)
    soup = BeautifulSoup(html_page, 'html.parser')

    content_div = soup.find('div', {'class': 'content'})
    html_tables = content_div.find_all('table', {'class': 'standard_tabelle'})

    fixtures_table = html_tables[0]
    standings_table = html_tables[1]

    fixtures_table_rows = fixtures_table.find_all('tr')
    dates = get_start_end_dates(fixtures_table_rows)
    dates = [str(date)[0:10] for date in dates]

    standings_table_rows = standings_table.find_all('tr')
    statistics = get_round_team_statistics(standings_table_rows[1:])

    for table_state in statistics:
        writer.writerow([get_original_seasons_string(season), table_state.team, dates[0],
                         dates[1], table_state.wins,
                         table_state.draws, table_state.losses, table_state.points,
                         table_state.goals_scored, table_state.goals_received,
                         table_state.position])

        print(get_original_seasons_string(season), table_state.team, dates[0], dates[1],
              table_state.wins,
              table_state.draws, table_state.losses, table_state.goals_scored,
              table_state.goals_received, table_state.position)


def scrape_league_standings():
    # get all seasons in database
    seasons = []
    raw_match_data_path = "../raw_data"

    # use seasons that has a match raw data file assigned
    for file in listdir(raw_match_data_path):
        file_tokens = file.split("_")
        file_tokens[-1] = file_tokens[-1][:-4]

        if len(file_tokens) > 2:
            season_str = file_tokens[1] + "/" + file_tokens[2]
            seasons.append(season_str)

    # use seasons that has match data in the database
    # seasons = MatchRawData.objects.all().values_list('season', flat=True). \
    #     distinct('season')

    seasons = [format_season_string(s) for s in seasons]

    for season in seasons:
        original_season_str = get_original_seasons_string(season).split("/")

        new_file_name = '../raw_data/standings_data/BPL_STANDINGS_%s' % (
                original_season_str[0] + "_" + original_season_str[1] + ".csv")

        exists = path.isfile(new_file_name)
        if exists:
            continue

        with open(new_file_name, 'w+') as csv_file:
            print("--------------------------- OPENING %s ---------------------------" %
                  new_file_name)

            writer = csv.writer(csv_file)

            header_row = ['season', 'team', 'round_start', 'round_end', 'wins', 'draws',
                          'losses', 'points', 'goals_scored', 'goals_received',
                          'position']

            writer.writerow(header_row)

            url = "https://www.worldfootball.net/schedule/eng-premier-league-%s" \
                  "-spieltag/" % season

            html_page = urlopen(url)
            soup = BeautifulSoup(html_page, 'html.parser')
            rounds = len(soup.find('select', {'name': 'runde'}).find_all('option'))

            for r in range(1, rounds + 1):
                scrape_round(r, season, writer)
