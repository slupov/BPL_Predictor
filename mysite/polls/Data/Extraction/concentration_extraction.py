from ...models import MatchRawData
from .season_tables_extraction import get_season_data
from django.db.models import Q


def extract_concentration(home_team, away_team, date, season, season_matches):
    # the number of matches to check for concentration
    concentration_matches = 5

    # the difference in table positions for a team to be considered 'weak'
    position_diff_weak = 7

    home_team_last_matches = [x for x in season_matches
                              if (x.home_team == home_team or x.away_team == home_team)
                              and x.date < date and x.season == season]

    home_team_last_matches = home_team_last_matches[:concentration_matches]
    home_team_last_matches.sort(key=lambda x: x.date, reverse=True)



    away_team_last_matches = [x for x in season_matches
                              if (x.home_team == away_team or x.away_team == away_team)
                              and x.date < date and x.season == season]
    away_team_last_matches = away_team_last_matches[:concentration_matches]
    away_team_last_matches.sort(key=lambda x: x.date, reverse=True)

    # home_team_last_matches = MatchRawData.objects.all(). \
    #     filter(Q(home_team=home_team) | Q(away_team=home_team), date__lt=date,
    #            season=season).order_by('-date')[:concentration_matches]
    #
    # away_team_last_matches = MatchRawData.objects.all(). \
    #     filter(Q(home_team=away_team) | Q(away_team=away_team), date__lt=date,
    #            season=season).order_by('-date')[:concentration_matches]

    #TODO THE REAL BOTTLE NECK

    season_data = get_season_data(season, date)

    concentration1 = get_team_concentration(home_team, home_team_last_matches,
                                            season_data, concentration_matches)

    concentration2 = get_team_concentration(away_team, away_team_last_matches,
                                            season_data, concentration_matches)

    return [concentration1, concentration2]


def get_team_concentration(team, team_last_matches, season_data, concentration_matches):
    nearest_match_lost_to_weak = concentration_matches
    has_lost_to_weak = False

    # iterate home_team's last matches and check if they lost to a weak team
    for curr_match in team_last_matches:
        game_result = curr_match.full_time_result

        home_team_season_data = \
            [a for a in season_data if a.team == curr_match.home_team][0]
        away_team_season_data = \
            [a for a in season_data if a.team == curr_match.away_team][0]

        position_diff = abs(home_team_season_data.position -
                            away_team_season_data.position)

        # check if home_team played at home or away
        if curr_match.home_team == team:
            # played at home
            has_lost_to_weak = position_diff >= 7 and game_result == 0
        else:
            # played away
            has_lost_to_weak = -position_diff >= 7 and game_result == 1

        if has_lost_to_weak:
            break
        else:
            nearest_match_lost_to_weak -= 1

    if not has_lost_to_weak:
        nearest_match_lost_to_weak = 0

    return 1 - (2 * (nearest_match_lost_to_weak / 10))
