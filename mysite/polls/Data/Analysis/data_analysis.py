import pandas as pd
from matplotlib import cm
from matplotlib import pyplot as plt
from pandas.plotting import scatter_matrix

from .dependence_graphs import generate_dependecy_graphs
from ...models import ExtractedFixtures

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn import preprocessing
from sklearn import utils


def analyze_data():
    all_data_df = pd.DataFrame.from_records(ExtractedFixtures.objects.all(). \
                                            filter(season__gte="17/18"). \
                                            order_by('season', 'home_team').values(),
                                            exclude=['id'])
    le = preprocessing.LabelEncoder()
    all_data_df['home_team'] = le.fit_transform(all_data_df['home_team'])
    all_data_df['away_team'] = le.fit_transform(all_data_df['away_team'])
    all_data_df['result']=le.fit_transform(all_data_df['result'])
    generate_dependecy_graphs(all_data_df)

    feature_names = ['home_team','away_team', 'goal_diff', 'score_diff']
    X = all_data_df[feature_names]
    Y = all_data_df['result']

    generate_scatter_matrix(X, Y)

    # apply min max normalization scaling to data

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state=0)

    # scaler = MinMaxScaler()
    #
    # X_train = scaler.fit_transform(X_train)
    # X_test = scaler.transform(X_test)

    # BUILDING MODELS

    # -----------> logistic regression
    logistic_regression(X_train, Y_train, X_test, Y_test)

    # -----------> decision_tree
    decision_tree(X_train, Y_train, X_test, Y_test)

    # -----------> k neighbours
    k_neighbours(X_train, Y_train, X_test, Y_test)

    # TODO Test for the rest from
    # https://towardsdatascience.com/solving-a-simple-classification-problem-with-python-fruits-lovers-edition-d20ab6b071d2?fbclid=IwAR0kByuLFgCf3-pFw3Ff45g7I_e_yma0uxBmhilj2PA5m2RxShClYP-rSXM
    # poisson_distribution(train_df, test_df)

    print("debug")


def logistic_regression(X_train, Y_train, X_test, Y_test):
    logreg = LogisticRegression(solver='lbfgs', multi_class='auto')
    logreg.fit(X_train, Y_train)

    print('Accuracy of Logistic regression classifier on training set: {:.2f}'
          .format(logreg.score(X_train, Y_train)))
    print('Accuracy of Logistic regression classifier on test set: {:.2f}'
          .format(logreg.score(X_test, Y_test)))


def decision_tree(X_train, Y_train, X_test, Y_test):
    clf = DecisionTreeClassifier().fit(X_train, Y_train)
    print('Accuracy of Decision Tree classifier on training set: {:.2f}'
          .format(clf.score(X_train, Y_train)))
    print('Accuracy of Decision Tree classifier on test set: {:.2f}'
          .format(clf.score(X_test, Y_test)))


def k_neighbours(X_train, Y_train, X_test, Y_test):
    knn = KNeighborsClassifier()
    knn.fit(X_train, Y_train)
    print('Accuracy of K-NN classifier on training set: {:.2f}'
          .format(knn.score(X_train, Y_train)))
    print('Accuracy of K-NN classifier on test set: {:.2f}'
          .format(knn.score(X_test, Y_test)))


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
