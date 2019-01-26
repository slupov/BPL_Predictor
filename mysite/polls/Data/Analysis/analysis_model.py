from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

ANALYSIS_ITERATIONS = 10
TRAIN = 0
TEST = 1


class AnalysisModel:
    def __init__(self, all_data_df, feature_names, classificator, model_name):
        self.feature_names = feature_names
        self.classificator = classificator

        self.name = model_name

        self.X = all_data_df[feature_names]
        self.Y = all_data_df[classificator]

        self.x_train = {}
        self.x_test = {}
        self.y_train = {}
        self.y_test = {}

        self.logistic_reg_avg = [0, 0]
        self.decision_tree_avg = [0, 0]
        self.k_neighbours_avg = [0, 0]
        self.bayes_avg = [0, 0]

    def __str__(self):
        log_reg_avg_str = \
            "|Accuracy of Logistic regression classifier on {} set: \033[31m{:.2f}\033[93m\n"

        dec_tree_avg_str = \
            "|Accuracy of Decision Tree classifier on {} set: \033[31m{:.2f}\033[93m\n"

        knn_avg_str = "|Accuracy of K-NN classifier on {} set: \033[31m{:.2f}\033[93m\n"

        bayes_avg_str = "|Accuracy of Bayes classifier on {} set: \033[31m{:.2f}\033[93m\n"

        header_str = "+------------------- START %s -------------------+\n" % \
                     self.name
        footer_str = "+-------------------- END %s --------------------+\n" % \
                     self.name
        empty_row_str = "|                                                        " \
                        "              |\n"

        classificator_str = "|Classificator: \033[31m'%s'\033[93m\n" % self.classificator
        features_str = "|Feature names: \033[31m%s\033[93m\n" % self.feature_names

        return "\033[93m%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s\033[0m" % (
            header_str,

            classificator_str,
            features_str,

            empty_row_str,

            log_reg_avg_str.format("training", self.logistic_reg_avg[TRAIN]),
            log_reg_avg_str.format("test", self.logistic_reg_avg[TEST]),

            empty_row_str,

            dec_tree_avg_str.format("training", self.decision_tree_avg[TRAIN]),
            dec_tree_avg_str.format("test", self.decision_tree_avg[TEST]),

            empty_row_str,

            knn_avg_str.format("training", self.k_neighbours_avg[TRAIN]),
            knn_avg_str.format("test", self.k_neighbours_avg[TEST]),
            empty_row_str,

            bayes_avg_str.format("training", self.bayes_avg[TRAIN]),
            bayes_avg_str.format("test", self.bayes_avg[TEST]),
            footer_str)

    def test(self):
        self.logistic_reg_avg[TRAIN] = 0
        self.logistic_reg_avg[TEST] = 0

        self.decision_tree_avg[TRAIN] = 0
        self.decision_tree_avg[TEST] = 0

        self.k_neighbours_avg[TRAIN] = 0
        self.k_neighbours_avg[TEST] = 0

        self.bayes_avg[TRAIN] = 0
        self.bayes_avg[TEST] = 0

        for i in range(0, ANALYSIS_ITERATIONS):
            self.x_train, self.x_test, self.y_train, self.y_test = \
                train_test_split(self.X, self.Y, random_state=0)

            # -----------> logistic regression
            self.logistic_reg_avg = \
                [x + y for x, y in zip(self.logistic_reg_avg, self.logistic_regression())]

            # -----------> decision_tree
            self.decision_tree_avg = \
                [x + y for x, y in zip(self.decision_tree_avg, self.decision_tree())]

            # -----------> k neighbours
            self.k_neighbours_avg = \
                [x + y for x, y in zip(self.k_neighbours_avg, self.k_neighbours())]

            # -----------> Bayes classifier
            self.bayes_avg = \
                [x + y for x, y in zip(self.bayes_avg, self.naive_bayes())]

        # apply average
        self.logistic_reg_avg = [x / ANALYSIS_ITERATIONS for x in self.logistic_reg_avg]
        self.k_neighbours_avg = [x / ANALYSIS_ITERATIONS for x in self.k_neighbours_avg]
        self.decision_tree_avg = [x / ANALYSIS_ITERATIONS for x in self.decision_tree_avg]
        self.bayes_avg = [x / ANALYSIS_ITERATIONS for x in self.bayes_avg]

    def logistic_regression(self):
        logreg = LogisticRegression(solver='lbfgs', multi_class='auto', max_iter=10000)
        logreg.fit(self.x_train, self.y_train)

        return [logreg.score(self.x_train, self.y_train),
                logreg.score(self.x_test, self.y_test)]

    def decision_tree(self):
        clf = DecisionTreeClassifier().fit(self.x_train, self.y_train)

        return [clf.score(self.x_train, self.y_train),
                clf.score(self.x_test, self.y_test)]

    def k_neighbours(self):
        knn = KNeighborsClassifier()
        knn.fit(self.x_train, self.y_train)

        return [knn.score(self.x_train, self.y_train),
                knn.score(self.x_test, self.y_test)]

    def naive_bayes(self):
        bayes = GaussianNB()
        bayes.fit(self.x_train, self.y_train)

        return [bayes.score(self.x_train, self.y_train),
                bayes.score(self.x_test, self.y_test)]
