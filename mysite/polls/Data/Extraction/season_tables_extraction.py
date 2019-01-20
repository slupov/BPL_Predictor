from ...models import MatchRawData, SeasonTables


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

    for team_name in teams_season:
        teams_season[team_name].position = \
            get_table_position(team_name, teams_season)

    return teams_season


def get_table_position(team, season_data):
    pivot_team = season_data[team]

    teams_with_more_pts = 0
    teams_with_same_pts_better_gdf = 0
    teams_with_same_pts_same_gdf_more_scored = 0

    for team_name in season_data:
        current_team = season_data[team_name]
        if current_team.team == pivot_team.team:
            continue

        if current_team.points > pivot_team.points:
            teams_with_more_pts += 1
        elif current_team.points == pivot_team.points:

            pivot_goal_diff = pivot_team.goals_scored - pivot_team.goals_received
            current_goal_diff = current_team.goals_scored - current_team.goals_received

            if current_goal_diff > pivot_goal_diff:
                teams_with_same_pts_better_gdf += 1

            elif current_goal_diff == pivot_goal_diff and \
                    current_team.goals_scored > pivot_team.goals_scored:
                teams_with_same_pts_same_gdf_more_scored += 1

    return 1 + teams_with_more_pts + teams_with_same_pts_better_gdf + \
           teams_with_same_pts_same_gdf_more_scored
