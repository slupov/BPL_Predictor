def extract_history(home_team, away_team, date, all_matches):
    history_matches_count = 5

    history_matches = [x for x in all_matches if
                       ((x.home_team == home_team and x.away_team == away_team) or
                        (x.home_team == away_team and x.away_team == home_team)) and
                       x.date < date]

    history_matches = history_matches[:history_matches_count]
    history_matches_count = len(history_matches)

    if history_matches_count == 0:
        # if teams have no history between each other, assume its all draws
        return 0.5

    result = 0

    away_result_parser = {0: 1, 0.5: 0.5, 1: 0}

    for match in history_matches:
        # determine whether home_team played at home or away
        if home_team == match.home_team:
            result += match.full_time_result
        else:
            result += away_result_parser[match.full_time_result]

    result /= history_matches_count
    return result
