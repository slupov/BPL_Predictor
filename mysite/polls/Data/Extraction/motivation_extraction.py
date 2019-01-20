from ...models import MatchRawData
from django.db.models import Q
from season_tables_extraction import get_season_data

key_positions = {1, 2, 3, 4, 5, 6, 17, 18}
derbies = {'Arsenal': {'Tottenham', 'Chelsea'},
           'Liverpool': {'Everton'},
           'Man United': {'Man City', 'Liverpool'},
           'Sunderland': {'Newcastle'}
           }


def extract_motivation(home_team, away_team, date_played):
    season = MatchRawData.objects.all().filter(date=date_played, home_team=home_team, away_team=away_team)[0].season
    derby = get_derby_score(home_team, away_team)
    home_team_season_data = get_season_data(season, date_played)[home_team]
    away_team_season_data = get_season_data(season, date_played)[away_team]
    dist1 = get_dist(home_team_season_data.position)
    dist2 = get_dist(away_team_season_data.position)
    left1 = get_tours_left(home_team, season, date_played)
    left2 = get_tours_left(away_team, season, date_played)
    tour1 = get_tour(left1)
    tour2 = get_tour(left2)
    motivation1 = calculate_motivation(derby, dist1, left1, tour1)
    motivation2 = calculate_motivation(derby, dist2, left2, tour2)
    return [motivation1,motivation2]


def get_derby_score(home_team, away_team):
    if ((home_team in derbies and away_team in derbies[home_team]) or (
            away_team in derbies and home_team in derbies[away_team])):
        return 1
    return 0


def get_dist(position):
    dist = 6
    if position in key_positions:
        return 0
    for x in key_positions:
        dist = min(dist, abs(position - x))
    return dist


def get_tours_left(team_name, season, date_played):
    return MatchRawData.objects.all().filter(Q(home_team=team_name) | Q(away_team=team_name), season=season,
                                             date__gte=date_played).count()


def get_tour(left):
    if left < 6:
        return 1
    return 0


def calculate_motivation(derby, dist, left, tour):
    return min(max(1 - (dist / (3 * left)), derby, (tour + dist) / 2), 1)
