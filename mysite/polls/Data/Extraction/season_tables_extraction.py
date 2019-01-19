from ...models import MatchRawData, SeasonTable


# param date - the date of the state of the season table we want to get
def get_season_data(season, date):
    all_matches = MatchRawData.objects.all().filter(season=season, date__lte=date)
    all_matches_size = all_matches.count()

    # key - team name; value - {SeasonTables}
    teams_season = {}

    for x in range(0, all_matches_size):
        current_match = all_matches[x]

        # create teams if not existing
        if current_match.home_team not in teams_season:
            teams_season[current_match.home_team] = SeasonTable()
            teams_season[current_match.home_team].season = season
            teams_season[current_match.home_team].team = current_match.home_team

        if current_match.away_team not in teams_season:
            teams_season[current_match.away_team] = SeasonTable()
            teams_season[current_match.away_team].season = season
            teams_season[current_match.away_team].team = current_match.away_team

        # give points, wins, draws, losses
        if current_match.full_time_result == 1:
            teams_season[current_match.home_team].wins += 1
            teams_season[current_match.home_team].points += 3

            teams_season[current_match.away_team].losses += 1
        elif current_match.full_time_result == 0.5:
            teams_season[current_match.home_team].draws += 1
            teams_season[current_match.away_team].draws += 1

            teams_season[current_match.home_team].points += 1
            teams_season[current_match.away_team].points += 1
        else:
            teams_season[current_match.away_team].wins += 1
            teams_season[current_match.away_team].points += 3

            teams_season[current_match.home_team].losses += 1

        # give goals scored, received
        teams_season[current_match.home_team].goals_scored += \
            current_match.full_time_home_goals
        teams_season[current_match.away_team].goals_received += \
            current_match.full_time_home_goals

        teams_season[current_match.away_team].goals_scored += \
            current_match.full_time_away_goals
        teams_season[current_match.home_team].goals_received += \
            current_match.full_time_away_goals

    return teams_season
