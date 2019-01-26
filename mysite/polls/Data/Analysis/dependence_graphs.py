from matplotlib import pyplot as plt
import numpy as np


def generate_dependecy_graphs(train_df):
    analyze_form_difference_dependence(train_df)
    analyze_goal_difference_dependence(train_df)
    analyze_score_difference_dependence(train_df)
    analyze_concentration_dependence(train_df)


def analyze_form_difference_dependence(train_df):
    y_train = np.array(train_df['result'])
    x_train = train_df.drop(['result', 'home_team', 'away_team'], axis=1)

    #: form_dif dependence
    y_good = [form1 - form2 for form1, form2, res in zip(
        train_df['home_form'], train_df['away_form'], train_df['result']) if res == 1]

    form_dif = train_df['home_form'] - train_df['away_form']
    y_all = [1 / list(form_dif).count(form) for form in y_good]

    plt.figure('Form hist')
    plt.hist(y_good, weights=y_all, color='green')

    plt.xlabel('Form difference')
    plt.ylabel('Win rate')

    # plt.show()
    plt.savefig('dependence_form.png')


def analyze_goal_difference_dependence(train_df):
    # : goal_dif dependence
    matches_won = len([x for x in train_df['result'] if x == 1])

    res = []
    for cnt, row in enumerate(train_df.values):
        dif = row[7]

        zipped = zip(train_df['result'], train_df['goal_diff'])

        res.append(sum([(x / matches_won) for x, y in zipped if (x == 1 and y < dif)]))

    plt.figure('Goal diff plot')
    plt.plot(train_df['goal_diff'], res, '.')

    plt.xlabel('Goal diff')
    plt.ylabel('Win rate')

    # plt.show()
    plt.savefig('dependence_goal_dif.png')


def analyze_score_difference_dependence(train_df):
    #: score_dif dependence
    res = []
    matches_won = len([x for x in train_df['result'] if x == 1])

    for cnt, row in enumerate(train_df.values):
        dif = row[8]
        res.append(sum(
            [x / matches_won for x, y in zip(train_df['result'], train_df['score_diff'])
             if x == 1 and y < dif]))

    plt.figure('Score diff plot')
    plt.plot(train_df['score_diff'], res, '.')

    plt.xlabel('Score diff')
    plt.ylabel('Win rate')

    # plt.show()
    plt.savefig('dependence_score_dif.png')


def analyze_concentration_dependence(train_df):
    #: score_dif dependence
    res = []
    matches_won = len([x for x in train_df['result'] if x == 1])

    for cnt, row in enumerate(train_df.values):
        concentration = row[6]
        res.append(sum(
            [x / matches_won for x, y in zip(train_df['result'],
                                             train_df['home_concentration'])
             if (x == 1 and y < concentration)]))

    plt.figure('Concentration plot')
    plt.plot(train_df['home_concentration'], res, '.')

    plt.xlabel('Concentration')
    plt.ylabel('Win rate')

    # plt.show()
    plt.savefig('dependence_concentration.png')
