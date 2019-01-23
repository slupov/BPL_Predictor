import pandas as pd
from matplotlib import cm
from matplotlib import pyplot as plt
from pandas.plotting import scatter_matrix

from .dependence_graphs import generate_dependecy_graphs
from ...models import ExtractedFixtures

from sklearn.preprocessing import MinMaxScaler


def analyze_data():
    all_data = ExtractedFixtures.objects.all().order_by('season', 'home_team')

    train_data = [x for x in all_data if x.season == "17/18"]
    test_data = [x for x in all_data if x.season == "18/19"]

    train_df = pd.DataFrame.from_records(
        ExtractedFixtures.objects.all().filter(season="17/18").values(), exclude=['id'])

    test_df = pd.DataFrame.from_records(
        ExtractedFixtures.objects.all().filter(season="18/19").values(), exclude=['id'])

    feature_names = ['result', 'goal_diff', 'score_diff']

    # apply min max normalization scaling to data
    scaler = MinMaxScaler()

    X_train = train_df[feature_names]
    Y_train = train_df['result']

    X_train_normalized = scaler.fit_transform(X_train)

    generate_dependecy_graphs(train_df)
    generate_scatter_matrix(X_train, Y_train)

    # poisson_distribution(train_df, test_df)

    print("debug")


def poisson_distribution(train_df, test_df):
    # get avarage column values
    train_mean = train_df.mean()
    test_mean = test_df.mean()

    print(train_mean, "\n\n")
    print(test_mean, "\n\n")

    # construct Poisson for each mean 'result' value {0, 0.5, 1}
    # # (i - (0.5 * (i + 1)) is the result to predict
    # poisson_pred = np.column_stack(
    #     [[poisson.pmf((i - (0.5 * (i + 1))), train_mean['result']) for i in range(1, 4)]])
    #
    # # plot histogram of actual results
    # plt.hist(train_df[['result']].values, range(3), alpha=0.7, label=['result'],
    #          color=["#FFA07A"])
    #
    # # add lines for the Poisson distributions
    # pois1, = plt.plot([i - 0.5 for i in range(1, 4)], poisson_pred[:1],
    #                   linestyle='-', marker='o', label="Result", color='green')
    #
    # leg = plt.legend(loc='upper right', fontsize=13, ncol=2)
    # leg.set_title("Poisson           Actual        ",
    #               prop={'size': '14', 'weight': 'bold'})
    #
    # plt.xticks([i for i in range(1, 4)])
    # plt.ylim([0.00, 1.00])
    # plt.xlim([0.00, 1.00])
    #
    # plt.xlim(0.0, 0.5)
    # plt.xlabel("Proportion of matches", size=13)
    # plt.ylabel("Match result", size=13)
    #
    # plt.title("Just a stupid test, idk wtf i am doin lmao", size=14, fontweight='bold')
    #
    # plt.tight_layout()
    # plt.show()

    print("debug")


def generate_scatter_matrix(trainX, trainY):
    cmap = cm.get_cmap('gnuplot')
    scatter = scatter_matrix(trainX, c=trainY, marker='o', s=40, hist_kwds={'bins': 15},
                             figsize=(9, 9), cmap=cmap)

    plt.suptitle('Scatter-matrix for each input variable')
    plt.savefig('extracted_fixtures_scatter_matrix')
