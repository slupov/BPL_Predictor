from ...models import MatchRawData
from django.db.models import Q
from .season_tables_extraction import get_season_data, get_team_season_data


def goal_diff_extraction(home_team, away_team, date_played, season):
    match = MatchRawData.objects.all().filter(home_team=home_team, away_team=away_team, date=date_played)[0]
    home_goals = match.full_time_home_goals
    away_goals = match.full_time_away_goals
    diff = abs(home_goals - away_goals)
    season_data = get_season_data(season, date_played)
    first_pos_team = get_first_pos_team(season_data)
    first_team_diff = 0 if first_pos_team is None else first_pos_team.goals_scored - first_pos_team.goals_received
    last_pos_team = get_last_pos_team(season_data)
    last_team_diff = 0 if last_pos_team is None else last_pos_team.goals_scored - last_pos_team.goals_received
    max_diff = abs(first_team_diff - last_team_diff)
    return calculate_goal_score_diff(diff, max_diff)


def score_diff_extraction(home_team, away_team, date_played, season):
    season_data = get_season_data(season, date_played)
    first_pos_team = get_first_pos_team(season_data)
    last_pos_team = get_last_pos_team(season_data)
    first_team_season_scores = 0 if first_pos_team is None else first_pos_team.points
    last_team_season_scores = 0 if last_pos_team is None else last_pos_team.points
    max_diff = first_team_season_scores - last_team_season_scores
    home_team_scores = 0 if get_team_season_data(season, date_played, home_team) is None else get_team_season_data(
        season, date_played, home_team).points
    away_team_scores = 0 if get_team_season_data(season, date_played, away_team) is None else get_team_season_data(
        season, date_played, away_team).points
    diff = abs(home_team_scores - away_team_scores)
    return calculate_goal_score_diff(diff, max_diff)


def calculate_goal_score_diff(diff, max_diff):
    return 0.5 + diff / (2 * (1 if max_diff == 0 else max_diff))


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
