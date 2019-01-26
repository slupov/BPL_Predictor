import pandas as pd
from pandas.plotting import scatter_matrix

from matplotlib import cm
from matplotlib import pyplot as plt

from sklearn import preprocessing

from ...models import ExtractedFixtures
from ...models import MatchRawData

from .analysis_model import AnalysisModel

from .dependence_graphs import generate_dependecy_graphs


def analyze_data():
    print("\033[31mStarting extracted data analysis \033[0m")
    analyze_extracted_data()

    print("\033[31mStarting raw match data analysis \033[0m")
    analyze_raw_match_data()


def analyze_extracted_data():
    extracted_data_df = pd.DataFrame.from_records(
        ExtractedFixtures.objects.all().filter(season__gte="17/18").
            order_by('season', 'home_team').values(), exclude=['id'])

    extracted_data_df.dropna()

    le = preprocessing.LabelEncoder()
    extracted_data_df['home_team'] = le.fit_transform(extracted_data_df['home_team'])
    extracted_data_df['away_team'] = le.fit_transform(extracted_data_df['away_team'])
    extracted_data_df['result'] = le.fit_transform(extracted_data_df['result'])

    generate_dependecy_graphs(extracted_data_df)

    feature_names = [['home_team', 'away_team', 'goal_diff', 'score_diff'],
                     ['home_team', 'away_team', 'goal_diff', 'score_diff'],
                     ['home_team', 'away_team', 'goal_diff', 'score_diff'],
                     ['home_team', 'away_team', 'goal_diff', 'score_diff'],
                     ['home_team', 'away_team', 'goal_diff', 'score_diff']]

    # BUILDING MODELS

    for i in range(0, len(feature_names)):
        model_name = "EXTRACTED DATA MODEL [%s]" % i
        model = AnalysisModel(extracted_data_df, feature_names[i], 'result', model_name)
        model.test()
        print(model)

        X = extracted_data_df[feature_names[i]]
        Y = extracted_data_df['result']

        generate_scatter_matrix(X, Y, "extracted_fixtures", i)

    print("Extracted data analysis ended.")


def analyze_raw_match_data():
    extracted_data_df = pd.DataFrame.from_records(
        MatchRawData.objects.all().filter(season__gte="17/18").
            order_by('season', 'home_team').values(), exclude=['id'])

    extracted_data_df.dropna()

    le = preprocessing.LabelEncoder()

    extracted_data_df['home_team'] = \
        le.fit_transform(extracted_data_df['home_team'])

    extracted_data_df['away_team'] = \
        le.fit_transform(extracted_data_df['away_team'])

    extracted_data_df['full_time_result'] = \
        le.fit_transform(extracted_data_df['full_time_result'])

    # generate_dependecy_graphs(extracted_data_df)

    feature_names = [
        ['home_team', 'away_team', 'home_shots', 'away_shots'],
        ['home_team', 'away_team', 'home_fouls_commited', 'away_fouls_commited'],
        ['home_team', 'away_team', 'home_yellow_cards', 'away_yellow_cards'],
        ['home_team', 'away_team', 'half_time_result']]

    # BUILDING MODELS

    for i in range(0, len(feature_names)):
        model_name="EXTRACTED RAW DATA MODEL [%s]" % i
        model = AnalysisModel(extracted_data_df, feature_names[i], 'full_time_result',
                              model_name)
        model.test()
        print(model)

        X = extracted_data_df[feature_names[i]]
        Y = extracted_data_df['full_time_result']

        generate_scatter_matrix(X, Y, "extracted_fixtures", i)

    print("Extracted raw match data analysis ended.")


def generate_scatter_matrix(trainX, trainY, model_type, model_idx):
    cmap = cm.get_cmap('gnuplot')
    scatter = scatter_matrix(trainX, c=trainY, marker='o', s=40, hist_kwds={'bins': 15},
                             figsize=(9, 9), cmap=cmap)

    plt.suptitle('Scatter-matrix for each input variable')
    plt.savefig('%s_scatter_matrix_%s' % (model_type, model_idx))
