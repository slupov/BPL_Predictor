from polls.Data.Extraction.raw_match_data_seed import seed_raw_match_data
from polls.Data.Extraction.raw_season_tables_seed import seed_raw_season_tables

from polls.Data.Extraction.training_model import seed_training_model
from polls.Data.Extraction.Web.scrape_league_standings import scrape_league_standings

from polls.Data.Analysis.data_analysis import analyze_data

import time


def start_up():
    start_time = time.time()
    scrape_league_standings()
    print("Team standings scraping took %s seconds to finish.\n" % (
            time.time() - start_time))

    start_time = time.time()
    seed_raw_match_data()
    print("Raw match data seed took %s seconds to finish.\n" % (time.time() - start_time))

    start_time = time.time()
    seed_raw_season_tables()
    print("Raw season tables seed took %s seconds to finish.\n" % (
            time.time() - start_time))

    start_time = time.time()
    seed_training_model()
    print("Training model data seed took %s seconds to finish." % (
            time.time() - start_time))

    start_time = time.time()
    analyze_data()
    print("Data analysis took %s seconds to finish." % (time.time() - start_time))
