from .season_tables_extraction import get_season_data, get_team_season_data
from ...models import MatchRawData


def goal_diff_extraction(home_team, away_team, date_played, season):
    match = MatchRawData.objects.all(). \
        filter(home_team=home_team, away_team=away_team, date=date_played)[0]
    all_matches = MatchRawData.objects.all().filter(season=season,date__lt=date_played)
    home_goals = match.full_time_home_goals
    away_goals = match.full_time_away_goals

    diff = home_goals - away_goals

    max_diff = 0
    for match in all_matches:
        current_home_goals = match.full_time_home_goals
        current_away_goals = match.full_time_away_goals
        diff = abs(current_home_goals - current_away_goals)
        if diff > max_diff: max_diff = diff

    return calculate_goal_score_diff(diff, max_diff)


def goal_diff_extraction_2(home_team, away_team, date_played, season):
    season_data = get_season_data(season, date_played)

    if len(season_data) == 0:
        return 0.5

    home_team_season_data = [x for x in season_data if x.team == home_team][0]
    away_team_season_data = [x for x in season_data if x.team == away_team][0]

    season_data = list(season_data)
    season_data.sort(key=lambda x: (x.goals_scored - x.goals_received), reverse=True)

    leader_season_data = season_data[0]

    home_goal_diff = home_team_season_data.goals_scored - \
                     home_team_season_data.goals_received

    away_goal_diff = away_team_season_data.goals_scored - \
                     away_team_season_data.goals_received

    leader_goal_diff = leader_season_data.goals_scored - \
                       leader_season_data.goals_received

    diff = home_goal_diff - away_goal_diff
    return calculate_goal_score_diff(diff, leader_goal_diff)


def score_diff_extraction(home_team, away_team, date_played, season):
    season_data = get_season_data(season, date_played)

    first_pos_team = get_first_pos_team(season_data)
    last_pos_team = get_last_pos_team(season_data)

    first_team_season_scores = 0 if first_pos_team is None \
        else first_pos_team.points
    last_team_season_scores = 0 if last_pos_team is None \
        else last_pos_team.points

    max_diff = first_team_season_scores - last_team_season_scores

    home_team_scores = 0 if get_team_season_data(season, date_played, home_team) is None \
        else get_team_season_data(season, date_played, home_team).points
    away_team_scores = 0 if get_team_season_data(season, date_played, away_team) is None \
        else get_team_season_data(season, date_played, away_team).points

    diff = abs(home_team_scores - away_team_scores)
    return calculate_goal_score_diff(diff, max_diff)


def calculate_goal_score_diff(diff, max_diff):
    if max_diff == 0:
        return 0.5

    return 0.5 + (diff / (2 * max_diff))


def get_first_pos_team(season_data):
    for t in season_data:
        if t.position == 1:
            return t


def get_last_pos_team(season_data):
    last_pos = 1

    for t in season_data:
        if t.position > last_pos:
            last_pos = t.position

    for t in season_data:
        if t.position == last_pos:
            return t
