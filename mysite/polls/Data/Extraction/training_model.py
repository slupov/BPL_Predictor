from ...models import MatchRawData
from ...models import ExtractedFixtures

from .form_extraction import extract_forms
from .concentration_extraction import extract_concentration
import time


def seed_training_model():
    print("Started training model seed.")

    # Clear the database table if it has any logs
    if ExtractedFixtures.objects.count != 0:
        # return
        ExtractedFixtures.objects.all().delete()

    # get all seasons in database
    seasons = MatchRawData.objects.all().values_list('season', flat=True).\
        distinct('season')

    training_model = []

    for season in seasons:
        print("------------------------------",season,"------------------------------")

        season_matches = MatchRawData.objects.all().filter(season=season)

        training_model = training_model + \
                         seed_training_model_season(season, season_matches)

    ExtractedFixtures.objects.bulk_create(training_model)

    print("Training model seed successfully finished.")


def seed_training_model_season(season, season_matches):
    season_training_model = []
    for curr_match in season_matches:
        # TODO Stoyan Lupov 19-01-2019 uncomment when it is decided what to do with form
        # calculations when there are less than 5 matches in a season
        # forms = extract_forms(curr_match.home_team, curr_match.away_team, curr_match.date)

        # TODO Stoyan Lupov 19-01-2019 extract_concentration is the BOTTLENECK here.
        # Too slow

        start_time = time.time()
        concentrations = extract_concentration(curr_match.home_team, curr_match.away_team,
                                               curr_match.date, curr_match.season,
                                               season_matches)

        print("Extract concentration took %s seconds" % (time.time() - start_time))

        extracted_fixture = ExtractedFixtures()
        extracted_fixture.season = season
        extracted_fixture.home_team = curr_match.home_team
        extracted_fixture.away_team = curr_match.away_team
        extracted_fixture.home_form = 0 #forms[0] # TODO Add real value
        extracted_fixture.away_form = 0 #forms[1] # TODO Add real value
        extracted_fixture.result = 0 # TODO Add real value
        extracted_fixture.home_concentration = concentrations[0]
        extracted_fixture.away_concentration = concentrations[1]
        extracted_fixture.goal_diff = 0 # TODO Add real value
        extracted_fixture.score_diff = 0 # TODO Add real value
        extracted_fixture.history = 0 # TODO Add real value
        extracted_fixture.home_motivation = 0 # TODO Add real value
        extracted_fixture.away_motivation = 0 # TODO Add real value

        season_training_model.append(extracted_fixture)
        # print(extracted_fixture)

    return season_training_model
