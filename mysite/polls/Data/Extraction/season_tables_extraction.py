from ...models import MatchRawData, SeasonTables
from django.core.exceptions import ObjectDoesNotExist


def get_team_season_data(season, date, team):
    """" Gets statistics for given team before the given date. Returns None if it did not
         find any statistics """
    result =  SeasonTables.objects.all().filter(
            season=season, team=team, round_end__lt=date).order_by('-round_end')

    if result.count() <= 0:
        return None

    return result[0]


def get_season_data(season, date):
    """" Gets statistics for whole season before the given date."""

    season_teams_count = SeasonTables.objects.all().filter(season=season).\
        values_list('team').distinct().count()

    return SeasonTables.objects.all().filter(season=season, round_end__lt=date). \
        order_by('-round_end')[:season_teams_count]
