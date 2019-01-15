from ...models import MatchRawData


def extract_form(home_team, away_team, date_played, season):
    home_team_last_five_matches = MatchRawData.objects.all().filter(date__lte=date_played)
    