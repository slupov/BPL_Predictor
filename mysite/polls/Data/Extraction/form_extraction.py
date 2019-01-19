from ...models import MatchRawData
from django.db.models import Q


# Calculates the form (last matches before the given fixture)

def extract_forms(home_team, away_team, date_played):
    form_matches_count = 5

    # get all matches that were played earlier than the given date
    home_last_matches = MatchRawData.objects.all() \
        .filter(Q(home_team=home_team) | Q(away_team=home_team), date__lt=date_played) \
        .order_by('-date')[:form_matches_count]

    away_last_matches = MatchRawData.objects.all() \
        .filter(Q(home_team=away_team) | Q(away_team=away_team), date__lt=date_played) \
        .order_by('-date')[:form_matches_count]

    form1 = 0
    form2 = 0

    game_result = 0

    home_results_form_parser = {1: 2, 0.5: 1, 0: 0}
    away_results_form_parser = {1: 0, 0.5: 1, 0: 1}

    for x in range(0, form_matches_count):
        game_result = home_last_matches[x].full_time_result

        # check if home_team played at home or away
        if home_last_matches[x].home_team == home_team:
            # played at home
            form1 += home_results_form_parser[game_result]
        else:
            # played away
            form1 += away_results_form_parser[game_result]

        game_result = away_last_matches[x].full_time_result

        # check if away_team played at home or away
        if away_last_matches[x].home_team == away_team:
            # played at home
            form2 += home_results_form_parser[game_result]
        else:
            # played away
            form2 += away_results_form_parser[game_result]

    # normalize forms
    form1 /= 10
    form2 /= 10

    return [form1, form2]
