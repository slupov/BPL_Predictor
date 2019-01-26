from ...models import MatchRawData
from ...models import ExtractedFixtures

from .form_extraction import extract_forms
from .concentration_extraction import extract_concentration
from .motivation_extraction import extract_motivation
from mysite.config import recalculate_training_table
from ..Extraction.history_extraction import extract_history
from .goal_score_diff_extraction import goal_diff_extraction, goal_diff_extraction_2,\
    score_diff_extraction

import time


def seed_training_model():
    print("Started training model seed.")

    # Clear the database table if it has any logs
    if ExtractedFixtures.objects.count != 0:
        if recalculate_training_table:
            ExtractedFixtures.objects.all().delete()
        else:
            return

    # get all seasons in database
    seasons = MatchRawData.objects.all().values_list('season', flat=True). \
        distinct('season')

    training_model = []

    for season in seasons:
        print("------------------------------", season, "------------------------------")

        season_matches = MatchRawData.objects.all().filter(season=season)

        training_model = training_model + \
                         seed_training_model_season(season, season_matches)

    ExtractedFixtures.objects.bulk_create(training_model)

    print("Training model seed successfully finished.")


def seed_training_model_season(season, season_matches):
    season_training_model = []
    all_matches = MatchRawData.objects.all().order_by('-date')

    for curr_match in season_matches:
        # calculations when less than 5 matches in a season -> zeroes for missing match
        forms = extract_forms(curr_match.home_team, curr_match.away_team, curr_match.date)

        start_time = time.time()
        concentrations = extract_concentration(curr_match.home_team, curr_match.away_team,
                                               curr_match.date, curr_match.season,
                                               season_matches)

        print("Extract concentration took %s seconds" % (time.time() - start_time))

        start_time = time.time()
        motivations = extract_motivation(curr_match.home_team, curr_match.away_team,
                                         curr_match.date, season)
        print("Extract motivation took %s seconds" % (time.time() - start_time))
        print("\n")

        start_time = time.time()
        goaldiff = goal_diff_extraction(curr_match.home_team, curr_match.away_team,
                                        curr_match.date, season)

        # goaldiff = goal_diff_extraction_2(curr_match.home_team, curr_match.away_team,
        #                                 curr_match.date, season)

        print("Extract goal difference took %s seconds" % (time.time() - start_time))
        print("\n")

        start_time = time.time()
        scorediff = score_diff_extraction(curr_match.home_team, curr_match.away_team,
                                          curr_match.date, season)
        print("Extract goal difference took %s seconds" % (time.time() - start_time))
        print("\n")

        extracted_fixture = ExtractedFixtures()

        extracted_fixture.season = season
        extracted_fixture.home_team = curr_match.home_team
        extracted_fixture.away_team = curr_match.away_team
        extracted_fixture.home_form = forms[0]
        extracted_fixture.away_form = forms[1]
        extracted_fixture.result = curr_match.full_time_result  # TODO Check if thats correct to use here
        extracted_fixture.home_concentration = concentrations[0]
        extracted_fixture.away_concentration = concentrations[1]
        extracted_fixture.goal_diff = goaldiff
        extracted_fixture.score_diff = scorediff
        extracted_fixture.history = extract_history(
            curr_match.home_team, curr_match.away_team, curr_match.date, all_matches)
        extracted_fixture.home_motivation = motivations[0]
        extracted_fixture.away_motivation = motivations[1]

        season_training_model.append(extracted_fixture)

    return season_training_model
